from names import Names
from devices import Devices
from network import Network
from monitors import Monitors
from parse import Parser
from scanner import Symbol
from scanner import Scanner
from error import Error

import pytest
import sys
import os

def test_device_list():
    path = "parse_test_files/test_device_list.txt"
    expected_errors = [
        # [1,"SW1",5,5], opencurly called before device_list, not in device_list
        [2,"912"],
        [3,"SW1"],
        [4,"-"]
    ]
    names = Names()
    devices = Devices(names)
    network = Network(names, devices)
    monitors = Monitors(names, devices, network)
    scanner = Scanner(path, names)
    parser = Parser(names, devices, network, monitors, scanner)
    Error.reset()
    parser.device_list()
    print(Error.gui_report_error(scanner))
    for i in range(len(expected_errors)):
        error = expected_errors[i] # the list for the ith error from expected_errors
        # make sure error types stored in error class align with those expected
        # by expected_errors
        assert Error.types[i] == error[0] , str(i+1) + "/" + \
        str(len(expected_errors)) + " error #" + str(i) + " on line " + \
        str(Error.symbols[i].line_number) + " caused by symbol \"" + \
        Error.symbols[i].string + "\"" \
        + " has error type " + str(Error.types[i]) + ", should be "+  str(error[0])
        assert Error.symbols[i].string == error[1]

@pytest.mark.parametrize(
    "file, expected_errors",
    # expected_errors, list of list of properties for each error that should occur
    # each error will take a list of the form:
    # error_type, symbol_string_that_caused_error, line_number, start_char_number
    # can determine line_number and start_char_number from text editor like
    # atom/vs code for writing tests. Usually at the bottom in the form:
    # line# : char#
    [
        ("no_errors", []),
        (
            "test_1",
            [
                [0,"CONNECTIONS"]
            ]
        ),
        (
            "test_2",
            [
                [7,"0"],
                [6,"2"],
                [22,"222"],
                [28,"G3"]
            ]
        ),
        (
            "test_3",
            [
                [8,"2"],
                [9,"0"],
                [11,"G1Q"],
                [16,"I5"]
            ]
        ),
        (
            "test_4",
            [
                [2,"912"],
                [4,"-"],
                [14,"1"],
                [16,"1"],
                [11,"G2I2"],
                [11,"G22"],
                [16,"I2"],
                [20,"SW19"],
                [20,"SW2"],
                [26,"W2"]
            ]
        )

    ]
)
# tests if query returns correct name ID for a name sting
def test_error_detection(file, expected_errors):
    path = "parse_test_files/"
    path += file
    path += ".txt"

    names = Names()
    devices = Devices(names)
    network = Network(names, devices)
    monitors = Monitors(names, devices, network)
    scanner = Scanner(path, names)
    parser = Parser(names, devices, network, monitors, scanner)
    Error.reset()
    parser.parse_network()
    print("error types list" + str(Error.types))
    for i in range(len(expected_errors)):
        error = expected_errors[i] # the list for the ith error from expected_errors
        # make sure error types stored in error class align with those expected
        # by expected_errors
        assert Error.types[i] == error[0] , str(i) + "/" + \
        str(len(expected_errors)) + " error #" + str(i) + " on line " + \
        str(Error.symbols[i].line_number) + " caused by symbol \"" + \
        Error.symbols[i].string + "\"" \
        + " has error type " + str(Error.types[i]) + ", should be "+  str(error[0])

        assert Error.symbols[i].string == error[1]
