# zlatin.py  (c)2020  Henrique Moreira

"""
  Latin-1 and related encodings.

  Compatibility: python 3.
"""

from waxpage.redit import char_map

# pylint: disable=missing-docstring


def simpler_list(a, sep=None):
    res = []
    if isinstance(a, (list, tuple)):
        for elem in a:
            s = char_map.simpler_ascii(elem)
            res.append(s)
    else:
        return char_map.simpler_ascii(a)
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
    """
    Helper to show a list as a string,
    each element of the list is preceded by an index 1..n
    :param a: list
    :param num_start: start indexes from (1)
    :param sep: separator between list elements
    :return: string, the full list string
    """
    x = num_start
    s = ""
    for el in a:
        elem_sep = "" if s == "" else sep
        shown = el if el else "''"
        s += "{}{}:{}".format(elem_sep, x, shown)
        x += 1
    return s


def cur_format(x, width=12, tail_blank=" "):
    """
    Currency format
    :param x: float, money
    :param width: general indentation width
    :param tail_blank: add a blank at the end in case of two decimals only,
                       or None: to not add anything
    :return: string, the indented currency number
    """
    dec_places = 3
    if tail_blank is None:
        tail_blank = ""
    if isinstance(x, int):
        y = float(x)
    else:
        y = x
    fmt = "{"+":{}.{}f".format(width, dec_places)+"}"
    s = fmt.format(y)
    pos = s.rfind(".")
    if 0 < pos < len(s) and s[-1] == "0":
        s = s[:-1] + tail_blank
    return s


if __name__ == "__main__":
    print("Module, please import it!")
