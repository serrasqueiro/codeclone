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
    for x in range(vMin, vMax+1):
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
# CLASS BinStream (abstract)
#
class BinStream:
  def init_bin_stream (self):
    self.bomMarker = (0x0, 0x0)


  def isLittleEndian (self):
    return self.bomMarker == (0xFF, 0xFE)


  def set_from_octets (self, bom0, bom1):
    if type( bom0 )==str:
      return self.set_from_octets( ord(bom0), ord(bom1) )
    assert type( bom0 )==int
    assert type( bom1 )==int
    hasBOM = False
    if bom0==0xFF and bom1==0xFE:
      self.bomMarker = (0xFF, 0xFE)
      hasBOM = True
    return hasBOM


#
# CLASS TextRed (abstract)
#
class TextRed(BinStream):
  def __init__ (self):
    self.init_bin_stream()
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
      if type( self.buf )==bytes:
        mayHaveBOM = len( self.buf )>=2
        hasBOM = self.set_from_octets( self.buf[ 0 ], self.buf[ 1 ] )
      if hasBOM:
        self.add_content( self.buf[ 2: ], 2 )
      else:
        self.add_content( self.buf, 1 )
    return isOk


  def add_content (self, data, ucs=1):
    self.byteSize += len( data )
    s = ""
    col = 0
    if ucs==2:
      isOk = False
      isLittle = self.isLittleEndian()
      coil = []
      idx = 0
      lineNr = -1
      if isLittle:
        for p in data:
          even = (idx % 2)==0
          if even:
            assert type(p)==int
            coil.append( p )
          else:
            if p>0:
              self.histogram.seen[ 256 ] += 1
              self.nonASCII7.append( (lineNr, idx, format(p, "#02x")) )
          idx += 1
        isOk = self.add_content( coil, 1 )
      return isOk
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
    dosLike = self.numLines==self.numCR
    isOk = (dosLike or self.numCR==0) and len( self.clutterChrs )==0
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

