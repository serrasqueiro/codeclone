# bdebug.py  (c)2020  Henrique Moreira

""" Basic Debug module
"""

# pylint: disable=missing-docstring

ANY_DEBUG = 1

debug_area = {
    'sample': 1,
    }


def main_test():
    """ Basic test """
    print("...\nIf you have defined ANY_DEBUG, you will see the next line.\n")
    dprint("sample", "Please import", __file__)
    print(".")


def debug_level() -> int:
    try:
        debug = ANY_DEBUG
    except NameError:
        debug = 0
    return int(debug)


def bprint(*args) -> bool:
    """ Basic debug print """
    return dprint('', *args)


def cprint(debug, *args) -> bool:
    """ Conditional debug print """
    if debug <= 0:
        return False
    return dprint('', *args)


def dprint(area, *args) -> bool:
    debug = debug_level()
    if debug <= 0:
        return False
    if area and debug_area[area] <= 0:
        return False
    if area:
        show = f"[{area}] "
    else:
        show = ""
    if len(args) <= 0:
        return True
    print(show, end='')
    print(*args)
    return True



#
# Main script
#
if __name__ == "__main__":
    print(f"Please import {__file__}")
    main_test()
