# -*- coding: utf-8 -*

"""
Utilities and Configuration manager
"""

from __future__ import unicode_literals
import os
import re
import glob

__version__ = '0.0.1'

# get absolute path
CUR_PATH = os.path.dirname(__file__)
ABS_PATH = os.path.abspath(CUR_PATH)

# project structure globals
ROOT_DIR = os.path.dirname(ABS_PATH)
DATA_PATH = os.path.abspath(os.path.join(ROOT_DIR, 'data'))
LIB_PATH = os.path.abspath(os.path.join(ROOT_DIR, 'helpers'))
JSON_PATH = os.path.abspath(os.path.join(DATA_PATH, 'pciids.json'))
DEFAULT_OUTPUT = os.path.abspath(os.path.join(DATA_PATH, 'output.md'))

# OS globals
KEXTS_PATHS = '/System/Library/Extensions/'
DARWIN_VERSION = os.uname()[2]
AMD_KEXTS = glob.glob(KEXTS_PATHS + 'AMD*.kext')

# kext regexes
LEGACY = re.compile('AMDLegacySupport.kext')
CONTROLLER = re.compile('AMD[0-9]{4,5}Controller.kext')
GRAPHICS = re.compile('AMDRadeonX[0-9]{4,5}.kext')
HW_SERVICE = re.compile('AMDRadeonX[0-9]{4,5}HWServices.kext')

# kext families
LEGACY_KEXT = filter(LEGACY.search, AMD_KEXTS)
CONTROLLER_KEXTS = filter(CONTROLLER.search, AMD_KEXTS)
GRAPHICS_KEXTS = filter(GRAPHICS.search, AMD_KEXTS)
HW_SERVICES_KEXTS = filter(HW_SERVICE.search, AMD_KEXTS)
ALL_KEXTS = LEGACY_KEXT + CONTROLLER_KEXTS + GRAPHICS_KEXTS + HW_SERVICES_KEXTS


def natural_sort(string_):
    """ Human expected alnum sort """
    return [int(s) if s.isdecimal() else s for s in re.split(r'(\d+)', string_)]


def str_to_int(string_list):
    """ convert list of hex strings into list of ints """
    int_list = [int(x, 16) for x in string_list]
    return int_list
