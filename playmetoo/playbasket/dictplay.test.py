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


def check (outFile, errFile, d):
    blanks = " "*4  # four blanks
    enforce = True
    pos = d.find( "{" )
    if pos<0: return 3

    def parse_dict (s):
        isOk = s.startswith("\n")
        s = s[1:]
        endPos = s.rfind( "}" )
        p = s[ :endPos-1 ].rstrip()
        x = p.split("\n"+blanks)
        idx = 0
        for a in x:
            if a.startswith( "}\n" ):
                break
            b = a if not a.startswith( blanks ) else a[ len(blanks): ]
            isOk = b.startswith( '"' ) and b.endswith( "," )
            if outFile is not None:
                outFile.write("'{}'\n".format( b ))
            if not enforce: continue
            if not isOk:
                return 4
            isOk = b.find( ": " )>0
            if not isOk:
                return 5
            s = b[ :-1 ]
            isOk = s.endswith( '"' ) or s[-1].isdigit()
            if not isOk:
                return 6
            idx += 1
        remain = x[ idx: ]
        if remain!=[]:
            supl = remain[ 1: ]
            print("Remain, unchecked:\n{}\n".format( supl ))
        return 0

    code = parse_dict( d[ pos+1: ] )
    return code


#
# Main script
#
if __name__ == "__main__":
    import sys
    dctKey = dict()
    dctVal = dict()
    args = sys.argv[ 1: ]
    outFile = sys.stdout
    errFile = sys.stderr
    if args!=[]:
        code = run_tests(outFile, errFile, args)
        sys.exit(code)

    for k, val in dict_MyPlaylists.items():
        print("{:.<12} {}".format( k, val ))
        assert type( k )==str
        assert type( val )==str
        assert len( k )<=12
        assert k[0].isalnum()
        assert len(val)>=2 and len(val)<30
        assert val.isdigit() or val.isalpha()
        assert val not in dctVal
        dctVal[ val ] = k
        u = k.upper()
        assert u not in dctKey
        dctKey[ u ] = k
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
    sys.exit(0)
