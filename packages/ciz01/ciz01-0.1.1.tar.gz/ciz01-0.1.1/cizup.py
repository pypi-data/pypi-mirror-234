def printChar(c: chr):
    if type(c) != chr:
        return exit("Function can only take char (chr) value")
    print(c,end='')