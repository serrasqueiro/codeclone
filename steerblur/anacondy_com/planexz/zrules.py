# zrules.py  (c)2020  Henrique Moreira

"""
  Simple rules for tables.

  Compatibility: python 3.
"""

from ztable.xdate import MsDate, MsTime


class ZRules():
    """
    Class ZRules -- basic filtering rules for tables
    """
    def __init__(self, rules=None):
        self.key_columns = []
        self.header = []
        self.header_hash = dict()
        self.content = []
        is_ok = self._init_ztable(rules)
        assert is_ok


    def _init_ztable(self, rules):
        if rules is None:
            return True
        if isinstance(rules, (list, tuple)):
            self.key_columns = rules
            return True
        return False


    def set_heading(self, str_list):
        if isinstance(str_list, list):
            self.header = str_list
            column_index = 0
            for a in str_list:
                column_index += 1
                if a not in self.header_hash:
                    self.header_hash[a] = column_index


    def dump(self):
        if self.key_columns != []:
            print(self.key_columns)


def cell_string(cell, d, default_s="", debug=0):
    assert isinstance(d, str)
    if d == "date":
        mDate = MsDate(cell)
        if mDate.jDate:
            if debug > 0:
                s = "{}='{}'".format(mDate, cell)
            else:
                s = str(mDate)
        else:
            s = default_s
    elif d == "time":
        mTime = MsTime(cell)
        if debug > 0:
            s = "{}='{}'".format(mTime, cell)
        else:
            s = str(mTime)
    elif d == "float":
        if cell == "":
            s = default_s
        else:
            y = float(cell)
            spl = "{:.9f}".format(y).split(".")
            assert len(spl) == 2
            tail = spl[1].rstrip("0")
            if tail == "":
                shown = spl[0]
            else:
                shown = spl[0] + "." + tail
            if debug > 0:
                s = "({})={}".format(cell, shown)
            else:
                s = shown
    elif d == "int":
        s = int(cell) if cell else ""
    else:
        s = cell
    return s


def work_column_defs(s):
    """
    Work on those columns, defined by user arguments.
    """
    if s is None:
        return None
    cols = ["."] + s.split(":")
    return cols


def keys_from_str(s):
    """
    Work on those columns, defined by user arguments.
    """
    res = []
    if isinstance(s, str):
        names = s.split(":")
        for a in names:
            if a == "":
                return None
            res.append(a)
    return res


if __name__ == "__main__":
    print("Module, please import it!")
