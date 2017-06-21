#!/usr/bin/env python2.7
# -*- coding: utf-8 -*

"""
Framebuffer extractor and video Connector reader
"""

from __future__ import unicode_literals
from __future__ import print_function
import glob
from subprocess import Popen, PIPE
import re
import struct

__version__ = '0.0.1'

REG_NAME = r"(__ZN[0-9]{1,2})([A-Z]{1}[a-z]+)(Info10createInfo)"
REG_LEAQ = r"(leaq)\s+(0x[0-9a-fA-F]+)"
REG_JMP = r"(jmp)\s+(0x[0-9a-fA-F]+)"
REG_RETQ = r"(retq)"
REG_MOVB = r"(movb)\s+\$(0x[0-9a-fA-F]+)"

PORT_TYPE = {'02000000': 'LVDS', '04000000': 'DVI-DL', '80000000': 'S-Video',
             '10000000': 'VGA', '00020000': 'DVI-SL', '00040000': 'DP',
             '00080000': 'HDMI', '00100000': 'Mini-DVI'}


def controller_kext_dis(kext_path):
    """
    Otool wrapper, disassemble file
    """
    cmd = Popen(['otool', '-Xvt', kext_path], stdout=PIPE)
    output = cmd.communicate()

    return output[0]


def addr_lookup(dump_file):
    """
    Generate list of personalities for current kext
    """
    tmp_fb = {}
    personalities = []
    for line in dump_file.split('\n'):
        fb_name = re.search(REG_NAME, line)
        if fb_name: # only do stuff once we have a FB name
            tmp_fb['name'] = fb_name.group(2)
        elif 'name' in tmp_fb.keys():
            fb_leaq = re.search(REG_LEAQ, line)
            fb_port = re.search(REG_MOVB, line)
            fb_off = re.search(REG_JMP, line)
            stop = re.search(REG_RETQ, line)
            if fb_leaq:
                tmp_fb['addr'] = fb_leaq.group(2)
            if fb_port and 'ports' not in tmp_fb.keys():
                tmp_fb['ports'] = int(fb_port.group(2), 16)
            if fb_off:
                tmp_fb['offset'] = hex(int(fb_off.group(2), 16) + 0x1a)
            if stop: # detected return addr, section complete
                personalities.append(tmp_fb)
                tmp_fb = {}
                del stop
        else:
            continue

    return personalities


def ports_reader(personalities, kext_path):
    """
    Read binary data offsets and extract available ports
    """
    kext_blob = kext_path

    with open(kext_blob, 'rb') as bin_data:
        for hexinfo in personalities:
            ports = []
            start_offset = int(hexinfo['addr'], 16) + int(hexinfo['offset'], 16)
            print("\n@", start_offset, 'hexdump:')
            bin_data.seek(start_offset)
            for i in range(hexinfo['ports'], 0, -1):
                blob = bin_data.read(24)
                #print(repr(blob))
                data = struct.unpack('>IIHHHHBBBBI', blob)
                print("<{0:08x} {1:08x} {2:04x} {3:04x} {6:02x} {7:02x} {8:02x} {9:02x}>".format(*data))

                port_code = "{0:08x}".format(data[0])
                if port_code in PORT_TYPE.keys():
                    ports.append(PORT_TYPE[port_code])

            print("* {}: {}".format(hexinfo['name'], ", ".join(ports)))



if __name__ == '__main__':
    # implement error handling
    KEXTS_PATHS = '/System/Library/Extensions/'
    CONTROLLER_KEXTS = glob.glob(KEXTS_PATHS + 'AMD*Controller.kext/Contents/MacOS/AMD*Controller')
    for kext in sorted(CONTROLLER_KEXTS):
        print("### {}".format(kext.split('/')[-4]))
        dump = controller_kext_dis(kext)
        hex_lookup = addr_lookup(dump)
        ports_reader(hex_lookup, kext)
        print("")
