# python_parse.py  (c)2018  Henrique Moreira (part of 'camelchassis')

"""
  python_parse - Parse python files.

  Compatibility: python 2 and 3.
"""


from redito import TextRed


#
# dump_usage()
#
def dump_usage ():
  print("""python_parse COMMAND [options]

Command is one of:
  dump      Dump (and check) input file(s).
""")
  return 0


#
# test_python_parse()
#
def test_python_parse (outFile):
  return 0



#
# python_parse()
#
def python_parse (outFile, args):
  code = 0
  if len( args )<=0:
    return dump_usage()
  cmd = args[ 0 ]
  del args[ 0 ]
  if cmd=="dump":
    code = do_dump( outFile, args )
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
  while anyOpt and len( args )>0:
    anyOpt = False
    if args[ 0 ]=='-v':
      anyOpt = True
      del args[ 0 ]
      verbose += 1
    if args[ 0 ]=='-o':
      anyOpt = True
      outName = args[ 1 ]
      del args[ :2 ]
  isVerbose = verbose>0
  # Process args (inputs):
  for aName in args:
    pparse = PyParse()
    isOk = pparse.file_reader( aName )
    if isOk:
      isTextOk = pparse.is_text_ok()
      invalidTabs = 0 if pparse.file_coname()!="PYTHON" else pparse.histogram.how_many( '\t' )
      semiEmptyLines = pparse.histogram.semiEmpty
      if isTextOk:
        if outName:
          output = open( outName, "w" )
        for aLine in pparse.lines:
          output.write(aLine + "\n")
        if outName:
          output.close()
      else:
        code = 8
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

