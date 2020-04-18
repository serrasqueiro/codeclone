# textmem.test.py  (c)2020  Henrique Moreira (part of 'jworks')

"""
  textmem.test - test module for textmem

  Compatibility: python 2 and 3.
"""

# pylint: disable=missing-function-docstring, unidiomatic-typecheck, invalid-name, wildcard-import

import sys
from sys import stdin
from jworks.textmem import TextMem, Base64Mem


def main():
    code = run_main(sys.stdout, sys.stderr, sys.argv[ 1: ])
    if code is None:
        code = 0
        print("""textmem.test [command]

Tests textmem module.
""")
    assert isinstance(code, int)
    sys.exit(code)


def run_main (outFile, errFile, inArgs):
    """ Main run.
    """
    code = None
    outName = None
    # Processing
    if inArgs == []:
        args = ["p", "mem_test.txt"]
    else:
        args = inArgs
    cmd = args[0]
    param = args[1:]
    # Checking options
    while len(param) > 0 and param[0].startswith("-"):
        if param[ 0 ] == "-o":
            outName = param[1]
            del param[:2]
            continue
        print("Wrong option:", param[0])
        return None
    if outName is not None:
        outFile = open(outName, "wb")
    # Work the commands
    if cmd == "d":  # Dump, with basic check
        code = test_dump(outFile, errFile, param, outName)
    if cmd == "p":  # Parse
        code = test_parse(outFile, errFile, param, outName)
    if cmd == "s":
        code = test_base64(param)
    return code


def test_dump(outFile, errFile, param, outName):
    code, line = 0, 0
    assert len(param) == 1
    name = param[0]
    tm = TextMem()
    isOk = tm.from_file(name)
    assert isOk
    for a in tm.cont:
        line += 1
        if a.endswith("\r"):
            a = a[:-1]
        assert not a.endswith("\r")
        s = a.rstrip()
        if s != a:
            code = 1
            errFile.write("Line {}: dangling blanks/ tabs\n".format(line))
        sOut = "{}\n".format(s)
        uops = tm.to_stream(outFile, tm.out_str(sOut, outName is None)) != 0
        if uops:
            errFile.write("Converted line to: {}\n".format(tm.simpler_str(s)))
    return code


def test_parse(outFile, errFile, param, outName):
    pOpt = {"allow-2-nl":True,
            }
    name = param[0]
    tm = TextMem()
    if name == ".":
        myText = """
    textmem.test python
    KGMpMjAxOSAgSGVu
    cmlxdWUgTW9yZWlyYQ==

    Realfornelos, fun
    http://xperteleven.com/players.aspx?TeamID=1845332&Boost=0&dh=1
    """
        tm.cont = myText.split("\n")
    else:
        tm.from_file(name)
    tm.parse(pOpt)
    for a in tm.leg:
        if isinstance(a, str):
            s = a
        else:
            if len(a) <= 1:
                s = "@\t{}\n".format(a[0])
            else:
                s = "{}\n{}\n".format(a[0], a[1])
        sOut = "{}\n".format(s)
        tm.to_stream(outFile, tm.out_str(sOut, outName is None))
    code = 0
    if tm.msgs != []:
        code = 1
        for msg in tm.msgs:
            errFile.write("Warn: {}\n".format(msg))
    return code


def test_base64(param):
    bm = Base64Mem()
    bm.hash_symbols()
    w = param[0] if len(param) > 0 else None
    if w is None:
        s = stdin.read()
    elif w == ".":
        print("Base64 symbols:", bm.symbols)
        return 0
    else:
        with open(w, "r") as fp:
            s = fp.read()
    for c in s:
        d = ord(c)
        shown = "\\n" if c == "\n" else c
        print("{}, ASCII #{}: hash value of BASE64 alphabet is {}".format(shown, d, bm.hash[d]))
    return 0


#
# Main script
#
if __name__ == "__main__":
    main()
