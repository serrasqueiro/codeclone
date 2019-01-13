# python_parse.py  (c)2018  Henrique Moreira (part of 'camelchassis')

"""
  python_parse - Parse python files.

  Compatibility: python 2 and 3.
"""

import sys
from redito import TextRed, WildStr


#
# dump_usage()
#
def dump_usage ():
  print("""python_parse COMMAND [options] file(s)

Command is one of:
  dump      Dump (and check) input file(s).
\t\t-v    Verbose (or -v -v ...)
\t\t-o    Output to (use @@ for: similar as input)
\t\t-u    Force input to be Unix (no CRs)
""")
  sys.exit( 0 )


#
# test_python_parse()
#
def test_python_parse (outFile):
  own = sys.argv[ 0 ]
  tred = PyParse()
  isOk = tred.file_reader( own )
  assert isOk
  if True:
    idx = 0
    for line in tred.lines:
      idx += 1
      print(str(idx)+"\t"+line)
  isOk = tred.is_text_ok()
  assert isOk
  return 0



#
# python_parse()
#
def python_parse (outFile, args):
  code = 0
  didAny = False
  if len( args )<=0:
    dump_usage()
  cmd = args[ 0 ]
  del args[ 0 ]
  if cmd=="test":
    didAny = True
    code = test_python_parse( outFile )
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
  args = inArgs
  anyOpt = True
  forceUnix = False
  while anyOpt and len( args )>0:
    anyOpt = False
    if args[ 0 ]=='-v':
      anyOpt = True
      del args[ 0 ]
      verbose += 1
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
    pparse = PyParse()
    isOk = pparse.file_reader( aName )
    if isOk:
      likeUnix = forceUnix==False or (forceUnix==True and pparse.numCR==0)
      isTextOk = pparse.is_text_ok() and likeUnix
      invalidTabs = 0 if pparse.file_coname()!="PYTHON" else pparse.histogram.how_many( '\t' )
      semiEmptyLines = pparse.histogram.semiEmpty
      if isTextOk:
        if outName:
          ws = WildStr( outName )
          s = ws.by_pathname( aName )
          if s!=outName and isVerbose:
            sys.stderr.write("Output to: " + s + "\n")
          output = open( s, "w" )
        for aLine in pparse.lines:
          output.write(aLine + "\n")
        if outName:
          if isVerbose:
            if pparse.streamType!="TEXT":
              sys.stderr.write("Warn: " + aName + ": " + pparse.streamType + "\n")
          output.close()
      else:
        code = 8
        if likeUnix==False:
          code = 4
          sys.stderr.write("Skipping non-Unix file: " + aName + "\n")
        if isVerbose:
          print("#Read:", aName, "size:", pparse.byteSize, "; lines:", pparse.numLines, "numCR:", pparse.numCR, "clutter#", len(pparse.clutterChrs), pparse.clutterChrs)
          print("#Non-ASCII7:", pparse.nonASCII7)
      if invalidTabs:
        code = 6
        sys.stderr.write("Tabs found (in python-like files): " + aName + "\n")
      if len( semiEmptyLines )>0:
        sys.stderr.write("Line with blanks only: " + str( len(semiEmptyLines) ) + "\n")
        if isVerbose:
          sys.stderr.write("\tLine numbers:" + str(semiEmptyLines) + "\n")
    else:
      sys.stderr.write("Error dumping: " + aName + "\n")
  return code



#
# CLASS PyParse
#
class PyParse(TextRed):
  def top_init (self):
    self.buf = ""
    return True


  pass


#
# Test suite
#
if __name__ == "__main__":
  import sys
  code = python_parse( sys.stdout, sys.argv[ 1: ] )
  if type( code )==int and code>0:
    sys.exit( code )
  pass

