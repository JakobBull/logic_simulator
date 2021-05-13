#!/usr/bin/env python3
"""Preliminary exercises for Part IIA Project GF2."""
import sys
import os

def open_file(path):
    """Open and return the file specified by path."""
    try:
        fo = open(path, "r")
        return fo
    except IOError:
        print('Error, file cannot be opened')
        sys.exit()
    #print(fo.name)



def get_next_character(input_file):
    """Read and return the next character in input_file."""
    str = input_file.read(1)
    return str


def get_next_non_whitespace_character(input_file):
    """Seek and return the next non-whitespace character in input_file."""
    fo = input_file
    str = fo.read(1)
    pos = input_file.tell()
    while str.isspace() == True:
        
        fo.seek(pos)
        str = fo.read(1)
        pos += 1

    return str
    
        
    


def get_next_number(input_file):
    """Seek the next number in input_file.

    Return the number (or None) and the next non-numeric character.
    """


def get_next_name(input_file):
    """Seek the next name string in input_file.

    Return the name string (or None) and the next non-alphanumeric character.
    """


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
        path = os.path.abspath(sys.argv[1])
        print(path)
        text = open_file(path)

        print("\nNow reading file...")
        # Print out all the characters in the file, until the end of file
        x = 'hi'
        while x != "":
            x = get_next_character(text)
            print(x, end='')
        
        text.seek(0, 0)

        print("\nNow skipping spaces...")
        # Print out all the characters in the file, without spaces
        x = 'hi'
        while x != "":
            x = get_next_non_whitespace_character(text)
            print(x, end='')

        print("\nNow reading numbers...")
        # Print out all the numbers in the file

        print("\nNow reading names...")
        # Print out all the names in the file

        print("\nNow censoring bad names...")
        # Print out only the good names in the file
        # name = MyNames()
        # bad_name_ids = [name.lookup("Terrible"), name.lookup("Horrid"),
        #                 name.lookup("Ghastly"), name.lookup("Awful")]

if __name__ == "__main__":
    main()
