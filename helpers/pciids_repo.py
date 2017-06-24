#!/usr/bin/env python2.7
# -*- coding: utf-8 -*

"""
PCI ID Vendor/Device database collector
"""

from __future__ import unicode_literals
from __future__ import print_function
import json
import sys
import os

__version__ = '0.0.3'

try:
    import requests
    import lxml # pylint: disable=unused-import
    from bs4 import BeautifulSoup
except ImportError:
    print("This tool needs community packages, please install beautifulsoup4, lxml and requests")
    print("pip install lxml beautifulsoup4 requests")
    sys.exit(1)

# module globals
SCRIPT_PATH = os.path.dirname(__file__)
DIRPATH = (os.path.abspath(SCRIPT_PATH))
JSON_PATH = '/'.join([DIRPATH, 'pciids.json'])

def get_vendor_pciids(vendor_id='1002'):
    """
    Extract PCI IDS from https://pci-ids.ucw.cz database
    Returned object is a dictionnary
    """

    base_url = 'http://pci-ids.ucw.cz/read/PC/'
    url = base_url + vendor_id
    device_list = {}
    try:
        result = requests.get(url, timeout=3)
    except requests.exceptions.Timeout:
        print("No internet connection, loading local file ...")
        with open(JSON_PATH, 'r') as local_file:
            local_device_list = json.load(local_file)
            return {int(k):v for k, v in local_device_list.items()}

    html_content = result.text
    soup = BeautifulSoup(html_content, 'lxml')

    table = soup.find("table", attrs={"class" : "subnodes"})
    rows = table.find_all('tr', attrs={"class" : "item"})

    for row in rows:
        dev_id = int(row.find_all("td")[0].get_text(), 16)
        dev_name = row.find_all("td")[1].get_text()
        #dev_comment = row.find_all("td")[2].get_text()
        device_list[dev_id] = dev_name

    return device_list

if __name__ == '__main__':
    IDS = get_vendor_pciids()
    with open(JSON_PATH, 'w') as file_dump:
        json.dump(IDS, file_dump, indent=4, sort_keys=True)
    print(IDS)
