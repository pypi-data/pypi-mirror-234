#!/usr/bin/env python
#
# Functions for calculating and checking fnv checksums
#
# This file is part of kitsat-python. https://github.com/netnspace/Kitsat-Python-Library
# (C) 2020 Samuli Nyman
#
#SPDX-License-Identifier:   GPL-3.0-or-later

def fnv (bytear):
    """Create fnv checksum for packet"""

    hval = 0x811c9dc5
    fnv_32_prime = 0x01000193
    uint32_max = 4294967296
    for s in bytear:
        hval = hval ^ s
        hval = (hval * fnv_32_prime) % uint32_max
    return hval

def check_fnv (bytear):
    """Test fnv checksum of packet"""

    local_fnv = fnv(bytear[:-4])
    parsed_fnv = int.from_bytes(bytear[-4:], byteorder='little')
    return local_fnv == parsed_fnv
