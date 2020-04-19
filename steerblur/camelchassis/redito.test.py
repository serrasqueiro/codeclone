# redito_test.py  (c)2018, 2020  Henrique Moreira (part of 'camelchassis')

"""
  redito_test - Common functions to streams and files.

  Compatibility: python 3.
"""

# pylint: disable=invalid-name, unused-argument


import sys
from redito import xCharMap, CharMap, BareText


def main():
    """ Main test script! """
    code = test_redito_test(sys.stdout, sys.argv[1:])
    sys.exit(code)


def test_redito_test(out, inArgs):
    """ Main module test! """
    def test_show(charmap):
        assert isinstance(charmap, CharMap)
        s = "T\xe1bua on ch\xe3o em (C\xd4TE) C\xf4te Ivoir."
        for x in [0, 1]:
            t = charmap.simpler_ascii( s, x )
            print( t )
            isOk = t=="Tabua on chao", "Ta'bua on cha~o em (COTE) Cote Ivor."
            assert isOk
        return 0

    dosCR = ""
    args = inArgs
    doAny = True
    while doAny and len(args) > 0:
        doAny = False
        if args[ 0 ]=='--dos':
            doAny = True
            del args[ 0 ]
            dosCR = "\r"
            continue
    if len( args ) < 0:
        return 0
    if len( args ) <= 0:
        return test_show(xCharMap)
    name = args[0]
    tred = BareText( name )
    isOk = tred.utf_file_reader()
    if isOk:
        for aLine in tred.lines:
            s = aLine
            out.write( s + dosCR + "\n" )
    return 0


#
# Test suite
#
if __name__ == "__main__":
    main()
