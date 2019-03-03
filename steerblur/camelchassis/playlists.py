# playlists.py  (c)2019  Henrique Moreira (part of 'camelchassis')

"""
  playlists - Classes to handle playlists

  Compatibility: python 2 and 3.
"""


from redito import BareText


#
# CLASS AnyPlaylist
#
class AnyPlaylist:
  def init_playlist (self, name):
    self.name = name
    self.items = []


  def __str__ (self):
    return self.to_str()


  pass


#
# CLASS WpList -- handles wpl contents
#
class WpList(AnyPlaylist):
  def __init__ (self, name=""):
    self.init_playlist( name )


  def add_src (self, srcQuote='""'):
    assert type( srcQuote )==str
    assert len( srcQuote )>=2
    if srcQuote[ 0 ]=='"' and srcQuote[ -1 ]=='"':
      s = srcQuote[ 1:-1 ]
    else:
      s = srcQuote
    self.items.append( s )
    path = from_html( s )
    return path


  def to_str (self):
    s = '\n'.join( self.items )
    return s


  pass


#
# from_html() -- converts to string from HTML (e.g. '&amp;' is '&')
#
def from_html (s):
  assert type( s )==str
  # TODO: convert HTML string into 'normal' Latin1 string
  return True


#
# Test suite
#
if __name__ == "__main__":
  import sys
  args = sys.argv[ 1: ]
  #code = test_playlists( sys.stdout, args )
  print("No tests; see e.g. boards.py")
  assert False

