# zexcess.py  (c)2020  Henrique Moreira

"""
  Simple Excel readout, respin of xcelat.py

  Compatibility: python 3.
"""


import zipfile
from xml.etree.ElementTree import iterparse
from redito import xCharMap


class ZRefs():
    def init_zrefs(self):
        self.str_ref = dict()


    def _add_ref(self, s_simpler, s_original):
        if s_simpler in self.str_ref:
            self.str_ref[s_simpler].append(s_original)
        else:
            self.str_ref[s_simpler] = s_original


class ZTable(ZRefs):
    """
    Class ZTable -- xcel tables
    """
    def __init__(self, t=[], strict_charset=None):
        self.cols_hist = {}
        self.minCol = None
        self.maxCol = None
        self.numCols = None
        self.cont = []
        self.strict_ch = strict_charset
        assert strict_charset in (None,
                                  "latin-like",
                                  )
        self.init_zrefs()
        isOk = self._init_ztable(t)
        assert isOk


    def _init_ztable(self, t):
        if isinstance(t, list):
            if len(t) > 0:
                self.add_rows( t, type(t[0]) )
            return True
        return False


    def add_rows(self, t, aType=dict):
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
                    a_val = self._normal_s_value(val)
                    s = self.best_cell(a_val)
                    r[ colVal - 1 ] = s
                self.cont.append( r )
        else:
            assert False
        return True


    def best_cell(self, s):
        try:
            f = float( s )
        except ValueError:
            f = None
        if f:
            v = f
        else:
            v = s
        return v


    def textual(self, s, decPlaces=None):
        if decPlaces is None:
            decPlaces = 9
        if isinstance(s, str):
            a = s
        elif isinstance(s, float):
            a = friendly_float( s, decPlaces )
        elif isinstance(s, int):
            a = str(s)
        else:
            a = "({})={}".format(type(s), s)
        return a


    def chr_separated(self, entry, sep=";"):
        if sep is None:
            return entry
        s = ""
        idx = 0
        if isinstance(entry, (list, tuple)):
            for a in entry:
                idx += 1
                if idx>1:
                    s += sep
                s += self.textual( a )
        return s


    def alt_chr_separated(self, entry, adapt, sep=";"):
        tryBlanks = True
        if sep is None:
            return self.chr_separated(entry, None)
        s = ""
        idx = 0
        if isinstance(entry, (list, tuple)):
            faceToAll = adapt.get( "*" )
            if faceToAll is not None:
                assert isinstance(faceToAll, dict)
            for a in entry:
                idx += 1
                if idx>1:
                    s += sep
                letra = num_to_column_letters(idx)
                aText = self.textual( a )
                face = adapt.get( letra )
                if face is not None or faceToAll is not None:
                    if face is None: face = faceToAll
                if face is not None:
                    repl = face.get( "replace" )
                    if repl is not None:
                        for a, b in repl:
                            for tryReplace in ("normal", "strip" if tryBlanks else ""):
                                if tryReplace=="": break
                                assert a!=b
                                assert a!=""
                                if tryReplace=="strip":
                                    aStr = cut_excess( aText )
                                else:
                                    aStr = aText
                                q = aStr.replace(a, b)
                                if q!=aText:
                                    aText = q
                                    break
                s += aText
        return s


    def _normal_s_value(self, s):
        if isinstance(s, str):
            if self.strict_ch is not None:
                res = xCharMap.simpler_ascii(s)
                if res != s:
                    self._add_ref(res, s)
            else:
                res = s
        else:
            res = s
        return res


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


    def contents (self):
        return self.sheets, self.cont


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


def num_to_column_letters(n):
    """ num_to_column_letters() -- A1, Z23, ... """
    assert isinstance(n, int)
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


def friendly_float (s, decPlaces, trimRight=True):
    """ friendly_float() -- float to string """
    prc = "{:."+str(decPlaces)+"f}"
    a = prc.format( s )
    if trimRight:
        if a.find(".")!=-1:
            a = a.rstrip("0").rstrip(".")
    return a


def cut_excess (s, cutWhat=(("  ", " "), ("\t", " "))):
    """ cut_excess() -- remove excessive blanks """
    if isinstance(s, str):
        q = s
        for this, by in cutWhat:
            if this=="" or this==by: break
            count = 10**4
            while count>0:
                count -= 1
                r = q.replace( this, by )
                if q==r: break
                q = r
            assert count>0
        res = q
    else:
        assert False
    return res


def expand_adapt (d):
    """ expand_adapt() """
    def basic_rules (rule, there=None):
        assert isinstance(rule, dict)
        r = dict()
        if there is None:
            for k, val in rule.items():
                assert isinstance(val, tuple)
                r[ k ] = list( val )
        else:
            assert isinstance(there, dict)
            # there is e.g. '{"replace", tuple("a","b")}'
            for k, tup in rule.items():
                val = list(tup)
                there[ k ] += val
        return r
    assert isinstance(d, dict)
    count = 0
    toDel = []
    copy = dict()
    byName = list( d.keys() )
    byName.sort()
    for k in byName:
        val = d[ k ]
        count += 10
        cols = k.split(";")
        if len( cols )>1:
            toDel.append( k )
            for c in cols:
                count += 1
                if c in copy:
                    basic_rules( val, copy[ c ] )
                else:
                    copy[ c ] = basic_rules( val )
        else:
            copy[ k ] = basic_rules( val )
    for k in toDel:
        del d[ k ]
    for k, val in copy.items():
        d[ k ] = val
    return count


#
# Test suite
#
if __name__ == "__main__":
    print("Module, please import it!")
