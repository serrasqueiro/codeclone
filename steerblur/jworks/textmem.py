# textmem.py  (c)2019  Henrique Moreira (part of 'jworks')

"""
  textmem module handles basic text memory files.

  Compatibility: python 2 and 3.
"""

from base64 import b64decode


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


  def from_file (self, inName=None):
    fIn = open(inName, "rb")
    buf = fIn.read().decode( self.decoding )
    fIn.close()
    self.cont = buf.split("\n")
    return True


#
# CLASS TextMem:
#
class TextMem(RawMem):
  def parse (self, opts=None):
    code = 0
    opt = opts if opts is not None else dict()
    assert type( self.cont )==list
    h = 0
    aText = ""
    for a in self.cont:
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
      self.leg.append( s )
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
