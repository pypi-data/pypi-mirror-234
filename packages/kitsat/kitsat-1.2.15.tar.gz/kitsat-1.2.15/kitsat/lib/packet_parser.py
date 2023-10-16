#!/usr/bin/env python
#
# Functions for parsing packets received from satellite into human-readable form
#
# This file is part of kitsat-python. https://github.com/netnspace/Kitsat-Python-Library
# (C) 2020 Tuomas Simula <tuomas@simu.la>
#
#SPDX-License-Identifier:   GPL-3.0-or-later

from . import math_utils
import struct

def parse(pkg):
    """Function for extracting data from packet and logging it"""

    timestamp_int = int.from_bytes(pkg[3:7], byteorder='little')

    orig_int = pkg[0]
    cmd_id_int = pkg[1]
    data_len_int = pkg[2]
    fnv_int = int.from_bytes(pkg[-4:], byteorder='little')

    data = pkg[7:7+data_len_int]
    data_str = parse_bytedata(orig_int, cmd_id_int, data)
    data_arr = [orig_int, cmd_id_int, data_len_int, timestamp_int, data_str, fnv_int]

    # Check that packet matches checksum
    if math_utils.check_fnv(pkg):
        return data_arr
    else:
        return "package corrupted"
        
        
def parse_imu(data):
    values = struct.unpack('f'*9, data)  # 'f' indicates a single-precision float, and we repeat it 9 times for 9 floats
    mag_values = "{:.2f},{:.2f},{:.2f}".format(values[0], values[1], values[2])
    gyr_values = "{:.2f},{:.2f},{:.2f}".format(values[3], values[4], values[5])
    acc_values = "{:.2f},{:.2f},{:.2f}".format(values[6], values[7], values[8])
    
    return ( "mag " + mag_values + "; gyr " + gyr_values + "; acc " + acc_values )
    
def parse_eps(data):
    return ( "mag " + mag_values + "; gyr " + gyr_values + "; acc " + acc_values )
    
    
def parse_gps(data):
    # Unpack the binary data into floats
    values = struct.unpack('f'*5, data)  # 'f' indicates a single-precision float, and we repeat it 5 times for 5 floats

    # Check for "nofix" equivalent in Python
    if values[0] == -1 or values[1] == -1:
        # Process as in your "nofix" case
        lat_lon = "0,0"
        altitude = "0"
        velocity = "0"
    else:
        lat_lon = "{:.5f},{:.5f}".format(values[0], values[1])
        altitude = "{:.2f}".format(values[2])
        velocity = "{:.2f}".format(values[3])

        # Format the time as in your C# code
        time_int = int(values[4])
        time_str = "{:06d}".format(time_int)
        time_formatted = "{}:{}:{}".format(time_str[:2], time_str[2:4], time_str[4:6])
        
        return ("lat_lon " + lat_lon + "; altitude " + altitude + "; velocity " + velocity + "; time " + time_formatted)


def parse_bytedata(orig, cmd_id, data):
    """Function for parsing received data into human-readable form"""
    try:
        data = data.decode('utf-8')
    except UnicodeDecodeError:  
        if orig == 3: #GPS
            if(cmd_id == 6):
                data = parse_gps(data)
        elif orig == 5: #IMU
            if(cmd_id == 14):
                data = parse_imu(data)
        elif orig == 8: # EPS
            if(cmd_id == 4):
                data = parse_eps(data)
        elif orig == 14: # Beacon
            # TODO
            pass

    return(data)
