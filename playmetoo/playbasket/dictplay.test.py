"""
  dictplay.test: dictplay.py test

  dictplay.test.py  (c)2019, 2020  Henrique Moreira
"""

# pylint: disable=missing-docstring, invalid-name

import sys
from playbasket.dictplay import dict_MyGridChannels
import misc.dictplays


def test_run(args):
    """
    Main function.
    :param args: system arguments
    :return: void
    """
    if args:
        if args == ["."]:
            # own module test:
            args = (sys.argv[0].replace("\\","/").split("/")[-1].split(".")[0]+".py",)
        code = run_tests(sys.stdout, sys.stderr, args)
        sys.exit(code)

    dict_MyPlaylists = misc.dictplays.init_all()["playlists"]
    check_dict(dict_MyPlaylists, True, 12)
    print(".\n")
    check_dict(dict_MyGridChannels, False, 17)
    print(".\n")
    sys.exit(0)


def run_tests (outFile, errFile, args):
    code = 0
    for fName in args:
        try:
            val = int(fName)
        except ValueError:
            val = None
        if val is not None:
            is_ok = check_value(outFile, val)
            print("check_value({}): {}".format(val, is_ok))
            if not is_ok:
                code = 1
            continue
        with open(fName, "r") as f:
            d = f.read()
            code = check( outFile, errFile, d )
            if code!=0:
                errFile.write("Error {} in {}\n".format( code, fName ))
                return 1
    return code


def check_dict (d, forceStrVal=False, maxKeyLen=-1):
    dctKey = dict()
    upKey = dict()
    dctVal = dict()
    for k, aVal in d.items():
        isInt = False
        val = aVal
        print("{:.<12} {}".format( k, val ))
        assert isinstance(k, str)
        isInt = isinstance(val, int)
        if forceStrVal:
            assert isinstance(val, str), f"val there is '{val}'"
        else:
            val = str( val )
        isOk = maxKeyLen==-1 or len( k )<=maxKeyLen
        if not isOk:
            print("Key too long ({} chars, max: {}): {}".format( len(k), maxKeyLen, k ))
        assert isOk
        assert k[0].isalnum()
        if isInt:
            assert aVal >= -1
        else:
            assert len(val) >= 2 and len(val) < 30
        assert val.isdigit() or val.isalpha()
        assert val not in dctVal
        dctVal[aVal] = k
        u = k.upper()
        assert u not in dctKey
        dctKey[u] = k
        y = replace_all(u, " +/()_")
        assert y not in upKey
        upKey[ y ] = u
        isOk = k.find("  ") == -1
        assert isOk
    keyList = list(dctVal.keys())
    keyList.sort()
    print("...by number:")
    allNumbers = None
    for x in keyList:
        print("{:<12} {}".format(x, dctVal[ x ]))
        try:
            i = int(x)
        except ValueError:
            i = None
        if allNumbers:
            assert i is not None
        else:
            if i is None:
                assert allNumbers is None
            allNumbers = True
    print("Values referred by playlist are allNumbers:", allNumbers)
    return True


def check (outFile, errFile, d):
    assert errFile is not None
    blanks = " "*4  # four blanks
    enforce = True
    warnDuplicate = True  # Warn duplicate values (not keys, though!)
    pos = d.find( "{" )
    if pos<0:
        return 3

    def parse_dict (s, level=0, debug=0):
        assert level<1000
        valDict = dict()
        code = 0
        print("parse_dict() ~{}, level={}".format( s.count('"'), level ))
        isOk = s.startswith("\n")
        assert isOk
        s = s[1:]
        endPos = s.rfind( "}" )
        p = s[ :endPos-1 ].rstrip()
        isOk = p.startswith( blanks )
        if debug>0:
            print("\nDebug: {}, p is '{}'\n<END/>\n\n".format(isOk,p))
        assert isOk
        x = p.split("\n"+blanks)
        idx = 0
        aDict = dict()
        for aLine in x:
            pos = aLine.find("\t#")
            if pos>0:
                a = aLine[:pos]
                comment = aLine[ pos+2: ]
                if debug>0:
                    print("Did eat comment ({}): '{}'".format( comment, a ))
            else:
                a = aLine
            if a.startswith( "}\n" ):
                break
            b = a if not a.startswith( blanks ) else a[ len(blanks): ]
            if outFile is not None:
                outFile.write("'{}'\n".format( b ))
            if not enforce:
                continue
            isOk = b.startswith( '"' )
            if not isOk:
                return 4
            isOk = b.endswith( "," )
            if not isOk:
                return 7
            posColon = b.find( ": " )
            isOk = posColon>0
            if not isOk:
                return 5
            s = b[ :-1 ]
            isOk = s.endswith( '"' ) or s[-1].isdigit()
            key = s[ 1:posColon-1 ]
            if key=="":
                return 8
            sVal = s[ posColon+1: ].strip()
            if debug>0:
                print("\nDebug: CHECK: (key={}) '{}' ; so far: {}".format(key, s, isOk))
            if not isOk:
                return 6
            if key in aDict:
                return 9  # Duplicate key
            aDict[ key ] = s
            if sVal in valDict:
                if warnDuplicate:
                    print("Warn: duplicate value '{}', first seen on '{}' (now at: '{}')"
                          "".format(sVal, valDict[sVal], key))
            else:
                valDict[sVal] = key
            idx += 1
        remain = x[ idx: ]
        if remain!=[]:
            supl = remain[ 1: ]
            s = ("\n"+blanks).join( supl )
            s = "\n"+blanks + s + "\n}"
            if debug>0:
                print("Remain, to check:\n{}\n".format( supl ))
            code = parse_dict( s, level+1 )
        return code

    code = parse_dict( d[ pos+1: ], 1 )
    return code


def check_value(outFile, val, in_dictionary=None, debug=0):
    assert isinstance(val, int)
    if in_dictionary is None:
        dct = dict_MyPlaylists
    else:
        dct = in_dictionary
    keys = []
    if val == 0:
        # Check them all
        lst = list(dct.values())
        outFile.write("Playlist ids: {}".format(lst))
        for p_id in lst:
            is_ok = isinstance(p_id, str)
            if debug > 0 or not is_ok:
                print("Check '{}' ({}), type: {}"
                      "".format(p_id, type(p_id), "ok" if is_ok else "INVALID TYPE!"))
            assert is_ok
            is_ok = check_value(outFile, int(p_id), dct)
            if not is_ok:
                return False
        return True
    for k, p_id in dct.items():
        if int(p_id) == val:
            keys.append(k)
    is_ok = len(keys) == 1
    if keys:
        first = keys[0]
        print("Found {}: {}".format(dct[first] if is_ok else "multiple!", keys))
    return is_ok


def replace_all (s, anyOf, byStr=""):
    assert isinstance(s, str)
    res = ""
    for c in s:
        if c in anyOf:
            res += byStr
        else:
            res += c
    return res


#
# Main script
#
if __name__ == "__main__":
    test_run(sys.argv[1:])
