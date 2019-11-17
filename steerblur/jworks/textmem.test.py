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
  from sys import stdin
  code = None
  line = 0
  pOpt = {"allow-2-nl":True,
          }
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
    code = 0
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
        code = 1
        errFile.write("Line {}: dangling blanks/ tabs\n".format( line ))
      sOut = "{}\n".format( s )
      uops = tm.to_stream( outFile, tm.out_str( sOut, outName is None ) )!=0
      if uops:
        errFile.write("Converted line to: {}\n".format( tm.simpler_str( s ) ))
  if cmd=="p":  # Parse
    inName = param[ 0 ]
    tm = TextMem()
    if inName==".":
      myText = """
textmem.test python
KGMpMjAxOSAgSGVu
cmlxdWUgTW9yZWlyYQ==

Realfornelos, fun
http://xperteleven.com/players.aspx?TeamID=1845332&Boost=0&dh=1
"""
      tm.cont = myText.split("\n")
    else:
      tm.from_file( inName )
    tm.parse( pOpt )
    for a in tm.leg:
      if type( a )==str:
        s = a
      else:
        if len( a )<=1:
          s = "@\t{}\n".format( a[ 0 ] )
        else:
          s = "{}\n{}\n".format( a[ 0 ], a[ 1 ] )
      sOut = "{}\n".format( s )
      tm.to_stream( outFile, tm.out_str( sOut, outName is None ) )
    code = 0
    if tm.msgs!=[]:
      code = 1
      for msg in tm.msgs:
        errFile.write("Warn: {}\n".format( msg ))
  if cmd=="s":
    bm = Base64Mem()
    bm.hash_symbols()
    w = param[ 0 ] if len( param )>0 else None
    if w is None:
      fp = open(stdin, "r")
      s = fp.read()
    elif w==".":
      print("Base64 symbols:", bm.symbols)
    else:
      for c in w:
        d = ord( c )
        print("{}, #{}: {}".format( c, d, bm.hash[ d ] ))
    code = 0
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
