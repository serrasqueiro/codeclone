# xcelar3.py  (c)2019  Henrique Moreira (part of 'camelchassis')

"""
  Simple Excel readout.

  Compatibility: python 2 and 3.
"""

import codecs
import zipfile
from xml.etree.ElementTree import iterparse


#
# test_xcelar3()
#
def test_xcelar3 (outFile, args):
  validCmd = False
  code = 0
  cmdStr = args[ 0 ]
  param = args[ 1: ]
  out = outFile
  showWarn = True
  if cmdStr=="xump":
    validCmd = True
    if out==sys.stdout:
      sys.stdout = rewrite( "" )
      out = sys.stdout
    for filename in param:
      rows = xcel_xlx_read( filename )
      for r in rows:
        s = str( r )
        out.write( s + '\n' )
  if cmdStr=="abmp":
    validCmd = True
    if out==sys.stdout:
      sys.stdout = rewrite( "" )
      out = sys.stdout
    for filename in param:
      rows = xcel_xlx_read( filename )
      aSep = " "
      idx = 0
      for r in rows:
        idx += 1
        linear = None
        if 'E' in r:
          try:
            m1 = r['D']
            m2 = r['E']
            linear = r['A'] + aSep + r['B'] + aSep + r['C'] + aSep + m1 + aSep + m2
          except:
            s = "(unknown)"
        else:
          s = "#"+str(len(r)) + ";"
        if linear:
          excDate = '{:>9}'.format( r['A'] )
          v1 = deval( m1 )
          v2 = deval( m2 )
          val1Str = '{:9.2f}'.format( v1 )
          val2Str = '{:9.2f}'.format( v2 )
          isHeader = r['A'].find( "Data" )==0
          if isHeader:
            val1Str = '{:9}'.format("Valor")
            val2Str = '{:9}'.format("Saldo")
            continue
          s = excDate + aSep + val1Str + aSep + val2Str + aSep + r['C']
          out.write( s + "\n" )
        else:
          lineStr = "Line " + str( idx )+": "
          if showWarn:
            sys.stderr.write( lineStr + s + "\n")
  if validCmd==False:
    print("""Commands are:

xump		Dump internal structure.
abmp		Dump AB.
""")
    return 0
  return code


#
# rewrite()
#
def rewrite (encoding=""):
  enc = "ISO-8859-1" if encoding=="" else encoding
  sys.stdout = codecs.getwriter( enc )(sys.stdout)
  out = sys.stdout
  return out


#
# deval()
#
def deval (m):
  try:
    f = float( m )
  except:
    f = 0.0
  return f


#
# xcel_xlx_read() -- read from xlsx
#
def xcel_xlx_read (filename, sheets=[]):
  z = zipfile.ZipFile( filename )
  strings = [el.text for e, el in iterparse(z.open('xl/sharedStrings.xml')) if el.tag.endswith('}t')]
  rows = []
  row = {}
  value = ''
  worksheetName = "xl/worksheets/sheet1.xml"
  if len( sheets )>0:
    worksheetName = "xl/worksheets/" + sheets[ 0 ] + ".xml"
  for e, el in iterparse( z.open( worksheetName ) ):
    if el.tag.endswith('}v'): # <v>84</v>
      value = el.text
    if el.tag.endswith('}c'): # <c r="A3" t="s"><v>84</v></c>
      if el.attrib.get('t') == 's':
        value = strings[int(value)]
      letter = el.attrib['r'] # AZ22
      while letter[-1].isdigit():
        letter = letter[:-1]
      row[letter] = value
      value = ''
    if el.tag.endswith('}row'):
      rows.append( row )
      row = {}
  return rows


#
# Test suite
#
if __name__ == "__main__":
  import sys
  if len( sys.argv )<=1:
    code = test_xcelar3( sys.stdout, [ "xump", "a.xlsx" ] )
  else:
    code = test_xcelar3( sys.stdout, sys.argv[ 1: ] )
  pass

