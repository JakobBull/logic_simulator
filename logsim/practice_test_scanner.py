from scanner import Symbol
from scanner import Scanner
from names import Names
import sys
import os

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
        scan = Scanner(path, Names())
        print("scanning from: scanner_test_files/scanner_test_line.txt")
        print("")
        print("type\tid\tline#\tstart_char#\tend_char#\tstring")
        while True:
            symbol = scan.get_symbol()
            print(symbol.type, end="\t")
            print(symbol.id, end="\t")
            print(symbol.line_number, end="\t")
            print(symbol.start_char_number, end="\t\t")
            print(symbol.end_char_number, end="\t\t")
            print(symbol.string)
            if(symbol.type == scan.EOF):
                break
