from scanner import Symbol
from scanner import Scanner
from names import Names
import pytest

def test_advance():
    scan = Scanner("scanner_test_files/test_advance.txt", Names())
    assert(scan.current_character == 'a')
    scan.advance()
    assert(scan.current_character == 'b')
    scan.advance()
    assert(scan.current_character == 'c')

def test_skip_spaces():
    scan = Scanner("scanner_test_files/test_skip_spaces.txt", Names())
    assert(scan.current_character == 'a')
    scan.advance()  #move forward to whitespace
    scan.skip_spaces()
    assert(scan.current_character == 'h')   #just spaces
    scan.advance()  ##move forward to whitespace
    scan.skip_spaces()
    assert(scan.current_character == 'b')   #tabs aswell

def test_get_name():
    scan1 = Scanner("scanner_test_files/test_get_name1.txt", Names())
    assert(scan1.get_name() == "hello")
    scan2 = Scanner("scanner_test_files/test_get_name2.txt", Names())
    assert(scan2.get_name() == "bye")

def test_get_number():
    scan1 = Scanner("scanner_test_files/test_get_number1.txt", Names())
    assert(scan1.get_name() == "123")
    scan2 = Scanner("scanner_test_files/test_get_number2.txt", Names())
    assert(scan2.get_name() == "0900")

def test_scanner():
    scan = Scanner("scanner_test_files/scanner_test_line.txt", Names())
    assert(scan.get_symbol().type == scan.KEYWORD)
    assert(scan.get_symbol().type == scan.NUMBER)
    assert(scan.get_symbol().type == scan.NAME)
    assert(scan.get_symbol().type == scan.EQUALS)
    assert(scan.get_symbol().type == scan.NAME)
    assert(scan.get_symbol().type == scan.KEYWORD)
    #scan.skip_spaces()
    #assert(scan.get_name() == "END")
    assert(scan.get_symbol().type == scan.KEYWORD)
    assert(scan.get_symbol().type == scan.SEMICOLON)
