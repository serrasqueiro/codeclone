# textlike.py  (c)2018  Henrique Moreira (part of 'vdbser')

"""
  textlike - Read and process text-like files.

  Compatibility: python 2 and 3.
"""

import sys
from redito import BareText


#
# dump_usage()
#
def dump_usage ():
  print("""textlike COMMAND [options] file(s)

Command is one of:
  dump      Dump input file(s), 7bit-ASCII
\t\t-v    Verbose (or -v -v ...)
\t\t-o    Output to (use @@ for: similar as input)
\t\t-u    Force input to be Unix (no CRs)
""")
  sys.exit( 0 )


#
# test_textlike()
#
def test_textlike (outFile, args):
  code = 0
  dumpClass = True
  own = sys.argv[ 0 ]
  if len( args )>0:
    own = args[ 0 ]
  tred = BareText()
  isOk = tred.file_reader( own )
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
  if didAny==False:
    dump_usage()
  return code



#
# do_dump()
#
def do_dump (outFile, inArgs):
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
  isVerbose = verbose>0
  # Process args (inputs):
  for aName in args:
    tred = BareText()
    tred.file_reader( aName )
    isOk = forceUnix==False or (forceUnix and tred.numCR==0)
    if isOk:
      if outName and not curOut:
        outFile = open( outName, "w" )
        curOut = outFile
      for aLine in tred.lines:
        outFile.write( aLine + "\n" )
    else:
      sys.stderr.write("Not unix: " + aName + "\n")
  if curOut:
    outFile.close()
  return code


#
# Test suite
#
if __name__ == "__main__":
  import sys
  code = textlike( sys.stdout, sys.argv[ 1: ] )
  if type( code )==int and code>0:
    sys.exit( code )
  pass

