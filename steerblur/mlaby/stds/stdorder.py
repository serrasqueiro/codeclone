# stdorder.py  (c)2020  Henrique Moreira (part of 'mlaby/stds')

"""
  stdorder module handles enhanced dictionaries.

  Compatibility: python 2 and 3.
"""


# test_stdorder()
#
def test_stdorder (outFile, inArgs):
    code = None
    if inArgs==[]:
        args = ["a"]
    else:
        args = inArgs
    cmd = args[0]
    param = args[1:]
    if cmd=="a":
            code = 0
            d = SDict( {"b": 1, "a": 0} )
            for x in d.byName:
                y = d.get( x )
                print(x, y)
    if code is not None:
        if param:
            print("Remaining params:", param)
    return code


#
# CLASS SDict
#
class SDict():
    def __init__ (self, aDict={}, isReverse=False):
        self.byName = None
        self.set_to( aDict, isReverse )


    def set_to (self, aDict, isReverse):
        self.ori = aDict
        if type(aDict)==dict:
            ks = list( aDict.keys() )
            ks.sort( reverse=isReverse )
            self.byName = ks
        else:
            self.byName = aDict
        return True


    def histog (self, column=-1, isReverse=False, mustExist=True):
        assert column>=1
        idx = column-1
        counts = dict()
        for k, val in self.ori.items():
            if mustExist:
                cell = val[ idx ]
            else:
                if len( cell )>=column:
                    cell = val[ idx ]
                else:
                    cell = None
            if cell is not None:
                if cell not in counts:
                    counts[ cell ] = 1
                else:
                    counts[ cell ] += 1
        xd = SDict( counts, isReverse )
        return xd


    def get (self, index):
        if index not in self.ori:
            return None
        return self.ori[ index ]


#
# Test suite
#
if __name__ == "__main__":
    import sys
    code = test_stdorder( sys.stdout, sys.argv[ 1: ] )
    if code is None:
        print("""stdorder.py command [options]
Test SDict and related classes.

a       Basic tests.

""")
        code = 0
    sys.exit( code )
