# safeurl.py  (c)2020  Henrique Moreira

"""
  safeurl: safe URL
"""

# pylint: disable=missing-docstring, invalid-name

import sys


class Deposit:
    """ Deposit class for URLs/ URIs """
    def __init__ (self, pURI=None):
        self.uri = pURI
        self.qual = pURI
        self.proto = None


    def show (self, outFile=sys.stdout):
        if outFile is not None:
            outFile.write("{}\n".format(self.to_string()))


    def to_string (self):
        info = "" if self.proto is None else self.proto
        other = "://" if self.proto is not None else ""
        s = "{}{}{}".format(info, other, self.uri)
        return s


    def to_uri (self, s, forceLocal=True):
        drive = None
        if isinstance(s, str):
            pos = s.rfind( "/" )
            if pos == -1:
                r = s.replace("\\", "/")
                if len(r) >= 2:
                    if r[0].isalpha() and r[1] == ":":
                        drive = r[:2]
            else:
                r = s
        else:
            assert False
        (self.proto, self.uri) = self.str_proto(r)
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
        assert isinstance(s, str)
        pos = s.find("://")
        if 1 < pos < 6:
            tup = (s[:pos], s[pos+3:])
        else:
            tup = (None, s)
        return tup
