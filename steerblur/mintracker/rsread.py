# rsread.py  (c)2019  Henrique Moreira

"""
  rsread: a simpler rss reader

  Compatibility: python 3.
"""

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
