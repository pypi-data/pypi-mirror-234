"""
Data structures to provide low-level interaction with the pre-production
database within Python.

E.g.

macbook:pf_db avt$ python3
Python 3.10.6 (main, Aug  3 2022, 05:37:08) [Clang 13.0.0 (clang-1300.0.29...
Type "help", "copyright", "credits" or "license" for more information.
>>> from ds20kdb import interface
>>> db = interface.Database()
>>> help(db.get)
>>> response = db.get('wafer')
>>> help(response)
>>> response.data
     wafer_pid  manufacturer         lot  ...  spad_size dose   description
0            1             2     9262109  ...         30    3  back... run B
1            2             2     9262109  ...         30    3  back... run A
2            3             2     9262109  ...         30    3  back... run C
3            4             2     9262109  ...         30    3  back... run A
4            5             2     9262109  ...         30    3  back... run B
..         ...           ...         ...  ...        ...  ...  ...
206        207             2     9306869  ...         30    3  ds-run=7
207        208             2     9306869  ...         30    3  ds-run=7
208        209             2     9306869  ...         30    3  ds-run=7
209        210             2     9306869  ...         30    3  ds-run=7
210        211             2     9306869  ...         30    3  ds-run=7

[211 rows x 8 columns]

>>> db.get('wafer', lot=9262109, wafer_number=12).data
   wafer_pid  manufacturer         lot  ...  spad_size dose    description
0          6             2     9262109  ...         30    3  back... run A

[1 rows x 8 columns]
"""

import contextlib
import csv
import datetime
from functools import wraps
import http.client as http_client
import io
import itertools
import logging
import platform
import urllib.parse

try:
    from importlib import metadata
except (ImportError, ModuleNotFoundError):
    try:
        import importlib_metadata as metadata
    except (ImportError, ModuleNotFoundError):
        py_version = platform.python_version()
        if py_version < '3.8':
            logging.warning(
                'Cannot import importlib, version information will NOT be available.'
            )
            logging.warning(
                'Unsupported Python version (%s), upgrade to Python 3.8 or newer.',
                py_version,
            )
        else:
            logging.error('Cannot import importlib')

import numpy as np
import requests
import pandas as pd

from ds20kdb import constants
from ds20kdb import auth

# read the package version number as originally specified in setup.py
try:
    __version__ = metadata.version('ds20kdb-avt')
except NameError:
    # end-user is probably using a Python version < 3.8
    __version__ = 'unknown'


##############################################################################
# utilities
##############################################################################


def dict_from_qrcode(qr_code_numerals):
    """
    --------------------------------------------------------------------------
    args
        qr_code_numerals : string or int
            e.g. '22061703000032001', where (from left to right):
                220617 - YYMMDD
                0      - PRODUCTION FLAG
                30     - VERSION
                00032  - SERIAL NUMBER
                001    - PART NUMBER
    --------------------------------------------------------------------------
    returns : dict or None
        {
            'timestamp': datetime.datetime, 'production': bool,
            'version': int, 'serial_number': int, 'part_number': int
        }
        e.g.
        dict_from_qrcode('22061703000032001')
        {
            'timestamp': datetime.datetime(2022, 6, 17, 0, 0),
            'production': False,
            'version_string': '3.0',
            'version_major': 3,
            'version_minor': 0,
            'serial_number': 32,
            'part_number': 1
        }

        dict if the received string looks plausible, None otherwise.
    --------------------------------------------------------------------------
    """
    if not qr_code_valid(qr_code_numerals):
        return None

    qr_code_numerals = str(qr_code_numerals)

    yymmdd = qr_code_numerals[:6]
    prod_flag = qr_code_numerals[6]
    version = qr_code_numerals[7:9]
    serial_number = qr_code_numerals[9:14]
    part_number = qr_code_numerals[14:17]

    return {
        'timestamp': datetime.datetime.strptime(yymmdd, '%y%m%d'),
        'production': prod_flag == '1',
        'version_string': f'{version[0]}.{version[1]}',
        'version_major': int(version) // 10,
        'version_minor': int(version) % 10,
        'serial_number': int(serial_number),
        'part_number': int(part_number),
    }


def qr_code_valid(qr_code_numerals):
    """
    Basic validation of string decoded from QR code.

    --------------------------------------------------------------------------
    args
        qr_code_numerals : string or int
            e.g. '22061703000032001', where (from left to right):
                220617 - YYMMDD
                0      - PRODUCTION FLAG
                30     - VERSION
                00032  - SERIAL NUMBER
                001    - PART NUMBER
    --------------------------------------------------------------------------
    returns : bool
        True if the received string looks plausible, False otherwise.
    --------------------------------------------------------------------------
    """
    # numerals only
    try:
        int(qr_code_numerals)
    except ValueError:
        return False

    qr_code_numerals = str(qr_code_numerals)

    # always 17 numerals
    if len(qr_code_numerals) != 17:
        return False

    yymmdd = qr_code_numerals[:6]
    prod_flag = qr_code_numerals[6]

    try:
        datetime.datetime.strptime(yymmdd, '%y%m%d')
    except ValueError:
        return False

    if prod_flag not in {'0', '1'}:
        return False

    # version, serial_number and part_number can be pretty much anything
    # so no further checks at this point

    return True


def wafer_map_valid_locations():
    """
    Generate all valid SiPM positions on the wafer. ASSUME that this
    layout is generic across all wafers.

    Wafer map geometry:

    columns (x) : 0 - 19
    rows    (y) : 0 - 25

      0,  0 : bottom left
     19, 25 : top right

    Valid SiPM positions within bounds:

    columns (x) : 2 - 17
    rows    (y) : 2 - 23

    HOWEVER...

    SiPMs in columns 2 and 17 cannot be probed at LNGS, therefore these four
    devices should be excluded when picking production wafers:

    column row
    02     12
    02     13
    17     12
    17     13

    In the database, the 'sipm' table itself (for a given wafer_id) contains
    SiPM PIDs for all 268 positions, but there will be no corresponding entry
    for the above four devices in the 'sipm_test' table.

    --------------------------------------------------------------------------
    args : none
    --------------------------------------------------------------------------
    yields : sequence of tuples (int, int)
        (wafer_column, wafer_row)
    --------------------------------------------------------------------------
    """
    # bottom half of wafer
    row_columns = {
        2: range(7, 12 + 1),
        3: range(6, 13 + 1),
        4: range(5, 14 + 1),
        5: range(4, 15 + 1),
        6: range(4, 15 + 1),
        7: range(3, 16 + 1),
        8: range(3, 16 + 1),
        9: range(3, 16 + 1),
        10: range(3, 16 + 1),
        11: range(3, 16 + 1),
        12: range(3, 16 + 1),
    }

    # column pattern is symmetrical: add top half of wafer
    for row, colrange in row_columns.copy().items():
        row_columns[25 - row] = colrange

    # yield all valid wafer map locations
    for row, colrange in row_columns.items():
        for column in colrange:
            yield column, row


def removesuffix(table_name, suffix):
    """
    Remove suffix from string.

    Python versions prior to 3.9 do not have <string>.removesuffix().

    --------------------------------------------------------------------------
    args
        string : string
            e.g. 'vpcb_asic_test'
        suffix : string
            e.g. '_test'
    --------------------------------------------------------------------------
    returns : string
        e.g.'vpcb_asic'
    --------------------------------------------------------------------------
    """
    if table_name.endswith(suffix):
        table_name = table_name[:-len(suffix)]

    return table_name


##############################################################################
# Result handling - structured to provide meaningful documentation to the
# caller of member functions of class Database.
##############################################################################


class Result:
    """
    A simple data container to hold results from database operations.
    """

    __slots__ = {
        'network_timeout': (
            'A boolean value indicating whether a network timeout occurred\n'
            'when communicating with the database.'
        ),
        'data': (
            'Data created from the database query response, supplied in an\n'
            'appropriate datatype.'
        ),
    }

    def __init__(self):
        self.network_timeout = False
        self.data = None

    def __str__(self):
        return '\n'.join(
            [
                f'network_timeout={self.network_timeout}',
                f'data={self.data}'
            ]
        )


##############################################################################
# database handling
##############################################################################


class Database(auth.Authentication):
    """
    Low-level database interaction.
    """

    base_url = constants.BASE_URL

    def __init__(self, connection=None):
        """
        requests configuration

        Database login credentials are obtained from a local configuration
        file. It will be assumed that these details are correct on the basis
        of the checks performed at the time the file was written. No further
        checks will be made here.
        """
        if connection is None:
            _credentials = self.read_credentials()
            if _credentials is None:
                logging.error('could not read local authentication credentials')
                logging.error('see documentation for method: create_credentials_file()')
                assert _credentials is not None, 'no valid credentials, exiting'
        else:
            uuser, upass, self.base_url = connection
            _credentials = {'username': uuser, 'password': upass}
            self.credentials_accepted_by_endpoint(_credentials)

        self.session = requests.Session()
        self.session.auth = (_credentials['username'], _credentials['password'])

        # set the requests pool size to something appropriate for the computer
        # this script is running on
        #
        # Random remote disconnections were experienced with the pre-production
        # database when writing with more than one thread, even if data writes
        # were independent. The initial value of _max_io_workers was set to
        # min(32, os.cpu_count() * 4), and decremented to 2. Even at 2 problems
        # were seen. Threaded reads worked perfectly.
        #
        # Can show the current pool size with:
        # self.session.get_adapter(self.base_url).poolmanager.connection_pool_kw['maxsize']
        self._max_io_workers = 1
        self.session.mount(
            'https://',
            requests.adapters.HTTPAdapter(
                pool_connections=1, pool_maxsize=self._max_io_workers
            ),
        )

    ##########################################################################
    # requests GET
    ##########################################################################

    def _cache_describe(function):
        """
        Since anything returned by the describe method will not change during
        a requests session, all responses that didn't time out can be safely
        cached, potentially reducing the number of interactions with the
        database server.

        Since any response that timed-out will contain no useful data,
        nothing should be written to the cache in that circumstance. Hence,
        we cannot simply decorate the describe method with
        functools lru_cache.

        This caching is principally for the benefit of users working with the
        database in interactive sessions.

        ----------------------------------------------------------------------
        args
            function : <class 'function'>
        ----------------------------------------------------------------------
        returns : class Result
        ----------------------------------------------------------------------
        """
        cache = {}

        @wraps(function)
        def wrapper(*args):
            try:
                return cache[args]
            except KeyError:
                retval = function(*args)
                if not retval.network_timeout:
                    cache[args] = retval
                return retval

        return wrapper

    ##########################################################################
    # generic

    @_cache_describe
    def describe(self, table_name=''):
        """
        Describe database. With no argument, this returns a list containing
        the table names of the database. With a table name specified this
        returns a list of the fields of the specified table.

        Usage:

            response = describe()
            response = describe('vtile')

            Read details of response with:

            response.list
            response.network_timeout

            Use help(response) for more information.

        ----------------------------------------------------------------------
        args
            table_name : string
        ----------------------------------------------------------------------
        returns : class Result
        ----------------------------------------------------------------------
        """
        result = Result()

        url_suffix = '/'.join(s for s in ['db/describe', table_name] if s)
        full_url = urllib.parse.urljoin(self.base_url, url_suffix)

        try:
            response = self.session.get(full_url)
        except requests.ConnectionError:
            result.network_timeout = True
            return result

        if response.status_code != requests.codes.ok:
            return result

        tables = [
            table.strip()
            for table in response.text.replace('"', '').strip('[]').split(',')
        ]
        result.data = tables

        return result

    def _row_limit_prefix(self, table_name, query_max_results):
        """
        Generate partial URL query string for limiting the number of returned
        rows. Perform some rudimentary validity checking.

        Initial tests indicate there's no need to compensate for SQL reserved
        words for the column name here.

        ----------------------------------------------------------------------
        args
            table_name : string
            query_max_results : iterable (max_rows, sort_by_column, direction)
                where:
                    max_rows : int, value >= 1
                        maximum number of rows to be returned in the response
                    sort_by_column : string, table field/column name
                    direction : string, 'a' or 'd'
                        e.g. (4, 'operator', 'a')
        ----------------------------------------------------------------------
        returns
            prefix : string
                e.g. '?l=4&ob=operator=a'
        ----------------------------------------------------------------------
        """
        prefix = ''

        try:
            max_rows, sort_by_column, direction = query_max_results
        except (ValueError, TypeError):
            logging.error('_row_limit_prefix: query_max_results malformed')
        else:
            # Do not generate a filtered query that will return nothing.
            try:
                num_rows = int(max_rows)
            except (TypeError, ValueError):
                logging.error('_row_limit_prefix: bad number of rows')
                return prefix

            if num_rows < 1:
                logging.error(
                    (
                        '_row_limit_prefix: bad number of rows (%s), '
                        'value should be > 0'
                    ),
                    num_rows
                )
                return prefix

            # Sort order: (a)scending, (d)ecending
            try:
                direction = direction.lower()
            except AttributeError:
                logging.error(
                    '_row_limit_prefix: unrecognised direction, '
                    'use "a" (ascending) or "d" (descending).',
                )
                return prefix

            if direction not in {'a', 'd'}:
                logging.error(
                    '_row_limit_prefix: unrecognised direction, '
                    'use "a" (ascending) or "d" (descending).',
                )
                return prefix

            # At the cost of an additional database lookup, check that the
            # field exists in the table.
            response = self.describe(table_name)
            if response.network_timeout or sort_by_column not in response.data:
                logging.error(
                    '_row_limit_prefix: unrecognised field "%s" for table "%s"',
                    sort_by_column,
                    table_name,
                )
                return prefix

            prefix = f'l={max_rows}&ob={sort_by_column}={direction}'

        return prefix

    @staticmethod
    def _join_subexpression(args):
        """
        Create database inner join subexpression. No error checking.

        ----------------------------------------------------------------------
        args
            args : tuple (int, (string, string, string))
                e.g. (0, ('wafer', 'sipm.wafer_id', 'wafer_pid'))
        ----------------------------------------------------------------------
        returns : string
            e.g. 'ij[0]=wafer&on[0]=sipm.wafer_id=wafer_pid'
        ----------------------------------------------------------------------
        """
        index, ref = args
        return f'ij[{index}]={ref[0]}&on[{index}]={ref[1]}={ref[2]}'

    def get(self, table_name, joins=None, **columns):
        """
        Generic GET operation.

        When supplied with just the table name, this function will return all
        rows of the table. If the 'columns' argument is supplied, a subset of
        the table will be returned, unless the dictionary is empty in which
        case this will yield the entire table. The joins argument allows the
        use of a rudimentary database inner join lookup.

        If the request for a subset of the table is obviously broken
        ('columns' is malformed, for example) it's better that we fail the
        whole request, rather than return the entire contents of the table.

        Note that when fully populated, the 'sipm' and 'sipm_test' tables
        could each contain ~60000 rows which may result in a >10MB response
        from the remote database. The query_max_results key in the columns
        argument may be used to specify the number of responses received.

        Usage:

            (1) response = get('wafer')
            (2) response = get('wafer', lot=9262109)
            (3) response = get('wafer', lot=9262109, wafer_number=12)

            (4) columns = {'lot': 9262109, 'wafer_number': 12}
                response = get('wafer', **columns)

            (5) response = get('wafer', query_max_results=(4, 'operator', 'a'))
                (special case to limit the query response to the given number
                 of rows. This request isn't processed by this interface, it's
                 simply passed on to the database to handle.)

            (6) joins = [
                    ('wafer', 'sipm.wafer_id', 'wafer_pid'),
                    ('sipm', 'sipm_id', 'sipm.sipm_pid'),
                ]
                response = get('wafer', joins=joins, wafer_pid=1261)
                (database inner join)

            (7) joins = [
                    ('wafer', 'sipm.wafer_id', 'wafer_pid'),
                    ('sipm', 'sipm_id', 'sipm.sipm_pid'),
                ]
                response = get(
                    'sipm_test', joins=joins, wafer_pid=1261,
                    query_max_results=(4, 'operator', 'a')
                )
                (can combine 5 and 6)

            Read details of response with:

            response.data
            response.network_timeout

            Use help(response) for more information.

        If the user has made a request to limit the number of rows they
        receive in the response, extract the key/value pair specifying this
        from the columns dict, so it doesn't get prepended with the table
        name as part of the existing column-based filtering. A long and
        unwieldy key (query_max_results) has been chosen to reduce the
        probability of intersection with future additions to the set of all
        database field names. Developers can check this with a call to
        get_unique_field_names().

        ----------------------------------------------------------------------
        args
            table_name : string
            joins : iterable
                [(table, field, field), ...]
                e.g.
                    [
                        ('wafer', 'sipm.wafer_id', 'wafer_pid'),
                        ('sipm', 'sipm_id', 'sipm.sipm_pid'),
                    ]
            columns : <class 'dict'>
                e.g. {'lot': 9262109, 'wafer_number': 12}

                special case:

                columns may contain key 'query_max_results'. If so, its value
                should be an iterable (max_rows, sort_by_column, direction)
                where:
                    max_rows : int, value >= 1
                        maximum number of rows to be returned in the response
                    sort_by_column : string, table field/column name
                    direction : string, 'a' or 'd'
                        e.g. (4, 'operator', 'a')
        ----------------------------------------------------------------------
        returns : class Result
        ----------------------------------------------------------------------
        """
        result = Result()
        url_suffix = f'item/{table_name}'
        query_max_results = columns.pop('query_max_results', None)

        # modify the URL so the database returns a subset of the table
        try:
            select_subset = '&'.join(
                f'w="{k}"=\'{v}\'' for k, v in columns.items()
            )
        except AttributeError:
            return result

        # limit number of rows returned if required
        if query_max_results is not None:
            prefix = self._row_limit_prefix(table_name, query_max_results)
            if prefix:
                select_subset = f'{prefix}&{select_subset}'
            else:
                # Attempt to limit number of rows failed, so do NOT
                # forward the unlimited GET operation to the database.
                return result

        # implement inner join
        if joins is None:
            prefix = ''
        else:
            prefix = '&'.join(map(self._join_subexpression, enumerate(joins)))
        select_subset = '&'.join(x for x in [prefix, select_subset] if x)

        # build query string
        url_suffix = '?'.join(s for s in [url_suffix, select_subset] if s)

        full_url = urllib.parse.urljoin(self.base_url, url_suffix)
        logging.debug('URL generated by get(): %s', full_url)

        try:
            response = self.session.get(full_url)
        except requests.ConnectionError:
            result.network_timeout = True
            return result

        if response.status_code != requests.codes.ok:
            return result

        result.data = pd.read_csv(
            io.StringIO(response.text), sep=',', encoding='utf-8',
            low_memory=False,
        )

        return result

    ##########################################################################
    # query database structure

    def get_db_structure(self):
        """
        Get database table/fields structure.

        Dictionary ordering by insertion order is only guaranteed for
        Python 3.7 onwards.

        ----------------------------------------------------------------------
        args : none
        ----------------------------------------------------------------------
        returns : dict or None (no response from db, no network connection)
            e.g. {<table_name>: <list of fields>, ...}
        ----------------------------------------------------------------------
        """
        try:
            return {
                table: self.describe(table).data
                for table in sorted(self.describe().data)
            }
        except TypeError:
            return None

    def get_unique_field_names(self):
        """
        Get all unique database field names.

        ----------------------------------------------------------------------
        args : none
        ----------------------------------------------------------------------
        returns : list or None (no response from db, no network connection)
            e.g. [
                'a', 'acs_pid', 'afterpulsing', 'amplitude_1pe', ...
                'wafer_number', 'wafer_pid', 'wafer_status_pid'
            ]
        ----------------------------------------------------------------------
        """
        try:
            fields = itertools.chain.from_iterable(
                self.get_db_structure().values()
            )
        except AttributeError:
            return None

        return sorted(set(fields))

    def get_table_names_for_field(self, field):
        """
        Get names of all tables that contain the given field.

        ----------------------------------------------------------------------
        args
            field : string
                e.g. 'qrcode'
        ----------------------------------------------------------------------
        returns : list or None (no response from db, no network connection)
            e.g. [
                'a', 'acs_pid', 'afterpulsing', 'amplitude_1pe', ...
                'wafer_number', 'wafer_pid', 'wafer_status_pid'
            ]
        ----------------------------------------------------------------------
        """
        try:
            tables = {
                table
                for table, fields in self.get_db_structure().items()
                if field in fields
            }
        except AttributeError:
            return None

        return sorted(tables)

    ##########################################################################
    # tailored enquiries

    def get_institute_id(self, text_ident):
        """
        Get the Institution ID for the given case-insensitive sub-string, if
        any.

        ----------------------------------------------------------------------
        args
            text_ident : string
                e.g. 'University of Liverpool'
        ----------------------------------------------------------------------
        returns
            result : class Result
        ----------------------------------------------------------------------
        """
        result = Result()

        # get all institutes
        response = self.get('institute')

        try:
            mask = response.data.name.str.contains(
                text_ident, case=False, na=False, regex=False
            )
        except AttributeError:
            pass
        else:
            try:
                response.data = int(response.data[mask].head().id.values[-1])
            except (AttributeError, IndexError):
                pass
            else:
                result = response

        return result

    def get_sipm_good(self, sipm_pid):
        """
        Get the status of the SiPM test result. This result indicates the
        pass/fail status of the initial wafer probe test.

        It's possible for there to be more than one test result for a given
        sipm_pid. Taking the minimum of 'good' and 'bad' will return 'bad'
        ensuring that in any pair of results any bad result, will result in
        a bad response.

        ----------------------------------------------------------------------
        args
            sipm_pid : int
        ----------------------------------------------------------------------
        returns
            result : class Result
        ----------------------------------------------------------------------
        """
        result = Result()

        response = self.get('sipm_test', sipm_id=sipm_pid)

        try:
            response.data = min(response.data.classification.values) == 'good'
        except (AttributeError, IndexError, TypeError, ValueError):
            pass
        else:
            result = response

        return result

    def get_sipm_pid(self, wafer_id, column, row):
        """
        Get the SiPM PID from the database.

        Work around a problem with the database for the sipm table, where
        using the column field results in a "Bad request" response. This
        means that we can't use the database query to obtain the definitive
        response. So instead request SiPMs that match the wafer_id and row,
        obtain the sipm_id and column, then process the response in this
        function to obtain the sipm_id.

        ----------------------------------------------------------------------
        args
            wafer_id : int
            column : int
            row : int
        ----------------------------------------------------------------------
        returns
            rdat : int or None
        ----------------------------------------------------------------------
        """
        response = self.get('sipm', wafer_id=wafer_id, row=row)

        # response will contain a DataFrame something like:
        #
        #     sipm_pid  wafer_id  column  row  tile_id tile_type
        # 0         12         1      12    9      NaN      VETO
        # 1         34         1      10    9      NaN      VETO
        # ...
        # 12       251         1       6    9      NaN      VETO
        # 13       254         1      13    9      NaN      VETO

        # Filter by column, then isolate sipm_pid.

        rdat = response.data
        try:
            rdat = int(rdat.loc[rdat.column == column].sipm_pid.values[-1])
        except (AttributeError, IndexError):
            rdat = None

        return rdat

    def get_sipm_test_id(self, sipm_pid):
        """
        Get the SiPM test_id given the sipm_pid. This serves as a check that
        the row was written successfully.

        It's plausible that more than one record may exist in the database for
        the same id, if corrections were made by submitting subsequent
        tables. So the value from the last record returned from the GET
        operation will be returned from this function.

        Example command line query:

        curl -u <USERNAME>:<PASSWORD> "<BASE_URL>item/sipm_test?w=sipm_id=29&c=id"
        id
        29

        ----------------------------------------------------------------------
        args
            sipm_pid : int
        ----------------------------------------------------------------------
        returns
            result : class Result
        ----------------------------------------------------------------------
        """
        result = Result()

        response = self.get('sipm_test', sipm_id=sipm_pid)

        try:
            response.data = int(response.data.id.values[-1])
        except (AttributeError, IndexError):
            pass
        else:
            result = response

        return result

    def get_vpcb_asic_pid(self, vpcb_pid):
        """
        Get the vPCB ASIC PID from the database, given the vPCB PID.

        ----------------------------------------------------------------------
        args
            vpcb_pid : int
        ----------------------------------------------------------------------
        returns
            result : class Result
        ----------------------------------------------------------------------
        """
        result = Result()

        response = self.get('vpcb_asic', vpcb_id=vpcb_pid)

        try:
            response.data = int(response.data.vpcb_asic_pid.values[-1])
        except (AttributeError, IndexError):
            pass
        else:
            result = response

        return result

    def get_vpcb_asic_pid_from_qrcode(self, qrcode):
        """
        Get vPCB ASIC PID given the QR-code.

        ----------------------------------------------------------------------
        args
            qrcode : string or int
                e.g. 22061703000024001
        ----------------------------------------------------------------------
        returns
            vpcb_asic_pid : class Result
        ----------------------------------------------------------------------
        """
        vpcb_asic_pid = Result()

        try:
            vpcb_pid = self.get_vpcb_pid(qrcode).data
        except AttributeError:
            pass
        else:
            with contextlib.suppress(AttributeError, IndexError):
                vpcb_asic_pid.data = self.get_vpcb_asic_pid(vpcb_pid).data

        return vpcb_asic_pid

    def get_vpcb_pid(self, qrcode):
        """
        Get the vPCB PID from the database, given the QR-code.

        ----------------------------------------------------------------------
        args
            qrcode : string or int
                e.g. 22061703000024001
        ----------------------------------------------------------------------
        returns
            result : class Result
        ----------------------------------------------------------------------
        """
        result = Result()

        # this returns a dataframe or None
        response = self.get('vpcb', qrcode=qrcode)

        try:
            response.data = int(response.data.vpcb_pid.values[-1])
        except (AttributeError, IndexError):
            pass
        else:
            result = response

        return result

    def get_vtile_pid_from_qrcode(self, qrcode):
        """
        Get the vTile PID given the QR-code.

        Once a vTile table has been written, this function can be used to
        obtain the vTile PID from the QR-code, so the vTile's 24 SiPM tables
        can be rewritten to include the vtile_pid.

        ----------------------------------------------------------------------
        args
            qrcode : string or int
                e.g. 22061703000024001
        ----------------------------------------------------------------------
        returns
            result : class Result
        ----------------------------------------------------------------------
        """
        result = Result()

        try:
            vpcb_asic_pid = self.get_vpcb_asic_pid_from_qrcode(qrcode).data
        except IndexError:
            pass
        else:
            response = self.get('vtile', vpcb_asic_id=vpcb_asic_pid)

            try:
                response.data = int(response.data.vtile_pid.values[-1])
            except (AttributeError, IndexError):
                pass
            else:
                result = response

        return result

    def get_wafer_pid(self, lot, wafer_number):
        """
        Get the wafer PID from the database, given the lot and wafer numbers.

        ----------------------------------------------------------------------
        args : none
        ----------------------------------------------------------------------
        returns
            result : class Result
        ----------------------------------------------------------------------
        """
        result = Result()

        # this returns a dataframe or None
        response = self.get(
            'wafer', lot=lot, wafer_number=wafer_number
        )

        try:
            response.data = int(response.data.wafer_pid.values[-1])
        except (AttributeError, IndexError):
            pass
        else:
            result = response

        return result

    ##########################################################################
    # tailored enquiries/processing

    def get_qrcode_from_vtile_pid(self, vtile_pid):
        """
        Get the QR-code for the given the vTile PID.

        ----------------------------------------------------------------------
        args
            vtile_pid : int
        ----------------------------------------------------------------------
        returns
            qrcode : int
                Always 17 digits: e.g. 22060103000010001
        ----------------------------------------------------------------------
        """
        try:
            vpcb_asic_id = self.get('vtile', vtile_pid=vtile_pid).data.vpcb_asic_id.values[-1]
        except IndexError:
            return None

        try:
            vpcb_id = self.get('vpcb_asic', vpcb_asic_pid=vpcb_asic_id).data.vpcb_id.values[-1]
        except IndexError:
            return None

        try:
            qrcode = int(self.get('vpcb', vpcb_pid=vpcb_id).data.qrcode.values[-1])
        except IndexError:
            return None

        return qrcode

    def get_qrcode_from_vpcb_asic_pid(self, vpcb_asic_pid):
        """
        Get the QR-code for the given the vpcb_asic PID.

        ----------------------------------------------------------------------
        args
            vpcb_asic_pid : int
        ----------------------------------------------------------------------
        returns
            qrcode : int
                Always 17 digits: e.g. 22060103000010001
        ----------------------------------------------------------------------
        """
        try:
            vpcb_id = self.get('vpcb_asic', vpcb_asic_pid=vpcb_asic_pid).data.vpcb_id.values[-1]
        except IndexError:
            return None

        try:
            qrcode = int(self.get('vpcb', vpcb_pid=vpcb_id).data.qrcode.values[-1])
        except IndexError:
            return None

        return qrcode

    def get_relevant_qrcodes(self):
        """
        Intended to be used by submit_vtile.py to display only QR-codes that
        have not already been allocated to a vTile.

        This is a relatively expensive method to call, with three database
        GET operations with potentially large responses.

        ----------------------------------------------------------------------
        args : none
        ----------------------------------------------------------------------
        returns
            unallocated_qrcodes : list
                e.g. [
                    22060103000008001,
                    22060103000009001,
                    ...
                    23020703000096001,
                    23052403000142001,
                ]
        ----------------------------------------------------------------------
        """
        # Get vpcb_asic_ids from table vtile. These all represent
        # vPCBs/vPCB+ASIC (and therefore QR-codes) that have been allocated
        # to a vTile.

        response = self.get('vtile')
        if response.network_timeout:
            return None

        vpcb_asic_id_allocated_to_vtile = set(response.data.vpcb_asic_id)

        # Get the vpcb_ids for all those found above.

        response = self.get('vpcb_asic')
        if response.network_timeout:
            return None

        dfv = response.data

        vpcb_id_allocated_to_vtile = set(
            dfv[dfv.vpcb_asic_pid.isin(vpcb_asic_id_allocated_to_vtile)].vpcb_id
        )

        # Remove the vpcb_ids from those listed in table vpcb. Anything left
        # hasn't been allocated yet.

        response = self.get('vpcb')
        if response.network_timeout:
            return None

        dfv = response.data

        unallocated_qrcodes = sorted(
            dfv[-dfv.vpcb_pid.isin(vpcb_id_allocated_to_vtile)].qrcode
        )

        return unallocated_qrcodes

    def get_relevant_solder_ids(self, institute_id):
        """
        Intended to be used by submit_vtile.py to display the most relevant
        solder syringes, so the user isn't presented with a myriad of
        options, most of which will be historic or irrelevant. Always tries
        to return something (in preference to nothing) so the GUI combobox
        isn't empty.

        Behaviour: return, in order of preference

        (1) Recent solder_ids (before expiry date, or expired for not more
        than 30 days) for the given institute.

        (2) if (1) was empty, return all solder_ids for the given institute

        (3) if (2) was empty, return all solder_ids

        Syringes are considered relevant if they are (a) in date, or recently
        out of date (since database entry may lag production), and
        (b) located at the institute in question.

        The date the syringe was brought up to room temperature isn't taken
        into consideration, since for larger 25g syringes institutes may have
        chosen to split the contents into multiple smaller containers before
        transferring to cold storage. Therefore, the room temperature date for
        an originating large syringe may be misleading.

        ----------------------------------------------------------------------
        args
            institute_id : int
        ----------------------------------------------------------------------
        returns : list of int, or None (timeout or bad institute_id)
            E.g. [17, 18]
        ----------------------------------------------------------------------
        """
        # Get the whole table, the size should be fairly small even when the
        # db is fully populated.
        response = self.get('solder')
        if response.network_timeout:
            return None

        retval = response.data

        cut_off_time = datetime.datetime.strftime(
            datetime.datetime.now() - datetime.timedelta(days=30),
            '%Y-%m-%d %H:%M:%S'
        )
        time_limited = retval[
            (retval.institute_id == institute_id)
            & (retval.expiry_date > cut_off_time)
        ]

        if not time_limited.empty:
            retval = time_limited
        else:
            institution_limited = retval[retval.institute_id == institute_id]

            if not institution_limited.empty:
                retval = institution_limited

        try:
            return sorted(retval.solder_pid.values)
        except AttributeError:
            return None

    def get_sipms_allocated(self, sipm_pids):
        """
        Indicate if the given sipm_pid(s) have been allocated to vTile(s).

        There are two ways of approaching this operation, (1) obtain the
        whole vtile table with a single GET operation and perform the search
        locally (as done in this method) or (2) make 24 targeted GET
        operations - one for each SiPM column - letting the db perform the
        search operation.

        The latter should perform better when the database fully populated,
        but in pre-production this is an order of magnitude slower, e.g.

        return any(
            not self.get('vtile', **{c: sipm_pid}).data.empty
            for c in sipm_columns
        )

        Column names can also be obtained from the database if required:

        sipm_columns = (
            c for c in self.describe('vtile').data if c.startswith('sipm_')
        )

        WARNING: This method will become expensive to run once the database
        becomes more populated.

        ----------------------------------------------------------------------
        args
            sipm_pids : iterable (containing int(s))
        ----------------------------------------------------------------------
        returns : dict (or None if the caller supplied a non-iterable)
            {sipm_pid: True if allocated}
                E.g. {19: True, 33: True, 1000000: False}
        ----------------------------------------------------------------------
        """
        vtile_table = self.get('vtile').data

        sipm_columns = (f'sipm_{x}' for x in range(1, 24+1))
        all_sipms = set(itertools.chain(*vtile_table[sipm_columns].values))

        try:
            return {s: s in all_sipms for s in sipm_pids}
        except TypeError:
            return None

    def get_table_row_and_modify(self, table_name, select, replacements=None, omit_pid=True):
        """
        Generic method that reads a row from a remote database table,
        replaces values of given fields, then returns the result as a dict
        (which may then be POSTed to the database later).

        Given that this function is generic in nature, it won't complain too
        loudly if more than one row was returned from the GET operation, it
        simply returns the last row. This behaviour is not particularly
        desirable now, but may be so at some stage in the future when the
        database may support multiple table rows with the same PID field
        value; database housekeeping may then consolidate them later into a
        single row. This behaviour may be problematic in the case where the
        caller's selection of rows is too broad.

        Fields (which map to DataFrame columns) that contain NaN/NaT values
        are removed.

        E.g. to add a new indium solder syringe to the database - given that
        many fields will be similar between syringes - it may be helpful to
        get an existing row and modify it. In this instance, adding a syringe
        from the same lot and the same institute, we can just change the
        local syringe PID to get a dict suitable for POSTing it to the
        database:

        get_table_row_and_modify(
            'solder', {'solder_pid': 1}, {'syringe_id': 12}
        )

        Which would return:

        {
            'manufacturer': 4,
            'solder_type': 'Indium Paste NC-SMQ80 Ind#1E 52In48Sn Type 4 ...',
            'production_date': '2022-06-02 00:00:00',
            'room_temperature_date': '2022-07-18 16:00:00',
            'expiry_date': '2022-12-02 00:00:00',
            'syringe_id': 12, 'lot': 'PS11120734', 'mass': 25
        }

        ----------------------------------------------------------------------
        args
            table_name : string
                The caller should ensure the table name is correct, since no
                check is made.
            select : dict
                sufficient {field: value, ...} pairs to obtain the desired row
                from the table. This will probably just contain the _pid field
                for the given table.
            replacements : dict
                Replacement values for fields {field: value, ...}. If this
                argument is not supplied it defaults to None, which is later
                transformed into an empty dict.
            omit_pid : bool
                The principal objective of this method is to return a dict
                that can be POSTed to the database. Since the database doesn't
                currently support POSTing tables with an existing primary key,
                there's little point returning a dict containing one; this
                behaviour may change in the future. Any field ending with _pid
                (and there should be only one such field) is a primary key and
                will be removed by default.
        ----------------------------------------------------------------------
        returns
            table : dict
        ----------------------------------------------------------------------
        """
        # Perform some sanity checks on the supplied table and field names.
        # Calls to describe() are cached, so the cost for these checks is
        # minimal.

        # check table name exists in the db
        db_table_names = self.describe().data
        if table_name not in db_table_names:
            logging.warning(
                'get_table_row_and_modify: unrecognised table "%s"', table_name
            )
            return {}

        # check field names contained in method arguments are valid
        db_field_names = self.describe(table_name).data
        if replacements is None:
            replacements = {}
        categories = {'select': select, 'replacements': replacements}
        select_fail = False

        for category, fields in categories.items():
            for field in fields:
                if field not in db_field_names:
                    logging.warning(
                        (
                            'get_table_row_and_modify: '
                            'table "%s", unrecognised field "%s" (%s)'
                        ),
                        table_name, field, category
                    )
                    select_fail = True

        if select_fail:
            return {}

        # checks complete: process enquiry

        # get the Pandas DataFrame for a subset of this table
        pdf_original = self.get(table_name, **select).data

        # drop all columns with Na{N/T} values
        pdf = pdf_original.dropna(axis=1)

        # convert to dict
        rows = pdf.to_dict('records')

        # if the result is empty, exit early
        if not rows:
            return {}

        num_rows = len(rows)
        if num_rows > 1:
            logging.warning(
                'get_table_row_and_modify: query returned %s rows (expected 1)', num_rows
            )
        table = rows[-1]

        for field, value in replacements.items():
            table[field] = value

        # remove PID field
        if omit_pid:
            table = {
                k: v for k, v in table.items()
                if not k.lower().endswith('_pid')
            }

        return table

    def get_vtile_info(self, qrcode):
        """
        Collate comprehensive information about a vTile given its QR-code.
        Amongst other information, the original wafer position of each SiPM is
        obtained.

        This is an EXPENSIVE method to call with many sequential database
        lookups. It may take a minute to complete.

        ----------------------------------------------------------------------
        args
            qrcode : int
        ----------------------------------------------------------------------
        returns : dict or None
            None is returned if any required datum could not be obtained.
            e.g.
                {
                    'qrcode': 23010603000083001,
                    'vpcb_pid': 58,
                    'vpcb_asic_pid': 75,
                    'vtile_pid': 63,
                    'sipm_1': {
                        'sipm_id': 691,
                        'lot': 9262109,
                        'wafer_number': 15,
                        'column': 4,
                        'row': 6
                    },
                    ...
                    'sipm_24': {
                        'sipm_id': 726,
                        'lot': 9262109,
                        'wafer_number': 15,
                        'column': 10,
                        'row': 4
                    },
                    'vpdu_id': nan,
                    'run_number': 2,
                    'production_date': '2023-01-12 13:00:00',
                    'solder_id': 13,
                    'institute_id': 5,
                    'institute_text': 'University of Liverpool',
                    'solder': {
                        'solder_pid': 13,
                        'manufacturer': 4,
                        'solder_type': 'Indium Paste NC-SMQ80 Ind#1E 52In48Sn...',
                        'production_date': '2022-11-10 00:00:00',
                        'room_temperature_date': '2022-12-12 15:00:00',
                        'expiry_date': '2023-05-10 00:00:00',
                        'syringe_id': 9,
                        'lot': 'PS11124740',
                        'mass': 25,
                        'institute_id': 5
                    },
                    'unique_wafers': {(9262109, 15), (9262109, 13)}
                }
        ----------------------------------------------------------------------
        """
        if not qr_code_valid(qrcode):
            return None

        summary = {'qrcode': qrcode}

        ##########################################################################
        response = self.get('vpcb', qrcode=qrcode)
        if response.network_timeout:
            return None

        try:
            vpcb_pid = int(response.data.vpcb_pid.values)
        except TypeError:
            return None

        summary['vpcb_pid'] = vpcb_pid

        ##########################################################################
        response = self.get('vpcb_asic', vpcb_id=vpcb_pid)
        if response.network_timeout:
            return None
        try:
            vpcb_asic_pid = int(response.data.vpcb_asic_pid.values)
        except TypeError:
            # some vpcbs never became vpcb_asic
            return None

        summary['vpcb_asic_pid'] = vpcb_asic_pid

        ##########################################################################
        response = self.get('vtile', vpcb_asic_id=vpcb_asic_pid)
        if response.network_timeout:
            return None
        try:
            vtile_table = response.data.to_dict('records')[-1]
        except IndexError:
            # some early vPCB entries never became vTiles
            return None

        summary.update(vtile_table)
        del summary['vpcb_asic_id']

        ##########################################################################
        response = self.get('institute', id=vtile_table['institute_id'])
        if response.network_timeout:
            return None
        institute_text = response.data.name.values[-1]
        summary['institute_text'] = institute_text

        ##########################################################################
        response = self.get('solder', solder_pid=vtile_table['solder_id'])
        if response.network_timeout:
            return None
        solder = response.data.to_dict('records')[-1]
        summary['solder'] = solder

        ##########################################################################
        # compute original wafer locations for SiPMs
        #
        # It seems safest to assume that requests.Session is not thread-safe.
        # Let's do this sequentially for the moment, and implement proper use of
        # the connection pool later.
        sipms = {k: v for k, v in summary.items() if k.startswith('sipm_')}

        for sipm_name, sipm_id in sipms.items():
            location = self.get_wafer_location_from_sipm_pid(sipm_id)
            summary[sipm_name] = {**{'sipm_id': sipm_id}, **location}

        ##########################################################################
        # get unique wafers
        summary['unique_wafers'] = {
            (v['lot'], v['wafer_number'])
            for k, v in summary.items()
            if k.startswith('sipm_')
        }

        return summary

    def get_vtile_pids_from_sipm_pids(self, sipm_pids):
        """
        Find out which vTile(s) SiPMs have been allocated to.

        Since a SiPM can only be attached to one vTile, the purpose of this
        method is to help track down problematic data entry.

        WARNING: This method will become expensive to run once the database
        becomes more populated.

        ----------------------------------------------------------------------
        args
            sipm_pids : iterable (containing int(s))
        ----------------------------------------------------------------------
        returns : dict (or None if the caller supplied a non-iterable)
            {sipm_pid: [vtile_pid, ...], ...}
                E.g. {19: [6, 12], 33: [12, 46]}
        ----------------------------------------------------------------------
        """
        def spid_to_vpids(vt_tab, colnames, sipm_pid):
            """sipm_pid -> [vtile_pid, vtile_pid, ...]"""
            return list(
                vt_tab.loc[
                    np.where(vt_tab[colnames].isin([sipm_pid]) == True)[0]
                ].vtile_pid.values
            )

        vtile_table = self.get('vtile').data
        column_names = [f'sipm_{x}' for x in range(1, 24 + 1)]

        try:
            return {
                sipm_pid: spid_to_vpids(vtile_table, column_names, sipm_pid)
                for sipm_pid in sipm_pids
            }
        except TypeError:
            return None

    def get_wafer_location_from_sipm_pid(self, sipm_pid):
        """
        Identify a SiPM's original wafer location based on its PID.

        ----------------------------------------------------------------------
        args
            sipm_pid : int
        ----------------------------------------------------------------------
        returns : dict
            E.g. {'lot': 9262109, 'wafer_number': 13, 'column': 12, 'row': 13}
        ----------------------------------------------------------------------
        """
        sipm = self.get('sipm', sipm_pid=sipm_pid).data.to_dict('records')[-1]
        wafer = self.get('wafer', wafer_pid=sipm['wafer_id']).data.to_dict('records')[-1]

        return {
            'lot': wafer['lot'],
            'wafer_number': wafer['wafer_number'],
            'column': sipm['column'],
            'row': sipm['row'],
        }

    ##########################################################################
    # requests HEAD
    ##########################################################################

    def remote_file_exists(self, url):
        """
        Check if a remote file exists at the given URL. It's only necessary to
        fetch the headers.
        """
        result = False

        try:
            response = self.session.head(url, timeout=46)
        except (requests.ConnectionError, requests.exceptions.ConnectTimeout):
            return result

        if response.status_code != requests.codes.ok:
            return result

        return True

    ##########################################################################
    # requests POST
    ##########################################################################

    ##########################################################################
    # generic

    @staticmethod
    def _dict_to_csv_string(table):
        """
        Convert a dictionary into a CSV-formatted string that requests.post
        will accept as a file.

        Support function for _post_generic().

        ----------------------------------------------------------------------
        args
            table : dict
                e.g.
                    {
                        'manufacturer': 2,
                        'lot': 3,
                        'wafer_number': 6,
                        'spad_size': 30,
                        'dose': 3,
                        'production_date': '2022-09-06 15:30:14',
                        'description': 5,
                    }
        ----------------------------------------------------------------------
        returns : string
            e.g.
                (
                    'manufacturer,lot,wafer_number,spad_size,dose,'
                    'production_date,description\n'
                    '2,3,6,30,3,2022-09-06 15:30:14,5\n'
                )
        ----------------------------------------------------------------------
        """
        sio = io.StringIO()

        # match line terminator used by pandas.DataFrame.from_dict
        csvw = csv.writer(sio, lineterminator='\n')

        csvw.writerow(table.keys())
        csvw.writerow(table.values())

        return sio.getvalue()

    def _post_generic(self, table, url_suffix):
        """
        Generic internal member function to POST a table to the database.

        ----------------------------------------------------------------------
        args
            table : dict
                e.g.
                    {
                        'manufacturer': 2,
                        'lot': 3,
                        'wafer_number': 6,
                        'spad_size': 30,
                        'dose': 3,
                        'production_date': '2022-09-06 15:30:14',
                        'description': 5,
                    }
            url_suffix : string
        ----------------------------------------------------------------------
        returns : bool
        ----------------------------------------------------------------------
        exceptions : may raise TypeError
        ----------------------------------------------------------------------
        """
        if not isinstance(table, dict):
            raise TypeError('Expected argument <table> to be a dictionary.')

        full_url = urllib.parse.urljoin(self.base_url, f'{url_suffix}?d=,&f=csv')

        try:
            response = self.session.post(
                full_url,
                files={'file': ('table.csv', self._dict_to_csv_string(table))}
            )
        except http_client.RemoteDisconnected:
            status = False
            logging.error('remote disconnected')
        else:
            status = response.status_code == requests.codes.ok

        return status

    ##########################################################################
    # categorical

    def _bad_fields(self, table, table_name, comp_fn):
        """
        Try and help the POST operation caller by identifying any announcing
        any incorrect fields, rather than getting a 400 bad request and leaving
        the caller with a return value of False.

        It's highly likely the caller will get the order of the arguments
        wrong at some stage when calling a POST operation. Try and avoid
        support issues by providing helpful feedback when that happens.

        Attempting to write a table with an explicitly specified primary key
        is unsupported by the database, so announce this to the user.

        comp_fn is a lambda expression used to detect user-submitted primary
        keys, such that this method can be used for checking fields for items
        and measurements.

        ----------------------------------------------------------------------
        args
            table : dict
                e.g.
                    {
                        'manufacturer': 2,
                        'lot': 3,
                        'wafer_number': 6,
                        'spad_size': 30,
                        'dose': 3,
                        'production_date': '2022-09-06 15:30:14',
                        'description': 5,
                    }
            table_name : string
            comp_fn : lambda function
        ----------------------------------------------------------------------
        returns : bool
        ----------------------------------------------------------------------
        exceptions : may raise TypeError
        ----------------------------------------------------------------------
        """
        if not isinstance(table, dict):
            raise TypeError('Expected argument <table> to be a dictionary.')

        try:
            db_fields = self.describe(table_name).data
        except TypeError:
            logging.error(
                'Argument order supplied to function may be incorrect.'
            )
            return True

        unrecognised_fields = {
            user_field
            for user_field in table
            if user_field not in db_fields
        }

        for field in unrecognised_fields:
            logging.error(
                'table %s, unrecognised field: %s', table_name, field
            )

        # additional check for primary keys
        primary_keys = {user_field for user_field in table if comp_fn(user_field)}
        for primary_key in primary_keys:
            logging.error(
                'explicitly specified primary keys are unsupported: %s', primary_key
            )

        # check for (potentially) missing fields
        # This may generate some false positives for fields that are optional
        # (not specified as non-NULL).
        for db_field in db_fields:
            if comp_fn(db_field):
                continue

            if db_field not in table:
                logging.warning('missing field: %s', db_field)

        return bool(unrecognised_fields)

    def post_item(self, table, table_name):
        """
        POST a table for a "physical" item to the database.

        ----------------------------------------------------------------------
        args
            table : dict
                e.g.
                    {
                        'manufacturer': 2,
                        'lot': 3,
                        'wafer_number': 6,
                        'spad_size': 30,
                        'dose': 3,
                        'production_date': '2022-09-06 15:30:14',
                        'description': 5,
                    }
            table_name : string
                e.g. 'wafer'
        ----------------------------------------------------------------------
        returns : bool
            Success of POST operation.
        ----------------------------------------------------------------------
        """
        # skip the POST operation if it will certainly fail
        if self._bad_fields(table, table_name, lambda f: f.endswith('_pid')):
            return False

        return self._post_generic(table, f'item/{table_name}')

    def post_measurement(self, table, table_name):
        """
        POST a table for a test result to the database.

        ----------------------------------------------------------------------
        args
            table : dict
                e.g.
                    {
                        'manufacturer': 2,
                        'lot': 3,
                        'wafer_number': 6,
                        'spad_size': 30,
                        'dose': 3,
                        'production_date': '2022-09-06 15:30:14',
                        'description': 5,
                    }
            table_name : string
        ----------------------------------------------------------------------
        returns : bool
            Success of POST operation.
        ----------------------------------------------------------------------
        """
        if not table_name.endswith('_test'):
            table_name += '_test'

        # skip the POST operation if it will certainly fail
        if self._bad_fields(table, table_name, lambda f: f == 'id'):
            return False

        return self._post_generic(
            table, f'measure/{removesuffix(table_name, "_test")}'
        )

    ##########################################################################
    # specific physical items
    #
    # These methods are simply wrappers for the generic post_item call.
    #
    # They are only defined to give an interactive user a chance to get the
    # database submission right by referring to the method documentation
    # using the Python interpreter's 'help()' command.
    #

    def post_pcb(self, table):
        """
        POST table: pcb
        """
        # return self.post_item(table, 'pcb')
        raise NotImplementedError

    def post_pdu(self, table):
        """
        POST table: pdu
        """
        # return self.post_item(table, 'pdu')
        raise NotImplementedError

    def post_manufacturer(self, table):
        """
        POST table: manufacturer

        The database consistently responds with "bad response" to this POST
        operation for some reason. The similar curl operation on the command
        line also fails. Tested 2022 09 09.
        """
        # return self.post_item(table, 'manufacturer')
        raise NotImplementedError

    def post_sipm(self, table):
        """
        POST table: sipm

        ----------------------------------------------------------------------
        args
            table : dict
                e.g.
                    {
                        # the wafer this device was picked from
                        'wafer_id': 2,
                        'sipm_grip_ring_id': 1,
                        'column, 12,
                        'row': 6,
                        'tile_type': 'VETO',
                        # the tile this SiPM is mounted on, if any
                        'tile_id: 12,
                    }
        ----------------------------------------------------------------------
        returns : bool
            Success of POST operation.
        ----------------------------------------------------------------------
        """
        return self.post_item(table, 'sipm')

    def post_solder(self, table):
        """
        POST table: solder

        Add solder paste syringe to the database.

        Example syringe label:

        INDIUM CORPORATION

        IPN: PASTEIN-83752-C001        ENGLISH
        FLUX: NC-SMQ80                 MADE IN THE USA
        COMP: 52IN 48SN                INDALLOY:1E
        MESH: -400+635                 LOT: PS11120734
        METAL: 83%                     QUAN (Gms): 25
                                       MFG: 02Jun2022
                                       USE BY: 02Dec2022
                                       STORE: -20°C to 5°C

        ----------------------------------------------------------------------
        args
            table : dict
                e.g.
                    {# Almost certainly Indium Corp.
                     'manufacturer': 4,
                     'solder_type': 'Indium Paste NC-SMQ80 Ind#1E 52In48Sn...',
                     # From the syringe label ("MFG").
                     'production_date': '2022-06-02 00:00:00',
                     # The date the syringe was taken from cold storage and
                     # brought up to room temperature.
                     'room_temperature_date': '2022-07-18 16:00:00',
                     # From the syringe label ("USE BY").
                     'expiry_date': '2022-12-02 00:00:00',
                     # The site's internal reference number for the syringe
                     'syringe_id': 7,
                     # From the syringe label ("LOT").
                     'lot': 'PS11120734',
                     # Mass of solder paste contained in the syringe (grams)
                     'mass': 25}
        ----------------------------------------------------------------------
        returns : bool
            Success of POST operation.
        ----------------------------------------------------------------------
        """
        return self.post_item(table, 'solder')

    def post_tile(self, table):
        """
        POST table: tile
        """
        # return self.post_item(table, 'tile')
        raise NotImplementedError

    def post_vasic(self, table):
        """
        POST table: vasic

        This is for a Veto ASIC.

        ----------------------------------------------------------------------
        args
            table : dict
                e.g.
                    {
                        'vasic_grip_ring_id: 1,
                        'vasic_wafer_id': 2,
                        'column': 6,
                        'row': 5,
                        'vpcb_asic_id': 5,
                    }
        ----------------------------------------------------------------------
        returns : bool
            Success of POST operation.
        ----------------------------------------------------------------------
        """
        return self.post_item(table, 'vasic')

    def post_vasic_grip_ring(self, table):
        """
        POST table: vasic_grip_ring

        ----------------------------------------------------------------------
        args
            table : dict
                e.g. {'serial: '1234'}
        ----------------------------------------------------------------------
        returns : bool
            Success of POST operation.
        ----------------------------------------------------------------------
        """
        return self.post_item(table, 'vasic_grip_ring')

    def post_vasic_wafer(self, table):
        """
        POST table: vasic_wafer

        ----------------------------------------------------------------------
        args
            table : dict
                e.g.
                    {
                        'production_date': '2022-09-06 15:30:14',
                        'manufacturer': 2,
                        'run_number', 123,
                        'serial': '123',
                    }
        ----------------------------------------------------------------------
        returns : bool
            Success of POST operation.
        ----------------------------------------------------------------------
        """
        return self.post_item(table, 'vasic_wafer')

    def post_vcable(self, table):
        """
        POST table: vcable

        ----------------------------------------------------------------------
        args
            table : dict
                e.g.
                    {
                        'production_date': '2022-09-06 15:30:14',
                        'manufacturer': 6,
                        'run_number', 123,
                        'serial': '123',
                        'type': '1234',
                        'length': 1.6,
                    }
        ----------------------------------------------------------------------
        returns : bool
            Success of POST operation.
        ----------------------------------------------------------------------
        """
        return self.post_item(table, 'vcable')

    def post_vmotherboard(self, table):
        """
        POST table: vmotherboard

        This is for a Veto motherboard with a vpdu installed.

        ----------------------------------------------------------------------
        args
            table : dict
                e.g.
                    {
                        'production_date': '2022-09-06 15:30:14',
                        'manufacturer': 6,
                        'run_number', 123,
                        'qrcode': '22060101112345123',
                        'vpdu_id': 6,
                    }
        ----------------------------------------------------------------------
        returns : bool
            Success of POST operation.
        ----------------------------------------------------------------------
        """
        return self.post_item(table, 'vmotherboard')

    def post_vpcb(self, table):
        """
        POST table: vpcb

        This is for a bare Veto PCB.

        ----------------------------------------------------------------------
        args
            table : dict
                e.g.
                    {
                        'production_date': '2022-09-06 15:30:14',
                        'manufacturer': 5,
                        'run_number', 12,
                        'qrcode': '22060101112345789',
                        # Omit this field if submitting the blank PCB for the
                        # first time. When this PCB has an ASIC added later
                        # and becomes a vpcb_asic, this ID can be added to
                        # point to that.
                        'vpcb_asic_id': 3,
                    }
        ----------------------------------------------------------------------
        returns : bool
            Success of POST operation.
        ----------------------------------------------------------------------
        """
        return self.post_item(table, 'vpcb')

    def post_vpcb_asic(self, table):
        """
        POST table: vpcb_asic

        This is for a Veto PCB with back-side components and an ASIC installed.

        ----------------------------------------------------------------------
        args
            table : dict
                e.g.
                    {
                        'production_date': '2022-09-06 15:30:14',
                        'vpcb_id': 5,
                        'vasic_id', 12,
                        'solder_mass': 18.1,
                        # this refers to the original bare vTile PCB's ID.
                        'vtile_id': 3,
                    }
        ----------------------------------------------------------------------
        returns : bool
            Success of POST operation.
        ----------------------------------------------------------------------
        """
        return self.post_item(table, 'vpcb_asic')

    def post_vpdu(self, table):
        """
        POST table: vpdu

        This is for a Veto PDU with 16 vtiles installed.

        ----------------------------------------------------------------------
        args
            table : dict
                e.g.
                    {
                        'production_date': '2022-09-06 15:30:14',
                        'manufacturer': 7,
                        'run_number': 234,
                        'serial': '1234567A'
                        'vmotherboard_id': 5,
                        # 16x vtile_pid
                        'vtile_1': 17,
                        'vtile_2': 18,
                        'vtile_3': 19,
                        'vtile_4': 20,
                        'vtile_5': 21,
                        'vtile_6': 22,
                        'vtile_7': 23,
                        'vtile_8': 24,
                        'vtile_9': 25,
                        'vtile_10': 26,
                        'vtile_11': 27,
                        'vtile_12': 28,
                        'vtile_13': 29,
                        'vtile_14': 30,
                        'vtile_15': 31,
                        'vtile_16': 32,
                        'detector_id': 3,
                    }
        ----------------------------------------------------------------------
        returns : bool
            Success of POST operation.
        ----------------------------------------------------------------------
        """
        return self.post_item(table, 'vpdu')

    def post_vtile(self, table):
        """
        POST table: vtile

        This is for a Veto PCB with back-side components, ASIC and SiPMs
        installed.

        The SiPM numbering is shown looking at the PCB with SiPMs visible and
        towards the viewer, and the backside components
        (resistors, capacitors, ASIC etc.) facing away from the viewer. The
        location of the QR code and ASIC on the back-side of the PCB are also
        shown to provide orientation.

        +----+----+----+----+
        | 19 | 13 |  7 |  1 |
        +----+---QR----+----+
        | 20 | 14 |  8 |  2 |
        +----+----+----+----+
        | 21 | 15 |  9 |  3 |
        +----+----+----+----+
        | 22 | 16 | 10 |  4 |
        +----+---ASIC--+----+
        | 23 | 17 | 11 |  5 |
        +----+----+----+----+
        | 24 | 18 | 12 |  6 |
        +----+----+----+----+

        ----------------------------------------------------------------------
        args
            table : dict
                e.g.
                    {
                        'production_date': '2022-09-06 15:30:14',
                        'manufacturer': 7,
                        'run_number': 234,
                        'serial': '1234567A'
                        'vpcb_asic_id': 5,
                        'solder_id': 2,
                        # 24x sipm_pid
                        'sipm_1': 17,
                        'sipm_2': 18,
                        'sipm_3': 19,
                        'sipm_4': 20,
                        'sipm_5': 21,
                        'sipm_6': 22,
                        'sipm_7': 23,
                        'sipm_8': 24,
                        'sipm_9': 25,
                        'sipm_10': 26,
                        'sipm_11': 27,
                        'sipm_12': 28,
                        'sipm_13': 29,
                        'sipm_14': 30,
                        'sipm_15': 31,
                        'sipm_16': 32,
                        'sipm_17': 33,
                        'sipm_18': 34,
                        'sipm_19': 35,
                        'sipm_20': 36,
                        'sipm_21': 37,
                        'sipm_22': 38,
                        'sipm_23': 39,
                        'sipm_24': 40,
                        # Omit this field if submitting the tile for the
                        # first time. When this tile is assembled onto a vPDU
                        # later, this ID can be added to point to that.
                        'vpdu_id': 3,
                    }
        ----------------------------------------------------------------------
        returns : bool
            Success of POST operation.
        ----------------------------------------------------------------------
        """
        return self.post_item(table, 'vtile')

    def post_wafer(self, table):
        """
        POST table: wafer

        Add a SiPM wafer table to the database.

        ----------------------------------------------------------------------
        args
            table : dict
                e.g.
                    {
                        'manufacturer': 2,
                        'lot': 3,
                        'wafer_number': 6,
                        'spad_size': 30,
                        'dose': 3,
                        'production_date': '2022-09-06 15:30:14',
                        'description': 5,
                    }
        ----------------------------------------------------------------------
        returns : bool
            Success of POST operation.
        ----------------------------------------------------------------------
        """
        return self.post_item(table, 'wafer')

    def post_wafer_defects(self, table):
        """
        POST table: wafer_defects
        """
        # return self.post_item(table, 'wafer_defects')
        raise NotImplementedError

    def post_wafer_status(self, table):
        """
        POST table: wafer_status
        """
        # return self.post_item(table, 'wafer_status')
        raise NotImplementedError

    ##########################################################################
    # specific test results
    #
    # These methods are simply wrappers for the generic post_measurement call.
    #
    # They are only defined to give an interactive user a chance to get the
    # database submission right by referring to the method documentation
    # using the Python interpreter's 'help()' command.
    #

    def post_dummyload_test(self, table):
        """
        POST table: dummyload_test
        """
        # return self.post_measurement(table, 'dummyload_test')
        raise NotImplementedError

    def post_pdu_pulse_test(self, table):
        """
        POST table: pdu_pulse_test
        """
        # return self.post_measurement(table, 'pdu_pulse_test')
        raise NotImplementedError

    def post_tile_cold_test(self, table):
        """
        POST table: tile_cold_test
        """
        # return self.post_measurement(table, 'tile_cold_test')
        raise NotImplementedError

    def post_tile_warm_test(self, table):
        """
        POST table: tile_warm_test
        """
        # return self.post_measurement(table, 'tile_warm_test')
        raise NotImplementedError

    def post_user_test(self, table):
        """
        POST table: user_test
        """
        # return self.post_measurement(table, 'user_test')
        raise NotImplementedError

    def post_vasic_test(self, table):
        """
        POST table: vasic_test
        """
        # return self.post_measurement(table, 'vasic_test')
        raise NotImplementedError

    def post_sipm_test(self, table):
        """
        POST table: sipm_test

        Add a test result for a SiPM that exists in the database.

        ----------------------------------------------------------------------
        args
            table : dict
                e.g.
                    {
                        'timestamp': '2022-09-06 15:30:14',
                        # initials of person adding this test result
                        'operator': 'ap',
                        'sipm_id': 137,
                        # 1=pass, 0=fail
                        'good': 1,
                        'comment': 'good/bad status based solely on wafer...',
                    }
        ----------------------------------------------------------------------
        returns : bool
            Success of POST operation.
        ----------------------------------------------------------------------
        """
        return self.post_measurement(table, 'sipm')

    def post_vpcb_asic_test(self, table):
        """
        POST table: vpcb_asic_test

        ----------------------------------------------------------------------
        args
            table : dict
        ----------------------------------------------------------------------
        returns : bool
            Success of POST operation.
        ----------------------------------------------------------------------
        """
        return self.post_measurement(table, 'vpcb_asic')

    def post_vpcb_test(self, table):
        """
        POST table: vpcb_test

        ----------------------------------------------------------------------
        args
            table : dict
        ----------------------------------------------------------------------
        returns : bool
            Success of POST operation.
        ----------------------------------------------------------------------
        """
        return self.post_measurement(table, 'vpcb')

    def post_vpdu_cold_test(self, table):
        """
        POST table: vpdu_cold_test

        ----------------------------------------------------------------------
        args
            table : dict
        ----------------------------------------------------------------------
        returns : bool
            Success of POST operation.
        ----------------------------------------------------------------------
        """
        return self.post_measurement(table, 'vpdu_cold_test')

    def post_vpdu_test(self, table):
        """
        POST table: vpdu_test

        ----------------------------------------------------------------------
        args
            table : dict
        ----------------------------------------------------------------------
        returns : bool
            Success of POST operation.
        ----------------------------------------------------------------------
        """
        return self.post_measurement(table, 'vpdu_test')

    def post_vmotherboard_test(self, table):
        """
        POST table: vmotherboard_test

        ----------------------------------------------------------------------
        args
            table : dict
        ----------------------------------------------------------------------
        returns : bool
            Success of POST operation.
        ----------------------------------------------------------------------
        """
        return self.post_measurement(table, 'vmotherboard')

    def post_vtile_test(self, table):
        """
        POST table: vtile_test

        ----------------------------------------------------------------------
        args
            table : dict
        ----------------------------------------------------------------------
        returns : bool
            Success of POST operation.
        ----------------------------------------------------------------------
        """
        return self.post_measurement(table, 'vtile')

    def post_vtile_cold_test(self, table):
        """
        POST table: vtile_cold_test
        """
        # return self.post_measurement(table, 'vtile_cold_test')
        raise NotImplementedError
