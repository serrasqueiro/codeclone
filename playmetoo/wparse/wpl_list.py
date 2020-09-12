#-*- coding: utf-8 -*-
# wpl_test.py  (c)2020  Henrique Moreira

"""
Test wpl_test.py
"""

# pylint: disable=unused-argument

import sys
import os.path
import xmltodict


def main():
    """ Main script """
    code = run(sys.stdout, sys.stderr, sys.argv[1:])
    if code is None:
        print("""python wpl_test.py file [...]
""")
        code = 0
    sys.exit(code)


def run(out, err, args) -> int:
    """ Main list of '.wpl' """
    param = args
    verbose = 0
    while param and param[0].startswith("-"):
        if param[0].startswith("-v"):
            verbose += int(param[0].count("v"))
            del param[0]
            continue
        return None
    if param == []:
        return None
    opts = {"verbose": verbose,
            "n-files": len(param),
            }
    for name in param:
        if not name:
            continue
        bname = os.path.basename(name)
        if verbose:
            err.write(f"Reading: {bname}\n")
        fp = open(name, "r", encoding="UTF-8")
        code, a_wpl = list_wpl(out, err, name, fp.read())
        if not bname:
            bname = name
        if code:
            err.write(f"Read file with error-code ({code}): {name}\n")
        else:
            dump_wpl(out, bname, a_wpl, opts)
    return code


def dump_wpl(out, name, a_wpl, opts=None) -> bool:
    """ Dump playlist
    """
    verbose, n_files = 0, 0
    if opts:
        verbose = opts["verbose"]
        n_files = opts["n-files"]
    head, tail, seq = a_wpl
    assert tail
    for one in seq:
        if not one:
            continue
        if n_files > 1:
            out.write(f"{name}:")
        out.write(f"{one}\n")
    return True


def list_wpl(out, err, name, cont) -> tuple:
    """ List '.wpl' (Windows Media Player playlist)
    """
    assert isinstance(cont, str)
    par = xmltodict.parse(cont)
    ks = par["smil"]
    head = ks["head"]
    tail = ks["body"]
    seq = tail["seq"]["media"]
    texts = [better_wpl_path(one["@src"]) for one in seq]
    return (0, (head, tail, texts))


def better_wpl_path(path) -> str:
    assert isinstance(path, str)
    if not path:
        return ""
    res = path.replace("\\", "/")
    return res


# Main script
if __name__ == "__main__":
    main()
