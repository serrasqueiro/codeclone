# safeurl.test.py  (c)2020  Henrique Moreira

"""
test safeurl.py
"""

# pylint: disable=unused-argument, invalid-name


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
    fIn = inFile
    x = safeurl.Deposit()
    if inArgs==[]:
        args = ["a"]
    else:
        args = inArgs
    cmd = args[0]
    param = args[1:]
    while param and param[0].startswith("-"):
        if param[0] == "--input":
            inName = param[1]
            fIn = open(inName, "r")
            del param[:2]
            continue
        return None
    if cmd == "a":
        test_a(fIn, x)
        code = 0
    if param:
        print("param:", param)
    return code


def test_a(fIn, x):
    """ Test A """
    for line in fIn.read().split("\n"):
        if not line:
            continue
        x.to_uri(line)
        print("Line: '{}' (proto: {})".format(line, x.proto))
        x.show()
        print("Qualified(file):", x.qual)
        print("proto:", x.proto)
        print("--\n")
    return 0


#
# Main script
#
if __name__ == "__main__":
    main()
