"""
String and list utilities

(c)2020  Henrique Moreira (part of 'draftdb', util)
"""

# pylint: disable=missing-docstring


def any_of(s, tup):
    """
    Finds whether any of chars in 'tup' is within string 's'
    :param s: input string
    :param tup: tuples
    :return: int, the ASCII character (integer), or -1 if none found
    """
    if not tup:
        return -1
    if isinstance(s, str):
        for c in s:
            d = ord(c)
            for tic in tup:
                if isinstance(tic, tuple):
                    op, num = tic
                    if op == ">":
                        match = d > int(num)
                    elif op == "<":
                        match = d < int(num)
                    else:
                        assert False
                elif isinstance(tic, str):
                    match = c == tic
                else:
                    assert False
                if match:
                    return d
    else:
        assert False
    return -1


def dict_order(dct, byName="a"):
    """
    Returns the keys and dictionary
    :param dct: dictionary
    :param byName: "a": ascending, "z": descending
    :return: keys, dictionary
    """
    do_revert = False
    if byName == "z":
        do_revert = True
    elif byName == "a":
        pass
    else:
        assert False
    if isinstance(dct, dict):
        keys = list(dct.keys())
    elif isinstance(dct, (list, tuple)):
        keys = dct
    else:
        assert False
    keys.sort(reverse=do_revert)
    return keys, dct


def expand_list(lst, pre="", cardinal=None, post="\n"):
    """
    Returns the string for the expanded list
    :param lst: list
    :param pre: string before each line
    :param post: string at the tail of each line
    :return: string
    """
    s = ""
    if cardinal:
        try:
            start_at = int(cardinal)
        except ValueError:
            start_at = 1
        s_cardinal = ": " if cardinal != "#" else ". "
    else:
        start_at = 0
    idx = start_at
    for row in lst:
        before = pre
        if cardinal:
            before = "{}{}{}".format(pre, idx, s_cardinal)
        s += before
        s += "{}".format(row)
        s += post
        idx += 1
    return s


#
# Main script
#
if __name__ == "__main__":
    print("Module, no run!")
