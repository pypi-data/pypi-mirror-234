#!/usr/bin/env python3
"""
GUI for POSTing DarkSide-20k vTiles to the pre-production database.
"""

import collections
import contextlib
import datetime
import functools
import json
import logging
import os
import sys
import time
import webbrowser
import tkinter
from tkinter import ttk
from tkinter import filedialog

from ttkwidgets import tooltips
from dateutil.parser import parse

from ds20kdb import interface


##############################################################################
# data structures
#
# Since users may request the validity of their data to be checked against the
# database more than once per vTile submission, these database enquiries
# are cached. This reduces database traffic and provide a more responsive
# experience for the user.
#
# Caching is performed outside the class definition to allow it to occur
# across all SiPMs.
##############################################################################


@functools.lru_cache(maxsize=64)
def get_wafer_pid_wrapper(dbi, lot_number, wafer_number):
    """ Cache wrapper """
    return dbi.get_wafer_pid(lot_number, wafer_number).data


@functools.lru_cache(maxsize=128)
def get_sipm_pid_wrapper(dbi, wafer_pid, column, row):
    """ Cache wrapper """
    return dbi.get_sipm_pid(wafer_pid, column, row)


class SiPM:
    """
    Basic data container used for SiPMs.

    This requires network access.
    """
    __slots__ = {
        'dbi': 'ds20kdb.interface.Database instance, used for db interaction',
        'lot_number': 'Wafer lot number, 7-digits, e.g. 9306869',
        'wafer_number': 'Wafer number, 1-2 digits in the range 1-25',
        'column': 'Physical location of this SiPM on the wafer',
        'row': 'Physical location of this SiPM on the wafer',
        'wafer_pid': 'Database PID of the wafer this SiPM came from',
        'sipm_pid': 'Database PID of this SiPM',
    }

    def __init__(self, dbi, lot_number, wafer_number, column, row):
        self.dbi = dbi
        self.lot_number = lot_number
        self.wafer_number = wafer_number
        self.column = column
        self.row = row
        self.wafer_pid = get_wafer_pid_wrapper(
            dbi, lot_number, wafer_number
        )
        self.sipm_pid = get_sipm_pid_wrapper(
            dbi, self.wafer_pid, column, row
        )

    def __repr__(self):
        return (
            'SiPM('
            f'dbi={self.dbi}, '
            f'lot_number={self.lot_number}, '
            f'wafer_number={self.wafer_number}, '
            f'column={self.column}, '
            f'row={self.row})'
        )

    def __str__(self):
        contents = {
            'lot number': self.lot_number,
            'wafer number': self.wafer_number,
            'SiPM column': self.column,
            'SiPM row': self.row,
            'wafer PID': self.wafer_pid,
            'SiPM PID': self.sipm_pid,
        }
        return ', '.join(f'{k}={v:>3}' for k, v in contents.items())


##############################################################################
# GUI data structures
#
# Principally used for setting of default conditions
##############################################################################


class ButtonSubmit(ttk.Button):
    """ Button: only used for the submit button """

    def set_default(self):
        """ Set default state """
        self.configure(state='disabled')


class ColourLabel(ttk.Label):
    """ Label: used for all labels """

    def set_default(self):
        """ Set default state """
        self.configure(foreground='black')


class SipmLotNum(ttk.Combobox):
    """ Drop-down menu: used for the wafer's lot number only """

    def set_default(self):
        """ Set default state """
        self.set('lot')


class SipmWaferNum(ttk.Combobox):
    """ Drop-down menu: used for the wafer number only """

    def set_default(self):
        """ Set default state """
        self.set('wafer')


class SipmColumn(ttk.Combobox):
    """ Drop-down menu: used for SiPM column numbers """

    def set_default(self):
        """ Set default state """
        self.set('col')


class SipmRow(ttk.Combobox):
    """ Drop-down menu: used for SiPM row numbers """

    def set_default(self):
        """ Set default state """
        self.set('row')


class Supplemental(ttk.Combobox):
    """
    Drop-down menu: used for the 4 supplemental items:

    Institute, solder syringe PID, QR-code, production run number
    """
    def set_default(self):
        """ Set default state """
        self.set('')


class Widget:
    """
    Generic container for tkinter widgets.
    """
    __slots__ = {
        'instance': 'Instance of the tkinter widget.',
        'itype': (
            'This is the widget type, which may be one of these three: '
            ' combobox (drop-down menu), label (text label), and '
            'text (console area).'
        ),
        'cluster': (
            'The cluster represents an umbrella under which a group of '
            'categories may be placed. The cluster names are: console, '
            'institute, production_date, qrcode, run_number, sipm_N (where N '
            'is a value between 1 and 24 inclusive), and solder_id. '
            'Only production_date and sipm_N have multiple categories. '
            'production_date has categories of year, month, day, hour and '
            'minute. sipm_N has categories of lot_number, wafer_number, '
            'column, and row.'
        ),
        'category': 'E.g. lot, label',
    }

    def __init__(self, instance, itype, cluster, category):
        self.instance = instance
        self.itype = itype
        self.cluster = cluster
        self.category = category


##############################################################################
# Build the GUI interface (main window areas)
##############################################################################


def populate_window_with_frames(root, frame):
    """
    Populate the main GUI window with labelled frames.

    --------------------------------------------------------------------------
    args
        root : tkinter.Tk
            The top-level Tk widget for the main GUI window
        frame : dict
            {<frame_name>: <ttk.LabelFrame>, ...}
    --------------------------------------------------------------------------
    returns
        frame : dict
            {<frame_name>: <ttk.LabelFrame>, ...}
            no explicit return, mutable type amended in place
    --------------------------------------------------------------------------
    """
    # SiPMs

    frame['sipm'] = ttk.LabelFrame(
        root,
        width=1024,
        height=256,
        text='SiPMs',
    )
    frame['sipm'].grid(row=0, column=0, columnspan=2)
    frame['sipm'].grid_propagate(False)

    # supplemental details

    frame['supp'] = ttk.LabelFrame(
        root,
        width=1024,
        height=192,
        text='Supplemental details',
    )
    frame['supp'].grid(row=1, column=0, columnspan=2)
    frame['supp'].grid_propagate(False)

    # production date

    frame['date'] = ttk.LabelFrame(
        root,
        width=512,
        height=64,
        text='Production date/time (timezone: UTC)',
    )
    frame['date'].grid(row=2, column=0, columnspan=1)
    frame['date'].grid_propagate(False)

    # buttons

    frame['button'] = ttk.LabelFrame(
        root,
        width=512,
        height=64,
        text='Actions',
    )
    frame['button'].grid(row=3, column=0, columnspan=1)
    frame['button'].grid_propagate(False)

    # console for error messages and other status messages

    frame['console'] = ttk.LabelFrame(
        root,
        width=512,
        height=128,
        text='Console',
    )
    frame['console'].grid(row=2, column=1, columnspan=1, rowspan=2)
    frame['console'].grid_propagate(False)


def populate_supplemental_frame(frame, widgets, dbi, defaults_file_path):
    """
    Populate the supplemental frame with widgets.

    --------------------------------------------------------------------------
    args
        root : tkinter.Tk
            The top-level Tk widget for the main GUI window
        widgets : list
        dbi : ds20kdb.interface.Database
            Instance of the Database interface class; allows communication
            with the database.
    --------------------------------------------------------------------------
    returns
        widgets : list
            no explicit return, mutable type amended in place
    --------------------------------------------------------------------------
    """
    inst = sorted(dbi.get('institute').data.name.values)
    wtmp = Widget(
        ColourLabel(
            frame['supp'],
            text='Manufacturing institute',
            font=('', 10),
            anchor='w',
        ),
        itype='label',
        cluster='institute',
        category=None,
    )
    wtmp.instance.grid(sticky='w', column=0, row=0)
    widgets.append(wtmp)
    wtmp = Widget(
        Supplemental(
            frame['supp'],
            textvariable='institute',
            values=inst,
            state='readonly',
            width=65,
        ),
        itype='combobox',
        cluster='institute',
        category=None,
    )
    wtmp.instance.grid(sticky='w', column=0, row=1)
    # If the user changes the institute, the available solder syringes must
    # be updated to match it.
    wtmp.instance.bind(
        '<<ComboboxSelected>>',
        functools.partial(refresh_solder, widgets, wtmp, dbi)
    )
    widgets.append(wtmp)

    # solder_id

    # Attempt to get institute name.
    # This is a little inefficient, since we'll load this file again later.
    table_json = quiet_load_json(defaults_file_path)

    try:
        institute_text = table_json['institute|None']
    except KeyError:
        # No institute name in defaults.
        # Load everything: all syringe_ids, from all institutes
        sold = sorted(map(int, dbi.get('solder').data.solder_pid.values))
    else:
        # attempt to limit selection based on institute/date
        institute_id = dbi.get_institute_id(institute_text).data
        sold = dbi.get_relevant_solder_ids(institute_id)

    wtmp = Widget(
        ColourLabel(
            frame['supp'],
            text='PID of solder syringe',
            font=('', 10),
            anchor='w'
        ),
        itype='label',
        cluster='solder_id',
        category=None,
    )
    wtmp.instance.grid(sticky='w', column=0, row=2)
    widgets.append(wtmp)
    wtmp = Widget(
        Supplemental(
            frame['supp'],
            textvariable='solder_id',
            values=sold,
            state='readonly',
            width=4,
        ),
        itype='combobox',
        cluster='solder_id',
        category=None,
    )
    wtmp.instance.grid(sticky='w', column=0, row=3)
    widgets.append(wtmp)

    # QR-code
    #
    # We really want the vpcb_asic_pid for the vTile submission, but it's
    # easier for the user to give us the QR-code, and we can look this up
    # using get_vpcb_asic_pid_from_qrcode.

    qrcd = dbi.get_relevant_qrcodes()
    wtmp = Widget(
        ColourLabel(
            frame['supp'],
            text='QR-code',
            font=('', 10),
            anchor='w'
        ),
        itype='label',
        cluster='qrcode',
        category=None,
    )
    wtmp.instance.grid(sticky='w', column=0, row=4)
    widgets.append(wtmp)
    wtmp = Widget(
        Supplemental(
            frame['supp'],
            textvariable='qrcode',
            values=qrcd,
            state='readonly',
            width=20,
        ),
        itype='combobox',
        cluster='qrcode',
        category=None,
    )
    wtmp.instance.grid(sticky='w', column=0, row=5)
    widgets.append(wtmp)

    # run_number

    runn = list(range(200))
    wtmp = Widget(
        ColourLabel(
            frame['supp'],
            text='Production run number',
            font=('', 10),
            anchor='w'
        ),
        itype='label',
        cluster='run_number',
        category=None,
    )
    wtmp.instance.grid(sticky='w', column=0, row=6)
    widgets.append(wtmp)
    wtmp = Widget(
        Supplemental(
            frame['supp'],
            textvariable='run_number',
            values=runn,
            state='readonly',
            width=4,
            tooltip='In 2022, this is identical to the vPDU number.',
        ),
        itype='combobox',
        cluster='run_number',
        category=None,
    )
    wtmp.instance.grid(sticky='w', column=0, row=7)
    widgets.append(wtmp)


def populate_production_date_frame(frame, widgets):
    """
    Populate the GUI production date frame with gridded widgets.

    Limited selections for some values:

        year    : 2022 - 2032
        minutes : 15 minute increments
        seconds : omitted, since this value isn't relevant

    The date will need to be checked later to make sure the month/day values
    make sense together.

    --------------------------------------------------------------------------
    args
        root : tkinter.Tk
            The top-level Tk widget for the main GUI window
        frame : dict
            {<frame_name>: <ttk.LabelFrame>, ...}
            Contains details of GUI window frames.
        widgets : list
            Contains details of GUI widgets.
        dbi : ds20kdb.interface.Database
            Instance of the Database interface class; allows communication
            with the database.
    --------------------------------------------------------------------------
    returns
        widgets : list
            no explicit return, mutable type amended in place
    --------------------------------------------------------------------------
    """
    # year

    years = list(range(2022, 2033))
    wtmp = Widget(
        ColourLabel(
            frame['date'],
            text='Year',
            font=('', 10),
            anchor='w',
        ),
        itype='label',
        cluster='production_date',
        category='year',
    )
    wtmp.instance.grid(sticky='w', column=0, row=0)
    widgets.append(wtmp)
    wtmp = Widget(
        Supplemental(
            frame['date'],
            values=years,
            state='readonly',
            width=8,
        ),
        itype='combobox',
        cluster='production_date',
        category='year',
    )
    wtmp.instance.grid(sticky='w', column=0, row=1)
    widgets.append(wtmp)

    # month

    months = list(range(1, 13))
    wtmp = Widget(
        ColourLabel(
            frame['date'],
            text='Month',
            font=('', 10),
            anchor='w',
        ),
        itype='label',
        cluster='production_date',
        category='month',
    )
    wtmp.instance.grid(sticky='w', column=1, row=0)
    widgets.append(wtmp)
    wtmp = Widget(
        Supplemental(
            frame['date'],
            values=months,
            state='readonly',
            width=8,
        ),
        itype='combobox',
        cluster='production_date',
        category='month',
    )
    wtmp.instance.grid(sticky='w', column=1, row=1)
    widgets.append(wtmp)

    # day

    days = list(range(1, 32))
    wtmp = Widget(
        ColourLabel(
            frame['date'],
            text='Day',
            font=('', 10),
            anchor='w',
        ),
        itype='label',
        cluster='production_date',
        category='day',
    )
    wtmp.instance.grid(sticky='w', column=2, row=0)
    widgets.append(wtmp)
    wtmp = Widget(
        Supplemental(
            frame['date'],
            values=days,
            state='readonly',
            width=8,
        ),
        itype='combobox',
        cluster='production_date',
        category='day',
    )
    wtmp.instance.grid(sticky='w', column=2, row=1)
    widgets.append(wtmp)

    # hour

    hours = list(range(0, 24))
    wtmp = Widget(
        ColourLabel(
            frame['date'],
            text='Hour',
            font=('', 10),
            anchor='w',
        ),
        itype='label',
        cluster='production_date',
        category='hour',
    )
    wtmp.instance.grid(sticky='w', column=3, row=0)
    widgets.append(wtmp)
    wtmp = Widget(
        Supplemental(
            frame['date'],
            values=hours,
            state='readonly',
            width=8,
        ),
        itype='combobox',
        cluster='production_date',
        category='hour',
    )
    wtmp.instance.grid(sticky='w', column=3, row=1)
    widgets.append(wtmp)

    # minutes

    minutes = list(range(0, 60, 15))
    wtmp = Widget(
        ColourLabel(
            frame['date'],
            text='Minutes',
            font=('', 10),
            anchor='w',
        ),
        itype='label',
        cluster='production_date',
        category='minute',
    )
    wtmp.instance.grid(sticky='w', column=4, row=0)
    widgets.append(wtmp)
    wtmp = Widget(
        Supplemental(
            frame['date'],
            values=minutes,
            state='readonly',
            width=8,
        ),
        itype='combobox',
        cluster='production_date',
        category='minute',
    )
    wtmp.instance.grid(sticky='w', column=4, row=1)
    widgets.append(wtmp)


def populate_action_button_frame(root, frame, widgets, dbi):
    """
    Populate the GUI button frame with gridded widgets.

    --------------------------------------------------------------------------
    args
        root : tkinter.Tk
            The top-level Tk widget for the main GUI window
        frame : dict
            {<frame_name>: <ttk.LabelFrame>, ...}
            Contains details of GUI window frames.
        widgets : list
            Contains details of GUI widgets.
        dbi : ds20kdb.interface.Database
            Instance of the Database interface class; allows communication
            with the database.
    --------------------------------------------------------------------------
    returns
        widgets : list
            no explicit return, mutable type amended in place
    --------------------------------------------------------------------------
    """
    # button to check user-entered values
    ttk.Button(
        frame['button'],
        text='check',
        command=lambda: check(dbi, root, widgets),
        tooltip=(
            'Check if the details entered above look reasonable. All fields '
            'must be green for the submit button to be enabled.'
        ),
    ).grid(column=1, row=0)

    # button to submit vTile to the database
    wtmp = Widget(
        ButtonSubmit(
            frame['button'],
            text='submit',
            command=lambda: submit(dbi, root, widgets),
            state='disabled',
            tooltip=(
                'It will not be possible to submit the vTile if any of the '
                'above values are missing/incorrect. Use the check button '
                'before attempting to submit.'
            ),
        ),
        itype='button',
        cluster='submit',
        category='None',
    )
    wtmp.instance.grid(column=2, row=0)
    widgets.append(wtmp)


def populate_console_frame(frame, widgets):
    """
    Populate the GUI button frame with gridded widgets.

    --------------------------------------------------------------------------
    args
        frame : dict
            {<frame_name>: <ttk.LabelFrame>, ...}
            Contains details of GUI window frames.
        widgets : list
            Contains details of GUI widgets.
    --------------------------------------------------------------------------
    returns
        widgets : list
            no explicit return, mutable type amended in place
    --------------------------------------------------------------------------
    """
    wtmp = Widget(
        tkinter.Text(frame['console'], state='disabled', height=6, width=70),
        itype='text',
        cluster='console',
        category=None,
    )
    wtmp.instance.grid(column=0, row=0)

    # add scrollbar
    scroll_bar = tkinter.Scrollbar(
        frame['console'], command=wtmp.instance.yview, orient='vertical'
    )
    scroll_bar.grid(row=0, column=1, sticky='ns')
    wtmp.instance.configure(yscrollcommand=scroll_bar.set)

    widgets.append(wtmp)


def populate_sipm_frame(frame, widgets, wafer_table_dataframe):
    """
    The SiPM numbering is shown looking at the PCB with SiPMs visible and
    towards the viewer, and the backside components(resistors, capacitors,
    ASIC etc.) facing away from the viewer. The location of the QR code and
    ASIC on the back-side of the PCB are also shown to provide orientation.

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

    Within the frame, each SiPM area is arranged like this:

    +------------------------------------------+
    | label                                    |
    +------------+--------------+--------+-----+
    | lot number | wafer number | column | row |
    +------------+--------------+--------+-----+

    --------------------------------------------------------------------------
    args
        frame : dict
            {<frame_name>: <ttk.LabelFrame>, ...}
            Contains details of GUI window frames.
        widgets : list
            Contains details of GUI widgets.
        wafer_table_dataframe : Pandas DataFrame
            A copy of the wafer table from the database
    --------------------------------------------------------------------------
    returns
        widgets : list
            no explicit return, mutable type amended in place
    --------------------------------------------------------------------------
    """
    col_start = 0
    row_start = 0
    col_offset = 4
    row_offset = 2

    # left-most grid position of the four values that define the SiPM:
    # lot_number, wafer_number, column, row
    #
    # {sipm_number: (column, row), ...}
    positions = {
        19: (0, 0), 13: (1, 0), 7: (2, 0), 1: (3, 0),
        20: (0, 1), 14: (1, 1), 8: (2, 1), 2: (3, 1),
        21: (0, 2), 15: (1, 2), 9: (2, 2), 3: (3, 2),
        22: (0, 3), 16: (1, 3), 10: (2, 3), 4: (3, 3),
        23: (0, 4), 17: (1, 4), 11: (2, 4), 5: (3, 4),
        24: (0, 5), 18: (1, 5), 12: (2, 5), 6: (3, 5),
    }

    lots = sorted({lo[0] for lo in wafer_table_dataframe[['lot']].values})
    wafs = sorted({wn[0] for wn in wafer_table_dataframe[['wafer_number']].values})
    cols, rows = map(set, zip(*interface.wafer_map_valid_locations()))
    cols = sorted(cols)
    rows = sorted(rows)

    # set up SiPM labels and comboboxes
    for sipm, (column, row) in positions.items():

        column_base = col_start + col_offset * column
        row_base = row_start + row_offset * row

        # sipm label

        wtmp = Widget(
            ColourLabel(frame['sipm'], text=f'SiPM {sipm}'),
            itype='label',
            cluster=f'sipm_{sipm}',
            category=None,
        )
        wtmp.instance.grid(column=column_base, row=row_base, sticky='w')
        widgets.append(wtmp)

        # 4 drop-down menus: lot number, wafer number, column, row

        row_base += 1

        wtmp = Widget(
            SipmLotNum(
                frame['sipm'],
                values=lots,
                state='readonly',
                width=11,
            ),
            itype='combobox',
            cluster=f'sipm_{sipm}',
            category='lot_number',
        )
        wtmp.instance.grid(column=column_base, row=row_base)
        wtmp.instance.set('lot')
        widgets.append(wtmp)

        wtmp = Widget(
            SipmWaferNum(
                frame['sipm'],
                values=wafs,
                state='readonly',
                width=5,
            ),
            itype='combobox',
            cluster=f'sipm_{sipm}',
            category='wafer_number',
        )
        wtmp.instance.grid(column=column_base+1, row=row_base)
        wtmp.instance.set('wafer')
        widgets.append(wtmp)

        wtmp = Widget(
            SipmColumn(
                frame['sipm'],
                values=cols,
                state='readonly',
                width=3,
            ),
            itype='combobox',
            cluster=f'sipm_{sipm}',
            category='column',
        )
        wtmp.instance.grid(column=column_base+2, row=row_base)
        wtmp.instance.set('col')
        widgets.append(wtmp)

        wtmp = Widget(
            SipmRow(
                frame['sipm'],
                values=rows,
                state='readonly',
                width=4,
            ),
            itype='combobox',
            cluster=f'sipm_{sipm}',
            category='row',
        )
        wtmp.instance.grid(column=column_base+3, row=row_base)
        wtmp.instance.set('row')
        widgets.append(wtmp)


##############################################################################
# Build the GUI interface (top menu bar)
##############################################################################


def populate_menu_bar(root, widgets, session_timestamp, defaults_file_path):
    """
    Populate the GUI menu bar.

    --------------------------------------------------------------------------
    args
        root : tkinter.Tk
            The top-level Tk widget for the main GUI window
        widgets : list
            Contains details of GUI widgets.
        session_timestamp : string
            e.g. '20221119_144629'
    --------------------------------------------------------------------------
    returns
        root : tkinter.Tk
            The top-level Tk widget for the main GUI window
            no explicit return, mutable type amended in place
    --------------------------------------------------------------------------
    """
    menubar = tkinter.Menu(root)
    root.config(menu=menubar)

    file_menu = tkinter.Menu(menubar, tearoff=False)
    tool_menu = tkinter.Menu(menubar, tearoff=False)
    help_menu = tkinter.Menu(menubar, tearoff=False)

    file_menu.add_command(
        label='Open...',
        command=lambda: load_file(widgets),
    )
    file_menu.add_command(
        label='Save',
        command=lambda: save_file_wrapper(session_timestamp, widgets),
    )
    file_menu.add_command(
        label='Save As...',
        command=lambda: save_file_as(session_timestamp, widgets),
    )

    # ------------------------------------------------------------------------
    file_menu.add_separator()
    file_menu.add_command(
        label='Import Tray...',
        command=lambda: import_tray(widgets),
    )
    file_menu.add_command(
        label='Export Python',
        command=lambda: export_python_wrapper(session_timestamp, root, widgets),
    )
    file_menu.add_command(
        label='Export Python As...',
        command=lambda: export_python_as(session_timestamp, root, widgets),
    )

    # ------------------------------------------------------------------------
    file_menu.add_separator()
    file_menu.add_command(
        label='Save Defaults',
        command=lambda: save_defaults(widgets, defaults_file_path),
    )
    file_menu.add_command(
        label='Clear Defaults',
        command=lambda: clear_defaults(widgets, defaults_file_path),
    )

    # ------------------------------------------------------------------------
    file_menu.add_separator()
    file_menu.add_command(
        label='Quit',
        command=root.destroy,
    )

    tool_menu.add_command(
        label='Clear GUI',
        command=lambda: clear_gui(widgets),
    )
    tool_menu.add_command(
        label='Clear GUI and load defaults',
        command=lambda: clear_gui_load_defaults(widgets, defaults_file_path),
    )
    tool_menu.add_command(
        label='Clear cache',
        command=clear_cache,
    )

    help_menu.add_command(
        label='About',
        command=lambda: about_popup(root),
    )
    help_menu.add_command(
        label='Documentation',
        command=lambda: webbrowser.open_new(
            'https://gitlab.in2p3.fr/darkside/productiondb_software/-/wikis/'
            'Submitting-vTiles-to-the-database-using-a-GUI'
        ),
    )

    menubar.add_cascade(
        label='File',
        menu=file_menu,
        underline=0
    )
    menubar.add_cascade(
        label='Tools',
        menu=tool_menu,
        underline=0
    )
    menubar.add_cascade(
        label='Help',
        menu=help_menu,
        underline=0
    )


##############################################################################
# Build the GUI interface (pop-up window for Help -> About)
##############################################################################


def about_popup(root):
    """
    Display the Help -> About window, centred on the main window.
    """
    about_w, about_h = 320, 192

    current_w = root.winfo_width()
    current_h = root.winfo_height()

    root_win_x, root_win_y = (int(s) for s in root.geometry().split('+')[1:])

    about_x = root_win_x + (current_w // 2) - (about_w // 2)
    about_y = root_win_y + (current_h // 2) - (about_h // 2)

    top = tkinter.Toplevel(root)
    top.geometry(f'{about_w}x{about_h}+{about_x}+{about_y}')
    top.title('About')

    # add frame

    local_frame = ttk.Frame(
        top,
        width=about_w,
        height=about_h,
    )
    local_frame.grid(row=0, column=0)
    local_frame.grid_propagate(False)

    # add contents (text)

    text = tkinter.Text(local_frame, height=10, width=70)
    text.grid(column=0, row=0)
    text.tag_configure('center', justify='center')
    message = (
        '\n'
        '- POST vTile -\n'
        f'ds20kdb interface version {interface.__version__}\n'
        '\n'
        'Adds a veto-tile to the DarkSide-20k\n'
        'pre-production database.\n'
        '\n'
        '- support -\n'
        'avt@hep.ph.liv.ac.uk'
    )
    text.insert(tkinter.END, message)
    text.tag_add('center', '1.0', 'end')
    text.configure(state='disabled')

    # add contents (button)

    ttk.Button(
        local_frame,
        text='ok',
        command=top.destroy,
    ).grid(column=0, row=1)
    local_frame.columnconfigure(0, weight=1)   # Set weight to row and
    local_frame.rowconfigure(1, weight=1)      # column where the widget is


##############################################################################
# Change the GUI interface state
##############################################################################


def clear_cache():
    """
    Clear cache of wafer and SiPM PIDs.

    --------------------------------------------------------------------------
    args : none
    --------------------------------------------------------------------------
    returns : none
    --------------------------------------------------------------------------
    """
    get_console_widget.cache_clear()
    get_sipm_pid_wrapper.cache_clear()
    get_wafer_pid_wrapper.cache_clear()


def clear_gui(widgets):
    """
    Return all drop-down menus and labels to their default state, discarding
    all user-entered information. Disable the submit button.

    --------------------------------------------------------------------------
    args
        widgets : list of class Widgit
            Contains details of GUI widgets.
    --------------------------------------------------------------------------
    returns : none
        GUI state affected
    --------------------------------------------------------------------------
    """
    for widget in widgets:
        if widget.itype in ('combobox', 'label', 'button'):
            widget.instance.set_default()


def clear_gui_load_defaults(widgets, defaults_file_path):
    """
    Return the GUI state to that set at application start.

    --------------------------------------------------------------------------
    args
        widgets : list of class Widgit
            Contains details of GUI widgets.
        defaults_file_path : string
            e.g. '/Users/avt/.ds20kdb_defaults'
    --------------------------------------------------------------------------
    returns : none
        GUI state affected
    --------------------------------------------------------------------------
    """
    clear_gui(widgets)
    load_defaults(widgets, defaults_file_path)


def clear_gui_sipms_only(widgets):
    """
    Return all SiPM drop-down menus and labels to their default state,
    discarding all user-entered information.

    --------------------------------------------------------------------------
    args
        widgets : list of class Widgit
            Contains details of GUI widgets.
    --------------------------------------------------------------------------
    returns : none
        GUI state affected
    --------------------------------------------------------------------------
    """
    for widget in widgets:
        if 'sipm' in widget.cluster and widget.itype in ('combobox', 'label'):
            widget.instance.set_default()


def clear_submit_button(widgets):
    """
    Disable the submit button.

    --------------------------------------------------------------------------
    args
        widgets : list of class Widgit
            Contains details of GUI widgets.
    --------------------------------------------------------------------------
    returns : none
        GUI state affected
    --------------------------------------------------------------------------
    """
    for widget in widgets:
        if widget.cluster == 'submit' and widget.itype == 'button':
            widget.instance.set_default()


def print_to_console(widgets, line):
    """
    Print log messages to the GUI console.

    --------------------------------------------------------------------------
    args
        widgets : list of class Widget instances
        line : string
    --------------------------------------------------------------------------
    returns : none
        GUI state affected
    --------------------------------------------------------------------------
    """
    # ensure line is terminated
    line = line if line.endswith('\n') else f'{line}\n'

    console = get_console_widget(tuple(widgets))

    console.configure(state='normal')
    console.insert(tkinter.END, line)
    console.configure(state='disabled')


def refresh_solder(widgets, institute_widget, dbi, _event):
    """
    Update the "PID of solder syringe" drop down box with values from the
    database when the user changes the institute.

    --------------------------------------------------------------------------
    args
        widgets : list
        institute_widget : class Widget
        dbi : ds20kdb.interface.Database
            Instance of the Database interface class; allows communication
            with the database.
        _event : class tkinter.Event
    --------------------------------------------------------------------------
    returns : none
        GUI state affected
    --------------------------------------------------------------------------
    """
    print_to_console(widgets, 'Institute changed: updating solder syringes.')

    institute_text = institute_widget.instance.get()
    institute_id = dbi.get_institute_id(institute_text).data
    sold = dbi.get_relevant_solder_ids(institute_id)

    # find solder combobox widget
    solder_items = next(
        widget.instance
        for widget in widgets
        if widget.cluster == 'solder_id' and widget.itype == 'combobox'
    )

    # Clear any existing user choice, then reload combobox with values
    # appropriate for the new institute.
    solder_items.set('')
    solder_items.configure(values=sold)


def refresh_qrcodes(widgets, dbi):
    """
    Update the QR-code drop down box with values from the database. This is
    typically called when the user has successfully submitted a vTile.

    --------------------------------------------------------------------------
    args
        widgets : list
        dbi : ds20kdb.interface.Database
            Instance of the Database interface class; allows communication
            with the database.
    --------------------------------------------------------------------------
    returns : none
        GUI state affected
    --------------------------------------------------------------------------
    """
    print_to_console(widgets, 'vTile submitted: updating QR-codes.')

    qrcd = dbi.get_relevant_qrcodes()

    # find qrcode combobox widget
    qrcode_items = next(
        widget.instance
        for widget in widgets
        if widget.cluster == 'qrcode' and widget.itype == 'combobox'
    )

    # Clear any existing user choice, then reload combobox with values
    # appropriate for the new institute.
    qrcode_items.set('')
    qrcode_items.configure(values=qrcd)


def set_button_state(button, disabled):
    """
    Generic set button state normal/disabled

    --------------------------------------------------------------------------
    args
        button : ButtonSubmit
            widget instance
        disabled : bool
            label status
    --------------------------------------------------------------------------
    returns : none
        GUI state affected
    --------------------------------------------------------------------------
    """
    button.configure(state='disabled' if disabled else 'normal')


def set_label_colour(label, good):
    """
    Set the label colour of an individual widget to green (good=True) or
    red (good=False).

    Used for indicating to the user whether the values they have entered are
    correct.

    --------------------------------------------------------------------------
    args
        label : ColourLabel
            widget instance
        good : bool
            label status
    --------------------------------------------------------------------------
    returns : none
    --------------------------------------------------------------------------
    """
    label.configure(foreground='#00B000' if good else '#C00000')


def update_gui_from_dict(widgets, table_json):
    """
    Used to update the GUI after a JSON file has been loaded.

    --------------------------------------------------------------------------
    args
        widgets : list
        table_json : dict
            e.g. {
                'sipm_19|lot_number': '9262109',
                'sipm_19|wafer_number': '15',
                'sipm_19|column': '10',
                'sipm_19|row': '21', ...
            }
    --------------------------------------------------------------------------
    returns : none
        GUI state affected
    --------------------------------------------------------------------------
    """
    for k, wval in table_json.items():
        wclu, wcat = k.split('|')
        if wcat == 'None':
            wcat = None

        with contextlib.suppress(StopIteration):
            widget = next(
                w for w in widgets
                if w.cluster == wclu and w.category == wcat and w.itype == 'combobox'
            )
            widget.instance.set(wval)


##############################################################################
# File I/O relating to the GUI menu bar
##############################################################################


def clear_defaults(widgets, defaults_file_path):
    """
    Removes the file containing user-set defaults, if it exists.

    --------------------------------------------------------------------------
    args
        widgets : list of class Widgit
            Contains details of GUI widgets.
        defaults_file_path : string
            e.g. '/Users/avt/.ds20kdb_defaults'
    --------------------------------------------------------------------------
    returns : none
        Possible filesystem change.
    --------------------------------------------------------------------------
    """
    try:
        os.remove(defaults_file_path)
    except FileNotFoundError:
        pass
    else:
        print_to_console(
            widgets, f'Deleted defaults file {defaults_file_path}'
        )


def export_python(root, widgets, filename):
    """
    --------------------------------------------------------------------------
    args
        root : tkinter.Tk
            The top-level Tk widget for the main GUI window
        widgets : list of class Widgit
            Contains details of GUI widgets.
        filename : string
    --------------------------------------------------------------------------
    returns : none
        file written to mass storage
    --------------------------------------------------------------------------
    """
    # get table from GUI variable
    try:
        table = json.loads(root.getvar(name='table_json_string'))
    except json.decoder.JSONDecodeError:
        print_to_console(widgets, 'No data to export.')
    else:
        with open(filename, 'w', encoding='utf-8') as outfile:
            outfile.write(f'table = {table}')


def export_python_as(session_timestamp, root, widgets):
    """
    Save file with a time-stamped filename.

    --------------------------------------------------------------------------
    args
        session_timestamp : string
            e.g. '20221119_144629'
        root : tkinter.Tk
            The top-level Tk widget for the main GUI window
        widgets : list of class Widgit
            Contains details of GUI widgets.
    --------------------------------------------------------------------------
    returns : none
        file written to mass storage
    --------------------------------------------------------------------------
    """
    suggested_filename = f'{session_timestamp}_post_vtile.py'

    filename = filedialog.asksaveasfilename(
        initialfile=suggested_filename,
        defaultextension='.py',
        filetypes=[
            ('Python Documents', '*.py'),
            ('All Files', '*.*'),
        ]
    )

    with contextlib.suppress(AttributeError):
        export_python(root, widgets, filename)


def export_python_wrapper(session_timestamp, root, widgets):
    """
    --------------------------------------------------------------------------
    args
        session_timestamp : string
            e.g. '20221119_144629'
        root : tkinter.Tk
            The top-level Tk widget for the main GUI window
        widgets : list of class Widgit
            Contains details of GUI widgets.
    --------------------------------------------------------------------------
    returns : none
        file written to mass storage
    --------------------------------------------------------------------------
    """
    export_python(root, widgets, f'{session_timestamp}_post_vtile.py')


def generic_load_json(widgets, filename):
    """
    Load JSON file.

    --------------------------------------------------------------------------
    args
        widgets : list of class Widgit
            Contains details of GUI widgets.
        filename : string
    --------------------------------------------------------------------------
    returns
        table_json : dict
            e.g. {
                'sipm_19|lot_number': '9262109',
                'sipm_19|wafer_number': '15',
                'sipm_19|column': '10',
                'sipm_19|row': '21', ...
            }
    --------------------------------------------------------------------------
    """
    table_json = {}

    with contextlib.suppress(FileNotFoundError):
        with open(filename, 'r', encoding='utf-8') as infile:
            try:
                table_json = json.load(infile)
            except (json.JSONDecodeError, UnicodeDecodeError):
                logging.error('could not read file: %s', filename)

                print_to_console(
                    widgets, f'Could not read file: {filename}'
                )
            else:
                print_to_console(widgets, f'Loaded file {filename}')

    return table_json


def quiet_load_json(filename):
    """
    Load JSON file.

    --------------------------------------------------------------------------
    args
        filename : string
    --------------------------------------------------------------------------
    returns
        table_json : dict
            e.g. {
                'sipm_19|lot_number': '9262109',
                'sipm_19|wafer_number': '15',
                'sipm_19|column': '10',
                'sipm_19|row': '21', ...
            }
    --------------------------------------------------------------------------
    """
    table_json = {}

    with contextlib.suppress(FileNotFoundError):
        with open(filename, 'r', encoding='utf-8') as infile:
            with contextlib.suppress(json.JSONDecodeError, UnicodeDecodeError):
                table_json = json.load(infile)

    return table_json


def load_defaults(widgets, defaults_file_path):
    """
    The defaults are loaded from the user's file at application start when the
    GUI comboboxes are empty, so there's no need to reset anything.

    --------------------------------------------------------------------------
    args
        widgets : list of class Widgit
            Contains details of GUI widgets.
        defaults_file_path : string
            e.g. '/Users/avt/.ds20kdb_defaults'
    --------------------------------------------------------------------------
    returns : none
        GUI state changed
    --------------------------------------------------------------------------
    """
    table_json = generic_load_json(widgets, defaults_file_path)

    update_gui_from_dict(widgets, table_json)


def load_file(widgets):
    """
    Load JSON file containing previously saved GUI combobox contents.

    --------------------------------------------------------------------------
    args
        widgets : list
            Contains details of GUI widgets.
    --------------------------------------------------------------------------
    returns : none
        GUI state affected
    --------------------------------------------------------------------------
    """
    filename = filedialog.askopenfilename(
        defaultextension='.json',
        filetypes=[
            ('JSON Documents', '*.json'),
            ('All Files', '*.*'),
        ]
    )

    if not filename:
        return

    table_json = generic_load_json(widgets, filename)

    if table_json:
        clear_gui(widgets)
        update_gui_from_dict(widgets, table_json)


def sipm_key(key):
    """
    Check if a string represents a SiPM.

    --------------------------------------------------------------------------
    args
        key : string
            e.g. 'sipm_1' or 'sipm_23'
    --------------------------------------------------------------------------
    returns : int or None
        int if the SiPM information appears valid, None otherwise
    --------------------------------------------------------------------------
    """
    try:
        sipm_text, number = key.split('_')
    except ValueError:
        sipm_text = number = None
    else:
        number = int(number)

    return number if sipm_text == 'sipm' and 1 <= number <= 24 else None


def import_tray(widgets):
    """
    Import data recorded during the wafer picking stage, where a file
    represents the contents of a SiPM tray (24 SiPMS).

    The contents of the file should look something like this:

    tray, 1
    lot, 9262109
    wafer_number, 15
    # sipm_number, wafer_column, wafer_row
    sipm_1, 07, 23
    sipm_2, 08, 23
    sipm_3, 09, 23
    sipm_4, 10, 23
    sipm_5, 11, 23
    sipm_6, 12, 23
    sipm_7, 06, 22
    sipm_8, 07, 22
    sipm_9, 08, 22
    sipm_10, 09, 22
    sipm_11, 10, 22
    sipm_12, 11, 22
    sipm_13, 12, 22
    sipm_14, 13, 22
    sipm_15, 06, 21
    sipm_16, 07, 21
    sipm_17, 08, 21
    sipm_18, 09, 21
    sipm_19, 10, 21
    sipm_20, 11, 21
    sipm_21, 12, 21
    sipm_22, 13, 21
    sipm_23, 14, 21
    sipm_24, 04, 20

    For the SiPM lines, there are some variants for tray locations:

    (1) empty (n=1):

    sipm_number,
    sipm_number

    (2) has come from another wafer (n=5):

    sipm_number, wafer_column, wafer_row, wafer_lot, wafer_number

    At some stage, we should also allow SiPM PIDs to be used (n=2):

    sipm_number, sipm_pid

    --------------------------------------------------------------------------
    args
        widgets : list
            Contains details of GUI widgets.
    --------------------------------------------------------------------------
    returns : none
        GUI state affected
    --------------------------------------------------------------------------
    """
    filename = filedialog.askopenfilename(
        defaultextension='.txt',
        filetypes=[
            ('TEXT Documents', '*.txt'),
            ('CSV Documents', '*.csv'),
            ('All Files', '*.*'),
        ]
    )

    if not filename:
        return

    data = {}
    lot_number = wafer_number = None
    sipms_from_default_wafer = set()

    with open(filename, 'r', encoding='utf-8') as infile:
        for line in infile:
            no_comment = line.split('#')[0]
            line = [
                field.strip() for field in no_comment.split(',')
                if field.strip()
            ]

            num_parts = len(line)

            if not line:
                continue

            sipm_definition = line[0].startswith('sipm_') and num_parts in {1, 3, 5}
            tray_wafer_definition = num_parts == 2

            if sipm_definition:
                try:
                    key, column, row, lot_num, wafer_num = line
                except ValueError:
                    try:
                        key, column, row = line
                    except ValueError:
                        # tray receptacle is empty
                        pass
                    else:
                        # sipm_number, wafer_column, wafer_row
                        sipm = sipm_key(key)
                        if sipm is not None:
                            with contextlib.suppress(ValueError):
                                data[f'{key}|column'] = int(column)
                                data[f'{key}|row'] = int(row)
                                sipms_from_default_wafer.add(sipm)
                else:
                    sipm = sipm_key(key)

                    # sipm_number, wafer_column, wafer_row, wlot, wnum
                    if sipm is not None:
                        with contextlib.suppress(ValueError):
                            data[f'{key}|column'] = int(column)
                            data[f'{key}|row'] = int(row)
                            data[f'{key}|lot_number'] = int(lot_num)
                            data[f'{key}|wafer_number'] = int(wafer_num)

            elif tray_wafer_definition:
                # preamble: tray number, (default) wafer lot/number
                key, value = line
                if key == 'lot':
                    try:
                        lot_number = int(value)
                    except ValueError:
                        lot_number = None
                elif key == 'wafer_number':
                    try:
                        wafer_number = int(value)
                    except ValueError:
                        wafer_number = None

    if lot_number is None or wafer_number is None:
        return

    # For SiPMs that didn't have a wafer lot and wafer number specified,
    # fill in the default values
    for number in sipms_from_default_wafer:
        data[f'sipm_{number}|lot_number'] = lot_number
        data[f'sipm_{number}|wafer_number'] = wafer_number

    clear_gui_sipms_only(widgets)
    update_gui_from_dict(widgets, data)

    print_to_console(widgets, f'Imported tray file {filename}')


def save_file_wrapper(session_timestamp, widgets):
    """
    --------------------------------------------------------------------------
    args
        session_timestamp : string
            e.g. '20221119_144629'
        widgets : list
            Contains details of GUI widgets.
    --------------------------------------------------------------------------
    returns : none
        file written to mass storage
    --------------------------------------------------------------------------
    """
    save_file(widgets, f'{session_timestamp}_post_vtile.json')


def save_defaults(widgets, defaults_file_path):
    """
    Save defaults that will be subsequently loaded at the next application
    start.

    --------------------------------------------------------------------------
    args
        widgets : list of class Widgit
            Contains details of GUI widgets.
        defaults_file_path : string
            e.g. '/Users/avt/.ds20kdb_defaults'
    --------------------------------------------------------------------------
    returns : none
        file written to mass storage
    --------------------------------------------------------------------------
    """
    def default_test(widget, def_clust):
        return (
            widget.itype == 'combobox'
            and widget.cluster in def_clust
            and bool(widget.instance.get())
        )

    default_clusters = {'institute'}
    valid_default = functools.partial(
        default_test, def_clust=default_clusters
    )

    with open(defaults_file_path, 'w', encoding='utf-8') as outfile:
        outfile.write(
            json.dumps(
                {
                    f'{w.cluster}|{w.category}': w.instance.get()
                    for w in widgets
                    if valid_default(w)
                }
            )
        )


def save_file(widgets, filename):
    """
    Save file with a time-stamped filename containing the values from all
    drop-down menus.

    --------------------------------------------------------------------------
    args
        widgets : list of class Widgit
            Contains details of GUI widgets.
        filename : string
    --------------------------------------------------------------------------
    returns : none
        file written to mass storage
    --------------------------------------------------------------------------
    """
    with open(filename, 'w', encoding='utf-8') as outfile:
        outfile.write(
            json.dumps(
                {
                    f'{w.cluster}|{w.category}': w.instance.get()
                    for w in widgets
                    if w.itype == 'combobox'
                }
            )
        )


def save_file_as(session_timestamp, widgets):
    """
    Save file with a time-stamped filename.

    --------------------------------------------------------------------------
    args
        session_timestamp : string
            e.g. '20221119_144629'
        widgets : list of class Widgit
            Contains details of GUI widgets.
    --------------------------------------------------------------------------
    returns : none
        file written to mass storage
    --------------------------------------------------------------------------
    """
    suggested_filename = f'{session_timestamp}_post_vtile.json'

    filename = filedialog.asksaveasfilename(
        initialfile=suggested_filename,
        defaultextension='.json',
        filetypes=[
            ('JSON Documents', '*.json'),
            ('All Files', '*.*'),
        ]
    )

    with contextlib.suppress(AttributeError):
        save_file(widgets, filename)


##############################################################################
# utilities
##############################################################################


@functools.lru_cache(maxsize=None)
def get_console_widget(widgets):
    """
    Find the console widget. There's only one entry for it, so we can simply
    return the first search result.

    The caller needs to convert the widgets list to a tuple so this call can
    be cached. The cost is negligible compared to the cost of the original
    uncached function call.

    --------------------------------------------------------------------------
    args
        widgets : tuple of class Widgit
            Contains details of GUI widgets.
    --------------------------------------------------------------------------
    returns : <class 'tkinter.Text'>
    --------------------------------------------------------------------------
    """
    return next(filter(lambda w: w.cluster == 'console', widgets)).instance


def database_alive(dbi):
    """
    --------------------------------------------------------------------------
    args
        dbi : ds20kdb.interface.Database
            Instance of the Database interface class; allows communication
            with the database.
    --------------------------------------------------------------------------
    returns : pandas.core.frame.DataFrame
        contents of the entire wafer table
    --------------------------------------------------------------------------
    """
    response = dbi.get('wafer')

    if response.network_timeout:
        sys.exit('Check network connection: timeout')

    return response.data


def timestamp_to_utc(tref):
    """
    Converts a timestamp into a string in UTC to the nearest second.

    e.g. 1567065212.1064236 converts to '20190829_075332'

    --------------------------------------------------------------------------
    args
        tref : float
            time in seconds since the epoch
    --------------------------------------------------------------------------
    returns : string
    --------------------------------------------------------------------------
    """
    utc = datetime.datetime.utcfromtimestamp(tref).isoformat().split('.')[0]
    return utc.replace('-', '').replace(':', '').replace('T', '_')


def timestamp_to_utc_ds20k(tref):
    """
    Converts a timestamp into a string in UTC to the nearest second.

    e.g. 1668688788.970397 converts to '2022-11-17 12:39:48'

    The DarkSide-20k database requires UTC date/time in this format:

    YYYY-MM-DD hh:mm:ss, e.g. 2022-07-19 07:00:00

    --------------------------------------------------------------------------
    args
        tref : float
            time in seconds since the epoch
    --------------------------------------------------------------------------
    returns : string
    --------------------------------------------------------------------------
    """
    utc = datetime.datetime.utcfromtimestamp(tref).isoformat().split('.')[0]
    return utc.replace('T', ' ')


##############################################################################
# handling user-supplied values
##############################################################################


def date_time_values_to_timestamp(dtf, widgets, table):
    """
    Convert discrete date/time values to a timestamp acceptable to the
    database.

    --------------------------------------------------------------------------
    args
        dtf : dict
            {string: {string: ttk.Label, string: string}, ...}
                e.g.
                    {
                        'year': {'label': ttk.Label, 'year': '2022'},
                        'month': {'label': ttk.Label, 'month': '12'},
                        ...
                    }
            Contains user-entered values from date/time related comboboxes.
        widgets : list of class Widgit
            Contains details of GUI widgets.
        table : dict
    --------------------------------------------------------------------------
    returns
        table : dict
            no explicit return, mutable type amended in place
    --------------------------------------------------------------------------
    """
    timestamp = None

    # The DarkSide-20k database requires UTC date/time in this format:
    # YYYY-MM-DD hh:mm:ss, e.g. 2022-07-19 07:00:00
    date_time_string = (
        f'{dtf["year"]}-{dtf["month"]}-{dtf["day"]} '
        f'{dtf["hour"]}:{dtf["minute"]}:00'
    )
    with contextlib.suppress(ValueError):
        timestamp = parse(date_time_string, fuzzy=False).strftime('%Y-%m-%d %H:%M:%S')

    good = timestamp is not None

    # set colour of all date/time labels
    for widget in widgets:
        if widget.cluster == 'production_date' and widget.itype == 'label':
            set_label_colour(widget.instance, good)

    if good:
        table['production_date'] = timestamp
    else:
        print_to_console(widgets, 'production date: incomplete/incorrect')


def process_other(widgets, table, dbi, other_definition):
    """
    Process any field that isn't a SiPM or a timestamp.

    All the values retrieved from the comboboxes were derived from the
    database, and none of the combobox values can contradict the others.
    It's still possible for database look-ups based on these values to fail.

    --------------------------------------------------------------------------
    args
        widgets : list
            Contains details of GUI widgets.
        table : dict
        dbi : ds20kdb.interface.Database
            Instance of the Database interface class; allows communication
            with the database.
        other_definition : tuple (string, string)
            (combobox widget cluster name, combobox widget value)
    --------------------------------------------------------------------------
    returns : none
    --------------------------------------------------------------------------
    """
    cluster, value = other_definition

    # get label associated with this widget combobox
    other_label_widget = next(
        w.instance for w in widgets
        if w.cluster == cluster and w.itype == 'label'
    )

    # exit early if the user hasn't selected a value from the drop-down menu
    user_selected_nothing = not bool(value)
    if user_selected_nothing:
        print_to_console(widgets, f'{cluster}: no value selected')
        set_label_colour(other_label_widget, good=False)
        return

    # perform database look-ups for those fields that require it
    good = False

    if cluster == 'qrcode':
        # Even though the QR-codes in the drop-down menu were obtained from
        # the database, there is a possibility that this database look-up
        # will fail if related content (vpcb_asic table) is missing/incorrect.
        response = dbi.get_vpcb_asic_pid_from_qrcode(value)
        vpcb_asic_pid = response.data
        if vpcb_asic_pid is None:
            print_to_console(
                widgets, f'{cluster}: failed vpcb_asic_pid look-up'
            )
        else:
            good = True
            table['vpcb_asic_id'] = vpcb_asic_pid

    elif cluster == 'institute':
        # This database look-up should only fail if related database entries
        # were deleted/amended after this application was initially run.
        institute_id = dbi.get_institute_id(value).data
        if institute_id is None:
            print_to_console(
                widgets, f'{cluster}: no match found'
            )
        else:
            good = True
            table['institute_id'] = institute_id

    else:
        # solder_id and run_number require no transformation or look-up
        good = True
        table[cluster] = value

    set_label_colour(other_label_widget, good=good)


def process_sipm(table, dbi, used_sipms, valid_locations, sipm_definition, errors):
    """
    Process a single SiPM - check if the user-entered data makes sense:

    (1) Have all fields been entered?
    (2) Is the given (column, row) position a valid location on the wafer
    (3) Does the SiPM as defined by wafer and location exist in the database?

    --------------------------------------------------------------------------
    args
        table : dict
        dbi : ds20kdb.interface.Database
            Instance of the Database interface class; allows communication
            with the database.
        used_sipms : dict
        valid_locations : set
        sipm_definition : dict
        errors: list of strings
    --------------------------------------------------------------------------
    returns
        table : dict
        used_sipms : dict
        GUI state affected (console).
            Error log written to console.
    --------------------------------------------------------------------------
    """
    sipm_ident, sipm_params = sipm_definition
    sipm_num = int(sipm_ident.split('_')[-1])

    good = True

    # initial checks
    #
    # (1) all fields are present?
    # (2) wafer location allowable?

    try:
        lot_number = sipm_params['lot_number']
        wafer_number = sipm_params['wafer_number']
        column = sipm_params['column']
        row = sipm_params['row']
    except KeyError:
        # at least one field was missing
        errors.append(f'SiPM {sipm_num:>2}: missing field(s)')
        # print_to_console(widgets, f'SiPM {sipm_num}: missing field(s)')
        good = False
    else:
        if (column, row) not in valid_locations:
            errors.append(
                f'SiPM {sipm_num:>2}: invalid wafer location (col={column}, row={row})'
            )
            good = False

    # local/database checks
    #
    # (1) can it be found in the database?
    # (2) if so, has the user specified this SiPM already?

    if good:
        # see if this sipm as described can be found in the database
        values = [lot_number, wafer_number, column, row]
        sipm = SiPM(dbi, *values)
        sipm_pid = sipm.sipm_pid

        if sipm_pid is not None:
            # store this PID even if it is already in used_sipms
            # we will manually remove all duplicates later in one go
            table[sipm_ident] = sipm_pid
            used_sipms[sipm_pid].add(sipm_num)
        else:
            errors.append(
                f'SiPM {sipm_num:>2}: could not be found in the database'
            )


def check(dbi, root, widgets):
    """
    Check all information the user entered into the GUI drop-down menus.

    --------------------------------------------------------------------------
    args
        dbi : ds20kdb.interface.Database
            Instance of the Database interface class; allows communication
            with the database.
        root : tkinter.Tk
            The top-level Tk widget for the main GUI window
        widgets : list
            Contains details of GUI widgets.
    --------------------------------------------------------------------------
    returns
        Error log written to console.
    --------------------------------------------------------------------------
    """
    table = {}
    used_sipms = collections.defaultdict(set)

    ##########################################################################
    print_to_console(
        widgets, f'Check start: {timestamp_to_utc_ds20k(time.time())}\n'
    )

    ##########################################################################
    # container for deferred error messages
    errors = []

    ##########################################################################
    # check values in user-entered comboboxes - and recolour labels based on
    # their validity

    valid_locations = set(interface.wafer_map_valid_locations())

    # e.g. {'year': '2024', 'month': '2', 'day': '3', 'hour': '3', 'minute': '15'})
    timestamp_parts = collections.defaultdict(dict)

    # e.g. {'sipm_1: {'lot_number': 9262109, 'wafer_number': 5, ...}, ...'}
    sipm_definitions = collections.defaultdict(dict)

    # e.g. {
    #          'institute': 'University of Liverpool',
    #          'solder_id': '4',
    #          'qrcode': '22061703000047001',
    #          'run_number': '3'
    #      }
    other_definitions = {}

    # collect user-submitted information from GUI widgets

    for widget in widgets:
        if widget.itype != 'combobox':
            continue

        if 'sipm' in widget.cluster:
            with contextlib.suppress(ValueError):
                sipm_definitions[widget.cluster].update(
                    {widget.category: int(widget.instance.get())}
                )
        elif widget.cluster == 'production_date':
            timestamp_parts[widget.category] = widget.instance.get()
        else:
            other_definitions[widget.cluster] = widget.instance.get()

    # check SiPMs, this sets table = {sipm_ident: sipm_pid, ...}
    for sipm_definition in sipm_definitions.items():
        process_sipm(
            table, dbi, used_sipms, valid_locations,
            sipm_definition, errors
        )

    ##########################################################################
    # issue warnings about any locally (GUI) duplicated SiPMs
    for sipm_numbers in used_sipms.values():
        if len(sipm_numbers) < 2:
            continue

        for sipm_number in sipm_numbers:
            table.pop(f'sipm_{sipm_number}')
            errors.append(f'SiPM {sipm_number:>2}: duplicate')

    ##########################################################################
    # Check if any user-submitted SiPMs are already allocated to vTiles
    # in the database. The call to get_sipms_allocated will become
    # increasingly expensive as the database is populated.

    sipm_pids = (
        sipm_pid for sipm_ident, sipm_pid in table.items()
        if sipm_ident.startswith('sipm_')
    )
    # {23: True, 34: True, ...}
    sipm_dupe_check = dbi.get_sipms_allocated(sipm_pids)

    # {23, ...}
    duplicate_sipm_pids = {
        sipm_pid
        for sipm_pid, duplicate in sipm_dupe_check.items()
        if duplicate
    }

    # {16: [4], 56: [9]}
    vtile_pids = dbi.get_vtile_pids_from_sipm_pids(duplicate_sipm_pids)

    for field, value in table.copy().items():
        if field.startswith('sipm_') and value in duplicate_sipm_pids:
            table.pop(field)

            qrcodes = ', '.join(
                f'{dbi.get_qrcode_from_vtile_pid(x)}' for x in vtile_pids[value]
            )
            sipm_number = int(field.split('_')[-1])
            errors.append(
                f'SiPM {sipm_number:>2}: already allocated to {qrcodes}'
            )

    print_to_console(widgets, '\n'.join(sorted(errors)))

    ##########################################################################
    # colour SiPM labels to indicate their status

    # set all SiPMs to False, only set the ones still present in table
    # (those that passed all the earlier tests) to True
    sipm_idents = {f'sipm_{x}': False for x in range(1, 24+1)}
    for field in table:
        if field.startswith('sipm_'):
            sipm_idents[field] = True

    for ident, good in sipm_idents.items():
        sipm_label_widget = next(
            w.instance for w in widgets
            if w.cluster == ident and w.itype == 'label'
        )
        set_label_colour(sipm_label_widget, good)

    ##########################################################################
    # check other parameters

    # check production date
    date_time_values_to_timestamp(timestamp_parts, widgets, table)

    # check supplementary parameters
    for other_definition in other_definitions.items():
        process_other(widgets, table, dbi, other_definition)

    # we'll need this for saving/exporting data file later
    root.setvar(name='table_json_string', value=json.dumps(table))

    ##########################################################################
    print_to_console(
        widgets, f'Check complete: {timestamp_to_utc_ds20k(time.time())}\n'
    )

    ##########################################################################
    # if the check passed, we can enable the submit button

    button_submit_widget = next(
        w.instance for w in widgets
        if w.cluster == 'submit' and w.itype == 'button'
    )
    set_button_state(button_submit_widget, disabled=len(table) != 29)


def submit(dbi, root, widgets):
    """
    POST vTile to the pre-production database.

    --------------------------------------------------------------------------
    args
        dbi : ds20kdb.interface.Database
            Instance of the Database interface class; allows communication
            with the database.
        root : tkinter.Tk
            The top-level Tk widget for the main GUI window
        widgets : list
            Contains details of GUI widgets.
    --------------------------------------------------------------------------
    returns
        Error log written to console.
    --------------------------------------------------------------------------
    """
    # get table from GUI variable
    table = json.loads(root.getvar(name='table_json_string'))
    post_succeeded = dbi.post_vtile(table)

    if post_succeeded:
        # Disable the submit button if the post succeeded to make sure the
        # user doesn't accidentally submit the same vTile more than once.
        clear_submit_button(widgets)

        # Incur an extra db lookup by referencing the table that has just been
        # written to the db, rather than retrieving the QR-code from the GUI
        # widget. This ensures that the QR-code will match the POST
        # operation, and any change made to the QR-code in the GUI by the user
        # between pressing CHECK and SUBMIT is irrelevant.
        qrcode = dbi.get_qrcode_from_vpcb_asic_pid(table['vpcb_asic_id'])
        status = f'succeeded: {qrcode}'

        # After a successful POST, there should be at least one less QR-code
        # on the list.
        refresh_qrcodes(widgets, dbi)

    else:
        status = 'failed'

    print_to_console(widgets, f'POST {status}\n')


##############################################################################
def main():
    """
    GUI for POSTing DarkSide-20k vTiles to the pre-production database.

    A 1024 x 576 pixel window should fit into any modern computer display
    without needing scrollbars.
    """

    ##########################################################################
    # define timestamp to be used for saving files
    ##########################################################################

    session_timestamp = timestamp_to_utc(time.time())

    ##########################################################################
    # Location of file from which to load/save GUI combobox default values
    # on application start.
    ##########################################################################

    filename = '.ds20kdb_defaults'
    home_directory = os.path.expanduser('~')
    defaults_file_path = os.path.join(home_directory, filename)

    ##########################################################################
    # set up GUI
    ##########################################################################

    root = tkinter.Tk()
    root_w = 1024
    root_h = 576
    root.geometry(f'{root_w}x{root_h}+0+0')
    root.title('POST vTile')

    ##########################################################################
    # shared GUI variable
    #
    # This may be used later for the import/export of the GUI content to a
    # Python file containing a dictionary suitable for manual submission to
    # the database.
    ##########################################################################

    root.setvar(name='table_json_string', value='')

    ##########################################################################
    # add menu bar and populate frames
    ##########################################################################

    frame = {}
    populate_window_with_frames(root, frame)

    widgets = []
    try:
        dbi = interface.Database()
    except AssertionError:
        sys.exit()
    wafer_table_dataframe = database_alive(dbi)

    populate_console_frame(frame, widgets)
    populate_menu_bar(root, widgets, session_timestamp, defaults_file_path)
    populate_sipm_frame(frame, widgets, wafer_table_dataframe)
    populate_supplemental_frame(frame, widgets, dbi, defaults_file_path)
    populate_production_date_frame(frame, widgets)
    populate_action_button_frame(root, frame, widgets, dbi)

    ##########################################################################
    # load defaults from file
    ##########################################################################

    load_defaults(widgets, defaults_file_path)

    ##########################################################################
    # run GUI
    ##########################################################################

    root.mainloop()


##############################################################################
if __name__ == '__main__':
    main()
