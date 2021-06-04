"""Deals with language errors.

Used in logsim to to call errors and print the line that causes the error
and a ^ to indicate where on the line the error occurs

Classes
-------
Error - creates errors and can print them.
"""
from scanner import Symbol
import sys
import os
import math


class Error:
    """Creates errors and prints them.

    This class contains the definition of an error, along with functions
    to print out the error output.

    many functions required for connecting devices together
    in the network, getting information about connections, and executing all
    the devices in the network.

    Parameters
    ----------
    error_message - list of all error types we test where index is error type.

    further inforamation here:
    https://docs.google.com/document/d/15lmjiRRd2pbk0f8T2uEusgCI
    7VyCCcWidIlgw62IdSo/edit?usp=sharing

    num_errors - count of total number of errors

    type[] - list of all error types that have occured

    symbols[] - list of symbols that have thrown errors

    Public methods
    --------------
    def print_error(cls, scanner): prints the error output for called errors

    def gui_report_error(cls, path): prints errors for GUI

    def get_lines(cls, scanner): Open and returns the file from scanner
    """

    num_errors = 0
    types = []
    symbols = []

    error_message = (
        "Headings called in wrong order",
        "Always need to follow a heading with {",
        "DEVICE: Name of device must contain a letter",
        "DEVICE: Name for device already used",
        "DEVICE: Expected symbol is an =",
        "DEVICE: Device type not found",
        "DEVICE: Word inputs required",
        "DEVICE: Invalid number of inputs",
        "DEVICE: Word halfperiod required",
        "DEVICE: Invalid halfperiod",
        "CONNECTION: Device not defined",
        "CONNECTION: No - found to define connection",
        "CONNECTION: No . found",
        "CONNECTION: Input not initialised",
        "CONNECTION: Input already defined",
        "Error creating connection",
        "D type output denoted by a .",
        "Not a valid D type output",
        "SIGNALS: Device not defined",
        "SIGNALS: = sign expected",
        "SIGNALS: Signal can only be set to 1 or 0",
        "SIGNALS: Integer number required",
        "SIGNALS: Expected ; to end line",
        "MONITOR: No devices monitored",
        "MONITOR: Device not defined",
        "MONITOR: Output not properly defined",
        "MONITOR: Device already monitored",
        "MONITOR: Expected ; to end line"
    )

    @classmethod
    def __init__(cls, type, symbol):
        """Create error. adds type and symbol string, increases num_errors."""
        # error type, number from list of error document
        cls.types.append(type)
        cls.symbols.append(symbol)
        cls.num_errors += 1
        # symbol that causes the error everytime an error called,
        # number of errors increased

    @classmethod
    def print_error(cls, scanner):
        """Print errors for terminal output."""
        lines = cls.get_lines(scanner)
        print(str(cls.num_errors) + " ERRORS!:\n")
        for i in range(cls.num_errors):
            print("Error " + str(i) + ":")
            line = lines[cls.symbols[i].line_number - 1]
            start_spaces = 0
            for c in line:
                if c.isspace():
                    start_spaces += 1
                else:
                    break
            start = cls.symbols[i].start_char_number
            end = cls.symbols[i].end_char_number
            print("\"" + line.strip() + "\"")
            cursor = cls.symbols[i].start_char_number - start_spaces
            for n in range(cursor):
                print(' ', end='')
            print("^")
            print(cls.error_message[cls.types[i]])
            # for n in range(len(Error.error_message[Error.types[i]])):
            # print('-', end = '')
            for n in range(8):
                print('-', end='')
            print("")

    @classmethod
    def gui_report_error(cls, path):
        """Return error output as a string for gui."""
        print("GUI reporting errrors")
        error_string = ""
        lines = cls.get_lines(path)
        #error_string += str(str(cls.num_errors) + " ERRORS!:\n")
        error_string += "1 ERROR!: \n"
        error_string += "\n"
        #for i in range(cls.num_errors):
        i = 0
        error_string += str("Error " + str(i+1) + ":")
        error_string += "\n"
        line = lines[cls.symbols[i].line_number - 1]
        start_spaces = 0
        for c in line:
            if c.isspace():
                start_spaces += 1
            else:
                break
        start = cls.symbols[i].start_char_number
        end = cls.symbols[i].end_char_number
        error_string += str("\"" + line.strip() + "\"")
        error_string += "\n"
        cursor = cls.symbols[i].start_char_number - start_spaces
        print("Cursor adding", cursor, "spaces")
        for _ in range(cursor):
            error_string += ' '
        error_string += str("^")
        error_string += "\n"
        error_string += str(cls.error_message[cls.types[i]])
        # for n in range(len(Error.error_message[Error.types[i]])):
        #    print('-', end = '')
        error_string += "\n"
        for _ in range(8):
            error_string += str('-')
        error_string += "\n"
        error_string += ""
        return error_string

    @classmethod
    def get_lines(cls, scanner):
        """Open and return the file specified by path for reading."""
        try:
            file = open(scanner.path, "r", encoding="utf-8")
            lines = file.readlines()
            return lines
        except IOError:
            print("error, can't find or open file")
            sys.exit()
