# infilter.py  (c)2018  Henrique Moreira (part of 'ptchamp')

"""
  infilter - Input portuguese Football championship

  Compatibility: python 2 and 3.
"""


from redito import BareText
from datex import ShortDate


#
# test_infilter()
#
def test_infilter (outFile, inArgs):
  args = inArgs
  inputName = None
  if len( args )<=0:
    input = sys.stdin
  else:
    inputName = args[ 0 ]
    del args[ 0 ]
    tred = BareText()
    isOk = tred.file_reader( inputName )
    assert isOk
  if inputName:
    zi = ZeroInputResults( tred.lines )
  for z in zi.gameLines:
    print( z )
  return 0


#
# CLASS GameResult -- one game result
#
class GameResult:
  def __init__ (self):
    self.points = [0, 0]
    self.pointStrs = ["", ""]
    self.teams = ["", ""]
    self.hasHomeTeam = True


  def home_team (self):
    assert len( team )>=2
    return teams[ 0 ]


  def visitor_team (self):
    assert len( team )>=2
    return teams[ 1 ]


  pass


#
# CLASS ZeroInputResults -- zerozero.pt text results
#
class ZeroInputResults:
  def __init__ (self, lines=[]):
    self.gameLines = []
    self.games = []
    self.results_init( lines )


  def results_init (self, lines):
    for aLine in lines:
      self.add_result( aLine )
    return True


  def add_result (self, textLine):
    s = textLine.replace("\t"," ").strip()
    if s=="" or s[ 0 ]=='#':
      return False
    pos = s.find( "/" )
    if pos>=2 and len( s )>pos+2:
      pDate = s[ pos-2:pos+4 ]
      if pDate[ -1 ]==" ":
        da = pDate[ :-1 ]
        dt = ShortDate( da )
        print("pDate:", "{"+da+"}", dt.year, "month:", dt.month, "day:", dt.day)
    return True


  pass


#
# Test suite
#
if __name__ == "__main__":
  import sys
  args = sys.argv[ 1: ]
  code = test_infilter( sys.stdout, args )
  pass

