import sys

def printChar(c: chr):
    if type(c) != chr:
        return sys.exit("Function can only take char (chr) value")
    print(c,end='')