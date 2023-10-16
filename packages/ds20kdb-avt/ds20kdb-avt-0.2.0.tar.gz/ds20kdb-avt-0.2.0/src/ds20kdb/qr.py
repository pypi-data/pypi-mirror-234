#!/usr/bin/env python3
"""
Simple OpenCV-based QR-code reader. Ignores other types of barcode.

qrtools looks like an abandoned project, and is heavily based on pyzbar.
pyzbar gets better results than using OpenCV's own detectAndDecode() and is
worth the additional dependency.

There seems to be no OpenCV API support for returning available camera
indices. Manually probing them leads to error messages being echoed which is
not ideal for this application.

https://docs.opencv.org/3.4/d8/dfe/classcv_1_1VideoCapture.html

The feature request for this issue has languished unresolved since 2015

https://github.com/opencv/opencv/issues/4269
"""

import argparse
import datetime
import sys

import cv2
try:
    from pyzbar.pyzbar import decode, ZBarSymbol
except ImportError as err:
    print(f'Problem importing pyzbar: err={err}, type(err)={type(err)}')
    sys.exit(1)


##############################################################################
def qr_code_valid(qr_code_numerals):
    """
    Basic validation of string decoded from QR code.

    --------------------------------------------------------------------------
    args
        qr_code_numerals : string
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


def dict_from_qrcode(qr_code_numerals):
    """
    --------------------------------------------------------------------------
    args
        qr_code_numerals : string
            e.g. '22061703000032001', where (from left to right):
                220617 - YYMMDD
                0      - PRODUCTION FLAG
                30     - VERSION
                00032  - SERIAL NUMBER
                001    - PART NUMBER
    --------------------------------------------------------------------------
    returns : dict or None
        {'timestamp': datetime.datetime, 'production': bool,
        'version': int, 'serial_number': int, 'part_number': int}
        e.g.
        dict_from_qrcode('22061703000032001')
        {'timestamp': datetime.datetime(2022, 6, 17, 0, 0),
         'production': False,
         'version_string': '3.0',
         'version_major': 3,
         'version_minor': 0,
         'serial_number': 32,
         'part_number': 1}

        dict if the received string looks plausible, None otherwise.
    --------------------------------------------------------------------------
    """
    if not qr_code_valid(qr_code_numerals):
        return None

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


def from_camera_index():
    """
    Handle command line help and options.

    --------------------------------------------------------------------------
    args : none
    --------------------------------------------------------------------------
    returns
        int : index of camera to use
    --------------------------------------------------------------------------
    """
    parser = argparse.ArgumentParser(
        description="Reads a QR code from a connected webcam, and prints the\
        interpreted string to stdout. The focal distance for detection of a\
        1cm square 21x21 QR-code on most tested webcams was between 4 and\
        8 cm. A standard UNIX error code is emitted at exit."
    )
    parser.add_argument(
        "camera_index",
        nargs="?",
        help="If your machine has more than one camera, specify the index\
        of the camera to be used for QR code reading. The default if this\
        value is unspecified is 0 which is the first camera found.",
        type=int,
        default=0,
        choices=range(8),
    )

    return parser.parse_args().camera_index


##############################################################################
def read(camera_index):
    """
    Simple OpenCV-based QR-code reader. Ignores other types of barcode.

    --------------------------------------------------------------------------
    args
        camera_index : int
            index of camera to use
    --------------------------------------------------------------------------
    returns
        text : string
            decoded value of QR-code
    --------------------------------------------------------------------------
    """
    video_stream = cv2.VideoCapture(index=camera_index)

    text = ""
    while True:
        # get frame from video stream
        _, frame = video_stream.read()

        # don't assume that the frame colourspace will be suitable for pyzbar
        try:
            im_grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        except cv2.error:
            # user specified a non-existent camera
            break

        # multiple QR-codes may be returned from the frame
        barcodes = [
            b.data.decode("utf-8") for b in decode(im_grey, symbols=[ZBarSymbol.QRCODE])
        ]

        # exit with success if a single valid QR-code is in the frame
        if barcodes and all(x is not None for x in barcodes):
            if len(barcodes) == 1 and qr_code_valid(barcodes[0]):
                text = barcodes[0]
                break

    return text


##############################################################################
def main():
    """
    Simple OpenCV-based QR-code reader.
    """
    text = read(from_camera_index())
    if text:
        retcode = 0
        print(text)
    else:
        retcode = 1

    return retcode


##############################################################################
if __name__ == "__main__":
    sys.exit(main())
