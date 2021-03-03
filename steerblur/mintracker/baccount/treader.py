# -*- coding: iso-8859-1 -*-
# treader.py  (c)2020  Henrique Moreira (part of 'mintracker')

""" Module for reading txu semi-colon separated files with accounts
"""

# pylint: disable=unused-argument

import sys
import os.path

MAIN_EXT = ".txu"
CONAME_EXT = ".txy"


def main():
    """ Main function """
    myprog = __file__
    code = run_main(sys.argv[1:])
    if code is None:
        print(f"""{myprog} COMMAND [options] txu-file [...]

Commands are:
  check

Options are:
  - tbd.
""")
    sys.exit(code if code else 0)


def run_main(args):
    """ Main basic module test.
    """
    if not args:
        return None
    cmd = args[0]
    param = args[1:]
    if cmd == "check":
        code = do_check(param)
        return code
    return None


def do_check(param):
    """ Do check input '.txu' files
    """
    for fname in param:
        code = reader(fname, ".".join(fname.split('.')[:-1]))
        if code:
            print(f"Error-code {code}: cannot process: {fname}")
            return code
    return 0


def reader(fname, base) -> int:
    is_ok = os.path.isfile(fname)
    if not is_ok:
        return 2
    if not base:
        return 3
    ext = fname[fname.rfind('.'):]
    if ext == MAIN_EXT:
        coname = base + CONAME_EXT
    else:
        coname = fname + CONAME_EXT
    print("NAME:", fname, "; CONAME:", coname)
    return 0


# Main script
if __name__ == "__main__":
    main()
