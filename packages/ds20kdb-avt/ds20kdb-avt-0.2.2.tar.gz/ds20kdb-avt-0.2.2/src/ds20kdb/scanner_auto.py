#!/usr/bin/env python3
r"""
Cross-platform script to manage "vpcb_asic", "vtile", "vmotherboard"
and "vpdu" scanner images. Copies the file to a webserver preserving the
timestamp, and updates the DB with the URL of the image, on the vpdu,
vmotherboard, vtile_test or vpcb_asic_test tables.

This version of the script has been designed to assist with the automation
(bulk submission) of scanned images. To enable this, the filename of
scanned images must be in the following two formats:

<qrcode>_<component>_<side>.png
<qrcode>_<component>_<side>_<info>.png

Only the first three parameters are used, the info parameter is ignored (it is
used locally to indicate incoming/outgoing inspection).

For safety, no uploads will be performed without --write (-w), and duplicate
records will not be overwritten without --overwrite (-o).

Examples showing both forms of authentication (macOS/Linux):

./scanner_auto.py <initials> <institute> -s ~/.ds20kdb_scanner_rc
./scanner_auto.py <initials> <institute> -c <remote_username> ~/.ssh/id_ecdsa

./scanner_auto.py tl liverpool -c tle ~/.ssh/id_ecdsa

or from Windows Anaconda PowerShell Prompt:

python scanner_auto.py tl liverpool -c tle $HOME\.ssh\id_ecdsa

If your files are in a specific directory you can use something like this:

python scanner_auto.py tl liverpool -c tle $HOME\.ssh\id_ecdsa -d $HOME\scans

Based on the original script by P.Franchini - p.franchini@lancaster.ac.uk
Available at:

    https://gitlab.in2p3.fr/darkside/productiondb_software/-/
            blob/master/examples_python/submit_scanner/scanner.py
"""

import argparse
import contextlib
from datetime import datetime
import glob
import hashlib
import itertools
import json
import logging
import os
import pathlib
import posixpath
import socket
import sys
import types

import paramiko
from PIL import Image

from ds20kdb import interface

if tuple(map(int, interface.__version__.split('.'))) < (0, 0, 86):
    raise RuntimeError(
        'ds20kdb v0.0.81 or newer required to run this script\n'
        'See https://gitlab.in2p3.fr/darkside/productiondb_software/'
    )


##############################################################################
# data structures
##############################################################################


class Connect:
    """
    Create a persistent SSH connection for use by a context manager.
    """
    remote_filestore = 'linappserv3.pp.rhul.ac.uk'

    def __init__(self, args):
        self.ssh = None

        try:
            remote_ipv4 = socket.getaddrinfo(self.remote_filestore, 0)[0][-1][0]
        except (IndexError, socket.gaierror):
            print(f'Could not obtain IP address for {self.remote_filestore}')
        else:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
                ssh.connect(
                    remote_ipv4, username=args.user, key_filename=args.key,
                )
            except (FileNotFoundError, TimeoutError, paramiko.ssh_exception.SSHException):
                print('Could not connect to remote image filestore.')
            else:
                self.ssh = ssh

    def __enter__(self):
        return self.ssh

    def __exit__(self, exc_type, exc_value, exc_traceback):
        with contextlib.suppress(AttributeError):
            self.ssh.close()

    def __bool__(self):
        return self.ssh is not None


class Component:
    """
    Upload a scanned image to the RHUL remote filestore and POST its
    associated record to the database.
    """
    dbi = interface.Database()

    __slots__ = {
        'comment': 'String that gets written the db table comments field.',
        'component': 'Component that was scanned.',
        'configuration': 'Hardware used to produce the scanned image.',
        'file': 'The full path and file of the scanned image.',
        'hash': (
            'Hex digest of the scanned image. This will be used later to '
            'verify that the file was uploaded successfully.'
        ),
        'key': 'Full path and file, local SSH private key.',
        'operator': 'Initials of the person who performed the scan.',
        'optical_inspection': 'URL of uploaded image.',
        'overwrite': (
            'Flag used to indicate if existing records may be overwritten'
        ),
        'institute': (
            'Search text used to find the institute_id. Used as the end of the '
            'remote path.'
        ),
        'institute_id': 'Numeric value from looking up institute in the database.',
        'institute_text': (
            'Full text institution name that relates to the institute_id.'
        ),
        'qrcode': '17-digit numeric as encoded into the QR-code image.',
        'remote_ipv4': 'IP address of the remote filestore.',
        'remote_path': 'URL of the location scanned images are uploaded to.',
        'side': 'The side of the PCB that was scanned.',
        'ssh': 'Instance of class Connect, persistent ssh connection.',
        'table': 'Table to be written to the database.',
        'timestamp_db': 'Timestamp string.',
        'timestamp_file': 'Timestamp string.',
        'user': 'Username for RHUL SSH/SFTP login, used for image upload.',
        'write': 'Flag used to enable/disable file upload and database writes.',
    }

    def __init__(self, args, image_details, ssh):
        self.file, self.qrcode, self.component, self.side = image_details
        self.ssh = ssh

        self.operator = args.operator
        self.institute = args.institute
        self.configuration = args.configuration
        self.write = args.write
        self.overwrite = args.overwrite

        self.optical_inspection = None
        self.table = None

        datetime_obj = datetime.fromtimestamp(os.path.getmtime(self.file))
        self.timestamp_db = datetime_obj.strftime('%Y-%m-%dT%H:%M:%S')
        self.timestamp_file = datetime_obj.strftime('%Y%m%dT%H%M%S')

        self.remote_path = posixpath.join('/scratch4/DarkSide/scanner', self.institute)
        self.comment = ', '.join(['visual inspection', self.component, self.side])

        self.hash = None

        # get institute ID and text of full institute name
        response = self.dbi.get_institute_id(self.institute)
        if response.network_timeout:
            print('timeout when trying to obtain institute_id')
            self.institute_id = None
            return

        self.institute_id = response.data
        try:
            self.institute_text = self.dbi.get(
                'institute', id=self.institute_id
            ).data.name.iloc[-1]
        except AttributeError:
            self.institute_text = None
            print('Failed to find full text institute name.')

    def __str__(self):
        items = {
            ' ': '-' * 40,
            'Image': self.file,
            'Image source': self.configuration,
            'Timestamp (database)': self.timestamp_db,
            'Timestamp (remote file)': self.timestamp_file,
            'Operator\'s initials': self.operator,
            'QR-code': self.qrcode,
            'Scanned component': self.component,
            'Scanned side': self.side,
            'Institute (remote suffix)': self.institute,
            'Institute full text': self.institute_text,
            'Institute ID': self.institute_id,
            'Comment field': self.comment,
            'Remote path': self.remote_path,
            'Permission to write': self.write,
            '  ': '-' * 40,
        }
        return '\n'.join(f'{k:<28}{v}' for k, v in items.items())

    def upload_image(self):
        """
        Upload file to linappserv3.pp.rhul.ac.uk using the SSH File Transfer
        Protocol.

        Checking if the file was uploaded and is readable is done via SFTP
        because on linappserv3, there's an unpredictable lag between writing
        the file and it being visible on the webserver. We don't
        particularly care about this delay because we're not going to try to
        view the contents of the file immediately, we're just going to write
        the URL to the db. This constitutes an adequate check.

        $ dig linappserv3.pp.rhul.ac.uk

        ;; ANSWER SECTION:
        linappserv3.pp.rhul.ac.uk. 86400 IN A   134.219.108.205

        If this instance refers to a TIFF file, it will be converted to a
        lossless PNG file before upload.

        ----------------------------------------------------------------------
        args : none
        ----------------------------------------------------------------------
        returns : none
            self.file and self.optical_inspection modified
            A PNG file may be created
        ----------------------------------------------------------------------
        """
        if not self.write:
            print('Use the --write command line option to enable image uploads.')
            return

        # Make sure we're uploading a PNG file, so we don't fill up the remote
        # filestore with huge uncompressed TIFF files from the scanner.
        extension = os.path.splitext(self.file)[-1].lower()
        if extension in {'.tif', '.tiff'}:
            print('converting file from TIFF to PNG')
            self.file = create_png_from_tiff(self.file)

        image_size_bytes = os.path.getsize(self.file)
        print(f'Uploading ~{image_size_bytes // (1024 * 1024)}MB...')

        filename = f'{self.qrcode}-{self.side}-{self.timestamp_file}.png'
        url = f'https://www.pp.rhul.ac.uk/DarkSide/scanner/{self.institute}/{filename}'

        # This temporarily loads the entire image into memory. Scanned images
        # should be around 60MB in size, so no problems are expected with
        # memory usage. SHA256 is used instead of blake2b simply because
        # sha256sum is available at the far end from the command line.
        with open(self.file, 'rb') as scanned_image:
            self.hash = hashlib.sha256(scanned_image.read()).hexdigest()

        print(f' local hash: {self.hash}')

        remote_file_readable = False

        with contextlib.closing(self.ssh.open_sftp()) as sftp:

            # create remote directory for the give institute name
            try:
                sftp.chdir(self.remote_path)  # Test if remote_path exists
            except (FileNotFoundError, IOError):
                sftp.mkdir(self.remote_path)  # Create remote_path
                sftp.chdir(self.remote_path)

            # send file, overwriting existing file and preserving the time
            local_file_path = self.file
            local_file_mtime = os.path.getmtime(local_file_path)

            remote_file_path = posixpath.join(self.remote_path, filename)

            sftp.put(local_file_path, remote_file_path)
            sftp.utime(remote_file_path, (local_file_mtime, local_file_mtime))

            # Check if local and remote files are the same.
            #
            # This is almost certainly overkill given the checks SFTP
            # performs. However, in the case where (for some reason)
            # garbage collection isn't performed at the far end in the
            # case of an interrupted transfer, this will be caught here.
            # sha256sum is ubiquitous on Linux systems, including the
            # remote filestore used here.

            _stdin, stdout, _stderr = self.ssh.exec_command(f'sha256sum {remote_file_path}')
            try:
                remote_hash = stdout.read().split()[0].decode('utf-8')
            except IndexError:
                pass
            else:
                remote_file_readable = remote_hash == self.hash
                print(f'remote hash: {remote_hash}')

        if remote_file_readable:
            print(f'Upload verified: {url}')
            self.optical_inspection = url
        else:
            print('File not copied to RHUL or URL not accessible')
            self.optical_inspection = None

    def generate_table_for_db_post(self):
        """
        Creates a table dictionary for the component, omitting any NOT NULL
        fields.

        ----------------------------------------------------------------------
        args : none
        ----------------------------------------------------------------------
        returns : none
            self.table modified
        ----------------------------------------------------------------------
        """
        if self.optical_inspection is None:
            return

        lut = {
            # vmotherboard_test
            'vmotherboard': self.table_vmotherboard,
            # vpcb_asic_test
            'vpcb_asic': self.table_vpcb_asic,
            # vpdu_test
            'vpdu': self.table_vpdu,
            # vtile_test
            'vtile': self.table_vtile,
        }
        table_common = {
            'comment': self.comment,
            'timestamp': self.timestamp_db,
            'operator': self.operator,
            'optical_inspection': self.optical_inspection,
            'configuration': self.configuration,
            'institute_id': self.institute_id,
        }

        self.table = lut[self.component](table_common)
        print(self.table)

    def table_vtile(self, table_common):
        """
        Build the table to suit measurement: vtile_test.

        ----------------------------------------------------------------------
        args
            table_common : dict
                table fields common to all components.
        ----------------------------------------------------------------------
        returns : dict
            all table fields required for database POST operation
        ----------------------------------------------------------------------
        """
        vtile_id = self.dbi.get_vtile_pid_from_qrcode(self.qrcode).data

        if vtile_id is None:
            print(f'failed to find the vtile_id for QR-code {self.qrcode}')
            return None

        return {**table_common, **{'vtile_id': vtile_id}}

    def table_vpdu(self, table_common):
        """
        Build the table to suit measurement: vpdu_test.

        ----------------------------------------------------------------------
        args
            table_common : dict
                table fields common to all components.
        ----------------------------------------------------------------------
        returns : dict
            all table fields required for database POST operation
        ----------------------------------------------------------------------
        """
        try:
            vmotherboard_id = self.dbi.get(
                'vmotherboard', qrcode=self.qrcode
            ).data.vmotherboard_pid[0]
        except KeyError:
            print('failed to find the vmotherboard_id - probably wrong QR code')
            return None
        vpdu_id = self.dbi.get('vpdu', vmotherboard_id=vmotherboard_id).data.vpdu_pid[0]
        if vpdu_id is None:
            print('failed to find the vpdu_id - probably wrong QR code')
            return None

        return {**table_common, **{'vpdu_id': vpdu_id}}

    def table_vmotherboard(self, table_common):
        """
        Build the table to suit measurement: vmotherboard_test.

        ----------------------------------------------------------------------
        args
            table_common : dict
                table fields common to all components.
        ----------------------------------------------------------------------
        returns : dict
            all table fields required for database POST operation
        ----------------------------------------------------------------------
        """
        try:
            vmotherboard_id = self.dbi.get(
                'vmotherboard', qrcode=self.qrcode
            ).data.vmotherboard_pid[0]
        except KeyError:
            print('failed to find the vmotherboard_id - probably wrong QR code')
            return None

        return {**table_common, **{'vmotherboard_id': vmotherboard_id}}

    def table_vpcb_asic(self, table_common):
        """
        Build the table to suit measurement: vpcb_asic_test.

        ----------------------------------------------------------------------
        args
            table_common : dict
                table fields common to all components.
        ----------------------------------------------------------------------
        returns : dict
            all table fields required for database POST operation
        ----------------------------------------------------------------------
        """
        vpcb_asic_id = self.dbi.get_vpcb_asic_pid_from_qrcode(self.qrcode).data
        if vpcb_asic_id is None:
            print('failed to find the vpcb_asic_id - probably wrong QR code')
            return None

        return {**table_common, **{'vpcb_asic_id': vpcb_asic_id}}

    def post_table(self):
        """
        Post test measurement table to the database.

        ----------------------------------------------------------------------
        args : none
        ----------------------------------------------------------------------
        returns : bool
            True if POST failed, False if successful.
        ----------------------------------------------------------------------
        """
        if not self.write:
            print('Use the --write command line option to enable database writes.')
            return True

        if self.optical_inspection is None:
            print('Problems occurred during image upload, skipping database POST.')
            return True

        print("Table:\t", self.component + '_test')
        print(self.table)

        post_successful = self.dbi.post_measurement(self.table, self.component)

        status = 'succeeded' if post_successful else 'failed'
        print(f'POST {status}')

        return not post_successful

    def skip_duplicate(self):
        """
        Ignore this image file if the QR-code exists in the measurement
        database table for the component, and we don't have permission to
        overwrite.

        ----------------------------------------------------------------------
        args : none
        ----------------------------------------------------------------------
        returns : bool
            True if the current file should be ignored, False otherwise.
        ----------------------------------------------------------------------
        """
        response = self.dbi.get(f'{self.component}_test', institute_id=self.institute_id)
        if response.network_timeout:
            return False

        # find any occurrence of the QR-code in test measurement URLs
        exists = False
        for url in response.data.optical_inspection.values:
            with contextlib.suppress(TypeError):
                if self.qrcode in url:
                    exists = True
                    break

        skip = exists and not self.overwrite

        if skip:
            print(
                f'{self.qrcode}, {self.component}, {self.side}: '
                'cannot overwrite without permission (--overwrite)'
            )

        return skip


##############################################################################
# file i/o
##############################################################################


def check_scanner_image_file(filepath):
    """
    Check that the scanner image filename conforms to the required format.

    --------------------------------------------------------------------------
    args
        val : string
            filename, e.g. '23020703000088001_vtile_circuit_in.png'
    --------------------------------------------------------------------------
    returns
        filepath : string
        qrcode : string
        component : string
        side : string
    --------------------------------------------------------------------------
    """
    filename = os.path.basename(filepath)

    try:
        qrcode, component, side, *_ = os.path.splitext(filename)[0].split('_')
    except ValueError:
        print(f'{filename}: filename not in appropriate format.')
        return None

    if not interface.qr_code_valid(qrcode):
        print(f'{filename}: invalid QR-code')
        return None

    if component not in {'vpcb_asic', 'vtile', 'vmotherboard', 'vpdu'}:
        print(f'{filename}: invalid component: {component}')
        return None

    if side not in {'circuit', 'sipm'}:
        print(f'{filename}: invalid side: {side}')
        return None

    return filepath, qrcode, component, side


def create_png_from_tiff(file):
    """
    Convert an uncompressed TIFF file (RGB colour model) as generated by the
    scanner, to a PNG file with lossless compression.

    The PNG file is created in the same directory as the original TIFF file.

    --------------------------------------------------------------------------
    args
        file : string
            path and filename
                e.g. '../23020703000088001_vtile_circuit_in.tif'
    --------------------------------------------------------------------------
    returns
        png : string
            path and filename
                e.g. '../23020703000088001_vtile_circuit_in.png'
    --------------------------------------------------------------------------
    """
    png = f'{os.path.splitext(file)[0]}.png'

    with Image.open(file) as tiff_image:
        tiff_image.save(png)

    return png


def read_credentials(filename):
    """
    Read credentials dictionary from a file from the location specified on the
    command line.

    --------------------------------------------------------------------------
    args
        filename : string
    --------------------------------------------------------------------------
    returns
        dict if the read was successful, or None otherwise
            e.g. {'username': 'user123', 'key': '~/.ssh/id_ecdsa'}
    --------------------------------------------------------------------------
    """
    # confidence checks phase 1
    try:
        size_bytes = os.path.getsize(filename)
    except IOError:
        logging.error(
            'file does not exist or is inaccessible: %s',
            filename
        )
        return None

    if size_bytes > 512:
        logging.warning(
            'file is suspiciously large (%s bytes): %s',
            size_bytes, filename
        )
        return None

    # read file contents
    with open(filename, 'r', encoding='utf-8') as ds20kdb_scanner_rc:
        try:
            credentials = json.load(ds20kdb_scanner_rc)
        except json.JSONDecodeError:
            logging.error('could not read file: %s', filename)
            return None

    # confidence checks phase 2
    if not isinstance(credentials, dict):
        logging.error(
            'file did not contain a dictionary: %s', filename
        )
        return None

    num_keys = len(credentials)
    if num_keys != 2:
        logging.error(
            'file has wrong number of entries (%s): %s', num_keys,
            filename
        )
        return None

    missing = {
        x for x in ['username', 'key']
        if x not in credentials.keys()
    }
    if missing:
        logging.error(
            'file is missing key(s) (%s): %s', ', '.join(missing),
            filename
        )
        return None

    return credentials


##############################################################################
# command line option handler
##############################################################################


def check_directory_exists(directory):
    """
    Check if directory exists.

    --------------------------------------------------------------------------
    args
        directory : string
    --------------------------------------------------------------------------
    returns
        directory : string
    --------------------------------------------------------------------------
    """
    if not os.path.isdir(directory):
        raise argparse.ArgumentTypeError(
            f'{directory}: directory does not exist'
        )

    return directory


def check_credentials_file(filename):
    """
    Check the specified credentials file: load it and check if the local
    private key file exists.

    --------------------------------------------------------------------------
    args
        filename : string
            filename, e.g. '~/.ds20kdb_scanner_rc'
    --------------------------------------------------------------------------
    returns
        filename : string
    --------------------------------------------------------------------------
    """
    cred = read_credentials(filename)

    if cred is None:
        raise argparse.ArgumentTypeError(f'{filename}: problem with file')

    if not os.path.exists(cred['key']):
        raise argparse.ArgumentTypeError(
            f'{cred["key"]}: private key file does not exist'
        )

    return filename


def check_arguments():
    """
    Handle command line options.

    --------------------------------------------------------------------------
    args : none
    --------------------------------------------------------------------------
    returns
        <class 'argparse.Namespace'>
    --------------------------------------------------------------------------
    """
    parser = argparse.ArgumentParser(
        description=(
            'Uploads scanned images for "vpcb_asic", "vtile", "vmotherboard" '
            'and "vpdu" scanner images. Copies the file to a webserver '
            'preserving the timestamp, and updates the DB with the URL of the '
            'image, on the vpdu, vmotherboard, vtile_test or vpcb_asic_test '
            'tables. Cross-platform. This version of the script has been '
            'designed to assist with the automation (bulk submission) of '
            'scanned images.'
        )
    )
    parser.add_argument(
        'operator', nargs=1, metavar='operator', help='Initials of operator.', type=str
    )
    parser.add_argument(
        'institute', nargs=1, metavar='institute',
        help=(
            'Searchable name of the institute in lowercase '
            '(e.g. ral, rhul, liverpool). '
            'In addition, the institute name defines the remote URL path, '
            'for example "https://www.pp.rhul.ac.uk/DarkSide/scanner/Liverpool/"'
        ),
        choices=['liverpool', 'ral', 'rhul'],
        type=str,
    )
    parser.add_argument(
        '-d', '--directory',
        nargs=1,
        metavar='image-directory',
        help='Directory containing images to be uploaded.',
        type=check_directory_exists, default=[pathlib.Path.cwd()],
    )
    parser.add_argument(
        '--configuration', nargs=1, metavar='configuration',
        help=(
            'Inspection hardware used. '
            'Defaults to the EPSON V850 Pro scanner'
        ),
        type=str, default='Scanner EPSON V850 Pro',
    )

    group1 = parser.add_mutually_exclusive_group()
    group1.add_argument(
        '-c', '--credentials', nargs=2, metavar=('username', 'keyfile'),
        help=(
            'RHUL PP IT username and local SSH private key used to set up '
            'passwordless login.'
        ),
        type=str, default=None
    )
    group1.add_argument(
        '-s', '--sftp', nargs=1, metavar='credentials-file',
        help=(
            'File containing RHUL PP IT username and local SSH private key '
            ' used to set up passwordless login, typically '
            '~/.ds20kdb_scanner_rc.'
        ),
        type=check_credentials_file, default=None
    )

    parser.add_argument(
        '-w',
        '--write',
        action='store_true',
        help='By default - for safety - this script will write NOTHING to\
        the database. This option allows data writes to occur.',
    )
    parser.add_argument(
        '-o',
        '--overwrite',
        action='store_true',
        help=(
            'If a measurement record for the QR-code (as found in the scanned '
            'image\'s filename) is found to exist in database table '
            '<component>_test, the scanned image should be overwritten, and '
            'a new record posted to the database. '
            'The default behaviour is not to overwrite.'
        ),
    )

    args = parser.parse_args()

    args.directory = args.directory[0]
    args.operator = args.operator[0]
    args.institute = args.institute[0].lower()
    if args.credentials:
        args.user = args.credentials[0]
        args.key = args.credentials[1]
    else:
        cred = read_credentials(args.sftp[0])
        if not os.path.exists(cred['key']):
            raise argparse.ArgumentTypeError(f'{cred["key"]}: file does not exist')
        args.key = cred['key']
        args.user = cred['username']

    del args.sftp
    del args.credentials

    return args


##############################################################################
def main():
    """
    Uploads scanned images to the RHUL fileserver and creates matching
    database entries. Tested for vtile, but should also work for vpcb_asic,
    vmotherboard and vpdu.
    """
    args = check_arguments()

    failure = []
    image_files = sorted(
        itertools.chain.from_iterable(
            glob.glob(os.path.join(args.directory, f'*.{extension}'))
            for extension in ['png', 'tif', 'tiff']
        )
    )

    # ------------------------------------------------------------------------

    with Connect(args) as ssh:
        if not ssh:
            image_files.clear()
            failure.append(True)

        for file in image_files:
            image_details = check_scanner_image_file(file)

            # Ignore this file if its filename is improperly formatted.
            if image_details is None:
                continue

            comp = Component(args, image_details, ssh)

            # Ignore this file if the QR-code exists in the measurement database
            # table for the component, and we don't have permission to overwrite.
            if comp.skip_duplicate():
                continue

            print(comp)

            comp.upload_image()
            comp.generate_table_for_db_post()
            failure.append(comp.post_table())

    # ------------------------------------------------------------------------

    status = types.SimpleNamespace(success=0, unreserved_error_code=3)
    if any(failure):
        return status.unreserved_error_code

    return status.success


##############################################################################
if __name__ == "__main__":
    sys.exit(main())
