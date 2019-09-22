# poco.py  (c)2019  Henrique Moreira (inspired on 'jogomundo')

"""
  Dump pdf files in different ways.

  Compatibility: python 2 and 3.
"""


import PyPDF2
from pdfz import extractText
from redito import xCharMap


#
# main_poco()
#
def main_poco (outFile, errFile, inArgs):
  code = None
  debug = 0
  verbose = 0
  outName = None
  try:
    cmd = inArgs[ 0 ]
  except:
    return None
  param = inArgs[ 1: ]
  # Parse args
  while len( param )>0 and param[ 0 ].startswith( "-" ):
    if param[ 0 ].startswith( "-v" ):
      verbose += param[ 0 ].count( "v" )
      del param[ 0 ]
      continue
    if param[ 0 ].startswith( "-o" ):
      outName = param[ 1 ]
      del param[ :2 ]
      continue
    print("Invalid option(s);\n", param)
    return None
  args = param
  if verbose>=3:
    print("Debug on!")
    debug = 1
  if outName is not None:
    outFile = open( outName, "w" )
  # Adjusts before run
  readKind = "text"
  if cmd=="seq-pdf":
    readKind = "seq"	# no blanks
  elif cmd=="textual-pdf":
    readKind = "textual"
  # Command run
  if cmd in ("raw-pdf",
             "textual-pdf",
             "seq-pdf",
             ):
    inName = args[ 0 ]
    tup = readerControl.pdf_text( inName, readKind, debug )
    code = tup[ 0 ]
    cont = tup[ 1 ]
    if code!=0:
      if code==2:
        errFile.write("Cannot read pdf: {}\n".format( inName ))
      else:
        errFile.write("No content: {}\n".format(inName))
    else:
      for a in cont:
        outFile.write("{}\n".format( a ))
    code = 0
  if outName is not None:
    outFile.close()
  return code


#
# CLASS ReaderControl
#
class ReaderControl:
  def __init__ (self):
    self.initFuncOriginal = PyPDF2.pdf.PageObject.extractText
    self.excessiveStrsReplacement = (" ", ("\n", "\n(---)\n\n"))


  #
  # pdf_reader()
  #
  def pdf_reader (self, aFile):
    fileReader = PyPDF2.PdfFileReader( aFile )
    return fileReader


  #
  # pdf_text()
  #
  def pdf_text (self, inName, readKind="text", debug=0):
    assert type( inName )==str
    res = []
    isOriginal = readKind=="seq"
    isTextual = readKind=="textual"
    if isOriginal:
      PyPDF2.pdf.PageObject.extractText = self.initFuncOriginal
    else:
      PyPDF2.pdf.PageObject.extractText = extractText
    try:
      op = open( inName, "rb" )
    except:
      op = None
    if op is None:
      return (2, res)
    pReader = self.pdf_reader( op )
    toASCII = "ASCII"
    cont = self.raw_content( pReader, toASCII )
    if cont is None:
      op.close()
      return (3, res)
    idx = 0
    for line in cont:
      idx += 1
      s = line.rstrip()
      if isTextual:
        s = trim_excessive( s, self.excessiveStrsReplacement )
      if debug>0:
        print("Debug: #{} (type: {}, len={}, strip_len={})".format( idx, type(line), len(line), len(s) ) )
        print(s, "<<<")
      res.append( s )
    op.close()
    return (0, res)


  #
  # raw_content()
  #
  def raw_content (self, pReader, altChr="?"):
    toASCII = altChr=="ASCII"
    nPages = pReader.numPages
    res = []
    for pageNum in range( nPages ):
      tuv = pReader.getPage( pageNum ).extractText()
      assert type(tuv)==str
      pageCont = ""
      last = ""
      for c in tuv:
        r = c
        if ord( c )==0x2022:
          r = "$ "
        elif c=="~":
          if last==c:
            r = "\n"
        elif ord( c )>=127:
          if toASCII:
            r = xCharMap.simpler_ascii( c )
          elif altChr is not None:
            r = altChr
        pageCont += r
        last = c
      res.append( pageCont )
    return res


#
# trim_excessive()
#
def trim_excessive (s, chrs=(" ",)):
  assert type( chrs )==tuple or type( chrs )==list
  for tup in chrs:
    sep = ""
    if type( tup )==tuple:
      e = tup[ 0 ]
      sep = tup[ 1 ]
      assert type( sep )==str
    else:
      assert type( tup )==str
      e = tup
    ee = e + e
    if sep=="":
      last = s
      while True:
        s = s.replace( ee, e )
        if s==last:
          break
    else:
      idx = 9999
      while idx>=0:
        idx -= 1
        pos1 = s.find( ee )
        pos2 = s.rfind( ee )
        if pos1==-1 or pos1==pos2:
          break
        s = s.replace( ee, e )
      if pos1!=-1:
        s = s.replace( ee, sep )
  return s


#
# Globals
#
readerControl = ReaderControl()

#
# Main script
#
if __name__ == "__main__":
  import sys
  code = main_poco( sys.stdout, sys.stderr, sys.argv[ 1: ] )
  if code is None:
    print("""
poco.py Command [options]

Commands are:
   raw-pdf file [file ...]
       Show raw PDF chars.
""")
    code = 0
  assert type( code )==int
  assert code<=127
  sys.exit( code )
