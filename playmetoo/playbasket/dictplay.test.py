# dictplay.test.py  (c)2019  Henrique Moreira

"""
  dictplay.test: dictionary for my playlists
"""

from dictplay import *



def run_tests (outFile, errFile, args):
    for fName in args:
        with open(fName, "r") as f:
            d = f.read()
            code = check( outFile, errFile, d )
            if code!=0:
                errFile.write("Error {} in {}\n".format( code, fName ))
                return 1
    return 0


def check_dict (d, forceStrVal=False, maxKeyLen=-1):
    dctKey = dict()
    upKey = dict()
    dctVal = dict()
    for k, aVal in d.items():
        isInt = False
        val = aVal
        print("{:.<12} {}".format( k, val ))
        assert type( k )==str
        isInt = type( val )==int
        if forceStrVal:
            assert type( val )==str
        else:
            val = str( val )
        isOk = maxKeyLen==-1 or len( k )<=maxKeyLen
        if not isOk:
            print("Key too long ({} chars, max: {}): {}".format( len(k), maxKeyLen, k ))
        assert isOk
        assert k[0].isalnum()
        if isInt:
            assert aVal>=-1
        else:
            assert len(val)>=2 and len(val)<30
        assert val.isdigit() or val.isalpha()
        assert val not in dctVal
        dctVal[ aVal ] = k
        u = k.upper()
        assert u not in dctKey
        dctKey[ u ] = k
        y = replace_all( u, " +/()_" )
        assert y not in upKey
        upKey[ y ] = u
        isOk = k.find( "  " )==-1
        assert isOk
    keyList = list( dctVal.keys() )
    keyList.sort()
    print("...by number:")
    allNumbers = None
    for x in keyList:
        print("{:<12} {}".format( x, dctVal[ x ] ))
        try:
            i = int(x)
        except:
            i = None
        if allNumbers:
            assert i is not None
        else:
            if i is None: assert allNumbers is None
            allNumbers = True
    print("Values referred by playlist are allNumbers:", allNumbers)
    return True


def check (outFile, errFile, d):
    blanks = " "*4  # four blanks
    enforce = True
    warnDuplicate = True  # Warn duplicate values (not keys, though!)
    pos = d.find( "{" )
    if pos<0: return 3

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
        if debug>0: print("\nDebug: {}, p is '{}'\n<END/>\n\n".format(isOk,p))
        assert isOk
        x = p.split("\n"+blanks)
        idx = 0
        aDict = dict()
        for aLine in x:
            pos = aLine.find("\t#")
            if pos>0:
                a = aLine[:pos]
                comment = aLine[ pos+2: ]
                if debug>0: print("Did eat comment ({}): '{}'".format( comment, a ))
            else:
                a = aLine
            if a.startswith( "}\n" ):
                break
            b = a if not a.startswith( blanks ) else a[ len(blanks): ]
            if outFile is not None:
                outFile.write("'{}'\n".format( b ))
            if not enforce: continue
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
            if debug>0: print("\nDebug: CHECK: (key={}) '{}' ; so far: {}".format(key, s, isOk))
            if not isOk:
                return 6
            if key in aDict:
                return 9  # Duplicate key
            aDict[ key ] = s
            if sVal in valDict:
                if warnDuplicate: print("Warn: duplicate value '{}', first seen on '{}' (now at: '{}')".format( sVal, valDict[sVal], key ))
            else:
                valDict[sVal] = key
            idx += 1
        remain = x[ idx: ]
        if remain!=[]:
            supl = remain[ 1: ]
            s = ("\n"+blanks).join( supl )
            s = "\n"+blanks + s + "\n}"
            if debug>0: print("Remain, to check:\n{}\n".format( supl ))
            code = parse_dict( s, level+1 )
        return code

    code = parse_dict( d[ pos+1: ], 1 )
    return code


def replace_all (s, anyOf, byStr=""):
    assert type( s )==str
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
    import sys
    args = sys.argv[ 1: ]
    outFile = sys.stdout
    errFile = sys.stderr
    if args!=[]:
        if args==["."]:
            # own module test:
            args = (sys.argv[0].replace("\\","/").split("/")[-1].split(".")[0]+".py",)
        code = run_tests(outFile, errFile, args)
        sys.exit(code)

    check_dict( dict_MyPlaylists, True, 12 )
    print(".\n")
    check_dict( dict_MyGridChannels, False, 17 )
    print(".\n")
    sys.exit(0)
