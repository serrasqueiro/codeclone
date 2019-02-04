# xcelar3.py  (c)2019  Henrique Moreira (part of 'camelchassis')

"""
  Simple Excel readout. Dumps 'AB' also.

  Compatibility: python 2 and 3.
"""

import datetime
import codecs
import zipfile
from xml.etree.ElementTree import iterparse


#
# test_xcelar3()
#
def test_xcelar3 (outFile, args):
  validCmd = False
  code = 0
  verbose = 0
  cmdStr = args[ 0 ]
  param = args[ 1: ]
  out = outFile
  showWarn = False
  showBin = False
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
    any = True
    while len( param[ 0 ] )>0 and any:
      any = False
      if param[ 0 ].find( "-v" )==0:
        verbose += param[ 0 ].count( "v" )
        any = True
        del param[ 0 ]
        continue
      if param[ 0 ]=="-b":
        showBin = True
    showWarn = verbose>0
    if out==sys.stdout and showBin:
      sys.stdout = rewrite( "" )
      out = sys.stdout
    for filename in param:
      rows = xcel_xlx_read( filename )
      aSep = " " if verbose<=0 else " ; " if verbose>=2 else ";"
      idx = 0
      hasDate = False
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
          exDateStr = r['A']
          isHeader = exDateStr.find( "Data" )==0
          tupDate = from_xcel_date( exDateStr )
          #print("isHeader:", isHeader, "; hasDate:", hasDate, "tupDate:", tupDate)
          if hasDate and tupDate[ 0 ]!=0:
            aDate = tupDate[ 1 ]
          else:
            aDate = "#"+exDateStr
          fmtDate = '{:>10}'.format( aDate )
          v1 = deval( m1 )
          v2 = deval( m2 )
          val1Str = '{:9.2f}'.format( v1 )
          val2Str = '{:9.2f}'.format( v2 )
          if isHeader:
            hasDate = True
            val1Str = '{:9}'.format("Valor")
            val2Str = '{:9}'.format("Saldo")
            if verbose<3:
              continue
          if isHeader:
            desc = "Descricao"
          else:
            desc = simpler_desc( r['C'] )
          s = fmtDate + aSep + val1Str + aSep + val2Str + aSep + desc
          out.write( s )
          out.write( "\n" )
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
# from_xcel_date()
#
def from_xcel_date (sXcelDate):
  # xcel date 42139 is ordinal 735733
  fail = False
  minDate = 42139
  try:
    i = int( sXcelDate )
  except:
    fail = True
  if fail or i<minDate or i>99999:
    return (0, sXcelDate)
  oDate = i - minDate + 735733
  return (oDate, xcel_str_date( datetime.datetime.fromordinal( oDate )))


#
# xcel_str_date()
#
def xcel_str_date (dttm, sep='-'):
  s = '{:04}'.format( dttm.year ) + sep + '{:02}'.format( dttm.month ) + sep + '{:02}'.format( dttm.day )
  return s


#
# simpler_desc()
#
def simpler_desc (s):
  res = s
  any = True
  while any:
    keep = res
    res = res.replace( "  ", " " ).replace( ";", ":," )
    any = keep!=res
  return res


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

