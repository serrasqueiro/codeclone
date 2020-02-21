# zrules.py  (c)2020  Henrique Moreira

"""
  Simple rules for tables.

  Compatibility: python 3.
"""


class ZRules():
    """
    Class ZRules -- basic filtering rules for tables
    """
    def __init__(self, rules=None):
        self.key_columns = []
        is_ok = self._init_ztable(rules)
        assert is_ok


    def _init_ztable(self, rules):
        if rules is None:
            return True
        if isinstance(rules, (list, tuple)):
            self.key_columns = rules
            return True
        return False


    def dump(self):
        if self.key_columns != []:
            print(self.key_columns)


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
