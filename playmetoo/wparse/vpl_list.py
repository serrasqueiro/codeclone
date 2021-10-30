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
    verbose = opts["verbose"]
    for name in param:
        assert not name.startswith("-")
    method = "fields" if verbose > 0 else "text"
    for name in param:
        code = dump_vpl(out, err, name, method, opts)
        if err:
            err.write(f"VPL('{name}'), code={code}\n")
        if code:
            return code
    return code

def dump_vpl(out, err, name, method:str, opts) -> int:
    """ Dump playlist
    """
    vpl = VPL(name)
    astr = vpl.text()
    code = vpl.parse()
    if method == "text":
        if out:
            out.write(astr)
        return code
    assert method == "fields"
    if opts["verbose"] > 1:
        print("#" * 20, "vpl.parse() follows", "#" * 20)
    for entry in vpl.content:
        for key in sorted(entry):
            there = entry[key]
            shown_key = key[1:] if key[0] < 'A' else key
            print(f"{shown_key}={there}")
        print("")
    return code

# Main script
if __name__ == "__main__":
    # import importlib; importlib.reload(wparse.vpl); from wparse.vpl import *
    main()
