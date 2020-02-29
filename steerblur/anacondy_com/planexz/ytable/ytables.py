# ytables.py  (c)2020  Henrique Moreira

"""
  Xcel tables, OS-independent

  Compatibility: python 3.
"""

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
        sheets = sheet_list if sheet_list else [""]
        if name:
            self._read_xcel(name, sheets)
        self._init_cache(self._book._sheets)


    def content(self, sheet_ref):
        sheet = self._get_sheet_by_ref(sheet_ref)
        return sheet


    def _init_cache(self, sheets):
        self._cache["sheet"] = []
        idx = 0
        for sheet in sheets:
            idx += 1
            title, visible, xml_path = sheet.title, sheet.sheet_state == "visible", sheet.path
            assert isinstance(title, str)
            self._cache["sheet"].append( (title, visible, xml_path) )
            self._cache["names"][title] = sheet
            self._cache["names"][idx] = sheet


    def _read_xcel(self, filename, sheet_list):
        assert isinstance(sheet_list, (list, tuple))
        self._book = load_workbook(filename)
        first = sheet_list[0]
        cont = self._book.active
        self._sheet_contents["@default"] = cont
        for sheet_name in sheet_list:
            if sheet_name != "":
                sheet = self._book.get_sheet_by_name(sheet_name)
                self._sheet_contents[sheet_name] = cont


    def _get_sheet_by_ref(self, sheet_ref):
        idx = 0
        if sheet_ref in self._cache["names"]:
            return self._cache["names"][sheet_ref]
        return None


if __name__ == "__main__":
    print("Module, please import it!")
