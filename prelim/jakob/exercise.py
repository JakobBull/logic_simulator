#!/usr/bin/env python3
"""Preliminary exercises for Part IIA Project GF2."""
import sys
import os

def open_file(path):

    try:
        f = open(path, "r")
        document = f.read()
        f.seek(0)
        return f

    except OSError:
        print("Error reading file {}".format(path))
        sys.exit()




def get_next_character(input_file):
    return input_file.read(1)
    

def get_next_non_whitespace_character(input_file):
    while True:
        character = input_file.read(1)
        if character.isspace():
            #print(character)
            pass
        else:
            return character



def get_next_number(input_file):
    while True:
        character = [input_file.read(1)]
        if character[0] == "":
            return [None, ""]

        if character[0].isdigit():
            while True:
                next_character = input_file.read(1)

                if next_character.isdigit():
                    character.append(next_character)
                else:
                    return [int("".join(character)), next_character]
        


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
        full_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), arguments[0])
        print("Path is {}".format(full_path))
        file = open_file(full_path)
                
        print("printing everything")        
        while True:
            character = get_next_character(file)

            if character == "":
                print("End of file reached")
                break
        
            print(character, end="")

        file.seek(0)

        print("printing non-white-spaces")  
        while True:
            character = get_next_non_whitespace_character(file)
        
            if character == "":
                print("\n End of file reached")
                break
            
            print(character, end = "")

        file.seek(0)

        print("printing numbers")  
        while True:
            character_list = get_next_number(file)
            if character_list[0] == None:
                print(" \n End of file reached")
                break
            
            print(character_list[0], end=", ")


        print("\nNow reading file...")
        # Print out all the characters in the file, until the end of file

        print("\nNow skipping spaces...")
        # Print out all the characters in the file, without spaces

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
