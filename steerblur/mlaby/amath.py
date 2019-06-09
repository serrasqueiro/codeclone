# amath.py  (c)2019  Henrique Moreira (part of 'mlaby')

"""
  amath module handles diverse math functions

  Compatibility: python 2 and 3.
"""

from sys import maxsize
from os import environ

#
# test_amath()
#
def test_amath (out, inArgs):
  code = 0
  if inArgs==["seq"]:
    args = [10, 10**2, 10**3, 10**4, 10**5, 10**6, 10**7, 10**8, 10**9, 10**10]
  else:
    args = inArgs
  if len( args )>0:
    lst = []
    for a in args:
      if a=="97a":
        v = a
      else:
        if calcNum.is_word( a ):
          h = calcNum.basic_whash( a )
          # with PYTHONHASHSEED=12346007, hash1000("Henrique")=479
          print(a, "; hash:", h, "hash():", calcNum.hash1000(a))
          continue
        v = atoi( a )
      p = calcNum.is_prime( v )
      print("v:", v, "is_prime()?", p, "; divisor by:", calcNum.lastDiv)
      try:
        i = previous_prime( v )
      except:
        i = -1
      print("Previous prime:", i if i>1 else "None?" if i!=-1 else "Non-string")
      lst.append ( i )
    count = 0
    pre = "("
    for v in lst:
      count += 1
      print(pre+str(v)+",", end="")
      pre = ""
    if count>0:
      print(")")
    return 0
  for tup in [(7,10), (980,1000), (9951,10000), (99951,100000)]:
    v = tup[ 0 ]
    up = tup[ 1 ]
    while v < up:
      p = is_prime( v )
      print("v:", v, "is_prime()?", "Yes" if p else "No", end="")
      if p:
        last = v
      else:
        print("; divisor by:", calcNum.lastDiv, end="")
      print("")
      v += 1+int( calcNum.is_odd(v) )
    print("Highest prime of", up, "is:", last, "Perc.:", "{:0.3f}%".format( last/up*100.0 ))
  return code


#
# CLASS CalcNum
#
class CalcNum:
  def __init__ (self):
    self.lastDiv = -1
    self.hashed = False
    self.lastPrimes = None
    self.randomicHash = None
    pass


  def init_hash (self):
    if self.randomicHash is None:
      self.randomicHash = 12346007
      environ[ "PYTHONHASHSEED" ] = str( self.randomicHash )
    if self.hashed:
      return False
    # last prime of each power, 10^n, n=1..10:
    self.lastPrimes = (7,97,997,9973,99991,999983,9999991,99999989,999999937,9999999967,)
    # Note: 10^9 < 2^32 < 10^10
    self.hashed = True
    for v in self.lastPrimes:
      assert is_prime(v)
    return True


  def hash (self, obj, power=9):
    if type( obj )==str:
      return self.hash1000( obj, power )
    res = []
    for a in obj:
      res.append( self.hash( a, power ) )
    return res


  def hash1000 (self, s, power=3):
    assert self.lastPrimes is not None
    nonNegativeK = maxIntSize
    if power>=1:
      m = self.lastPrimes[ power-1 ]
    else:
      assert power>=0
      m = 999983
    return 1 + (custom_hash( s ) % nonNegativeK) % m


  def is_odd (self, num):
    return (num % 2)!=0


  def is_even (self, num):
    return (num % 2)==0


  def is_prime (self, num):
    n = atoi( num, None )
    if n is None:
      return False
    return is_prime( num )


  def basic_whash (self, word):
    """Basic word hash.

    Args:
      word (str): the word string for the hash.

    Returns:
      int: the hash for the entered word.
    """
    if type( word )==str:
      w = word.lower() + "." + word.upper()  # any dummy concatentation
      if self.is_word( word ):
        h = self.hash1000( w )
      else:
        h = 0
      return h
    elif type( word )==list:
      res = []
      for elem in word:
        res.append( self.bash_whash( elem ) )
      return res
    assert False


  def is_word (self, word, allowDash=""):
    any = False
    if type( word )==str:
      c = None
      for c in word.lower():
        if c>='a' and c<='z':
          any = True
        else:
          if c not in allowDash:
            return False
      if c is not None:
        if c in allowDash:  # cannot be the latest char
          return False
    return any


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
def is_prime (n):
  calcNum.lastDiv = -1
  if n <= 1:
    calcNum.lastDiv = n
    return False
  for i in range(2,int(n**0.5)+1):
    if n%i==0:
      calcNum.lastDiv = i
      return False
  calcNum.lastDiv = n
  return True


#
# previous_prime()
#
def previous_prime (n):
  while n > 1:
    n -= 1
    p = is_prime( n )
    if p:
      return n
    n -= int( (n%2)!=0 )
  return 1


#
# custom_hash()
#
def custom_hash (obj):
  # Hint:	# export PYTHONHASHSEED=12346007
  res = hash( obj )
  return res


#
# Globals
#
calcNum = CalcNum()
calcNum.init_hash()
maxIntSize = ((maxsize + 1) * 2)


#
# Test suite
#
if __name__ == "__main__":
  import sys
  outFile = sys.stdout;
  code = test_amath( outFile, sys.argv[ 1: ] )
  sys.exit( code )

