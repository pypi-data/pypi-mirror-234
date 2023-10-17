#!/usr/bin/env python3
"""
Generate a wafer map suitable for picking good SiPMs from a wafer using a die
ejector, such that they may be transferred to trays and later installed onto
vTiles.

Identification of good/bad SiPMs:

classification  quality flags
'good'          {0, 1}
'bad'           {2, 4, 5, 6, 8, 9, 10, 12, 14, 16, 17, 18, 20, 21, 22, 24, 26,
                 27, 28, 30}

For picking a wafer, we can just use good/bad classification.

>>> set(dbi.get('sipm_test', classification='bad').data.quality_flag)
{2, 4, 5, 6, 8, 9, 10, 12, 14, 16, 17, 18, 20, 21, 22, 24, 26, 27, 28, 30}
>>> set(dbi.get('sipm_test', classification='good').data.quality_flag)
{0, 1}
"""

import argparse
import sys
import types

try:
    from ds20kdb import visual
except ModuleNotFoundError:
    print('Please install ds20kdb-avt')
    sys.exit(3)
except ImportError:
    print('Please upgrade to the latest ds20kdb-avt version')
    sys.exit(3)
else:
    from ds20kdb import interface


##############################################################################
# command line option handler
##############################################################################


def check_arguments():
    """
    handle command line options

    --------------------------------------------------------------------------
    args : none
    --------------------------------------------------------------------------
    returns : none
    --------------------------------------------------------------------------
    """
    parser = argparse.ArgumentParser(
        description='Generate a wafer map suitable for picking good SiPMs\
        from a wafer using a die ejector, such that they may be transferred\
        to trays and later installed onto vTiles. Support requests to:\
        Alan Taylor, Physics Dept.,\
        University of Liverpool, avt@hep.ph.liv.ac.uk')
    parser.add_argument(
        'lot', nargs=1, metavar='lot',
        help='Wafer lot number.',
        type=int)
    parser.add_argument(
        'wafer_number', nargs=1, metavar='wafer_number',
        help='Wafer number.',
        type=int)

    args = parser.parse_args()

    return args.lot[0], args.wafer_number[0]


##############################################################################
# main
##############################################################################

def main():
    """
    Generate a wafer map suitable for picking good SiPMs from a wafer using a
    die ejector, such that they may be transferred to trays and later
    installed onto vTiles.
    """
    lot, wafer_number = check_arguments()

    status = types.SimpleNamespace(success=0, unreserved_error_code=3)
    dbi = interface.Database()

    print(f'looking up {lot}.{wafer_number:02}')
    try:
        wafer_pid = int(
            dbi.get('wafer', lot=lot, wafer_number=wafer_number).data.wafer_pid.values[0]
        )
    except AttributeError:
        print('Check Internet connection')
        return status.unreserved_error_code
    except TypeError:
        print(f'No response from the database for {lot}.{wafer_number:02}')
        return status.unreserved_error_code

    print(f'PID {wafer_pid}')

    ##########################################################################
    # get information for this wafer's SiPMs

    print('Obtaining SiPMs for this wafer')
    dfr = dbi.get('sipm', wafer_id=wafer_pid).data

    ##########################################################################
    # obtain (col, row) locations for good/bad SiPMs

    print('Obtaining SiPMs with bad classification(s)')
    bad_sipm_ids = set(dbi.get('sipm_test', classification='bad').data.sipm_id)
    wafer_map_bad = {
        (col, row)
        for sipm_pid, col, row in zip(dfr.sipm_pid, dfr.column, dfr.row)
        if sipm_pid in bad_sipm_ids
    }

    # Since there is more than one test in table 'sipm_test' for each sipm_id,
    # it is possible that a SiPM may have both 'good' and 'bad'
    # classifications. We only care about a bad classification existing, since
    # we won't select that SiPM for use on a vTile.

    all_locations = set(interface.wafer_map_valid_locations())
    wafer_map_good = all_locations.difference(wafer_map_bad)

    ##########################################################################
    # draw wafer

    print('Saving wafer map')
    sipm_groups = [
        {
            'name': 'good',
            'locations': wafer_map_good,
            'sipm_colour': 'green',
            'text_colour': 'black',
        },
        {
            'name': 'bad',
            'locations': wafer_map_bad,
            'sipm_colour': 'darkred',
            'text_colour': 'lightgrey',
        },
    ]

    waf = visual.DrawWafer(
        wafer_lot=lot,
        wafer_number=wafer_number,
        sipm_groups=sipm_groups
    )
    waf.save()

    return status.success


##############################################################################
if __name__ == '__main__':
    sys.exit(main())
