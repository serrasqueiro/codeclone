# boards.py  (c)2019  Henrique Moreira

"""
  Checker for svg boards.

  Compatibility: python 2 and 3.
"""


import sys
from ymap import YParse, f_open_to_read


#
# show_usage()
#
def show_usage ():
  print("""boards.py

Params are:
    check      Basic check of xml.

    dump       Dump internal struct(s).

    ludo-s     Check LUDO svg.
""")
  sys.exit( 0 )


#
# Main function
#
def run_boards (outFile, inArgs):
  code = 0
  verbose = 0
  cmd = inArgs[ 0 ]
  args = inArgs[ 1: ]
  errFile = sys.stderr
  #print("Command:", cmd, "args:", args)
  didAny = True
  while didAny and len( args )>0:
    didAny = False
    if args[ 0 ].find( '-v' )==0:
      didAny = True
      verbose += args[ 0 ].count( 'v' )
      del args[ 0 ]
      continue

  # Main shirp!
  xp = YParse()
  didAny = False
  if cmd=="check":
    didAny = True
    if len( args )<=0:
      show_usage()
    inName = args[ 0 ]
    f = f_open_to_read( inName )
    preStr = inName + ": "
    if not f:
      errFile.write(preStr + "cannot open.\n")
      return 2
    isOk = xp.add_data( f.read() )>=0
    if not isOk:
      errFile.write(preStr + "Trailing stuff.\n")
      return 11
    isOk = len( xp.aStack )==0
    if not isOk:
      errFile.write(preStr + "Stack is not empty.\n")
      return 12
  if cmd=="dump":
    didAny = True
    if len( args )<=0:
      show_usage()
    inName = args[ 0 ]
    f = f_open_to_read( inName )
    if f:
      xp.add_data( f.read() )
      for se in xp.contents:
        s = se.props + se.tag
        if se.text!="":
          print("TEXT:", se.text)
        else:
          print("TAG:", s)
        if verbose>0:
          print( se )
      if verbose>1:
        for aProp in xp.props:
          print("PROP:", aProp)
    else:
      errFile.write("Bogus...\n")
      return 2
  if not didAny:
    show_usage()
  assert code==0
  return code


#
# Main script
#
if __name__ == "__main__":
  import sys
  code = 0
  if len( sys.argv )<=1:
    show_usage()
  else:
    code = run_boards( sys.stdout, sys.argv[ 1: ] )
  sys.exit( code )
