# redito.py  (c)2018  Henrique Moreira (part of 'camelchassis')

"""
  redito - Common functions to streams and files.

  Compatibility: python 2 and 3.
"""


#
# CLASS BasicHist -- basic histogram
#
class BasicHistogram:
  def __init__ (self, vMin=0, vMax=256):
    self.seen = []
    self.semiEmpty = []
    for x in range(vMin, vMax):
      self.seen.append( 0 )
    pass


  def how_many (self, aChr):
    if type( aChr )==str:
      count = 0
      for c in aChr:
        count += self.seen[ ord( c ) ]
    elif type( aChr )==int:
      count = self.seen[ c ]
    return count


#
# CLASS TextRed (abstract)
#
class TextRed:
  def __init__ (self):
    self.numLines = 0
    self.numCR = 0  # usually we want to avoid '\r'
    self.byteSize = 0
    self.noEOL = False
    self.clutterChrs = []
    self.nonASCII7 = []
    self.skipNonASCII7bit = True
    self.lines = []
    self.inFilename = ""
    self.extension = ( "", [""] )
    self.histogram = BasicHistogram()
    self.top_init()


  def set_filename (self, filename):
    self.inFilename = filename
    pos = filename.rfind( "." )
    coName = ""
    if pos>0:
      ext = filename[ pos: ]
    else:
      ext = ""
    if ext=='.py':
      coName = "PYTHON"
    self.extension = ( ext, [coName] )
    return coName


  def file_coname (self):
    return self.extension[ 1 ][ 0 ]


  def file_reader (self, filename):
    isOk = True
    self.set_filename( filename )
    try:
      f = open( filename, "rb" )
    except:
      isOk = False
    self.buf = ""
    if isOk:
      self.buf = f.read()
      f.close()
      self.add_content( self.buf )
    return isOk


  def add_content (self, data):
    self.byteSize += len( data )
    s = ""
    col = 0
    for el in data:
      if type( el )==str:
        # Python 2.x
        c = ord( el )
      else:
        c = el
      self.histogram.seen[ c ] += 1
      if c==ord('\n'):
        self.add_lines( s )
        s = ""
        col = 0
      elif c==ord('\r'):
        self.numCR += 1
      elif c<ord(' ') and c!=ord('\r') and c!=ord('\t'):
        self.clutterChrs.append( (self.numLines+1, 0, format(c, "#02x")) )
        s += "?"
      else:
        col += 1
        if c>=127:
          self.nonASCII7.append( (self.numLines+1, col, format(c, "#02x")) )
        if c<127 or self.skipNonASCII7bit==False:
          s += chr( c )
    if len( s )>0:
      self.noEOL = True
      self.add_lines( s+"\n" )
    return True


  def add_lines (self, textLines):
    isOk = type(textLines)==str
    assert isOk
    for aLine in textLines.split( '\n' ):
      self.numLines += 1
      self.lines.append( aLine )
      if len( aLine )>0 and len( aLine.strip() )==0:
        self.histogram.semiEmpty.append( self.numLines )
    return isOk


  def is_text_ok (self, requireASCII7=True):
    isOk = self.numCR==0 and len( self.clutterChrs )==0
    if requireASCII7 and len( self.nonASCII7 )>0:
      isOk = False
    return isOk


  pass



#
# Test suite
if __name__ == "__main__":
  import sys
  args = sys.argv[ 1: ]
  print("No tests yet, ignored:", args)
  pass

