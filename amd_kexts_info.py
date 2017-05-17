#!/usr/bin/env python2.7
# -*- coding: utf-8 -*

"""
Usage: %(scriptName)s [OPTION]...

Options:
  -h,  --help            Prints this message
"""

from __future__ import unicode_literals
#from __future__ import print_function
import plistlib
import glob
from helpers.pciids_repo import get_vendor_pciids


def read_amd_plist(kext_path):
    """ Scan kext plist and exctract pciid data """
    
    device_list = []

    personalities = plistlib.readPlist(kext_path)['IOKitPersonalities']
    
    for controller in personalities.keys():
        if 'IOPCIMatch' in personalities[controller].keys():
            # just need 2 bytes from device, as a string
            ids = personalities[controller]['IOPCIMatch']
            ids = ids.lower().replace('1002', '').replace('0x', '').split()
            device_list.extend(ids)
        else: # older amd plist files have different structure
            ids = personalities[controller]['IONameMatch']#.split(','))
            if isinstance(ids, list): # even older kexts have multiple strings tags
                ids = [ i.replace('pci1002,', '') for i in ids ]
                device_list.extend(ids)
            else:
                ids = ids.split(',')[1]
                device_list.append(ids)
              
    return device_list


def display_kext_info(kexts_paths, pci_ids):
    """ Compares macOS amd kext devices to online pci ids DB and print output """
    
    for path in kexts_paths:
        kext_name = path.split('/')[4]
        macos_amd_devices = read_amd_plist(path)
        print kext_name
        for device in sorted(macos_amd_devices):
            if device in pci_ids.keys():
                print "pci {}: {}".format(device , pci_ids[device])
            else:
                print "pci {}: {}".format(device, 'unknown device')
        print ""


if __name__ == '__main__':
    # implement error handling
    kexts_path = '/System/Library/Extensions/'
    controller_kexts = glob.glob(kexts_path + 'AMD*Controller.kext/Contents/Info.plist')
    graphics_kexts = glob.glob(kexts_path + 'AMDRadeonX*.kext/Contents/Info.plist')

    amd_devices = get_vendor_pciids('1002') # 1002 is AMD
    display_kext_info(controller_kexts, amd_devices)
    display_kext_info(graphics_kexts, amd_devices)
