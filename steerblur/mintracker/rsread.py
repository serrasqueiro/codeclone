# rsread.py  (c)2019  Henrique Moreira

"""
  rsread: a simpler rss reader

  Compatibility: python 3.
"""

import datetime
from lxml import etree
# http://lxml.de/tutorial.html


#
# main_rsread()
#
def main_rsread (outFile, errFile, inArgs):
    code = None
    debug = 0
    verbose = 0
    return code


#
# CLASS TextContent
#
class TextContent:
    def init_textcontent (self):
        self.content = []
        self.originalInput = []


#
# CLASS RssEcho
#
class RssEcho(TextContent):
    def __init__ (self):
        self.init_textcontent()
        self.seq = []
        self.keying = dict()


    def add_from_string (self, s):
        idx = 0
        if type( s )==str:
            v = s
        else:
            assert False
        lines = v.split( "\n" )
        for a in lines:
            idx += 1
            s = a.strip()
            if s!="":
                if s.startswith( "<!--" ) and s.endswith( "-->" ):
                    pass
                else:
                    self.content.append( s )
                    self.originalInput.append( idx )
        return True


    def new_date (self, s):
        if type( s )==str:
            cDate = s
        else:
            cDate = None
        assert cDate is not None
        newDate = RssDate( cDate )
        return newDate


#
# CLASS HumanDate
#
class HumanDate:
    def init_humandate (self):
        self.s = ""


#
# CLASS RssDate
#
class RssDate(HumanDate):
    def __init__ (self, s):
        self.init_humandate()
        self.dttm = self.try_rss_date( s )


    def __str__ (self):
        return "-" if self.dttm is None else str( self.dttm )


    def from_cdate (self, s):
        dt = datetime.datetime.strptime(s, "%a, %d %b %Y %H:%M:%S")  # e.g. "Mon, 21 Oct 2019 23:57:58"
        return dt


    def from_rss_date (self, s):
        dt = datetime.datetime.strptime(s, "%a, %d %b %Y %H:%M:%S %z")  # e.g. "Mon, 21 Oct 2019 23:57:58 +0100"
        return dt


    def try_rss_date (self, rfcDate):
        if type( rfcDate )==str:
            s = rfcDate
        else:
            s = None
        assert s is not None
        try:
            dt = self.from_rss_date( s )
        except:
            dt = None
        return dt


#
# Globals
#


#
# Main script
#
if __name__ == "__main__":
    import sys
    code = main_rsread( sys.stdout, sys.stderr, sys.argv[ 1: ] )
    if code is None:
        print("""
rsread.py Command [options]

Commands are:
   dump rss-file [rss-file ...]
""")
        code = 0
    assert type( code )==int
    assert code<=127
    sys.exit( code )
