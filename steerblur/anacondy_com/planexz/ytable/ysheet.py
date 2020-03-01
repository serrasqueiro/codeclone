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
                          }
        if sheet_content:
            self._init_sheet(self._sheet)


    def _init_sheet(self, sh):
        self.title = sh.title
        self.row_limits_y = (sh.min_row, sh.max_row)
        self.row_limits_x = (sh.min_column, sh.max_column)
        self._init_internal(sh)

    def _init_internal(self, sh):
        sz = sh.page_setup.paperSize
        self.page["orientation"] = sh.page_setup.orientation
        self.page["height,width"] = (sh.page_setup.paperHeight, sh.page_setup.paperWidth)
        self.page["paperSize"] = sz
        self.page["@paperSize"] = "A4" if sz == 9 else "unknown"  # ToDo
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
        return True


    def get_header_numbers(self):
        """
        Get header row numbers
        :return: list, header rows
        """
        return self._internal["@auto_filter:rows"]


    def get_column_names(self):
        """
        Returns the column names, e.g. three columns, tuple ("A", "B", "C")
        :return: tuple (of strings)
        """
        return self._internal["@col"]

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


if __name__ == "__main__":
    print("Module, please import it!")
