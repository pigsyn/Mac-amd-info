#!/usr/bin/env python2.7
# -*- coding: utf-8 -*

"""
Simple tool that report human readable informations about macOS supported AMD GPU's
"""

from __future__ import unicode_literals, print_function
import argparse
import sys
import re
from helpers.kext_reader import display_kext_info, output_kext_info
from helpers.pciids_db import VendorPciid
from helpers.common import (LEGACY_KEXT, CONTROLLER_KEXTS, GRAPHICS_KEXTS,
                            HW_SERVICES_KEXTS, DEFAULT_OUTPUT)

__version__ = '0.1.9'


# cli options
PARSER = argparse.ArgumentParser(description='Report human readable informations about AMD GPU',
                                 formatter_class=argparse.RawTextHelpFormatter)
PARSER.add_argument('-V', '--version', action='version',
                    version='%(prog)s {}'.format(__version__))
PARSER.add_argument('--output', const=DEFAULT_OUTPUT, nargs='?',
                    dest='filename',
                    help='write output to file, default is output.md')
PARSER.add_argument('-f', '--filter', nargs='+', dest='filters',
                    help=R'''show kexts matching a python regex pattern, -f 2.00 shows only 2*00 series controllers''') # pylint: disable=line-too-long
PARSER.add_argument('-l', action='store_true', default=False, help='show Legacy kexts')
PARSER.add_argument('-c', action='store_true', help='show Controllers kexts')
PARSER.add_argument('-g', action='store_true', help='show Graphic Accelerators kexts')
PARSER.add_argument('-s', action='store_true', help='show HW Services kexts')
ARGS = PARSER.parse_args()

# pci ids parser
AMD_DEVICES = VendorPciid('1002').get_vendor_pciids()

# options handling
if ARGS.filename:
    DISPLAY = False # don't print to stdout if filename is provided
else:
    DISPLAY = True

# look for generic dumping or kext types combination
# if no parameters, show all kexts except legacy one
DEFAULTS_PARMS = (not ARGS.l and not ARGS.c and not ARGS.g and not ARGS.s)

if DEFAULTS_PARMS:
    KEXTS = CONTROLLER_KEXTS + GRAPHICS_KEXTS + HW_SERVICES_KEXTS
else:
    KEXTS = []
    if ARGS.l:
        KEXTS.extend(LEGACY_KEXT)
    if ARGS.c:
        KEXTS.extend(CONTROLLER_KEXTS)
    if ARGS.g:
        KEXTS.extend(GRAPHICS_KEXTS)
    if ARGS.s:
        KEXTS.extend(HW_SERVICES_KEXTS)

if ARGS.filters: # prune kext list when regex is provided
    FILTERS = [re.compile(regex) for regex in ARGS.filters]
    MATCH_KEXT = []
    for regex in FILTERS:
        TMP_KEXTS = filter(regex.search, KEXTS)
        MATCH_KEXT.extend(TMP_KEXTS)
    KEXTS = set(MATCH_KEXT) # don't want duplicates

if not KEXTS:
    print('No kext found with provided parameters: {}'.format(' '.join(sys.argv)))
    sys.exit(1)

# write or display output
if not DISPLAY:
    output_kext_info(KEXTS, AMD_DEVICES, ARGS.filename)
    print("Updated output in {}".format(ARGS.filename))
else:
    print(display_kext_info(KEXTS, AMD_DEVICES), end='')
