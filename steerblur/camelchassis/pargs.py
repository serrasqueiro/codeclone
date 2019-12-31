# pargs.py  (c)2019  Henrique Moreira (part of 'camelchassis')

"""
  pargs module handles posix arguments.

  Compatibility: python 2 and 3.
"""


#
# test_pargs()
#
def test_pargs (outFile, errFile, inArgs):
  if inArgs==[]:
    args = ["command-a", "-i", "/tmp/abc", "-vvz", "arg1"]
  else:
    args = inArgs
  cmd = args[ 0 ]
  param = args[ 1: ]
  eq = {"-i":("--input", "--input-file",),
        }
  opts = arg_parse(param, eq)
  if opts is None:
    print("opts is None!")
    return 4
  for k, val in opts.items():
    if k!="~":
      print("key={}, val='{}'".format( k, val ))
  idx = 0
  for p in param:
    idx += 1
    print("Param#{}: {}".format( idx, p ))
  return 0


#
# arg_parse() -- posix-like argument parsing
#
def arg_parse (param, optEq={}, rest=True):
  dct = dict()
  assert type( param )==list
  # Check whether equivalent options are consistent
  for k, val in optEq.items():
    assert k[ 0 ]=="-"
    assert type( val )==tuple or type( val )==list
    assert len( val )>0
    for v in val:
      assert v.startswith( "-" )
  while len( param )>0 and param[ 0 ].startswith( "-" ):
    p = param[ 0 ]
    if p.startswith( "--" ):
      a = p[ 2: ]
      pos = a.find( "=" )
      if pos<0:
        dct[ a ] = 1
      elif pos>0:
        left = a[ :pos ]
        right = a[ pos+1: ]
        dct[ left ] = right
      else:
        return None
      del param[ 0 ]
    else:
      if p in optEq:
        opts = optEq[ p ]
        if len( param )<2:
          return None
        dct[ opts[0] ] = param[ 1 ]
        del param[ :2 ]
      else:
        a = p[ 1: ]
        for c in a:
          opt = "-" + c
          if opt in optEq:
            c = optEq[ opt ][ 0 ]
          if c in dct:
            dct[ c ] += 1
          else:
            dct[ c ] = 1
        del param[ 0 ]
  if rest:
    dct[ "~" ] = param
  return dct


#
# Test suite
#
if __name__ == "__main__":
  import sys
  code = test_pargs(sys.stdout, sys.stderr, sys.argv[ 1: ])
  assert type( code )==int
  if code!=0:
    sys.stderr.write("Error code: {}\n".format( code ))
  sys.exit( code )
