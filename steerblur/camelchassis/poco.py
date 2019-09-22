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
    print("Invalid option(s);\n", param)
    return None
  args = param
  if verbose>=3:
    print("Debug on!")
    debug = 1
  # Command run
  if cmd=="raw-pdf":
    inName = args[ 0 ]
    tup = readerControl.pdf_text( inName, "text", debug )
    code = tup[ 0 ]
    cont = tup[ 1 ]
    if code!=0:
      if code==2:
        errFile.write("Cannot read pdf: {}\n".format( inName ))
      else:
        errFile.write("No content: {}\n".format(inName))
      return code
    for a in cont:
      outFile.write("{}\n".format( a ))
    code = 0
  return code


#
# CLASS ReaderControl
#
class ReaderControl:
  def __init__ (self):
    self.initFuncOriginal = PyPDF2.pdf.PageObject.extractText


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
    if readKind=="text":
      PyPDF2.pdf.PageObject.extractText = extractText
    else:
      PyPDF2.pdf.PageObject.extractText = self.initFuncOriginal
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
      preDebug = "" if debug<=0 else " (type: {}, len={})".format( type(line), len(line) )
      if debug>0:
        aList = line.split( " " )
      else:
        aList = [line]
      s = "{}{}: {}".format( idx, preDebug, "\n".join( aList ) )
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
