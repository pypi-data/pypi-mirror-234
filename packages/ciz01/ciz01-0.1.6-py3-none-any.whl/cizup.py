import sys

def printChar(c):
    if type(c) == str or type(c) == chr:
        if len(str(c))!=1:
            return sys.exit("The length of the parameter cannot be greater than or less than one. \n For example: \n cizup.printChar('c')")
        return print(c,end='')
    elif  type(c) == int:
        return print(c,end='')
    return sys.exit("Function can only take char (chr), string (str), or int value.")