# textmem.test.py  (c)2019  Henrique Moreira (part of 'jworks')

"""
  textmem.test - test module for textmem

  Compatibility: python 2 and 3.
"""

from textmem import *


#
# run_main()
#
def run_main (outFile, errFile, inArgs):
  code = None
  line = 0
  outName = None
  # Processing
  if inArgs==[]:
    return run_main(outFile, errFile, ["a"])
  cmd = inArgs[ 0 ]
  param = inArgs[ 1: ]
  # Checking options
  while len( param )>0 and param[ 0 ].startswith("-"):
    if param[ 0 ]=="-o":
      outName = param[ 1 ]
      del param[ :2 ]
      continue
    print("Wrong option:", param[ 0 ])
    return None
  if outName is not None:
    outFile = open(outName, "wb")
  # Work the commands
  if cmd=="d":  # Dump, with basic check
    inName = param[ 0 ]
    tm = TextMem()
    isOk = tm.from_file( inName )
    assert isOk
    for a in tm.cont:
      line += 1
      if a.endswith("\r"):
        a = a[ :-1 ]
      assert a.endswith("\r")==False
      s = a.rstrip()
      if s!=a:
        errFile.write("Line {}: dangling blanks/ tabs\n".format( line ))
      sOut = "{}\n".format( s )
      outFile.write(sOut.encode( tm.encoding ))
  if cmd=="p":  # Parse
    code = 0
    inName = param[ 0 ]
    tm = TextMem()
    tm.from_file( inName )
    tm.parse()
    for a in tm.leg:
      s = a
      sOut = "{}\n".format( s )
      outFile.write(sOut.encode( tm.encoding ))
  return code


#
# Main script
#
if __name__ == "__main__":
  import sys
  code = run_main(sys.stdout, sys.stderr, sys.argv[ 1: ])
  if code is None:
    code = 0
    print("""textmem.test [command]

Tests textmem module.""")
  assert type( code )==int
  sys.exit( code )
