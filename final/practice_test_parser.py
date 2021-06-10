from names import Names
from devices import Devices
from network import Network
from monitors import Monitors
from parse import Parser
from scanner import Symbol
from scanner import Scanner
from error import Error

import sys
import os


def open_file(path):
    try:
        """Open and return the file specified by path for reading"""
        return open(path, "r", encoding="utf-8")
    except IOError:
        print("error, can't find or open file")
        sys.exit()

def main():
    """Preliminary exercises for Part IIA Project GF2."""

    # Check command line arguments
    arguments = sys.argv[1:]
    if len(arguments) != 1:
        print("Error! One command line argument is required.")
        sys.exit()

    else:
        print("\nNow opening file...")
        # Print the path provided and try to open the file for reading
        path = os.getcwd()+ "/" + arguments[0]
        print(path)    #print path
        names = Names()
        devices = Devices(names)
        network = Network(names, devices)
        monitors = Monitors(names, devices, network)
        scanner = Scanner(path, names)
        parser = Parser(names, devices, network, monitors, scanner)
        Error.reset()
        parser.parse_network()

if __name__ == "__main__":
    main()
