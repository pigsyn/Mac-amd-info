# -*- coding: utf-8 -*

"""
PCI ID Vendor/Device database parser
"""

from __future__ import unicode_literals, print_function
import json
import sys
from helpers.common import JSON_PATH

__version__ = '0.1.1'

try:
    import requests
    import lxml  # pylint: disable=unused-import
    from bs4 import BeautifulSoup
except ImportError:
    print("This tool needs community packages, please install beautifulsoup4, lxml and requests")
    print("pip install lxml beautifulsoup4 requests")
    sys.exit(1)


class VendorPciid(object):
    """
    Extract PCI IDS from https://pci-ids.ucw.cz database
    Returned object is a dictionnary
    """

    def __init__(self, vendor_id='1002', load_path=JSON_PATH):
        self.vendor_id = vendor_id
        self.load_path = load_path
        self.base_url = 'https://pci-ids.ucw.cz/read/PC/'
        self.url = "{0}{1}".format(self.base_url, self.vendor_id)
        self.device_list = {}
        self.save_json = True

    def get_vendor_pciids(self):
        """ Extracts table data from url """
        try:
            result = requests.get(self.url, timeout=3)
        except BaseException:
            print('Could not access {}, loading local json file ...'.format(self.url))
            return self.load_local_json()
        html_content = result.text
        soup = BeautifulSoup(html_content, 'lxml')

        table = soup.find("table", attrs={"class": "subnodes"})
        rows = table.find_all('tr', attrs={"class": "item"})

        for row in rows:
            dev_id = int(row.find_all("td")[0].get_text(), 16)
            dev_name = row.find_all("td")[1].get_text()
            # dev_comment = row.find_all("td")[2].get_text()
            self.device_list[dev_id] = dev_name

        return self.device_list

    def load_local_json(self):
        """ Load local json file """
        self.save_json = False
        with open(self.load_path, 'r') as local_file:
            local_device_list = json.load(local_file)
            return {int(k): v for k, v in local_device_list.items()}
