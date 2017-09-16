#!/usr/bin/env python2.7
# -*- coding: utf-8 -*

"""
PCI ID Vendor/Device database collector
"""

from __future__ import unicode_literals, print_function
import json
import sys
import os

CUR_PATH = os.path.dirname(__file__)
ABS_PATH = os.path.abspath(CUR_PATH)
ROOT_DIR = os.path.dirname(ABS_PATH)
sys.path.insert(1, ROOT_DIR)

from helpers.pciids_db import VendorPciid # pylint: disable=wrong-import-position
from helpers.common import JSON_PATH # pylint: disable=wrong-import-position

if __name__ == '__main__':
    # tries to refresh local json
    IDS = VendorPciid('1002')
    PCIIDS = IDS.get_vendor_pciids()
    print('{}: {}'.format('Can update json', IDS.save_json))
    if IDS.save_json:
        print('Saving JSON under: {}'.format(IDS.json_path))
        with open(JSON_PATH, 'w') as file_dump:
            json.dump(PCIIDS, file_dump, indent=4, sort_keys=True)
