#!/usr/bin/env python
#
# Class for the command line interface
#
# This file is part of kitsat-python. https://github.com/netnspace/Kitsat-Python-Library
# (C) 2020 Tuomas Simula <tuomas@simu.la>
# Maintained by Tessa Nikander <tessa@kitsat.fi>
#
#SPDX-License-Identifier:   GPL-3.0-or-later

import multiprocessing
import sys
import threading
from time import sleep

from blessed import Terminal
from serial.serialutil import SerialException
from serial.tools import list_ports

import importlib.resources as pkg_resources

from kitsat.lib import modem


class Cli:
    """
    A class for the CLI, handling terminal IO
    """
 
    def __init__ (self):
        if sys.version_info >= (3, 9):
            self.path_to_sat_cmd_csv = pkg_resources.files('kitsat.cfg') / 'sat_commands.csv'
            self.path_to_cli_cmd_csv = pkg_resources.files('kitsat.cfg') / 'cli_commands.csv'
        else:
            with pkg_resources.path('kitsat.cfg', 'sat_commands.csv') as p:
                self.path_to_sat_cmd_csv = p
            with pkg_resources.path('kitsat.cfg', 'cli_commands.csv') as q:
                self.path_to_cli_cmd_csv = q

        self.terminal = Terminal()

        self.input_prefix = '>>> '
        print(self.input_prefix, end='')

        # Event to signal input and output threads to end
        self.stop_event = threading.Event()

        # Modem object, does all the communtication to satellite
        self.conn = modem.Modem(_is_cli = True, beep_on_connect = True)

        # Start loop to listen for input in another thread
        input_listener = threading.Thread(target=self.input_listener)
        input_listener.start()
        
        # Start loop to print output in another thread
        output_listener = threading.Thread(target=self.output_listener)
        output_listener.start()

        # Message to explain the CLI shortly
        self.help_msg = """   \nKitSat CLI: a CLI for communicating with the KitSat educational satellite\n\nConnect to satellite or groundstation with "connect {port}" or "connect_auto"\nList available ports with "list_ports"\nSee this message with "help" and list of commands with "list_commands"\nExit the CLI with "exit" or "quit"\n"""
        self.write(self.help_msg)

        self.get_ports() 


    def exit_program (self):
        """Exit program gracefully"""

        self.write("exiting...")
        print('\r', end='')

        self.conn.disconnect()

        # Set stop flag to signal all threads to stop
        self.stop_event.set()  


    def input_listener (self):
        """Threaded loop for listening to user input"""

        # List all commands for satellite and CLI
        sat_commands = set()
        sat_commands_help = []
        cli_commands = []

        # Max command length: store length of longest string in each column
        mcl = [0, 0]

        # Get all commands from sat_commands.csv
        with self.path_to_sat_cmd_csv.open() as f:
            satcmd_csv = f.read().splitlines()
            satcmd_csv = satcmd_csv[1:]
            for row in satcmd_csv:
                row = row.split(',', 5)
                sat_commands.add(row[0])
                sat_commands_help.append([row[0], row[4], row[5]])

                mcl[0] = max(mcl[0], len(row[0]))
                mcl[1] = max(mcl[1], len(row[4]))
            

        # Get all commands from cli_commands.csv
        with self.path_to_cli_cmd_csv.open() as f:
            clicmd_csv = f.read().splitlines()
            clicmd_csv = clicmd_csv[1:]
            for row in clicmd_csv:
                row = row.split(',', 3)
                cli_commands.append([row[0], row[2], row[3]])

                mcl[0] = max(mcl[0], len(row[0]))
                mcl[1] = max(mcl[1], len(row[2]))

        mcl[0] += 3
        mcl[1] += 3

        # Actual input loop
        while not self.stop_event.is_set():

            # Get input
            cmd = input()
            self.write(self.terminal.move_up() + '{}{}'.format(self.input_prefix, cmd))
            
            # Huge if/elif/else structure to determine what to do with the input
            if cmd.split() == []:
                pass

            elif cmd == 'exit' or cmd =='quit':
                self.exit_program()

            elif cmd.split()[0] == 'connect':
                try:
                    port = cmd.split()[1]
                except (IndexError) as e:
                    self.write('Error: port not specified, try "connect {port}" or "connect_auto"')
                else: 
                    try:
                        self.conn.connect(port)
                    except SerialException as e:
                        self.write("Error: could not open port {}, try another port".format(port))
            
            elif cmd == 'connect_auto':
                self.conn.connect_auto()

            elif cmd == 'disconnect':
                self.conn.disconnect()

            elif cmd == 'beep_on_connect':
                self.conn.beep_on_connect = not self.conn.beep_on_connect
                self.write('beep_on_connect set to {}'.format(self.conn.beep_on_connect))

            elif cmd.split()[0] == 'help':
                try:
                    found = False
                    for row in cli_commands:
                        if cmd.split()[1] == row[0]:
                            found = True
                            self.write(row[1])
                            if not row[2] == '':
                                self.write('Parameters: {}'.format(row[2]))
                    for row in sat_commands_help:
                        if cmd.split()[1] == row[0]:
                            found = True
                            self.write(row[1])
                            if not row[2] == '':
                                self.write('Parameters: {}'.format(row[2]))
                    if not found:
                        self.write("Cannot display help message for unknown command {}".format(smd.split()[0]))
                except IndexError:
                    self.write(self.help_msg)
            
            elif cmd == 'list_commands':
                for row in cli_commands:
                    cmd_str = "{}:".format(row[0]) + self.terminal.move_x(mcl[0]) + "{}".format(row[1])
                    if not row[2] == '':
                        cmd_str = cmd_str + self.terminal.move_x(mcl[0] + mcl[1]) + "Parameters: {}".format(row[2])
                    self.write(cmd_str)
                for row in sat_commands_help:
                    cmd_str = "{}:".format(row[0]) + self.terminal.move_x(mcl[0]) + "{}".format(row[1])
                    if not row[2] == '':
                        cmd_str = cmd_str + self.terminal.move_x(mcl[0] + mcl[1]) + "Parameters: {}".format(row[2])
                    self.write(cmd_str)
            
            elif cmd == 'list_ports':
                self.get_ports()
            
            elif cmd == 'port_in_use':
                self.write(self.conn.port)
            
            elif cmd[:11] == 'set_timeout':
                try: 
                    self.conn.timeout = float(cmd.split()[1])
                except ValueError:
                    self.write("Error: {} is not a valid number".format(cmd.split()[1]))
                except IndexError:
                    self.write("Error: timeout value not specified")
            
            elif cmd.split()[0] == 'cam_download_pic':
                try:
                    int(cmd.split()[1])
                except (ValueError, IndexError) as e:
                    self.write(e)
                else:
                    self.conn.write(cmd)
            
            elif cmd.split()[0] in sat_commands:
                self.conn.write(cmd)
            
            else:
                self.write("unknown command")
            
            sleep(0.001)

    
    def output_listener (self):
        """Threaded loop for printing output from KitSat modem"""
        
        while not self.stop_event.is_set():
            if self.conn.in_waiting():
                output = self.conn.read()
                if type(output) == list:
                    self.write("{}: Received {} from {}, {}".format(output[3], output[4], output[0], output[1]))
                else:
                    self.write(output)
            sleep(0.001)


    def write (self, *msgs, delimiter=" "):
        """Print data to terminal in a nice-looking way"""

        msg_str = ""
        for msg in msgs:
            msg_str += str(msg) + delimiter
        print(self.terminal.move_x(0) + "{}\n{}".format(msg_str, self.input_prefix), end='')


    def get_ports (self):
        """List all available serial ports"""

        self.write("Available ports:")
        ports = self.conn.list_ports()
        for i, port in enumerate(ports):
            self.write(' ', i, ': ', port, delimiter="")
        self.write('Connect with "connect {index}" or "connect {port name}"')


def main ():
    """Function for running the cli"""

    multiprocessing.set_start_method('spawn')
    cli = Cli()


# Start program, if this file is run directly from terminal
if __name__ == '__main__':
   main()
