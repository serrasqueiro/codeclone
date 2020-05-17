# safeurl.test.py  (c)2020  Henrique Moreira

"""
test safeurl.py
"""

# pylint: disable=missing-docstring, invalid-name


import sys
import playbasket.safeurl as safeurl


def main():
    """ Main! """
    code = run_tests(sys.stdout, sys.stderr, sys.stdin, sys.argv[1:])
    if code is None:
        print("""safeurl.test.py [a|b|...]
""")
        code = 0
    sys.exit(code)


def run_tests (outFile, errFile, inFile, inArgs):
    """ Basic tests """
    code = None
    x = safeurl.Deposit()
    if inArgs==[]:
        args = ["a"]
    else:
        args = inArgs
    cmd = args[0]
    param = args[1:]
    if cmd == "a":
        input = inFile
        for line in inFile.read().split("\n"):
            x.to_uri( line )
            print("Line: '{}' (proto: {})".format( line, x.proto ))
            x.show()
            print("Qualified(file):", x.qual)
            print("")
        code = 0
    if param:
        print("param:", param)
    return code


#
# Main script
#
if __name__ == "__main__":
    main()
