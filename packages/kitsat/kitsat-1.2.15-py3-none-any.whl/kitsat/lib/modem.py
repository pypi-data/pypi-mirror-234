#!/usr/bin/env python
#
# Base class for communicating with the KitSat satellite
#
# This file is part of kitsat-python. https://github.com/netnspace/Kitsat-Python-Library
# (C) 2020 Tuomas Simula <tuomas@simu.la>
#
#SPDX-License-Identifier:   GPL-3.0-or-later

import csv
import multiprocessing
import os
import pickle
import queue

from os import path
from time import sleep, time, localtime, gmtime, strftime

import serial
from serial.tools import list_ports
from serial.serialutil import SerialException

from . import math_utils
from . import cmd_parser
from . import packet_parser


def _download_pic(ser, _msg_queue, stop_flag, img_num, start_time, _is_cli):
    """Download picture over radio"""

    ser.timeout = 5

    if _is_cli: _msg_queue.put("downloading image")

    # Get number of blocks for image to be downloaded
    ser.write(cmd_parser.parse('cam_num_blocks {}'.format(img_num), _msg_queue))
    ser.read_until(b'packet:')
    ser.read(2)
    data_len = int.from_bytes(ser.read(), 'little')
    ser.read(4)
    blocks_amt = int(ser.read(data_len).decode('ascii'))
    if _is_cli:
        _msg_queue.put("Downloading {} blocks".format(blocks_amt))
    else:
        _msg_queue.put(blocks_amt)

    ser.timeout = 1


    # Create paths for blockfile and actual image
    file_dir = os.path.dirname(__file__)
   
    images_path = os.path.join(file_dir, '..', 'data', 'files', start_time, 'downloaded')
    blocks_path = os.path.join(images_path, 'image-{}.jpeg.blocks'.format(img_num))
    img_pth = os.path.join(images_path, 'image-{}.jpeg'.format(img_num))
    if not os.path.isdir(images_path):
        os.makedirs(images_path)

    # Check, if some of the blocks for this image are saved in data
    try:
        with open(blocks_path, 'rb') as blockfile:
            blocks = pickle.load(blockfile)
    except(FileNotFoundError, EOFError):
        # If not, create file to store the blocks and initialize the blocks array
        # The last element of the array keeps track of the next blocks to download
        with open(blocks_path, 'wb') as blockfile:
            blocks = [b'x00' for x in range(blocks_amt)]
            i = 0
            blocks.append([i])
            pickle.dump(blocks, blockfile)
    else:
        # If file is found, get the iterator i from last element of the blocks array
        i = blocks[-1][-1]

    try:
        while blocks[-1][0] < blocks_amt and stop_flag.value == 0:
            # Send command to get blocks
            if _is_cli: _msg_queue.put("cam_get_blocks {} {}".format(img_num, ' '.join(str(x) for x in blocks[-1])))
            cmd = cmd_parser.parse('cam_get_blocks {} {}'.format(img_num, ' '.join(str(x) for x in blocks[-1])), _msg_queue)
            ser.write(cmd)

            # Read the 20 incoming packages
            for x in range(20):
                # Read until the 'packet:' syncword
                pre_pkg = ser.read_until(b'packet:')
                if pre_pkg[-7:] == b'packet:': 
                    pkg = bytearray(ser.read(7))        # Read the first seven bytes of incoming packet
                    pkg.extend(ser.read(pkg[2] + 4))    # Read data length + fnv
                    
                    # If origin and command id match the 'get blocks' values
                    if pkg[:2] == b'\x02\x03':
                        if _is_cli: _msg_queue.put(packet_parser.parse(pkg))
                        
                        # Check that package is correct length and the fnv matches
                        if len(pkg) == 64 and math_utils.check_fnv(pkg):    
                            block_index = int.from_bytes(pkg[3:7], 'little')
                            
                            # If index of block is in list of blocks to download, remove it from the list
                            if block_index in blocks[-1]:
                                blocks[-1].remove(block_index)
                            # If index of block is higher than expected, add missing block indices to list of blocks to download
                            if block_index > i:
                                for x in range(block_index - i):
                                    if not i+x in blocks[-1]:
                                        blocks[-1].append(i+x)

                            # New highest block index expected
                            i = max(i, block_index + 1)
                            # Put the received data into the blocks list
                            blocks[block_index] = pkg[7:7+pkg[2]]
                        
                        # If package is incomplete, put its index to list of blocks to download
                        elif not i in blocks[-1]:
                            blocks[-1].append(i)
                            i += 1
                    
                    # If package is not from the expected origin, parse it like normal
                    else:
                        msq_queue.put(packet_parser.parse(pkg))

                # Break conditions for the loop
                if stop_flag.value == 1 or i >= blocks_amt:
                    break

            # Put the index for the next block to download to list of blocks to be downloaded
            blocks[-1].append(i)
            
            # Save received blocks into a data file
            with open(blocks_path, 'wb') as blockfile:
                pickle.dump(blocks, blockfile)
            
    # Run when while loop ends, even if the program is exited through ctr-c
    finally:

        # If download not yet complete, save blocks into a data file
        if i < blocks_amt:
            if blocks[-1] == []:
                blocks[-1] = [i]
            with open(blocks_path, 'wb') as blockfile:
                pickle.dump(blocks, blockfile)
        
        # If download is complete, save image
        else:
            with open(img_path, 'wb') as img:
                for block in blocks[:-1]:
                    img.write(block)
            if _is_cli: _msg_queue.put("image downloaded to {}".format(os.path.normpath(img_path)))


def _serial_process(_cmd_queue, _msg_queue, ser, stop_flag, start_time, _is_cli):
    """
    Method that actually does the communication with the satellite
    Runs in a separate process
    """

    ser.timeout = 1
    ser.open()

    # Parse path for log files
    file_dir = os.path.dirname(__file__)
    logs_path = os.path.join(file_dir, '..', 'data', 'logs')
    logfile_path = os.path.join(logs_path, 'received_packages.csv')

    # If logs directory doesn't exist, create it
    if not os.path.isdir(logs_path):
        os.makedirs(logs_path)
        with open(logfile_path, 'w') as log:
            logwriter = csv.writer(log)
            logwriter.writerow(['Time received', 'Orig', 'Command id', 'Satellite timestamp', 'Data length', 'Data', 'Fnv'])
        _msg_queue.put("log for received packages created in {}".format(os.path.normpath(logfile_path)))

    # Actual communication loop, run until stop flag is set
    while stop_flag.value == 0:
        
        # Write any packages in the command queue to serial
        if not _cmd_queue.empty(): 
            cmd = _cmd_queue.get()
            ser.write(cmd)

        # Read input from serial
        if ser.in_waiting > 10:
            pkg = ser.read_until(b'packet:')        #read until 'packet:' syncword
            if pkg [len(pkg)-7:] == b'packet:':
                pkg = bytearray(ser.read(3))        #read until data length byte
                pkg.extend(ser.read(pkg[2] + 8))    #read data length + timestamp and fnv
                parsed_pkg = packet_parser.parse(pkg)
                _msg_queue.put(parsed_pkg)

                # Log received packets 
                with open(logfile_path, 'a') as log:
                    logwriter = csv.writer(log, escapechar='\\')
                    t = strftime('%Y-%m-%d %H:%M:%SZ', gmtime())
                    logwriter.writerow([t] + parsed_pkg)
            
                # If data still coming, see if it's a stream:
                # TODO: implement streams in a better way
                if pkg[:2] == b'\x02\x0c':
                    if ser.read(8) == b'\n\rstream':
                        if _is_cli:
                            _msg_queue.put("downloading image")
                        
                        file_dir = os.path.dirname(__file__)
                        images_path = os.path.join(file_dir, '..', 'data', 'files', start_time, 'streamed') 
                        if not os.path.isdir(images_path):
                            os.makedirs(images_path)

                        # Find smallest uint i where image-i doesn't yet exist in the images folder
                        i = 1
                        file_dir = os.path.dirname(__file__)
                        while os.path.exists(os.path.join(images_path, 'image-{}.jpeg'.format(i))):
                            i += 1

                        img_path = os.path.join(images_path, 'image-{}.jpeg'.format(i))
                        
                        img_arr = bytearray()
                        temp = b''
                        lasttemp = b''
                        while True:
                            lasttemp = temp
                            temp = ser.read()
                            img_arr.extend(temp)
                            if temp == b'\xd9' and lasttemp == b'\xff': #jpeg end bytes
                                break

                        # Write image as images/image-i
                        with open(img_path, 'wb') as img:
                            img.write(img_arr)
                        if _is_cli: _msg_queue.put("image downloaded to {}".format(os.path.normpath(img_path)))

            elif pkg [:8] == b'starting' and _is_cli:
                _msg_queue.put("satellite reset")
        
        sleep(0.001)

    ser.close() #  Close serial port when process is killed


class Modem:
    """
    A class to communicate with the KitSat satellite over a serial connection
    """

    # Baud rate of the serial connection
    # This should never be changed!
    _BAUD_RATE = 115200

    def __init__(self, port = None, timeout = 1, beep_on_connect = False, start_time = None, _is_cli = False):

        if start_time == None:
            start_time = strftime("%Y_%m_%d_%H%M%S", localtime())

        self.port = port
        self.timeout = timeout
        self.beep_on_connect = beep_on_connect
        self.start_time = start_time
        self._is_cli = _is_cli
        self.ports = []

        self.is_connected = False

        self._ser = serial.Serial()
        self._cmd_queue = multiprocessing.Queue()
        self._msg_queue = multiprocessing.Queue()
        self._data_queue = multiprocessing.Queue()
        self._stop_flag = multiprocessing.Value('i', 1)

        if not self.port == None:
            self.connect(self.port)

 
    def connect(self, port):
        """Connects manually to given port
        Attribute port can be a string or index of port in self.ports"""

        if self.is_connected:
            if self._is_cli:
                self._msg_queue.put("Error: already connected on port {}".format(self.port))
            else:
                raise SerialException("Error: already connected on port {}".format(self.port))
        else:
            try:
                int(port)
            except ValueError:
                self.port = port
            else:
                try:
                    self.port = self.ports[int(port)]
                except IndexError:
                    if self._is_cli:
                        self._msg_queue.put("Error: port not found with index {}".format(port))
                    else:
                        raise SerialException("Error: port not found with index {}".format(port))
                    return 0

            self._ser.port = self.port
            self._ser.timeout = self.timeout
            self._ser.baudrate = self._BAUD_RATE

            if self._is_cli:
                self._msg_queue.put("connecting...")                
            try:
                self._ser.open()
            except SerialException as e:
                if self._is_cli:
                    self._msg_queue.put(e)
                else:
                    raise SerialException(e)
                return 0
            finally:
                self._ser.close()
 
            if self.beep_on_connect:
                self._ser.open()
                self._ser.write(cmd_parser.parse('beep 1', self._msg_queue))
                self._ser.close()

            self._stop_flag.value = 0
            self._serial_process = multiprocessing.Process(target=_serial_process, args=(self._cmd_queue, self._msg_queue, self._ser, self._stop_flag, self.start_time, self._is_cli, ))
            self._serial_process.start()

            self.is_connected = True

            if self._is_cli: self._msg_queue.put("connected on port {}".format(self.port))
            
            return 1


    def connect_auto(self):
        """Connect automatically to an available satellite or groundstation"""

        if self.is_connected:
            if self._is_cli: 
                self._msg_queue.put("Error: already connected on port {}".format(self.port))
            else:
                raise SerialException("Error: already connected on port {}".format(self.port))
            return 0
        else:
            
            if self._is_cli: self._msg_queue.put("connecting...")
            
            # Set serial params and start connection
            self._ser.timeout = self.timeout
            self._ser.baudrate = self._BAUD_RATE
            
            satellites = []
            gs = []

            ports = self.list_ports()
            for port in ports:
                try:
                    self._ser.port = port
                    if self._ser.is_open == False:
                        try:
                            self._ser.open()
                        except SerialException as e:
                            if self._is_cli:
                                msg_queue.put(e)
                            else:
                                raise SerialException(e)
                            return 0
                    
                    for i in range(3):
                        self._ser.write(cmd_parser.parse('ping_local', self._msg_queue))
                        self._ser.read_until()

                    self._ser.write(cmd_parser.parse('ping_local', self._msg_queue)) 
                    syncword = self._ser.read_until(b'packet:')
                    if syncword[-7:] == b'packet:':
                        ping_local = bytearray(self._ser.read(7))
                        ping_local.extend(self._ser.read(ping_local[2] + 4)) 

                        if ping_local[:3] == b'\n\x03\x01' and ping_local[7] == 49 and math_utils.check_fnv(ping_local):
                            satellites.append(port)
                        elif ping_local[:3] == b'\n\x03\x01' and ping_local[7] == 48 and math_utils.check_fnv(ping_local):
                            gs.append(port)
                    if self._ser.in_waiting:
                        self._ser.read_until()

                except IndexError:
                    pass
                finally:
                    self._ser.close()

            if self._is_cli: 
                self._msg_queue.put('---')
                self._msg_queue.put('found the following satellites: ')
                for sat in satellites:
                    self._msg_queue.put(sat)

            if self._is_cli: 
                self._msg_queue.put('found the following groundstations: ')
                for s in gs:
                    self._msg_queue.put(s)

            if not satellites == []:
                self.port = satellites[0]
                self._ser.port = self.port

                # Start the communication loop in a separate process
                self._stop_flag.value = 0
                self._serial_process = multiprocessing.Process(target=_serial_process, args=(self._cmd_queue, self._msg_queue, self._ser, self._stop_flag, self.start_time, self._is_cli,))
                self._serial_process.start()

                self.is_connected = True
                
                if self._is_cli: 
                    self._msg_queue.put("---")
                    self._msg_queue.put("connected on port {}".format(self.port))
                
                if self.beep_on_connect:
                    # Make satellite beep on succesful connect
                    self._ser.open()
                    self._ser.write(cmd_parser.parse('beep 1'))
                    self._ser.close()

                return 1
            
            elif not gs == []:
                self.port = gs[0]
                self._ser.port = self.port
                
                # Start the communication loop in a separate process
                self._stop_flag.value = 0
                self._serial_process = multiprocessing.Process(target=_serial_process, args=(self._cmd_queue, self._msg_queue, self._ser, self._stop_flag, self.start_time, self._is_cli,))
                self._serial_process.start()

                self.is_connected = True
                
                if self._is_cli: self._msg_queue.put("connected on port {}".format(self.port))

                return 1

            else:
                if self._is_cli: 
                    self._msg_queue.put('connection failed')
                    self._msg_queue.put('if you do have a satellite or gs connected, reseting or turning it off and on again might help')
                return 0


    def disconnect(self):
        """Disconnect from satellite or groundstation"""

        if self.is_connected:
            self.is_connected = False
            self._stop_flag.value = 1
            
            # End communication loop so serial port can be opened in this process on next call to connect
            self._serial_process.join()
            if self._is_cli: self._msg_queue.put("disconnected port {}".format(self.port))
        else:
            if self._is_cli: self._msg_queue.put("already disconnected")

    
    def write(self, cmd, timeout = None):
        """Parse command and put it into output queue"""
       
        if timeout == None: timeout = self.timeout

        if cmd[:16] == 'cam_download_pic':
            _download_pic(ser, _msg_queue, stop_flag, int(cmd.split()[1]), start_time, _is_cli)
        else:
            self._cmd_queue.put(cmd_parser.parse(cmd), True, timeout)

    def writeraw(self, cmd, timeout = None):
        """Write manually parsed command into output queue"""

        if timeout == None: timeout = self.timeout
        self._cmd_queue.put(cmd, True, timeout)


    def read(self, timeout = None):
        """Read next msg from msg queue"""

        if timeout == None: timeout = self.timeout
        return self._msg_queue.get(True, timeout)


    def in_waiting(self):
        """Return whether msg queue is empty or not"""

        return self._msg_queue.qsize()


    def list_ports(self):
        """List available serial ports"""

        ports_ = list_ports.comports()
        self.ports = []
        for port in ports_:
            self.ports.append(port.device)
        return self.ports
