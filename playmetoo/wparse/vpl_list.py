#-*- coding: utf-8 -*-
# vpl_list.py  (c)2021  Henrique Moreira

"""
VUPlayer run samples: dumps Playlist *.vpl files
"""

# pylint: disable=unused-argument, missing-function-docstring

import sys
from wparse.vpl import VPL


def main():
    """ Main script """
    code = run(sys.stdout, sys.stderr, sys.argv[1:])
    if code is None:
        print("""python vpl.py file [...]
""")
    sys.exit(code if code else 0)


def run(out, err, args) -> int:
    """ Main tests for classes """
    param = args
    verbose = 0
    while param and param[0].startswith("-"):
        if param[0].startswith("-v"):
            verbose += int(param[0].count("v"))
            del param[0]
            continue
        return None
    if not param:
        return None
    opts = {
        "verbose": verbose,
    }
    return run_param(out, err, param, opts)

def run_param(out, err, param, opts) -> int:
    """ Main function """
    for name in param:
        assert not name.startswith("-")
    for name in param:
        code = dump_vpl(out, err, name, opts)
        if err:
            err.write(f"VPL('{name}'), code={code}\n")
        if code:
            return code
    return code

def dump_vpl(out, err, name, opts) -> int:
    """ Dump playlist
    """
    vpl = VPL(name)
    astr = vpl.text()
    if out:
        out.write(astr)
    code = vpl.parse()
    if opts["verbose"] <= 0:
        return code
    print("#" * 20, "vpl.parse() follows:")
    for entry in vpl.content:
        keys = sorted(entry.keys())
        for key in keys:
            there = entry[key]
            print(f"{key}={there}")
        print("")
    return code

# Main script
if __name__ == "__main__":
    # import importlib; importlib.reload(wparse.vpl); from wparse.vpl import *
    main()
