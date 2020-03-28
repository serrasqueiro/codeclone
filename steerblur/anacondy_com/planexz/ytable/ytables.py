# ytables.py  (c)2020  Henrique Moreira

"""
  Xcel tables, OS-independent

  Compatibility: python 3.
"""

# pylint: disable=import-error, protected-access

import openpyxl.cell
from openpyxl import load_workbook


class XcelTable():
    """
    Tabular/ text tables
    """
    def __init__ (self, name=None, sheet_list=None):
        self.filename = name
        self._book = None
        self._cache = {"sheet": [],
                       "names": dict(),
                       }
        self._sheet_contents = {"@default": None}
        self.sheets_to_read = sheet_list if sheet_list else []
        assert isinstance(self.sheets_to_read, (list, tuple))
        if name:
            self._read_xcel(name)
        self._init_cache(self._book)


    def content(self, sheet_ref):
        """
        Get the sheet content for a sheet given its name or number (1 is the first)
        :param sheet_ref: Reference sheet name or number
        :return: sheet object
        """
        sheet = self._get_sheet_by_ref(sheet_ref)
        return sheet


    def get_sheet_names(self, get_invisible=False):
        """
        Get
        :return:
        """
        res = []
        assert isinstance(get_invisible, bool)
        for title, visible, _ in self._cache["sheet"]:
            if visible or get_invisible:
                res.append(title)
        return res


    def _init_cache(self, book):
        if book is None:
            return False
        sheets = book._sheets
        self._cache["sheet"] = []
        idx = 0
        for sheet in sheets:
            idx += 1
            title, visible, xml_path = sheet.title, sheet.sheet_state == "visible", sheet.path
            assert isinstance(title, str)
            self._cache["sheet"].append( (title, visible, xml_path) )
            self._cache["names"][title] = sheet
            self._cache["names"][idx] = sheet
        return True


    def _get_sheet(self, sheet_list):
        assert isinstance(sheet_list, (list, tuple))
        assert sheet_list != []
        res = []
        for sheet_name in sheet_list:
            if sheet_name != "":
                sheet = self._book.get_sheet_by_name(sheet_name)
                self._sheet_contents[sheet_name] = sheet
                res.append(sheet_name)
        return res


    def _read_xcel(self, filename):
        self._book = load_workbook(filename)
        cont = self._book.active
        self._sheet_contents["@default"] = cont


    def _get_sheet_by_ref(self, sheet_ref):
        if sheet_ref in self._cache["names"]:
            return self._cache["names"][sheet_ref]
        return None


class XCell():
    """
    Tabular/ text tables
    """
    _cell = None

    def __init__ (self, cell=None):
        self._cell = cell
        assert isinstance(cell, (openpyxl.cell.cell.Cell, type(None)))


    def get_font_str(self, back_newline=False):
        return self.get_attr_str(self._cell.font, "font", back_newline)


    def get_attr_str(self, a_var, a_type, back_newline):
        assert isinstance(back_newline, bool)
        xy = getattr(a_var, "__elements__", None)
        if back_newline:
            s = str(a_var)
            shown = s.replace("\n", "\\n")
        else:
            shown = self.get_string_from_attr(a_var, a_type, xy)
        return shown

    def get_string_from_attr(self, a_var, a_type, xy):
        assert isinstance(xy, (list, tuple))
        alist = []
        if xy is None:
            return str(a_var)
        if a_type == "font":
            for att in xy:
                shown = getattr(a_var, att)
                if shown is None:
                    continue
                #if isinstance(shown, openpyxl.styles.colors.Color) ...
                named_tag = getattr(shown, "tagname", None)
                if named_tag == "color":
                    pass
                else:
                    s = "{}={}".format(att, shown)
                    alist.append(s)
        else:
            return str(a_var)
        return ", ".join(alist)


def get_non_empty(alist, what_if=None, exclude=None):
    """
    Return the list of non-empty elements (what_if="") or non-None elements
    :param alist: input list
    :param what_if: what not to return
    :return: list
    """
    res = []
    excl_list = [] if exclude is None else exclude
    for x in alist:
        if x == what_if:
            continue
        if isinstance(x, str) and x in excl_list:
            continue
        res.append(x)
    return res


if __name__ == "__main__":
    print("Module, please import it!")
