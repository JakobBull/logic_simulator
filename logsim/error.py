from scanner import Symbol
from scanner import Scanner
import sys
import os
import math

class Error:
    num_errors = 0
    types = []
    symbols = []

    error_message = {
        0: "!error0!",
        1: "!error1!",
        2: "!error2!"
    }
    def __init__(self, type, symbol):
        Error.types.append(type)        # error type, number from list of error document
        Error.symbols.append(symbol)    # symbol that causes the error
        Error.num_errors += 1           # everytime an error called, number of errors increased
    def print_error(scan,path):
        lines = Error.get_lines(path)
        for i in range(Error.num_errors):
            line = lines[Error.symbols[i].line_number-1]
            start_spaces = 0
            for c in line:
                if c.isspace():
                    start_spaces+=1
                else: break
            start = Error.symbols[i].start_char_number
            end = Error.symbols[i].end_char_number
            print(line.strip())
            cursor = Error.symbols[i].start_char_number-1-start_spaces
            for n in range(cursor):
                print(' ', end = '')
            print("^")
            print(Error.error_message.get(Error.types[i]))
    def get_lines(path):
        try:
            """Open and return the file specified by path for reading"""
            file = open(path, "r", encoding="utf-8")
            lines = file.readlines()
            return lines
        except IOError:
            print("error, can't find or open file")
            sys.exit()
