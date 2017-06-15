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
from helpers.pciids_repo import get_vendor_pciids

__version__ = '0.1.5'

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
            # just need 2 bytes from device, as a string
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

    for path in sorted(kexts_paths):
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


if __name__ == '__main__':
    # implement error handling
    KEXTS_PATHS = '/System/Library/Extensions/'
    LEGACY_KEXT = glob.glob(KEXTS_PATHS + 'AMDLegacySupport.kext/Contents/Info.plist')
    CONTROLLER_KEXTS = glob.glob(KEXTS_PATHS + 'AMD*Controller.kext/Contents/Info.plist')
    GRAPHIC_KEXTS = glob.glob(KEXTS_PATHS + 'AMDRadeonX*.kext/Contents/Info.plist')

    AMD_DEVICES = get_vendor_pciids('1002') # 1002 is AMD
    display_kext_info(LEGACY_KEXT, AMD_DEVICES)
    display_kext_info(CONTROLLER_KEXTS, AMD_DEVICES)
    display_kext_info(GRAPHIC_KEXTS, AMD_DEVICES)
