"""Read the circuit definition file and translate the characters into symbols.

Used in the Logic Simulator project to read the characters in the definition
file and translate them into symbols that are usable by the parser.

Classes
-------
Scanner - reads definition file and translates characters into symbols.
Symbol - encapsulates a symbol and stores its properties.
"""
import sys
import os
from userint import UserInterface

class Symbol:

    """Encapsulate a symbol and store its properties.

    Parameters
    ----------
    No parameters.

    Public methods
    --------------
    No public methods.
    """

    def __init__(self):
        """Initialise symbol properties."""
        self.type = None
        self.id = None      #number if symbol is a number
        # extended to include symbol's line and character number
        self.line_number = None
        self.start_char_number = None
        self.end_char_number = None
        self.string = None


class Scanner:

    """Read circuit definition file and translate the characters into symbols.

    Once supplied with the path to a valid definition file, the scanner
    translates the sequence of characters in the definition file into symbols
    that the parser can use. It also skips over comments and irrelevant
    formatting characters, such as spaces and line breaks.

    Parameters
    ----------
    path: path to the circuit definition file.
    names: instance of the names.Names() class.

    Public methods
    -------------
    get_symbol(self): Translates the next sequence of characters into a symbol
                      and returns the symbol.
    """
    def __init__(self, path, names):
        """"Open specified file and initialise reserved words and IDs."""
        # opens specified file
        try:
            """Open and return the file specified by path for reading"""
            self.file =  open(path, "r", encoding="utf-8")
        except IOError:
                print("error, can't find or open file")
                sys.exit()
        # initialises reserved words and IDs
        self.names = names
        self.symbol_type_list = [self.COMMA, self.SEMICOLON, self.EQUALS,
            self.KEYWORD, self.NUMBER, self.NAME, self.EOF] = range(7)
        self.keywords_list = ["DEVICES", "CONNECT", "MONITOR", "END"]
        [self.DEVICES_ID, self.CONNECT_ID, self.MONITOR_ID,
            self.END_ID] = self.names.lookup(self.keywords_list)

        #initialise current character to be first character
        char = self.file.read(1)
        self.current_character = char

        self.current_line_number = 1;
        self.current_char_number = 0;

    def get_symbol(self):
        """Translate the next sequence of characters into a symbol."""
        symbol = Symbol()
        self.skip_spaces()  # current character now not whitespace
        symbol.line_number = self.current_line_number
        symbol.start_char_number = self.current_char_number
        if self.current_character.isalpha():  # name
            name_string = self.get_name()
            symbol.string = name_string
            if name_string in self.keywords_list:
                symbol.type = self.KEYWORD
            else:
                symbol.type = self.NAME
            [symbol.id] = self.names.lookup([name_string])
        elif self.current_character.isdigit():  # number
            symbol.id = self.get_number()
            symbol.type = self.NUMBER
        elif self.current_character == "=":  # punctuation
            symbol.type = self.EQUALS
            self.advance()
        elif self.current_character == ",":
            symbol.type = self.COMMA
            self.advance()
        elif self.current_character == ";":
            symbol.type = self.SEMICOLON
            self.advance()
        elif self.current_character == "":  # end of file
            symbol.type = self.EOF
        else:  # not a valid character
            self.advance()
        symbol.end_char_number = self.current_char_number
        return symbol

    def advance(self):  #Need to advance once to get to fist character of file!
        # advance: reads the next character from the definition file
        # and places it in current_character
        char = self.file.read(1)
        self.current_character = char
        if(self.current_character == '\n'):
            self.current_line_number += 1
            self.current_char_number = 1
        else:
            self.current_char_number += 1

    def skip_spaces(self):
        # skip_spaces: calls advance as necessary until current_character
        # is not whitespace
        """Skip whitespace until a non-whitespace character is reached."""
        #
        while self.current_character.isspace():
            self.advance()

    def get_name(self):
        """similar to get_next_name in the preliminary exercises,
        except that it now assumes the current character is a letter,
        returns only the name string and places the next non-alphanumeric
        character in current_character """

        """get_next_name: Seek the next name string in input_file.
        Return the name string (or None) and the next non-alphanumeric character.
        """
        name = ""
        name += self.current_character
        while True:
            self.advance()
            if not self.current_character.isalnum():
                #self.current_character = char
                break
            else: name+=self.current_character
        return name

    def get_number(self):
        """assumes the current character is a digit,
        returns the integernumber and places the next
        non-digit character in current_character"""
        #should number be able to start with a 0?
        integernumber = ""
        integernumber += self.current_character
        while True:
            self.advance()
            if self.current_character.isdigit():
                integernumber += self.current_character
            else:
                break
        return integernumber
