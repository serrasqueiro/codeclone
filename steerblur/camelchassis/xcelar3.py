# xcelar3.py  (c)2019  Henrique Moreira (part of 'camelchassis')

"""
  Simple Excel readout. Dumps 'AB' also.

  Compatibility: python 2 and 3.
"""

import datetime
import codecs
import zipfile
from xml.etree.ElementTree import iterparse
from redito import xCharMap


#
# test_xcelar3()
#
def test_xcelar3 (outFile, errFile, args):
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
    for filename in param:
      errFile.write("Reading Xcel: " + filename + "\n")
      rows = xcel_xlx_read( filename )
      idx = 0
      for row in rows:
        idx += 1
        isOk = True
        try:
          print( row )
        except:
          isOK = False
        if not isOk or row[ 'A' ]==43553:
          resume = str( row )[ :20 ]
          errFile.write("{:5}: ".format( tup[ 0 ] ) + resume + "\n")
  if cmdStr=="dump":
    validCmd = True
    #if out==sys.stdout:
    #  sys.stdout = rewrite( "" )
    #  out = sys.stdout
    for filename in param:
      rows = xcel_xlx_read( filename )
      rf = RexFilter( rows )
      rf.to_lines()
      idx = 0
      for row in rf.lines:
        idx += 1
        pre = ""
        for entry in row:
          s = basic_ascii( entry ).strip()
          out.write( pre + s )
          pre = "\t"
        out.write( "\n" )
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
        any = True
        del param[ 0 ]
        showBin = True
        continue
    showWarn = verbose>0
    if out==sys.stdout and showBin:
      sys.stdout = rewrite( "" )
      out = sys.stdout
    for filename in param:
      rows = xcel_xlx_read( filename )
      rf = RexFilter( rows )
      rf.to_lines()
      if rf.stats[ 1 ]>=1 and rf.y>=2:
        first = basic_ascii( rf.lines[ 0 ] )
        sec = basic_ascii( rf.lines[ 1 ] )
        isUniverso = sec.find( "'Data','Movimento'" )==0
        isABCred = first.find( " a Cr.dito ")>0
        if verbose>=2:
          print("rf #1", first)
          print("rf #2", sec, "sec type:", type(sec), "len:", len(sec))
        if isUniverso:
          del rows[ :2 ]
        if isABCred:
          del rows[ :2 ]
          conta = rows[ 0 ]
          del rows[ 0 ]
          maxNum = 9
          idx = 0
          for r in rows:
            idx += 1
            maxNum -= 1
            if maxNum<0:
              break
            tenseAscii = str( list_ascii( r ) )
            if tenseAscii.find( "Data Lanc.")>=0:
              break
          if maxNum>0:
            del rows[ :idx ]
      aSep = " " if verbose<=0 else " ; " if verbose>=2 else ";"
      idx = 0
      hasDate = False
      for r in rows:
        idx += 1
        if 'C' not in r:
          print("row#{} has no 'C'".format(idx), xCharMap.simpler_ascii( r ))
          continue
        if False:
          if r['C'].find("TRF")==0:
            print("E:", r['E'], "=", deval(r['E']), end='!')
        linear = None
        if 'C' in r:
          columnC = r['C']
        else:
          columnC = "(C)"
        if 'D' in r:
          columnD = basic_ascii( r['D'] )
        else:
          columnD = "?"
        if isABCred:
          r['E'] = r['A']
        if 'E' in r:
          try:
            m1 = columnD
            m2 = r['E']
            linear = r['A'] + aSep + r['B'] + aSep + columnC + aSep + m1 + aSep + m2
          except:
            s = "(unknown)"
        else:
          s = "#"+str(len(r)) + ";"
        if linear:
          exDateStr = r['A']
          isHeader = exDateStr.find( "Data" )==0
          tupDate = from_xcel_date( exDateStr )
          #print("isHeader:", isHeader, "; hasDate:", hasDate, "tupDate:", tupDate)
          if (hasDate or isABCred) and tupDate[ 0 ]!=0:
            aDate = tupDate[ 1 ]
          else:
            if isUniverso:
              aDate = exDateStr
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
            if isUniverso:
              desc = basic_ascii( r['B'] ).strip()
            else:
              desc = simpler_desc( columnC )
          if isUniverso:
            s = fmtDate + aSep + val2Str + aSep + desc
          elif isABCred:
            s = fmtDate + aSep + val1Str + aSep + desc.strip()
          else:
            s = fmtDate + aSep + val1Str + aSep + val2Str + aSep + desc
          basicStr = xCharMap.simpler_ascii( s )
          out.write( basicStr )
          out.write( "\n" )
        else:
          lineStr = "Line " + str( idx )+": "
          if showWarn:
            errFile.write( lineStr + s + "\n")
  if cmdStr=="raw":
    validCmd = True
    idx = 0
    for d in ([{'A':"col_one", 'B':"col_two", 'C':"three"}, {'B':"single"}],
              [{'C':"apple"}, {'AC':"cell"}]):
      idx += 1
      rf = RexFilter( d )
      rf.to_lines()
      print("\nTest", idx, "starts here:")
      print("Stats:", rf.stats)
      if rf.stats[ 3 ]>26:
        y = 0
        for row in rf.lines:
          y += 1
          x = 0
          for entry in row:
            x += 1
            cellName = rf.cell_name( y, x )
            if entry!="":
              print(cellName + ":", entry)
            assert type( entry )==str
      else:
        for row in rf.lines:
          print( row )
      print("<<<")
    for tup in [(26, "Z"), (27, "AA"), (28, "AB"), (29, "AC"), (30, "AD"),
                (221, "HM"), (286, "JZ"), (287, "KA"), (834, "AFB")]:
      x = tup[ 0 ]
      letras = rf.col_to_letter( x )
      isOk = letras==tup[ 1 ]
      print("Xcel columns:", x, letras, "OK" if isOk else "NotOk")
      assert isOk
  if validCmd==False:
    print("""Commands are:

dump		Dump Xcel as ASCII.

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
# basic_ascii()
#
def basic_ascii (s, sep=",", quotes="'"):
  res = ""
  if type( s )==list or type( s )==tuple:
    quotesLeft = quotes
    quotesRight = quotes
    for elem in s:
      if res!="":
        res += sep
      one = basic_ascii( quotesLeft + elem + quotesRight )
      res += one
  elif type( s )==int:
    res = str( s )
  else:
    for c in s:
      tic = "."
      if c>=' ' and c<='~':
        tic = c
      res += tic
  return res



#
# list_ascii()
#
def list_ascii (aList):
  res = []
  if type( aList )==list or type( aList )==tuple:
    for elem in aList:
      res.append( basic_ascii( elem ) )
  elif type( aList )==dict:
    for key, val in aList.items():
      res.append( [key, basic_ascii( val )] )
  return res


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
def xcel_xlx_read (filename, sheets=[], errFile=None, maxNumcols=-1):
  z = zipfile.ZipFile( filename )
  strings = [el.text for e, el in iterparse(z.open('xl/sharedStrings.xml')) if el.tag.endswith('}t')]
  rows = []
  row = {}
  value = ''
  iter = 0
  shownIter = 0
  tooManyCols = False
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
      numCols = len( row )
      if maxNumcols!=-1 and numCols>maxNumcols:
        tooManyCols = True
        break
      rows.append( row )
      row = {}
      iter += 1
      if errFile is not None:
        if shownIter<=0:
          errFile.write("Row: {}...\n".format( iter ))
          shownIter = 100
        shownIter -= 1
  if errFile is not None:
    strBogus = " Too many columns: {}".format( numCols )
    errFile.write("Row: {}...{}\n".format(iter, "" if not tooManyCols else strBogus))
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
# RexFilter
#
class RexFilter:
  def __init__ (self, rows=[]):
    self.table = rows
    self.lines = []
    self.init_stats()


  def init_stats (self, minCol=0, maxCol=0, minY=-1, maxY=0, emptyLine=0, nonDict=0):
    self.stats = ("min.col", minCol,
                  "max.col", maxCol,
                  "min.y", minY,
                  "max.y", maxY,
                  "empty.line", emptyLine,
                  "non.dict", nonDict,
                  "-", -1)
    self.y = maxY
    return True


  def letter_to_col_idx (self, c):
    if c=="":
      return 0
    one = c[ 0 ]
    if one<'A' or one>'Z':
      return 0
    v = 0
    for a in c:
      v *= 26
      if a<'A' or a>'Z':
        return -999
      v += ord(a)-ord('A')+1
    return v


  def col_to_letter (self, num):
    assert type( num )==int
    assert num>0
    res = ""
    val = num
    if val<=26:
      return chr( ord('A') + val - 1 )
    while val>0:
      val -= 1
      v = val % 26
      letra = chr( ord('A') + v )
      res = letra + res
      val = val // 26
    return res


  def cell_name (self, y, x, fixY="", fixX=""):
    assert type(y)==int
    assert type(x)==int
    if y>0 and x>0:
      return fixX + self.col_to_letter( x ) + fixY + str( y )
    assert False
    return ""


  def to_lines (self, idx=0):
    res = []
    minCol = 0
    maxCol = -1
    nonDict = 0
    nEmptyLines = 0
    y = 0
    isOk = True
    for r in self.table:
      y += 1
      n = len( r )
      isDict = type( r )==dict
      nEmptyLines += int( len( r )==0 )
      if isDict:
        colLo = -1
        colHi = -1
        for letra, val in r.items():
          col = self.letter_to_col_idx( letra )
          if col<colLo or colLo==-1:
            colLo = col
          if col>colHi:
            colHi = col
        col = colLo
        num = colHi
        if num<minCol or minCol==0:
          minCol = num
        if num>maxCol:
          maxCol = num
      else:
        nonDict += 1
        isOk = False
    for r in self.table:
      if type( r )==dict:
        i = idx
        row = []
        while i<maxCol:
          i += 1
          letra = self.col_to_letter( i )
          field = ""
          if letra in r:
            field = r[ letra ]
          row.append( field )
        self.lines.append( row )
    self.init_stats( minCol, maxCol, 0, y, nEmptyLines, nonDict )
    return isOk

#
# Test suite
#
if __name__ == "__main__":
  import sys
  print("*"*10, "superseeded by xcelat.py", "*"*10)
  if len( sys.argv )<=1:
    code = test_xcelar3( sys.stdout, sys.stderr, [ "xump", "a.xlsx" ] )
  else:
    code = test_xcelar3( sys.stdout, sys.stderr, sys.argv[ 1: ] )
  pass

