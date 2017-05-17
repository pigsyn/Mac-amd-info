#!/usr/bin/env python2.7
# -*- coding: utf-8 -*

"""
Usage: %(scriptName)s [OPTION]...

Options:
  -h,  --help            Prints this message
"""

from __future__ import unicode_literals
#from __future__ import print_function
import sys

try:
    import requests
    import lxml
    from bs4 import BeautifulSoup
except ImportError:
    print "This tool needs community packages, please install beautifulsoup4, lxml and requests"
    print "pip install lxml beautifulsoup4 requests"
    sys.exit(1)

def get_vendor_pciids(vendor_id='1002'):
    """
    Extract PCI IDS from https://pci-ids.ucw.cz database
    Returned object is a dictionnary
    """
    base_url = 'https://pci-ids.ucw.cz/read/PC/'
    url = base_url + vendor_id
    device_list = {}
    result = requests.get(url)
    html_content = result.text
    soup = BeautifulSoup(html_content, 'lxml')

    table = soup.find("table", attrs={"class" : "subnodes"})
    rows = table.find_all('tr', attrs={"class" : "item"})

    for row in rows:
        dev_id = row.find_all("td")[0].get_text()
        dev_name = row.find_all("td")[1].get_text()
        dev_comment = row.find_all("td")[2].get_text()
        device_list[dev_id] = dev_name

    return device_list

if __name__ == '__main__':
    # implement error handling
    IDS = get_vendor_pciids()
    print IDS
    