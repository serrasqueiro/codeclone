# boards.py  (c)2019  Henrique Moreira

"""
  Checker for svg boards.

  Compatibility: python 2 and 3.
"""


import sys
from ymap import *
from redito import BareText, xCharMap
from playlists import *
from os import getcwd


#
# show_usage()
#
def show_usage ():
  print("""boards.py

Params are:
    check      Basic check of xml.

    dump       Dump internal struct(s).

    playlist   Dump playlist

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
    else:
      if verbose>0:
        print("Opened:", inName)
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
      content = f.read()
      if len( content )<(xp.stepWiseProgress * 10):
        xp.report = None
      xp.add_data( content )
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
      if verbose>0:
        atStr = "at " + getcwd() + "; file: "
      errFile.write("Bogus: " + atStr + inName + "\n")
      return 2
  if cmd=="playlist":
    didAny = True
    if len( args )<=0:
      listed = [0]
    else:
      listed = args
    for name in listed:
      isWPL = False
      isStdin = type( name )==int
      tred = BareText()
      if not isStdin:
        fileExt = file_extension( name )
        isWPL = fileExt==".wpl"
      useUTF_input = isWPL
      if isStdin:
        isOk = tred.file_reader()
        assert isOk
      else:
        if useUTF_input:
          isOk = tred.utf_file_reader( name )
        else:
          isOk = tred.file_reader( name )
      if not isOk:
        errFile.write("Bogus: " + name + "\n")
        return 2
      isOk = len( tred.nonASCII7 )==0
      if verbose>=2:
        props = tred.to_str().split( "\n" )
        print("playlist", "OK" if isOk else "NotOk", ":", props[ 0 ] if props[ 0 ]!="" else "(stdin)")
        print('\n'.join( props[ 1: ] ))
      wp = WpList()
      if verbose>0:
        for aLine in tred.lines:
          print(aLine)
      else:
        xp.tolerateCR = False
        idx = 0
        for aLine in tred.lines:
          idx += 1
          xp.add_data( aLine, idx )
        for aProp in xp.props:
          isEnclosed = aProp[ 0 ]==3
          s = aProp[ 1 ]
          isSrc = isEnclosed and s.find( "<media src=" )==0 and s[ -2: ]=="/>"
          if isSrc:
            src = s[ len( "<media src=" ):-2 ].strip()
            wp.add_src( src )
        print( wp )
      if not isOk:
        code = 1
      pass

  if not didAny:
    show_usage()
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
