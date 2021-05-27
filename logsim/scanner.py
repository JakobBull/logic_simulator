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
        self.id = None
        # extended to include symbol's line and character number
        self.line_number = None
        self.char_number = None


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
        self.current_character = ""

    def get_symbol(self):
        """Translate the next sequence of characters into a symbol."""
        symbol = Symbol()
        self.skip_spaces()  # current character now not whitespace
        if self.current_character.isalpha():  # name
            name_string = self.get_name()
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
        return symbol

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
            char = self.get_character()
            if not char.isalnum():
                self.current_character = char
                break
            else: name+=char
        return name

    def get_number(self):
        """assumes the current character is a digit,
        returns the integernumber and places the next
        non-digit character in current_character"""
        #only expecting binary numbers
        integernumber = ""
        integernumber += self.current_character
        while True:
            self.current_character = self.get_character()
            if self.current_character.isdigit():
                integernumber += char
            else:
                break
        return integernumber

    def advance(self):
        """reads the next character from the definition file and places
        it in current_character skip_spaces: calls advance as necessary
        until current_character is not whitespace"""
        self.get_character()
        self.current_character = self.read_command()

    def skip_spaces(self):
        """Skip whitespace until a non-whitespace character is reached."""
        self.get_character()
        while self.current_character.isspace():
            self.get_character()

    def read_command(self):
        """Return the first non-whitespace character."""
        self.skip_spaces()
        return self.character

    def get_character(self):
        """Read and return the next character in input_file."""
        char = self.file.read(1)
        if char is None: return ""
        else: return char
