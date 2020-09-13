#-*- coding: utf-8 -*-
# wpl_test.py  (c)2020  Henrique Moreira

"""
Test wpl_test.py
"""

# pylint: disable=unused-variable, invalid-name

import sys
import os.path
import xmltodict


def main():
    """ Main script """
    code = run(sys.stdout, sys.stderr, sys.argv[1:])
    if code is None:
        print("""python wpl_list.py file [...]
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
        code, a_wpl = read_wpl(fp.read(), name)
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
        if n_files > 1 or verbose > 0:
            out.write(f"{name}:")
        out.write(f"{one}\n")
    return True


def read_wpl(cont, path="", debug=1) -> tuple:
    """ Reads '.wpl' (Windows Media Player playlist)
    """
    assert isinstance(cont, str)
    assert 0 <= debug <= 9
    par = xmltodict.parse(cont)
    ks = par["smil"]
    head = ks["head"]
    body = ks.get("body")
    if body is None:
        return (2, (head, None, tuple()))
    tail = body["seq"]
    seq = tail["media"]
    if not isinstance(seq, (list, tuple)):
        what = seq["@src"]
        assert isinstance(what, str)
        seq = (seq,)
    if debug > 0:
        idx = 0
        shown = f"{path}: " if path else ""
        print(f"\nDebug:\n{shown}tail keys ({tail.keys()}) = {type(tail)}")
        print(f"seq type {type(seq)}, len# {len(seq)}")
        for one in seq:
            idx += 1
            print(f"{idx}: ({type(one)}) {one}")
    texts = [better_wpl_path(one["@src"]) for one in seq]
    return (0, (head, seq, texts))


def better_wpl_path(path) -> str:
    """ Use slashes instead of backslashes for indicating paths!
    """
    assert isinstance(path, str)
    if not path:
        return ""
    res = path.replace("\\", "/")
    return res


# Main script
if __name__ == "__main__":
    main()
