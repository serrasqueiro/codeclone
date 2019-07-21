# gen_dat.py  (c)2019  Henrique Moreira (part of 'mlaby')

"""
  gen_dat is a multi-generic module, handles hex bases, etc.

  Compatibility: python 2 and 3.
"""

#
# test_gen_dat()
#
def test_gen_dat (outFile, errFile, me, inArgs):
  code = None
  if me=="gen_dat":
    if inArgs==[]:
      return None
    cmd = inArgs[ 0 ]
    return basic_gen_dat( outFile, errFile, cmd, inArgs[ 1: ] )
  else:
    print("me:", me)
    assert False  # ToDo...!
  return code


#
# basic_gen_dat()
#
def basic_gen_dat (outFile, errFile, cmd, inArgs):
  args = inArgs
  code = 0
  if cmd=="conv":
    for num in args:
      if num=="":
        continue
      isHex = num.startswith( "0x" )
      if isHex:
        conv = conv_hex( num )
        if conv is None:
          code = 11
          errFile.write("Error {}, invalid hex: {}\n".format( code, num ))
        else:
          outFile.write("{}\n".format( conv ))
      else:
        try:
          n = int( num )
        except:
          n = None
        if n is None:
          errFile.write("Uops: {}\n".format( num ))
        else:
          b = conv_to_binary( n )
          outFile.write("{}b\n".format( b ))
      if code!=0:
        return code
    return 0
  return None


#
# conv_hex()
#
def conv_hex (num):
  bug = None
  if type( num )==str:
    try:
      d = int( num, 16 )
      conv = d
    except:
      bug = "conv"
  elif type( num )==list or type( num )==tuple:
    res = []
    for a in num:
      res.append( conv_hex( a ) )
    return res
  else:
    assert False
  if bug:
    return None
  return conv


#
# conv_to_binary()
#
def conv_to_binary (num):
  if type( num )==int:
    if num>=0 and num<256:
      conv = "{0:08b}".format( num )
    else:
      s = bin( num )
      assert s[ :2 ]=="0b"
      conv = s[ 2: ]
  else:
    assert False
  return conv


#
# find_back()
#
def find_back (s, anyOf):
  assert s is not None
  found = None
  aLen = len( s )
  if type( s )==str:
    idx = aLen-1
    while idx>=0:
      c = s[ idx ]
      if c in anyOf:
        found = c
        return found, idx
      idx -= 1
  return found, -1


#
# strip_back()
#
def strip_back (s, anyOf, skipFound=True):
  found, pos = find_back( s, anyOf )
  if found is None:
    return s
  xtra = len( found ) if skipFound else 0
  return s[ pos+xtra: ]


#
# strip_fwd()
#
def strip_fwd (s, anyOf, skipFound=True):
  found, pos = find_back( s, anyOf )
  if found is None:
    return s
  xtra = 0 if skipFound else len( found )
  return s[ :pos+xtra ]


#
# Test suite
#
if __name__ == "__main__":
  import sys
  prog = strip_fwd( strip_back( sys.argv[ 0 ], ("\\", "/") ), "." )
  code = test_gen_dat( sys.stdout, sys.stderr, prog, sys.argv[ 1: ] )
  if code is None:
    code = 0
    print("""gen_dat.py

If script is gen_dat.py:
  conv [num ...]
            Shows the numbers 'num', ...
""")
  sys.exit( code )
