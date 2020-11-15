#-*- coding: utf-8 -*-
# vpl.py  (c)2020  Henrique Moreira

"""
VUPlayer playlist handling (classes)
"""

# pylint: disable=unused-argument, missing-function-docstring

import sys
from wparse.playlist import GenericPlaylist, \
     safe_path, \
     unencode


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
    opts = {"verbose": verbose,
            }
    for name in param:
        assert not name.startswith("-")
    for name in param:
        code = dump_vpl(out, err, name, opts)
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


class VPL(GenericPlaylist):
    """ VUPlayer playlist class """
    def __init__(self, name=""):
        self._path = name
        self._headerline = "#VUPlayer playlist"
        self._line_sep = "\r\n"
        self.content = list()
        if name:
            self._data = open(name, "rb").read()
        else:
            self._data = bytes(self._headerline + self._line_sep, encoding="ascii")

    def data(self) -> bytes:
        return self._data

    def listed(self) -> list:
        line_sep = bytes(self._line_sep, encoding="ascii")
        lines = self._data.split(line_sep)
        return [simpler_entry(line) for line in lines]

    def text(self) -> str:
        data = unencode(self._data)
        astr = data.replace('\r', '\n').replace('\x01', '\n')
        return astr.lstrip(self._headerline+"\n")

    def parse(self, start=1) -> int:
        """ Parses '_data' content, and returns 0 if all ok! """
        code = 0
        line_sep = bytes(self._line_sep, encoding="ascii")
        cont = self._data.split(line_sep)
        if unencode(cont[0]) != self._headerline:
            start = 0
        listed = VPL._entries(cont[start:])
        self.content = listed
        code = int(start > 0)	# non-zero means an error
        return code

    def linear(self, start=1) -> list:
        """ Returns a plain list of (linear) content.
        """
        res = list()
        line_sep = bytes(self._line_sep, encoding="ascii")
        cont = self._data.split(line_sep)
        if unencode(cont[0]) != self._headerline:
            start = 0
        for item in cont[start:]:
            if not item:
                continue
            there = unencode(item.split(b'\x01'))
            res.append(there)
        return res

    @staticmethod
    def _entries(bytelist) -> list:
        res = list()
        idx = 0
        for bline in bytelist:
            if not bline:
                continue
            fields = bline.split(b'\x01')
            if len(fields) < 2:
                continue
            idx += 1
            path = safe_path(unencode(fields[0]))
            entry = {"!path": path,
                     "#index": idx,
                     }
            for attr in fields[1:]:
                astr = attr.decode("ascii")
                assign = astr.split("=", maxsplit=1)
                assert len(assign) == 2
                entry[assign[0]] = assign[1]
            res.append(entry)
        return res


def simpler_entry(ubytes) -> str:
    astr = unencode(ubytes)
    return tuple(astr.split('\x01'))


# Main script
if __name__ == "__main__":
    # import importlib; importlib.reload(wparse.vpl); from wparse.vpl import *
    main()
