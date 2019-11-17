# textmem.py  (c)2019  Henrique Moreira (part of 'jworks')

"""
  textmem module handles basic text memory files.

  Compatibility: python 2 and 3.
"""

from base64 import b64decode
from redito import xCharMap


#
# abstract CLASS RawMem
#
class RawMem:
  def __init__ (self, buf=[], rawASCII=False):
    self.msgs = []
    self.hash = None
    if rawASCII:
      self.decoding = "ascii"
    else:
      self.decoding = "iso-8859-1"
    self.encoding = self.decoding
    if type( buf )==str:
      self.cont = buf.split("\n")
    elif type( buf )==list:
      self.cont = buf
    else:
      assert False
    self.leg = []


  def simpler_str (self, s):
    if type( s )==str:
      a = xCharMap.simpler_ascii( s )
    else:
      a = "?"
    return a


  def from_file (self, inName=None):
    fIn = open(inName, "rb")
    buf = fIn.read().decode( self.decoding )
    fIn.close()
    self.cont = buf.split("\n")
    return True


  def out_str (self, s, isTextStream=True):
    isStr = type( s )==str
    if isTextStream:
      a = s
    else:
      a = s.encode( self.encoding )
    return a


  def to_stream (self, aStream, a):
    code = -1
    try:
      aStream.write( a )
      code = 0
    except UnicodeEncodeError:
      s = self.simpler_str( a )
      aStream.write( s )
    return code


#
# CLASS TextMem:
#
class TextMem(RawMem):
  def parse (self, opts=None, debug=0):
    def flush_block (blk, b64Tups, toList):
      assert type( blk )==list
      assert type( b64Tups )==list
      if blk==[]:
        return False
      skip = False
      one = blk[ 0 ]
      if len( blk )<=1:
        skip = one.startswith( "###" )
      if skip:
        return False
      if len( b64Tups )>=2:
        aText = ""
        idx = b64Tups[ 0 ][ 0 ]
        for tup in b64Tups:
          aText += tup[ 1 ]
        aList = []
        i = 0
        for a in blk:
          i += 1
          if i==idx:
            break
          aList.append( a )
        aList.append( aText )
        toList.append( aList )
      else:
        toList.append( blk )
      b64Tups = []
      return True

    code = 0
    bm = Base64Mem()
    bm.hash_symbols()
    opt = opts if opts is not None else dict()
    assert type( opt )==dict
    assert type( self.cont )==list
    h = 0
    lastH = 0
    blk = []
    b64Tups = []
    aText = ""
    lineIdx = 0
    for a in self.cont:
      msg = None
      lineIdx += 1
      if a=="":
        flush_block( blk, b64Tups, self.leg )
        blk = []
        if lastH==0:
          msg = "Extra empty line"
        h = 0
      else:
        h += 1
      tent = bm.string_decode( a )
      if tent is None:
        s = a
        b64Tups = []
      else:
        myText = []
        isText = self.is_text( tent, myText )
        if isText:
          s = myText[ 0 ]
          b64Tups.append( (len(blk)+1, s) )
        else:
          s = a
          b64Tups = []
      if h>0:
        blk.append( s )
        if debug>0:
          dbgStr = "." if tent is None else tent
          print("Debug: '{}'\n{}\n".format( self.simpler_str(s), dbgStr ))
      lastH = h
      if msg is not None:
        message = "Line {}: {}".format( lineIdx, msg )
        if debug>0:
          print("Debug:", message)
        self.msgs.append( message )
    flush_block( blk, b64Tups, self.leg )
    return code


  def is_text (self, s, myText):
    if type( s )==bytes:
      try:
        a = s.decode("ascii")
      except:
        a = None
    else:
      assert type( s )==str
      a = s
    if a is not None:
      myText.append( a )
      return True
    return False


#
# CLASS Base64Mem:
#
class Base64Mem(RawMem):
  def hash_symbols (self):
    symb = """
ABCDEFGHIJKLMNOPQRSTUVWXYZ
abcdefghijklmnopqrstuvwxyz
0123456789
+/="""
    self.symbols = symb.replace( "\n", "" )
    self.hash = dict()
    for d in range( 256 ):
      c = chr( d )
      try:
        w = self.symbols.index( c )
      except:
        w = -1
      self.hash[ d ] = w
    return True


  def seem_base64 (self, s):
    isBase64 = False
    if type( s )==list:
      for el in s:
        isBase64 = seem_base64( el )
        if not isBase64:
          return False
      return isBase64
    elif type( s )==str:
      countFinish = 0
      hasFinish = False
      for c in s:
        h = self.hash[ ord(c) ]
        isBase64 = h>=0
        if not isBase64:
          return False
        if h>64:
          hasFinish = True
          countFinish += 1
          if countFinish>3:
            return False
        else:
          if hasFinish:
            return False
    return isBase64


  def string_decode (self, s):
    if type( s )==str:
      try:
        b = b64decode( s )
      except:
        b = None
    else:
      assert False
    return b


#
# No main...!
#
if __name__ == "__main__":
  print("see textmem.test.py")
