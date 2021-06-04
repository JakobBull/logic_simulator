#!/usr/bin/env python3
"""Parse command line options and arguments for the Logic Simulator.

This script parses options and arguments specified on the command line, and
runs either the command line user interface or the graphical user interface.

Usage
-----
Show help: logsim.py -h
Command line user interface: logsim.py -c <file path>
Graphical user interface: logsim.py <file path>
"""
import getopt
import gui
import sys

import wx
import io

from names import Names
from devices import Devices
from network import Network
from monitors import Monitors
from scanner import Scanner
from parse import Parser
from userint import UserInterface
from gui import Gui


def main(arg_list):
    """
    Parse the command line options and arguments specified in arg_list.

    Run either the command line user interface, the graphical user interface,
    or display the usage message.
    """

    usage_message = ("Usage:\n"
                     "Show help: logsim.py -h\n"
                     "Command line user interface: logsim.py -c <file path>\n"
                     "Graphical user interface: logsim.py <file path>")
    try:
        options, arguments = getopt.getopt(arg_list, "hc:")
    except getopt.GetoptError:
        print("Error: invalid command line arguments\n")
        print(usage_message)
        sys.exit()


    for option, path in options:
        print("option is", option, "path is", path)
        if option == "-h":  # print the usage message
            print(usage_message)
            sys.exit()
        elif option == "-c":  # use the command line user interface
            # Initialise instances of the four inner simulator classes
            names = Names()
            devices = Devices(names)
            network = Network(names, devices)
            monitors = Monitors(names, devices, network)
            try:
                """Open and return the file specified by path for reading"""
                with open(path) as f:
                    content = f.readlines()
                file = "".join(content)
            except IOError:
                print("error, can't find or open file")
                sys.exit()
            file = io.StringIO(file)
            scanner = Scanner(path, file, names)
            parser = Parser(names, devices, network, monitors, scanner)
            if parser.parse_network():
                # Initialise an instance of the userint.UserInterface() class
                userint = UserInterface(names, devices, network, monitors)
                userint.command_interface()
    
    if not options:  # no option given, use the graphical user interface
        
        """Call main loop.

        Call the gui FrameManager to handle all operation.
        """
        gui.FrameManager("Logic Simulator")

if __name__ == "__main__":
    main(sys.argv[1:])
