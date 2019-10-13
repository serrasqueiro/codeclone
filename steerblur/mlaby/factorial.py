"""
 factorial.py -- (c)2019 Henrique Moreira
"""


#
# main - at this script
#
def main (outFile, inArgs):
  args = inArgs
  if args==[]:
    args = ["3", "5"]
  for n in args:
    if n.find( "." )>=0:
      n = float( n )
    try:
      fato = fact( n )
    except:
      fato = None
    s = "" if fato is not None else " (Invalid value)"
    print("{}! = {}{}".format( n, fato, s ))
  return 0


#
# fact() -- mathematical factorial function, n!
#
def fact (nonNegativeNumber):
  assert type( nonNegativeNumber )!=float
  n = int( nonNegativeNumber )
  if n < 0:
    return -1  # error
  num = 1
  while n >= 1:
    num = num * n
    n = n - 1
  return num


if __name__=="__main__":
  import sys
  code = main( sys.stdout, sys.argv[ 1: ] )
  assert type( code )==int
  sys.exit( code )
