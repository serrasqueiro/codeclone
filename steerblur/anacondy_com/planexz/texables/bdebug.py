# bdebug.py  (c)2020  Henrique Moreira

""" Basic Debug module
"""

# pylint: disable=missing-docstring

#DEBUG = 1

def dprint(debug, *args):
    sep = ""
    if debug > 0:
        print("###", args)
        print("---<")
        for item in args:
            print(sep, end='')
            print(item, end='')
            sep = " "
        print("")


def bprint(*args):
    try:
        debug = DEBUG
    except NameError:
        debug = 0
    dprint(int(debug), *args)


#
# Main script
#
if __name__ == "__main__":
    print(f"Please import {__file__}")
    print("...\nIf you have defined DEBUG, you will see a next line.\n")
    bprint("Import", __file__)
