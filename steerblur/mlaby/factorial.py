# factorial.py -- (c)2019 Henrique Moreira
"""
Short how-to to calculate factorial
"""

import sys
import math


# pylint: disable=missing-function-docstring, invalid-name


def main():
    """ Main! """
    code = main_func(sys.stdout, sys.argv[1:])
    sys.exit(code)


def main_func (out, inArgs) -> int:
    """ Main function """
    args = inArgs
    if not args:
        args = ["3", "5"]
    for n in args:
        if "." in n:
            n = float(n)
        try:
            fato = fact(n)
        except ValueError:
            fato = None
        shown = "" if fato is not None else " (Invalid value)"
        print("{}! = {}{}".format(n, fato, shown))
    return 0


def fact (nonNegativeNumber, doNative=True) -> int:
    """ mathematical factorial function, n! """
    n = int(nonNegativeNumber)
    if n < 0:
        return -1	# error!
    if doNative:
        num = math.factorial(n)
        return num
    num = 1
    while n >= 1:
        num = num * n
        n = n - 1
    return num


if __name__=="__main__":
    main()
