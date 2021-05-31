from scanner import Symbol
from scanner import Scanner
from names import Names
from parse import Parser


import pytest
import sys
import os

def test_headings_order():
    scan = Scanner("parse_test_files/test_headings.txt", Names())
    parse = Parser(Names(), scan)
    parse.parse_network()
    assert SyntaxError("Headings called in wrong order")
