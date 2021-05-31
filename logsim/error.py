from scanner import Symbol
from scanner import Scanner

class Error:
    num_errors = 0
    types = []
    symbols = []

    error_message = {
        0: "!error0!",
        1: "!error1!",
        2: "!error2!"
    }
    def __init__(self, type, symbol):
        Error.types.append(type)        # error type, number from list of error document
        Error.symbols.append(symbol)    # symbol that causes the error
        Error.num_errors += 1           # everytime an error called, number of errors increased
    def print_error(scan):
        #needs to be a new scanner
        for i in range(Error.num_errors):
            print("print line " + str(Error.symbols[i].line_number))
            for n in range(Error.symbols[i].line_number):
                print(' ', end = "")
            print("^")
            print(Error.error_message.get(Error.types[i]))
