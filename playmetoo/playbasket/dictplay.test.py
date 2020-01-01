# dictplay.test.py  (c)2019  Henrique Moreira

"""
  dictplay.test: dictionary for my playlists
"""

from dictplay import *


#
# Main script
#
if __name__ == "__main__":
    dctKey = dict()
    dctVal = dict()
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
    pass
