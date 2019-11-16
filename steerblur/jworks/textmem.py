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
  def parse (self, opts=None):
    def flush_block (blk, toList):
      if blk==[]:
        return False
      skip = False
      one = blk[ 0 ]
      if len( blk )<=1:
        skip = one.startswith( "###" )
      if skip:
        return False
      toList.append( blk )
      return True

    code = 0
    opt = opts if opts is not None else dict()
    assert type( self.cont )==list
    h = 0
    blk = []
    aText = ""
    for a in self.cont:
      if a=="":
        flush_block( blk, self.leg )
        blk = []
        h = 0
      else:
        h += 1
      try:
        tent = b64decode( a )
      except:
        tent = None
      if tent is None:
        s = a
      else:
        myText = []
        isText = self.is_text( tent, myText )
        if isText:
          s = myText[ 0 ]
        else:
          s = a
      if h>0:
        blk.append( s )
    flush_block( blk, self.leg )
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
# No main...!
#
if __name__ == "__main__":
  print("see textmem.test.py")
