#!/usr/bin/env python
#
# Function for parsing command strings into packets that can be sent to satellite
#
# This file is part of kitsat-python. https://github.com/netnspace/Kitsat-Python-Library
# (C) 2020 Tuomas Simula <tuomas@simu.la>
#
#SPDX-License-Identifier:   GPL-3.0-or-later

import pkgutil
from . import math_utils


def parse(cmd, msg_queue = None, is_cli = False):
    """Function for parsing command strings into packets that can be sent to satellite"""

    csv_file = pkgutil.get_data('kitsat', 'cfg/sat_commands.csv').decode('utf-8').splitlines()
    csv_file = csv_file[1:]

    packet = bytearray()
    paramtype = ''
    
    cmd = cmd.split(' ', 1)

    # Find command in command_list.csv
    for row in csv_file:
        row = row.split(',')
        if row[0] == cmd[0]:
            packet.append(int(row[1]))
            packet.append(int(row[2]))
            paramtype = row[3]
            break
    
    # Check that the included params are of correct type
    if paramtype == 'int':
        try:
            int(cmd[1])
        except (ValueError, IndexError) as e:
            if is_cli:
                msg_queue.put(e)
            packet = b''
        else:
            packet.append(len(cmd[1].encode('utf-8')))
            packet.extend(bytearray(cmd[1], 'utf-8'))

    elif paramtype == 'int|int':
        try:
            params = cmd[1].split(' ')
            int(params[0])
            int(params[1])
        except (ValueError, IndexError) as e:
            msg_queue.put(e)
            packet = b''
        else:
            packet.append(len(cmd[1].encode('utf-8')))
            packet.extend(bytearray(cmd[1], 'utf-8'))
    
    elif paramtype == 'str':
        try:
            packet.append(len(cmd[1].encode('utf-8')))
        except IndexError as e:
            msg_queue.put(e)
            packet = b''
        else:
            packet.extend(bytearray(cmd[1], 'utf-8'))
    
    else:
        packet.append(0)
    
    # Add FNV checksum and put constructed packet to output queue
    if not packet == b'':
        packet.extend(math_utils.fnv(bytearray(packet)).to_bytes(4, 'little'))
    return(packet)
