# textlike.py  (c)2018  Henrique Moreira (part of 'vdbser')

"""
  textlike - Read and process text-like files.

  Compatibility: python 2 and 3.
"""

import sys
from redito import BareText, xCharMap


#
# dump_usage()
#
def dump_usage ():
  print("""textlike COMMAND [options] file(s)

Command is one of:
  dump      Dump input file(s), 7bit-ASCII
  iso-dump  Dump input file(s), near_text() 7bit-ASCII
  utf-dump  Similar to iso-dump, but input is UTF-8
\t\t-v    Verbose (or -v -v ...)
\t\t-o    Output to (use @@ for: similar as input)
\t\t-u    Force input to be Unix (no CRs)
""")
  sys.exit( 0 )


#
# test_textlike()
#
def test_textlike (outFile, inArgs):
  code = 0
  verbose = 0
  dumpClass = True
  args = inArgs
  anyOpt = True
  while anyOpt and len( args )>0:
    anyOpt = False
    if args[ 0 ].find( '-v' )==0:
      anyOpt = True
      verbose += args[ 0 ].count( 'v' )
      del args[ 0 ]
      continue
  own = sys.argv[ 0 ]
  if own.endswith( "latin1_test.py" ):
    return own_latin1_test( args )
  if len( args )>0:
    inName = args[ 0 ]
    param = args[ 1: ]
  else:
    inName = own
    param = []
  tred = BareText( inName )
  if tred.extension_matches( "PS" ):
    code = test_treat_pdf( tred, param )
    isOk = True
  else:
    isOk = tred.file_reader( inName )
  assert isOk
  if True:
    idx = 0
    for line in tred.lines:
      idx += 1
      print(str(idx)+"\t"+line)
  isOk = tred.is_text_ok()
  code = int( isOk==False )
  if dumpClass:
    print(tred.inFilename, "is_text_ok()?", tred.is_text_ok(), "extension:", tred.extension)
    print("numLines:", tred.numLines, "CRs:", tred.numCR)
    print("byteSize:", tred.byteSize, "noEOL?", tred.noEOL)
    print("clutterChrs len:", len( tred.clutterChrs ), "nonASCII7 len:", len( tred.nonASCII7))
    print("skipNonASCII7bit?", tred.skipNonASCII7bit)
  sys.stderr.write("Code: " + str(code) + "\n")
  return code


#
# test_treat_pdf()
#
def test_treat_pdf (tred, param):
  import PyPDF2
  pdfName = tred.get_filename()
  print("Debug test_treat_pdf:", pdfName, "; param:", param)

  read_pdf = PyPDF2.PdfFileReader(pdfName)
  for i in range(read_pdf.getNumPages()):
    page = read_pdf.getPage(i)
    print('Page No - ', 1 + read_pdf.getPageNumber(page))
    page_content = page.extractText()
    print()
    print( page_content )
  return 0


#
# textlike()
#
def textlike (outFile, inArgs):
  code = 0
  didAny = False
  args = inArgs
  if len( args )<=0:
    dump_usage()
  cmd = args[ 0 ]
  del args[ 0 ]
  if cmd=="test":
    didAny = True
    code = test_textlike( outFile, args )
  if cmd=="dump":
    didAny = True
    code = do_dump( outFile, args )
  if cmd=="iso-dump":
    didAny = True
    # TODO!
    assert False
    code = do_dump( outFile, args, "latin1" )
  if cmd=="utf-dump":
    didAny = True
    code = do_dump( outFile, args, "utf-8" )
  if didAny==False:
    dump_usage()
  return code


#
# do_dump()
#
def do_dump (outFile, inArgs, dumpType="dump"):
  code = 0
  verbose = 0
  output = outFile
  outName = None
  curOut = None
  args = inArgs
  anyOpt = True
  forceUnix = False
  while anyOpt and len( args )>0:
    anyOpt = False
    if args[ 0 ].find( '-v' )==0:
      anyOpt = True
      verbose += args[ 0 ].count( 'v' )
      del args[ 0 ]
      continue
    if args[ 0 ]=='-u' or args[ 0 ]=='--force-unix':
      anyOpt = True
      del args[ 0 ]
      forceUnix = True
      continue
    if args[ 0 ]=='-o':
      anyOpt = True
      outName = args[ 1 ]
      del args[ :2 ]
      continue
    if args[ 0 ][ 0 ]=='-':
      dump_usage()
  # Process args (inputs):
  for aName in args:
    tred = BareText()
    if dumpType=="utf-8":
      readOk = tred.utf_file_reader( aName )
    else:
      readOk = tred.file_reader( aName )
    if not readOk:
      sys.stderr.write("Uops: " + aName + "\n")
      return 2
    isOk = forceUnix==False or (forceUnix and tred.numCR==0)
    if isOk:
      if outName and not curOut:
        outFile = open( outName, "w" )
        curOut = outFile
      for aLine in tred.lines:
        outFile.write( aLine + "\n" )
    else:
      sys.stderr.write("Not unix: " + aName + "\n")
    if verbose>=2:
      aLen = len( tred.nonASCII7 )
      if aLen>0:
        print("Latin1 chars, is_text_ok()?", tred.is_text_ok())
        for a in tred.nonASCII7:
          print( "Line", str(a[0])+": column:", a[1], a[2] )
  if curOut:
    outFile.close()
  return code


#
# own_latin1_test() -- pre-filled tests
#
def own_latin1_test (inArgs):
  args = inArgs
  print("ARGS:", args)
  print("")
  a = """ISO8859-1 (Latin-1) text:
"c\xE3o vir\xE1 na dire\xE7\xE3o certa, abre a p\xE1gina diz \xD3scar \xE0 \xE9gua!"

\xE1\xE9\xED\xF3\xFA
\xE0....
\xC1\xC9\xCD\xD3\xDA
\xC0....
\xE3..\xF5.
\xC3..\xD5.

Cedil:
\x09\xE7\xC7
"""
  aList = a.split( "\n" )
  for lineStr in aList:
    s = xCharMap.simpler_ascii( lineStr )
    t = xCharMap.simpler_ascii( lineStr, 1 )
    if s=="":
      continue
    print("s:", s)
    print("t:", t)
    lastS = s
    print("")
  isOk = lastS.strip()=="cC"
  assert isOk
  return 0


#
# Main script
#
if __name__ == "__main__":
  import sys
  code = textlike( sys.stdout, sys.argv[ 1: ] )
  sys.exit( code )

