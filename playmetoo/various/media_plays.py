# media_plays.py  (c)2020  Henrique Moreira

"""
  media_plays: basic playlist readers

  Compatibility: python 3.
"""

import pargs
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
    opts = pargs.arg_parse(param, eq)
    if "v" in opts:
        verbose = opts[ "v" ]
        assert verbose<=3
    else:
        opts[ "v" ] = 0
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
        self.header = header
        self.urls = [] if url is None else [url]


    def set_from_list (self, aList):
        if type( aList )==list or type( aList )==tuple:
            if len( aList )<2:
                return False
        else:
            assert False
        self.header = aList[0]
        self.urls = aList[1:]
        return True


    def __str__ (self):
        n = len( self.urls )
        if n<=1:
            u = self.urls[0]
        else:
            u = "{} ...".format( self.urls[0] )
        s = "{}\n{}".format( self.header, u )
        return s


#
# media_list()
#
def media_list(outFile, errFile, opts, param):
    code = 0
    verbose = opts[ "v" ]

    def flush (moves, tups, numLines=2):
        if numLines>0:
            isOk = len( moves )==2
        else:
            isOk = True
        if isOk:
            mElem = MediaElem( moves[0], moves[1] )
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
                        isOk = flush(moves, tups)
                        if not isOk:
                            errFile.write("Line {}: invalid pairs.\n".format( line ))
                            return (1, [])
                        moves = []
                middle.append( s )
                if len( middle )>2:
                    errFile.write("Line {}: Too many empty lines ({}).\n".format( line, len(middle) ))
                    return (1, [])
            else:
                middle = []
                moves.append( s )
        if moves!=[]:
            isOk = flush(moves, tups)
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
        for mElem in tups:
            outFile.write("{}\n\n".format( mElem ))
        if verbose>0:
            outFile.write("# {}\n".format(desc[0].header))
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
