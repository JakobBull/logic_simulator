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

# tests scanner works on a single line
def test_scanner():
    scan = Scanner("scanner_test_files/scanner_test_line.txt", Names())
    assert(scan.get_symbol().type == scan.KEYWORD)
    assert(scan.get_symbol().type == scan.NUMBER)
    assert(scan.get_symbol().type == scan.NAME)
    assert(scan.get_symbol().type == scan.EQUALS)
    assert(scan.get_symbol().type == scan.NAME)
    assert(scan.get_symbol().type == scan.NAME)
    assert(scan.get_symbol().type == scan.SEMICOLON)
    assert(scan.get_symbol().type == scan.EOF)

# test that the scanner works on our example_1
def test_scanner_example_file():
    scan = Scanner("scanner_test_files/example_1.txt", Names())
    i = 0
    # order of symbol_type_list definition in scanner determines which
    # numbers mean which type as shown below

    # the symbol_type_list from scanner
    # self.symbol_type_list = [self.LEFT_BRACKET, self.RIGHT_BRACKET,
    # self.EQUALS, self.PERIOD, self.DASH, self.SEMICOLON, self.KEYWORD,
    # self.NUMBER, self.NAME, self.EOF] = range(10)

    # {         0
    # }         1
    # =         2
    # .         3
    # -         4
    # ;         5
    # KEYWORD   6
    # NUMEBR    7
    # NAME      8
    # EOF       9

    correct_type_list = [
        6,0,            # NETWORK{
        6,0,            #   DEVICES{
        8,2,6,5,        #       SW1 = SWITCH;
        8,2,6,5,        #       SW2 = SWITCH;
        8,2,6,5,        #       G1 = NAND;
        8,2,6,5,        #       G2 = NAND;
        1,              #   }
        6,0,            #   CONNECTIONS{
        8,4,8,3,8,5,    #       SW1 - G1.I1;
        8,4,8,3,8,5,    #       SW2 - G2.I2;
        8,4,8,3,8,5,    #       G1 - G2.I1;
        8,4,8,3,8,5,    #       G2 - G1.I2;
        1,              #   }
        6,0,            #   SIGNALS{
        6,0,            #       SETSIGNAL{
        8,2,7,6,7,5,    #           SW1 = 0 starttime 0;
        8,2,7,6,7,5,    #           SW2 = 0 starttime 0;
        1,              #       }
        6,0,1,          #       SETCLOCK{}
        1,              #   }
        6,0,            #   MONITOR{
        8,5,            #       G1;
        8,5,            #       G2;
        1,              #   }
        1,              # }
        9               # EOF
    ]
    while True:
        symbol = scan.get_symbol()
        assert(symbol.type == correct_type_list[i])
        print(i, end = "\t")
        print(correct_type_list[i], end = "\t")
        print(symbol.type)
        i+=1
        if(symbol.type == scan.EOF): break
