# safeurl.py  (c)2020  Henrique Moreira

"""
  safeurl: safe URL
"""


import sys


#
# CLASS Deposit
#
class Deposit:
    def __init__ (self, pURI=None):
        self.uri = pURI
        self.qual = pURI
        self.proto = None


    def show (self, outFile=sys.stdout):
        if outFile is not None:
            outFile.write("{}\n".format( self.to_string() ))


    def to_string (self):
        s = "{}{}{}".format( "" if self.proto is None else self.proto, "://" if self.proto is not None else "", self.uri )
        return s


    def to_uri (self, s, forceLocal=True):
        res = ""
        drive = None
        if type( s )==str:
            pos = s.rfind( "/" )
            if pos==-1:
                r = s.replace("\\", "/")
                if len(r)>=2:
                    if r[0].isalpha() and r[1]==":": drive = r[:2]
            else:
                r = s
        else:
            assert False
        (self.proto, self.uri) = self.str_proto( r )
        addQual = 0
        if forceLocal:
            if drive is not None:
                addQual = 1
        if addQual:
            self.qual = "file:///" + self.uri
        else:
            self.qual = self.uri
        return True


    def str_proto (self, s):
        assert type( s )==str
        p = s.find("://")
        if p>1 and p<6:
            tup = (s[:p], s[p+3:])
        else:
            tup = (None, s)
        return tup