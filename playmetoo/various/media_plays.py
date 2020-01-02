# media_plays.py  (c)2020  Henrique Moreira

"""
  media_plays: basic playlist readers

  Compatibility: python 3.
"""

import pargs
from pargs import split_first
from redito import xCharMap


#
# main()
#
def main (outFile, errFile, inArgs):
    code = None
    if inArgs==[]: return None
    cmd = inArgs[ 0 ]
    param = inArgs[ 1: ]
    verbose = 0
    eq = dict()
    eq = {"s":("--strict", ),
          }
    opts = pargs.arg_parse(param, eq)
    if opts is None: return None
    if "-v" in opts:
        verbose = opts[ "-v" ]
        assert verbose<=3
    else:
        opts[ "-v" ] = 0
    if "-s" not in opts: opts[ "-s" ] = 0
    if verbose<0:
        print("param:", param)
        for k, val in opts.items():
            print("option {}: {}".format( k, val ))
        return 0
    if cmd=="media-list":
        code = media_list(outFile, errFile, opts, param)
        if verbose>0:
            errFile.write("Exit-code: {}\n".format( code ))
    return code


#
# CLASS MediaElem
#
class MediaElem:
    def __init__ (self, header=None, url=None):
        self.ref = -1
        self.header = header
        self.urls = [] if url is None else [url]


    def set_from_list (self, aList, aRef=-1):
        if type( aList )==list or type( aList )==tuple:
            if len( aList )<2:
                return False
        else:
            assert False
        self.header = aList[0]
        self.urls = aList[1:]
        self.ref = int( aRef )
        return True


    def __str__ (self):
        n = len( self.urls )
        if n<=1:
            u = self.urls[0]
        else:
            u = "{} ...".format( self.urls[0] )
        s = "{}\n{}".format( self.header, u )
        return s


    def valid_URL (self, s=None):
        validProtos = ("file", "http", "https")
        if type( s )==list:
            for a in s:
                isOk = self.valid_URL( a )
                if not isOk: return False
            return True
        elif type( s )==str:
            isOk = s.find( "://" )>1
        elif s is None:
            assert type( self.urls )==list
            return self.valid_URL( self.urls )
        else:
            assert False
        if isOk:
            spl = split_first( s, "://" )
            prot = spl[0]
            isOk = len( spl )==2 and prot in validProtos
        else:
            isOk = self.valid_ref( s )
        return isOk


    def valid_ref (self, s):
        assert type( s )==str
        if s=="": return True
        isOk = s.isdigit() or (s[0].isalpha() and s.isalnum())
        return isOk

#
# media_list()
#
def media_list(outFile, errFile, opts, param):
    code = 0
    verbose = opts[ "-v" ]
    strictLevel = opts[ "-s" ]
    numSep = 2
    maxLines = 2

    def flush (moves, tups, lineNr, numLines=2):
        if numLines>0:
            isOk = len( moves )==2
        else:
            isOk = True
        if isOk:
            mElem = MediaElem( moves[0], moves[1] )
            mElem.ref = lineNr
            tups.append( mElem )
        return isOk

    def parse_input (outFile, errFile, lines):
        line = 0
        tups = []
        if lines!=[]:
            h = lines[0]
            if h.startswith( "#" ):
                line += 1
                comment.header = h[ 1: ].strip()
                del lines[0]
        middle = []
        moves = []
        for a in lines:
            line += 1
            s = a.strip("\t ")
            if s!=a:
                errFile.write("Line {}: Trailing or leading Blanks/ tabs\n".format( line ))
                return (1, [])
            if s=="":
                if middle==[]:
                    if moves!=[]:
                        isOk = flush(moves, tups, line, maxLines)
                        if not isOk:
                            errFile.write("Line {}: invalid pairs.\n".format( line ))
                            return (1, [])
                        moves = []
                middle.append( s )
                if len( middle )>2:
                    errFile.write("Line {}: Too many empty lines ({}).\n".format( line, len(middle) ))
                    return (1, [])
            else:
                if middle!=[] and len(tups)>0:
                    if strictLevel>0:
                        #print("Check lines in between:", len(middle), "s:", s)
                        if len(middle)!=numSep:
                            errFile.write("Line {}: Few empty lines ({}), expected {}.\n".format( line, len(middle), numSep ))
                            return (1, [])
                middle = []
                moves.append( s )
        if moves!=[]:
            isOk = flush(moves, tups, line)
            if not isOk:
                return (1, [])
        return (0, tups)

    for name in param:
        desc = [MediaElem("#"), [], (name,)]
        comment, mList = desc[0], desc[1]
        lines = open(name, "r").read().split("\n")
        assert lines!=[]
        if lines[-1]=="": del lines[-1]
        errCode, tups = parse_input(outFile, errFile, lines)
        bugs = 0
        if strictLevel>0:
            for mElem in tups:
                assert mElem.header!=""
                assert len(mElem.urls)>=1
                isOk = mElem.valid_URL()
                if not isOk:
                    bugs += 1
                    errFile.write("Line {}: invalid mElem: {}\n".format( mElem.ref, ";".join(mElem.urls) ))

        for mElem in tups:
            outFile.write("{}\n".format( mElem ))
            if verbose>0: outFile.write("--\n")
            outFile.write("\n")
        h = desc[0].header
        sExtra = "" if bugs==0 else " (bugs: {})".format( bugs )
        if verbose>0:
            if h!="#":
                outFile.write("# {}{}\n".format(h, sExtra))
        if errCode!=0:
            return 1
    return code


#
# Main script
#
if __name__ == "__main__":
    import sys
    code = main( sys.stdout, sys.stderr, sys.argv[ 1: ] )
    if code is None:
        print("""media_plays command [options] [args]

media-list      List of media description with links.
""")
        code = 0
    assert type( code )==int
    assert code<=127
    sys.exit( code )
