from scanner import Symbol
from scanner import Scanner
from names import Names
from parse import Parser


import pytest
import sys
import os

def test_working_spec():
    scan = Scanner("parse_test_files/test_working_spec.txt", Names())
    parse = Parser(Names(), scan)
    parse.parse_network()
    assert True


def test_headings_order():
    scan = Scanner("parse_test_files/test_headings.txt", Names())
    parse = Parser(Names(), scan)
    with pytest.raises(SyntaxError, match= "Headings called in wrong order"):
        parse.parse_network()
 
def test_OPENCURLY():
    scan = Scanner("parse_test_files/test_OPENCURLY.txt", Names())
    parse = Parser(Names(), scan)
    with pytest.raises(SyntaxError, match="Always need to follow a heading with {"):
        parse.parse_network()

def test_device_NAME():
    scan = Scanner("parse_test_files/test_device_NAME.txt", Names())
    parse = Parser(Names(), scan)
    with pytest.raises(SyntaxError, match= "Device: Name of device must contain a letter"):
        parse.parse_network()

def test_reused_name():
    scan = Scanner("parse_test_files/test_reused_NAME.txt", Names())
    parse = Parser(Names(), scan)
    with pytest.raises(SyntaxError, match="Device: Name for device already used"):
        parse.parse_network()




