# zexcess.py  (c)2020  Henrique Moreira

"""
  Simple Excel readout, respin of xcelat.py

  Compatibility: python 3.
"""


import zipfile
from xml.etree.ElementTree import iterparse


#
# CLASS ZTable()
#
class ZTable:
    def __init__ (self, t=[]):
        self.cols_hist = {}
        self.minCol = None
        self.maxCol = None
        self.numCols = None
        self.cont = []
        isOk = self._init_ztable( t )
        assert isOk


    def _init_ztable (self, t):
        if type( t )==list:
            if len( t )>0:
                self.add_rows( t, type(t[0]) )
            return True
        return False


    def add_rows (self, t, aType=dict):
        if aType==dict:
            for row in t:
                k = ';'.join( row.keys() ).split( ";" )
                k.sort()
                if len( k )<=0:
                    continue
                last = k[ -1 ]
                s = ';'.join( k )
                if s in self.cols_hist:
                    self.cols_hist[ s ] += 1
                else:
                    self.cols_hist[ s ] = 1
                if self.maxCol:
                    if last > self.maxCol:
                        self.maxCol = last
                else:
                    self.maxCol = last
                if self.minCol:
                    if last < self.minCol:
                        self.minCol = last
                else:
                    self.minCol = last
            nCol = column_number( self.maxCol )-column_number( 'A' )+1
            if self.numCols:
                if nCol > self.numCols:
                    self.numCols = nCol
            else:
                self.numCols = nCol
            for row in t:
                r = [""] * self.numCols
                for k, val in row.items():
                    colVal = column_number( k )
                    #print("::: colVal", colVal, "For column_number:", k, "nCol=", nCol, "maxCol=", self.maxCol)
                    s = self.best_cell( val.strip() )
                    r[ colVal - 1 ] = s
                self.cont.append( r )
        else:
            assert False
        return True


    def best_cell (self, s):
        try:
            f = float( s )
        except:
            f = None
        if f:
            v = f
        else:
            v = s
        return v


    def textual (self, s, decPlaces=None):
        if decPlaces is None:
            decPlaces = 9
        if type( s )==str:
            a = s
        elif type( s )==float:
            a = friendly_float( s, decPlaces )
        elif type( s )==int:
            a = str( s )
        else:
            a = "({})={}".format( type(s), s )
        return a


    def chr_separated (self, entry, sep=";"):
        if sep is None:
            return entry
        s = ""
        idx = 0
        if type( entry )==list or type( entry )==tuple:
            for a in entry:
                idx += 1
                if idx>1:
                    s += sep
                s += self.textual( a )
        return s


#
# ZSheets
#
class ZSheets():
    def __init__ (self, filename=None, sheets=[]):
        self.filename = filename
        if filename:
            tup = self.xlx_read( filename, sheets)
        else:
            tup = (None, None)
        self.sheets, self.cont = tup


    def xlx_read (self, filename, sheets=[], debug=0):
        z = zipfile.ZipFile( filename )
        try:
            strings = [el.text for e, el in iterparse(z.open('xl/sharedStrings.xml')) if el.tag.endswith('}t')]
        except:
            strings = []
        wSheets = []
        #worksheetName = "xl/worksheets/sheet1.xml"
        if len( sheets )<=0:
            iList = z.infolist()
            for zInfo in iList:
                fName = zInfo.filename
                for wDir in ["xl/worksheets/"]:
                    if fName.startswith( wDir ) and fName.endswith( ".xml" ):
                        wsName = fName[ len( wDir ):-4 ]
                        sheets.append( wsName )
        k = 0
        for w in sheets:
            k += 1
            worksheetName = "xl/worksheets/" + w + ".xml"
            sheetTag = "Sheet{}".format( k )    # TODO: use real xcel sheet name
            if debug>0:
                print("Debug: {}, '{}'".format( sheetTag, w ))
            wSheet = (w, worksheetName, sheetTag)
            wSheets.append( wSheet )

        sh = []
        for tup in wSheets:
            sh.append( self.xlx_read_sheet( z, strings, tup[ 1 ] ) )
        return (wSheets, sh)


    def xlx_read_sheet (self, z, strings, worksheetName, debug=0):
        rows = []
        row = {}
        value = ""
        if debug>0:
            print("Debug: xlx_read_sheet() '{}'".format( worksheetName ))
        for e, el in iterparse( z.open( worksheetName ) ):
            if el.tag.endswith('}v'): # <v>84</v>
                value = el.text
            if el.tag.endswith('}c'): # <c r="A3" t="s"><v>84</v></c>
                if el.attrib.get('t') == 's':
                    if value.isdigit():
                        value = strings[ int(value) ]
                    else:
                        value = "?"
                letter = el.attrib['r'] # AZ22
                while letter[-1].isdigit():
                    letter = letter[:-1]
                row[ letter ] = value
                value = ''
            if el.tag.endswith('}row'):
                rows.append(row)
                row = {}
        return rows


#
# column_number()
#
def column_number (letter):
    assert len( letter )>0
    v = 0
    if len( letter )==1:
        isOk = letter>='A' and letter<='Z'
        assert isOk
        v = ord( letter ) - ord( 'A' ) + 1
    else:
        for c in letter:
            v *= 26
            isOk = c>='A' and c<='Z'
            v += ord( c ) - ord( 'A' ) + 1
    return v


#
# num_to_column_letters()
#
def num_to_column_letters (n):
    assert type( n )==int
    assert n>0 and n<=9999
    s = ""
    while n > 0:
        n -= 1
        v = n % 26
        s = chr( ord('A')+v ) + s
        n //= 26
        if n<=0:
            break
    return s


#
# friendly_float()
#
def friendly_float (s, decPlaces, trimRight=True):
    prc = "{:."+str(decPlaces)+"f}"
    a = prc.format( s )
    if trimRight:
        if a.find(".")!=-1:
            a = a.rstrip("0").rstrip(".")
    return a


#
# Test suite
#
if __name__ == "__main__":
    print("Module, please import it!")
