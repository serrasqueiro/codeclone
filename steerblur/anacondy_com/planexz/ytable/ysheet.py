# ysheet.py  (c)2020  Henrique Moreira

"""
  ysheet, yet another Xcel table sheet, OS-independent

  Compatibility: python 3.
"""

# pylint: disable=attribute-defined-outside-init

class XName():
    """
    Abstract class XName -- holds name and alias information
    """
    def _set_name(self, name=None):
        self.name = name
        self._alias = {"str": dict(),
                       }

    def get_alias(self, which=None):
        """
        Returns the alias for ...which.
        :param which: nick name of the alias
        :return: dict
        """
        if which is None:
            return self._alias
        return self._alias.get(which)


class XcelSheet(XName):
    """
    Workbook sheet helper
    """
    def __init__ (self, sheet_content=None, name=None):
        self._set_name(name)
        self.title = name
        self._sheet = sheet_content
        self.row_limits_y, self.row_limits_x = (0, 0), (0, 0)
        self.page = {"orientation": "portrait",  # xt._book._sheets[0].page_setup.orientation
                     "height,width": (None, None),  # xt._book._sheets[0].page_setup.paperHeight
                     "paperSize": 9,  # xt._book._sheets[0].page_setup.paperSize (9 = "A4")
                     "@paperSize": "A4",
                     }
        self._internal = {"encoding": "",
                          "@is_UTF8": True,
                          "column_dimensions": None,
                          "@col": tuple(),  # two columns: ("A", "B")
                          "@col:width": dict(),  # xt._book._sheets[0].column_dimensions["A"].width
                          "auto_filter": None,  # sheet.auto_filter
                          "@auto_filter": "",  # sheet.auto_filter.ref
                          "@auto_filter:rows": list(),
                          "@header": {"#rows": 0,
                                      "columns": [],  # ["A", "B"]
                                      "sub-row": [],  # [] (if applicable)
                                      "bold": [],  # ["A"] , the key columns
                                      "sample": None,  # header cell sample, e.g. tuple-6: (xcell.value, xcell.has_style, type(xcell.font), xcell.font, xcell.font.b, xcell.font.name)
                                      },
                          "@header:names": {"columns": [],
                                            "by-column-letter": dict(),
                                            }
                          }
        if sheet_content:
            self._init_sheet(self._sheet)


    def _init_sheet(self, sh):
        self.title = sh.title
        self.row_limits_y = (sh.min_row, sh.max_row)
        self.row_limits_x = (sh.min_column, sh.max_column)
        self._init_internal(sh)

    def _init_internal(self, sh):
        """
        Init internal vars/ dicts
        :param sh: sheet
        :return: void
        """
        def str_from_paper_size(sheet, xcel_size, def_str=""):
            if isinstance(xcel_size, int):
                sz = str(xcel_size)
            elif isinstance(xcel_size, str):
                sz = xcel_size
            else:
                assert False
            assert isinstance(def_str, str)
            if sz == sheet.PAPERSIZE_A4:
                s = "A4"
            elif sz == sheet.PAPERSIZE_LETTER:
                s = "Letter"
            elif sz == sheet.PAPERSIZE_A3:
                s = "A3"
            else:
                s = def_str
            return s

        sz = sh.page_setup.paperSize
        assert isinstance(sz, int)
        self.page["orientation"] = sh.page_setup.orientation
        self.page["height,width"] = (sh.page_setup.paperHeight, sh.page_setup.paperWidth)
        self.page["paperSize"] = sz
        self.page["@paperSize"] = str_from_paper_size(sh, sz, "unknown")
        self._internal["column_dimensions"] = sh.column_dimensions
        ks = list(sh.column_dimensions.keys())
        ks.sort()
        if "worksheet" in ks:
            idx = ks.index("worksheet")
            del ks[idx]
        self._internal["@col"] = tuple(ks)
        for letter in ks:
            assert len(letter) <= 4
            self._internal["@col:width"][letter] = sh.column_dimensions[letter].width
        is_utf8 = sh.encoding == "utf-8"
        self._internal["encoding"], self._internal["@is_UTF8"] = sh.encoding, is_utf8
        self._internal["auto_filter"] = sh.auto_filter
        self._internal["@auto_filter"] = sh.auto_filter.ref
        self._set_headers(sh.auto_filter.ref, sh.auto_filter)

    def _set_headers(self, s_filter_ref, auto_filter):
        def list_from_auto_filter_ref(s):
            assert isinstance(s, str)
            if not s:
                return []
            if not s.endswith(":"):
                q = s + ":"
            else:
                q = s
            spl = q.split(":")
            if len(spl) <= 1:
                spl = spl + spl
            row0 = row_number(spl[0])
            row1 = row_number(spl[1])
            if row0 > row1 or row0 <= 0 or row1 <= 0:
                return []
            a_list = []
            for idx in range(row0, row1+1):
                a_list.append(idx)
            return a_list

        self._internal["@auto_filter:rows"] = list()
        if s_filter_ref is None or auto_filter is None:
            return False
        assert isinstance(s_filter_ref, str)
        self._internal["@auto_filter:rows"] = list_from_auto_filter_ref(s_filter_ref)
        self._set_header_dicts(self._internal["@auto_filter:rows"])
        return True


    def _set_header_dicts(self, header_rows):
        sheet = self._sheet
        sub_row = []
        column_letters, column_names, bold_cols = [], [], []
        sample = None
        y, tries = 0, 20
        for row in sheet.iter_rows():
            tries -= 1
            if tries <= 0:
                break
            y += 1
            if y in header_rows:
                first = sub_row == []
                sub_row.append(row)
                num_cols = len(row)
                if first and num_cols > 0:
                    # Check if cells are non-empty
                    for cell in row:
                        s = cell.value
                        letra = cell.column_letter
                        is_bold = cell.font.b
                        if s:
                            if sample is None:
                                sample = get_sample(cell)
                            column_letters.append(letra)
                            column_names.append(field_clean_name(s))
                            if is_bold:
                                bold_cols.append(letra)
        self._internal["@header"]["#rows"] = len(header_rows)
        self._internal["@header"]["columns"] = column_letters
        self._internal["@header"]["sub-row"] = sub_row
        self._internal["@header"]["bold"] = bold_cols
        self._internal["@header"]["sample"] = sample
        self._internal["@header:names"]["columns"] = column_names
        self._internal["@header:names"]["by-column-letter"] = map_column_letter(column_letters, column_names)


    def get_header_numbers(self):
        """
        Get header row numbers
        :return: list, header rows
        """
        return self._internal["@auto_filter:rows"]

    def get_header_columns(self):
        return self._internal["@header"]["columns"]

    def get_header_column_names(self):
        return self._internal["@header:names"]["columns"]

    def get_header_column(self, letter=None):
            dct = self._internal["@header:names"]["by-column-letter"]
            if letter is None:
                return dct
            return dct[letter]

    def get_column_names(self):
        """
        Returns the column names, e.g. three columns, tuple ("A", "B", "C")
        :return: tuple (of strings)
        """
        return self._internal["@col"]

    def get_bold_headers(self):
        """
        Returns header columns with bold 'font'
        :return: tuple, names of bold headers and a second element with a list of header names
        """
        bold_cols = self._internal["@header"]["bold"]
        dct = self._internal["@header:names"]["by-column-letter"]
        res = []
        for letra in bold_cols:
            res.append(dct.get(letra))
        return (bold_cols, res)

    def column_dimension(self, col_ref=None):
        """
        Return the column dimensions
        :param col_ref: column letter (Xcel reference)
        :return: dictionary of dimensions, or just the individual column dimension (a float)
        """
        if col_ref is None:
            return self._internal["@col:width"]  # the whole dictionary with column widths
        return self._internal["@col:width"][col_ref]


    def encoding(self):
        """
        Returns the sheet encoding (usually 'utf-8')
        :return: string, the encoding name
        """
        return self._internal["encoding"]


    def set_sheet(self, sheet_content):
        """
        Set sheet, and initialize data members
        :param sheet_content: sheet
        :return: void
        """
        self._sheet = sheet_content
        self._init_sheet(self._sheet)


def row_number(s):
    """
    Return the row number of an Xcel column/row string reference
    :param s: input string
    :return: int, -1 on error, or the row number (1..n)
    """
    assert isinstance(s, str)
    idx = 0
    q = None
    for c in s:
        if c.isdigit():
            q = s[idx:]
            break
        idx += 1
    if q is None:
        return -1
    return int(q)


def get_sample(xcell):
    s = xcell.value
    return (s, xcell.has_style, type(xcell.font), xcell.font, xcell.font.b, xcell.font.name)


def field_clean_name(s):
    if isinstance(s, int):
        r = "field_{}".format(s)
    elif isinstance(s, str):
        r = s.replace("_", "")
    else:
        assert False
    return r


def map_column_letter(letters, names):
    assert len(letters) == len(names)
    dct = dict()
    idx = 0
    for letter in letters:
        name = names[idx]
        idx += 1
        dct[letter] = name
        dct[idx] = name  # maybe useful
    return dct


if __name__ == "__main__":
    print("Module, please import it!")
