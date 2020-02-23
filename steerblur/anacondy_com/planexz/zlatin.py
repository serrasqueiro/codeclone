# zlatin.py  (c)2020  Henrique Moreira

"""
  Latin-1 and related encodings.

  Compatibility: python 3.
"""

from redito import xCharMap

# pylint: disable=missing-docstring


def simpler_list(a, sep=None):
    res = []
    if isinstance(a, (list, tuple)):
        for elem in a:
            s = xCharMap.simpler_ascii(elem)
            res.append(s)
    else:
        return xCharMap.simpler_ascii(a)
    if sep is None:
        return res
    return sep.join(res)


def flow_list(a, pre, post="\n"):
    s = ""
    if isinstance(a, str):
        s = "{}{}{}".format(pre, a, post)
        return s
    if isinstance(a, (list, tuple)):
        for elem in a:
            s = "{}{}{}{}".format(s, pre, elem, post)
    return s


def numbered_list(a, num_start=1, sep="; "):
    x = num_start
    s = ""
    for el in a:
        elem_sep = "" if s == "" else sep
        shown = el if el else "''"
        s += "{}{}:{}".format(elem_sep, x, shown)
        x += 1
    return s


if __name__ == "__main__":
    print("Module, please import it!")
