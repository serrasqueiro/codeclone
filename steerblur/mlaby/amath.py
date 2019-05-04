# amath.py  (c)2018  Henrique Moreira (part of 'luke')

"""
  amath module handles diverse math functions

  Compatibility: python 2 and 3.
"""

#
# test_amath()
#
def test_amath (out, inArgs):
  code = 0
  args = inArgs
  if len( args )>0:
    v = args[ 0 ]
  else:
    v = 901
  while v < 1001:
    p = is_prime( v )
    print("v:", v, "is_prime()?", "Yes" if p else "No")
    v += 2
  return code


#
# CLASS CalcNum
#
class CalcNum:
  def __init__(self):
    pass


#
# atoi() -- any string or type to integer
#
def atoi (a, defaultValue=0):
  if type( a )==int:
    return a
  if type( a )==float:
    return int( a )
  if type( a )==str:
    try:
      v = int( a )
    except:
      v = None
  if v is None:
    return defaultValue
  return v


#
# afloat() -- strict conversion of float from string
#
def afloat (aStr, defaultValue=0.0):
  assert type( aStr )==str
  assert type( defaultValue )==float
  try:
    v = float( aStr )
  except:
    v = None
  if v is None:
    v = 0.0
  return v


#
# is_prime()
#
def is_prime (aNum):
  n = atoi( aNum )
  for i in range(2,int(n**0.5)+1):
    if n%i==0:
      return False
  return True


#
# Test suite
#
if __name__ == "__main__":
  import sys
  outFile = sys.stdout;
  code = test_amath( outFile, sys.argv[ 1: ] )
  sys.exit( code )

