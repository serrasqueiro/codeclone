"""
  dictbas: basic dictionary helpers

  dictbas.py  (c)2020  Henrique Moreira
"""

# pylint: disable=missing-docstring


def search_id(dct, val, as_str=True):
    if isinstance(val, (int, float)):
        s = str(val) if as_str else val
    else:
        s = val
    for k in dct.keys():
        if dct[k] == s:
            return k
    return None


def dict_order(dct):
    if isinstance(dct, dict):
        order, vals = list(dct.keys()), dct
    else:
        return None
    order.sort()
    return order, vals


if __name__ == "__main__":
    print("Module only, do not run.")
