#!/usr/bin/env python3
"""Preliminary exercises for Part IIA Project GF2."""
import sys
import os
from mynames import MyNames


def open_file(path):
    try:
        """Open and return the file specified by path for reading"""
        return open(path, "r", encoding="utf-8")
    except IOError:
        print("error, can't find or open file")
        sys.exit()


def get_next_character(input_file):
    """Read and return the next character in input_file."""
    char = input_file.read(1)
    if char is None: return ""
    else: return char


def get_next_non_whitespace_character(input_file):
    """Seek and return the next non-whitespace character in input_file."""
    #don't know why this doesn't work
    #i = 1
    #while (char := get_next_character(input_file)).isspace():
    #        input_file.seek(i)
    #        i+=1
    #return char
    while True:
        char = input_file.read(1)
        if char.isspace(): pass
        else: break
    return char


def get_next_number(input_file):
    """Seek the next number in input_file.

    Return the number (or None) and the next non-numeric character.
    """
    number = ""
    while True:
        char = input_file.read(1)
        if char.isdigit():
            number += char
        else: break
    return (char,number)


    """
    #search till first digit
    while not (char := get_next_character(input_file)).isdigit():
        input_file.seek(i)
            i+=1
            input_file.seek(i)
        elif char == '': return [None, ""]
    number = number + char
    return number


    #store string of digits in number
    while (char := get_next_character(input_file)).isdigit():
        number = number + char
        i += 1
        input_file.seek(i)
    next_non_digit = char
    return [number, next_non_digit]

    #store string of digits in number
    while (char := get_next_character(input_file)).isdigit():
        number = number + char
        i += 1
        input_file.seek(i)
    next_non_digit = char
    return [number, next_non_digit]
    """

def get_next_name(input_file):
    """Seek the next name string in input_file.

    Return the name string (or None) and the next non-alphanumeric character.
    """
    name =""
    #find star character
    char = get_next_non_whitespace_character(input_file)
    if char.isalpha():
        name += char
        while True:
            char = input_file.read(1)
            if not char.isalnum(): break
            else: name+=char
    return (char,name)



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
        print(path)    #print path
        fo = open_file(path) #open file

        print("\nNow reading file...")
        # Print out all the characters in the file, until the end of file

        #This seems like a simpler way than using the get_next_character function
        #for line in fo:
        #    for char in line:
        #        print(char, end = '')
        # := assigns variables in expressions

        i = 1
        fo.seek(0)
        while (char := get_next_character(fo)) != "":
            print(char, end = '')
            fo.seek(i)
            i+=1

        print("\nNow skipping spaces...")
        # Print out all the characters in the file, without spaces
        #i = 1
        #fo.seek(0)
        #while not (char := get_next_non_whitespace_character(fo)) == "":
        #    print(char, end = '')
        #    fo.seek(i)
        #    i+=1

        fo.seek(0)
        while True:
            char = get_next_non_whitespace_character(fo)
            print(char, end = '')
            if char == "":
                break

        print("\nNow reading numbers...")
        # Print out all the numbers in the file
        fo.seek(0)
        while True:
            char,number = get_next_number(fo)
            if number != "": print(number, end = ' ')
            if char == "":
                break

        print("\nNow reading names...")
        # Print out all the names in the file
        fo.seek(0)
        while True:
            char,name = get_next_name(fo)
            if name != "": print(name)
            if char == '': break


        print("\nNow censoring bad names...")
        # Print out only the good names in the file
        name = MyNames()
        bad_name_ids = [name.lookup("Terrible"), name.lookup("Horrid"),
                         name.lookup("Ghastly"), name.lookup("Awful")]

        fo.seek(0)
        while True:
            char,nam = get_next_name(fo)

            if name.lookup(nam) != None: pass
            elif nam != "": print(nam)
            if char == '': break

if __name__ == "__main__":
    main()
