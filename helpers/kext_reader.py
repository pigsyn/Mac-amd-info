# -*- coding: utf-8 -*

"""
AMD Kext parser
"""

from __future__ import unicode_literals, print_function
import re
import plistlib
from helpers.common import natural_sort, str_to_int, PLIST_FILTER

__version__ = '0.0.3'


def read_kext_plist(kext_path):
    """ Scan kext plist and exctract pciid data """

    kext_name = kext_path.split('/')[-1]
    plist_file = '/'.join([kext_path, 'Contents/Info.plist'])
    device_list = []
    personalities = plistlib.readPlist(plist_file)['IOKitPersonalities']
    fb_names = []
    if 'Controller' in personalities.keys():
        for k in personalities['Controller'].keys():
            if k.startswith('ATY'):
                fb_names.append(k.split(',')[1])
    # print(' '.join(fb_names))

    for controller in personalities.keys():
        if any(regex.match(controller) for regex in PLIST_FILTER):
            if 'IOPCIMatch' in personalities[controller].keys():
                # just need 2 bytes from device string
                ids = personalities[controller]['IOPCIMatch']
                ids = str_to_int(ids.replace('1002', '').split())
                device_list.extend(ids)
            else:  # older amd plist files have different structure
                ids = personalities[controller]['IONameMatch']  # .split(','))
                if isinstance(ids, list):  # even older kexts have multiple strings tags
                    ids = str_to_int([i.replace('pci1002,', '') for i in ids])
                    device_list.extend(ids)
                else:
                    ids = int(ids.split(',')[1], 16)
                    device_list.append(ids)

    return {'name': kext_name, 'devices': device_list, 'personalities': fb_names}


def display_kext_info(kexts_paths, pci_ids):
    """
    Compares macOS amd kext pci devices to online pciids DB and return output in markdown format
    """

    output = ''
    for path in sorted(kexts_paths, key=natural_sort):
        macos_amd_devices = read_kext_plist(path)
        output += '### {}\n'.format(macos_amd_devices['name'])
        for device in sorted(macos_amd_devices['devices']):
            if device in pci_ids.keys():
                description = pci_ids[device]
            else:
                description = 'unknown device'
            output += '* pci device: {:x} - {}\n'.format(device, description)
        # if macos_amd_devices['personalities']:
        #    print("* personalities: {}".format(', '.join(macos_amd_devices['personalities'])))
        output += '\n'
    return output


def output_kext_info(kexts_paths, pci_ids, output_path):
    """ Write output to file """

    with open(output_path, 'w') as output_file:
        output = display_kext_info(kexts_paths, pci_ids)
        output_file.write(output)
