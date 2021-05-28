from scanner import Symbol
from scanner import Scanner
from names import Names

scan = Scanner("scanner_test_files/scanner_test_line.txt", Names())
print("type\tid\tline#\tstart_char#\tend_char#\tstring")
for i in range(20):
    symbol = scan.get_symbol()
    print(symbol.type, end = "\t")
    print(symbol.id, end = "\t")
    print(symbol.line_number, end = "\t")
    print(symbol.start_char_number, end = "\t\t")
    print(symbol.end_char_number, end = "\t\t")
    print(symbol.string)
    if(symbol.type == scan.EOF): break
