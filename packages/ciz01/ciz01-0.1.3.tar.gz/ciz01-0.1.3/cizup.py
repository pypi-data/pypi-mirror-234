import sys

def printChar(c: str):
    if len(str)!=1:
        return sys.exit("Function can only take char (chr) value. The paremeter is not be big 1. \n For example: \n cizup.printChar('c')")
    print(c,end='')