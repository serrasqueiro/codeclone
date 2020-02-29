# zexcess.py  (c)2020  Henrique Moreira

"""
  Simple Excel readout, respin of xcelat.py

  Compatibility: python 3.
"""

# pylint: disable=missing-function-docstring, line-too-long, invalid-name, no-self-use

import zipfile
from xml.etree.ElementTree import iterparse
from ztable.textual import trim_text
from redito import xCharMap


class ZRefs():
    """
    ZRefs (abstract) class
    """
    def init_zrefs(self):
        self.str_ref = dict()


    def _add_ref(self, s_simpler, s_original):
        if s_simpler in self.str_ref:
            self.str_ref[s_simpler].append(s_original)
        else:
            self.str_ref[s_simpler] = [s_original]


class ZTable(ZRefs):
    """
    Class ZTable -- xcel tables
    """
    def __init__(self, t=None, strict_charset=None):
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
        if t is None:
            return True
        if isinstance(t, list):
            if len(t) > 0:
                self.add_rows(t, type(t[0]))
            return True
        return False


    def add_rows(self, t, aType=dict):
        if aType == dict:
            for row in t:
                k = ';'.join( row.keys() ).split( ";" )
                k.sort()
                if len(k) <= 0:
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
                if idx > 1:
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
                if idx > 1:
                    s += sep
                letra = num_to_column_letters(idx)
                aText = self.textual( a )
                face = adapt.get( letra )
                if face is not None or faceToAll is not None:
                    if face is None:
                        face = faceToAll
                if face is not None:
                    repl = face.get( "replace" )
                    if repl is not None:
                        for r, b in repl:
                            for tryReplace in ("normal", "strip" if tryBlanks else ""):
                                if tryReplace == "":
                                    break
                                assert r != b
                                assert r != ""
                                if tryReplace == "strip":
                                    aStr = trim_text(aText)
                                else:
                                    aStr = aText
                                q = aStr.replace(r, b)
                                if q != aText:
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


class ZSheets():
    """
    ZSheets class -- xcel sheet(s)
    """
    def __init__ (self, filename=None, sheets=None):
        self.filename = filename
        self._sheet_wb_list, self._sheet_wb_dict = None, dict()
        if filename:
            tup = self.xlx_read( filename, sheets)
        else:
            tup = (None, None)
        self.sheets, self.cont = tup


    def contents (self):
        return self.sheets, self.cont


    def xlx_read (self, filename, sheets=None, debug=0):
        z = zipfile.ZipFile( filename )
        sheet_list = sheets if sheets is not None else []
        try:
            stream = z.open('xl/sharedStrings.xml')
        except FileNotFoundError:
            stream = None
        if stream is None:
            strings = []
        else:
            strings = [el.text for e, el in iterparse(stream) if el.tag.endswith('}t')]
        self._get_workbook_list(z)
        wSheets = []
        #worksheetName = "xl/worksheets/sheet1.xml"
        if len(sheet_list) <= 0:
            iList = z.infolist()
            for zInfo in iList:
                fName = zInfo.filename
                for wDir in ["xl/worksheets/"]:
                    if fName.startswith( wDir ) and fName.endswith(".xml"):
                        wsName = fName[ len( wDir ):-4 ]
                        sheet_list.append( wsName )
        for w in sheet_list:
            sheet_file = self._sheet_wb_dict.get(w)
            if sheet_file is None:
                sheet_file = w
                sheet_tag = w
            else:
                sheet_tag = sheet_file
            worksheet_filename = "xl/worksheets/" + sheet_file + ".xml"
            wSheets.append( (w, worksheet_filename, sheet_tag) )

        sh = []
        for _, worksheet_filename, _ in wSheets:
            sh.append( self.xlx_read_sheet(z, strings, worksheet_filename) )
        return (wSheets, sh)


    def xlx_read_sheet (self, z, strings, worksheetName, debug=0):
        rows = []
        row = dict()
        value = ""
        if debug > 0:
            print("Debug: xlx_read_sheet() '{}'".format( worksheetName ))
        for _, el in iterparse( z.open( worksheetName ) ):
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
                row = dict()
        return rows


    def _get_workbook_list(self, z):
        if "xl/workbook.xml" not in z.NameToInfo:
            return None
        name_seq = []
        with z.open('xl/workbook.xml') as wb:
            itp = iterparse(wb)
            wb_list = [el.attrib for e, el in itp if el.tag.endswith('}sheet')]
        # wb_list[0]["name"], wb_list[0]["sheetId"], wb_list[0]["{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"]
        self._sheet_wb_list = []
        idx = 0
        for d_sheet in wb_list:
            idx += 1
            sheet_ref = "sheet{}".format(idx)
            xml_id = []
            for key, val in d_sheet.items():
                if key.endswith("}id"):
                    assert xml_id == []
                    simpler_key = key.split("{")[1].split("}")[-1]
                    assert simpler_key.startswith("id")
                    xml_id.append( (simpler_key, val, ("complete-sheet-ref", key)) )
            sheet_name = d_sheet["name"]
            name_seq.append(sheet_name)
            self._sheet_wb_list.append( (sheet_name, d_sheet["sheetId"], xml_id) )
            self._sheet_wb_dict[sheet_name] = sheet_ref
        self._sheet_wb_dict["@sheets"] = name_seq
        return name_seq


def column_number (letter):
    """
    Column number, from letter
    :param letter: input letter
    :return: the column number
    """
    assert len(letter) > 0
    v = 0
    if len(letter) == 1:
        if letter.isupper():
            v = ord(letter) - ord('A') + 1
        else:
            v = -1
    else:
        for c in letter:
            v *= 26
            if not c.isupper():
                v = -1
                break
            v += ord(c) - ord('A') + 1
    assert v >= 0
    return v


def num_to_column_letters(n):
    """ num_to_column_letters() -- A1, Z23, ... """
    assert isinstance(n, int)
    assert 0 < n <= 9999
    s = ""
    while n > 0:
        n -= 1
        v = n % 26
        s = chr( ord('A')+v ) + s
        n //= 26
        if n <= 0:
            break
    return s


def friendly_float (s, decPlaces, trimRight=True):
    """ friendly_float() -- float to string """
    prc = "{:."+str(decPlaces)+"f}"
    a = prc.format( s )
    if trimRight:
        if a.find(".") != -1:
            a = a.rstrip("0").rstrip(".")
    return a


def cut_excess (s):
    """ cut_excess() -- remove excessive blanks """
    return trim_text(s)


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
        if len(cols) > 1:
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
