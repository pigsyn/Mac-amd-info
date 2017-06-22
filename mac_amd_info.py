#!/usr/bin/env python2.7
# -*- coding: utf-8 -*

"""
Simple tool that report human readable informations about macOS supported AMD GPU's
"""

from __future__ import unicode_literals
from __future__ import print_function
import plistlib
import glob
import re
import argparse
import sys
import os
from helpers.pciids_repo import get_vendor_pciids

__version__ = '0.1.7'

def read_amd_plist(kext_path):
    """ Scan kext plist and exctract pciid data """

    plist_filter = [
        re.compile('Controller'),
        re.compile('.*GraphicsAccelerator'),
        re.compile('ATI Support'),
        re.compile('.*HW Services')]

    device_list = []

    personalities = plistlib.readPlist(kext_path)['IOKitPersonalities']

    for controller in personalities.keys():
        if any(regex.match(controller) for regex in plist_filter):

            if 'IOPCIMatch' in personalities[controller].keys():
            # just need 2 bytes from device string
                ids = personalities[controller]['IOPCIMatch']
                ids = hex_to_int(ids.replace('1002', '').split())
                device_list.extend(ids)
            else: # older amd plist files have different structure
                ids = personalities[controller]['IONameMatch']#.split(','))
                if isinstance(ids, list): # even older kexts have multiple strings tags
                    ids = hex_to_int([i.replace('pci1002,', '') for i in ids])
                    device_list.extend(ids)
                else:
                    ids = int(ids.split(',')[1], 16)
                    device_list.append(ids)

    return device_list


def hex_to_int(string_list):
    """ convert list of hex strings into list of ints """
    int_list = [int(x, 16) for x in string_list]
    return int_list


def display_kext_info(kexts_paths, pci_ids):
    """ Compares macOS amd kext devices to online pci ids DB and print output """

    for path in sorted(kexts_paths, key=unicode.lower):
        kext_name = path.split('/')[-3]
        macos_amd_devices = read_amd_plist(path)
        print('### {}'.format(kext_name))
        for device in sorted(macos_amd_devices):
            if device in pci_ids.keys():
                description = pci_ids[device]
            else:
                description = 'unknown device'
            print("* pci device: {:x} - {}".format(device, description))
        print("")


def write_output(kexts_paths, pci_ids, output_path='output.md'):
    """ Write output to file, markdown format """

    with open(output_path, 'w') as output:
        for path in sorted(kexts_paths, key=unicode.lower):
            kext_name = path.split('/')[-3]
            macos_amd_devices = read_amd_plist(path)
            output.write('### {}\n'.format(kext_name))
            for device in sorted(macos_amd_devices):
                if device in pci_ids.keys():
                    description = pci_ids[device]
                else:
                    description = 'unknown device'
                output.write("* pci device: {:x} - {}\n".format(device, description))
            output.write("\n")


if __name__ == '__main__':
    # cli options
    PARSER = argparse.ArgumentParser(description='Report human readable informations about AMD GPU',
                                     formatter_class=argparse.RawTextHelpFormatter)
    PARSER.add_argument('-V', '--version', action='version',
                        version='%(prog)s {}'.format(__version__))
    PARSER.add_argument('--output', const='output.md', nargs='?',
                        dest='filename',
                        help='write output to file, default is output.md')
    PARSER.add_argument('-f', '--filter', nargs='+', dest='filters',
                        help=R'''show kexts matching a python regex pattern, -f 2.00 shows only 2*00 series controllers''') # pylint: disable=line-too-long
    PARSER.add_argument('-l', action='store_true', default=False, help='show Legacy kexts')
    PARSER.add_argument('-c', action='store_true', help='show Controllers kexts')
    PARSER.add_argument('-g', action='store_true', help='show Graphic Accelerators kexts')
    ARGS = PARSER.parse_args()

    # Script Globals
    SCRIPT_PATH = os.path.dirname(__file__)
    DIRPATH = (os.path.abspath(SCRIPT_PATH))
    KEXTS_PATHS = '/System/Library/Extensions/'
    LEGACY_KEXT = glob.glob(KEXTS_PATHS + 'AMDLegacySupport.kext/Contents/Info.plist')
    CONTROLLER_KEXTS = glob.glob(KEXTS_PATHS + 'AMD*Controller.kext/Contents/Info.plist')
    GRAPHIC_KEXTS = glob.glob(KEXTS_PATHS + 'AMDRadeonX*.kext/Contents/Info.plist')
    ALL_KEXTS = LEGACY_KEXT + CONTROLLER_KEXTS + GRAPHIC_KEXTS
    AMD_DEVICES = get_vendor_pciids('1002') # 1002 is AMD

    # options handling
    if ARGS.filename:
        DISPLAY = False # don't print to stdout if filename is provided
    else:
        DISPLAY = True

    # look for generic dumping or kext types combination
    # if no parameters, show all kexts except legacy one
    DEFAULTS_PARMS = (not ARGS.l and not ARGS.c and not ARGS.g)

    if DEFAULTS_PARMS:
        KEXTS = CONTROLLER_KEXTS + GRAPHIC_KEXTS
    else:
        KEXTS = []
        if ARGS.l:
            KEXTS.extend(LEGACY_KEXT)
        if ARGS.c:
            KEXTS.extend(CONTROLLER_KEXTS)
        if ARGS.g:
            KEXTS.extend(GRAPHIC_KEXTS)

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
        write_output(KEXTS, AMD_DEVICES, ARGS.filename)
        print("Updated output in {}".format(ARGS.filename))
    else:
        display_kext_info(KEXTS, AMD_DEVICES)
