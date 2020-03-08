"""
String and list utilities

(c)2020  Henrique Moreira (part of 'draftdb', util)
"""

# pylint: disable=missing-docstring


def any_of (s, tup):
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


#
# Main script
#
if __name__ == "__main__":
    print("Module, no run!")
