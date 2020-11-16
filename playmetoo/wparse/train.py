#-*- coding: utf-8 -*-
# train.py  (c)2020  Henrique Moreira

"""
Train playlists:
   - .vpl: VUPlayer
   - .m3u, .m3u8: normal and UTF-8 based playlists
   - .wpl: Microsoft 'Windows Playlist' (Windows Media Player and such)
"""

# pylint: disable=no-self-use, missing-function-docstring

import sys
import os
from wparse.playlist import unencode, fields_comp
from wparse.vpl import VPL

EXT_TRAIN = (".vpl",
             ".m3u", ".m3u8",
             ".wpl",
             )


def main():
    """ Main script """
    code = run(sys.stdout, sys.stderr, sys.argv[1:])
    if code is None:
        print("""python train.py path [path ...]
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
    listed = list()
    for name in param:
        if os.path.isfile(name) and name.lower().endswith(EXT_TRAIN):
            ext = name.lower().split(".")[-1]
            listed.append(f".{ext}\t{name}")
        else:
            err.write(f"Ignored: {name}\n")
    #listed.sort()
    if verbose > 0:
        print("\n".join(listed))
    code = run_train(out, err, listed, opts)
    return code


def run_train(out, err, rows, opts) -> int:
    """ Training from playlists
    """
    code = 0
    train = PTrain()
    for row in rows:
        ext, path = row.split("\t")
        if ext == ".vpl":
            play = VPL(path)
        else:
            play = None
        if play is None:
            err.write(f"Skipped unhandled playlist ({ext}): {path}\n")
            continue
        is_ok = train.train(play, ext)
        if opts["verbose"] > 0:
            print("{}: {}".format(path, "OK" if is_ok else "NotOk"))
        if not is_ok:
            shown = "\n".join(train.fields[ext]["@msgs"])
            err.write(f"# Bogus for {path}:\n{shown}\n")
            return 1
    for ext in sorted(list(train.fields.keys())):
        print("")
        print(f"::: {ext} :")
        spec = train.fields[ext]
        msgs = spec["@msgs"]
        for what in sorted(list(spec.keys())):
            shown = spec[what]
            if what == "key-order":
                shown = idx_keys(spec[what])
            out.write(f"fields[{ext}]['{what}']: {shown}\n")
        if msgs:
            shown = "\n".join(msgs)
            err.write(f"# Bogus input ({ext}):\n{shown}\n")
    return code


class PTrain:
    """ Playlist Training, fields and statistics! """
    _head_to_ext = {"#VUPlayer": ".vpl",
                    }

    """ Playlist Training """
    def __init__(self):
        self.ext = ""
        self.fields = dict()

    def train(self, playlist, extension="") -> bool:
        lines = playlist.linear()
        is_ok = self._add_content(playlist.data(), lines, extension)
        return is_ok

    def fields_by(self, extension) -> dict:
        return self.fields[extension]

    def _add_content(self, bhead, cont, extension) -> bool:
        bin_head = bhead[:9]
        header = unencode(bin_head)
        if extension:
            self.ext = extension
        else:
            self.ext = self._head_to_ext[header]
        this = self._add_payload(cont)
        if self.ext not in self.fields:
            self.fields[self.ext] = this
        return self._add_data(this, self.fields[self.ext])

    def _add_data(self, this, dest):
        new = this["key-order"]
        known = dest["key-order"]
        res, bogus = fields_comp(known, new)
        if bogus:
            dest["@msgs"] = [f"Inc.p. '{idx_keys(new)}'"] + \
                            [f"- for  '{idx_keys(known)}': {bogus}"]
            return False
        if res:
            dest["key-order"] = res
        dest["@msgs"] += this["@msgs"]
        dest["samples"] += this["samples"]
        return True

    def _add_payload(self, cont) -> dict:
        this = {"key-order": list(),
                "@msgs": list(),
                "samples": 0,
                "no-key-1": 0,
                "min-lr": 999,	# Min. number of left+right assignments
                "min-lr#": 999,	# Min. number of left+right index
                "max-lr": 0,	# Max. number of left+right assignments
                }
        min_items = 999
        ori_key = list()
        idx = 0
        for entry in cont:
            idx += 1
            keys = list()
            n_zero, n_items = 0, 0
            for item in entry:
                left_right = item.split("=", maxsplit=1)
                if len(left_right) <= 1:
                    n_zero += 1
                else:
                    left, _ = left_right
                    keys.append(left)
                n_items += 1
            n_lr = len(keys)
            if n_items <= min_items:
                min_items = n_items
            this["no-key-1"] += int(n_zero == 1)
            if n_lr < this["min-lr"]:
                this["min-lr"] = n_lr
                this["min-lr#"] = idx
            if n_lr > this["max-lr"]:
                this["max-lr"] = n_lr
            this["samples"] += 1
            if ori_key:
                keep, bogus = fields_comp(ori_key, keys)
                if bogus:
                    msg = f"Field {bogus} at {idx_keys(ori_key)} incompatible with: {idx_keys(keys)}"
                    this["@msgs"].append(msg)
                elif keep:
                    ori_key = keep
            else:
                ori_key = keys
        this["key-order"] = ori_key
        return this


def idx_keys(fields, sep=" ") -> str:
    """ Show field index and key, to ease human understanding. """
    astr, idx = "", 0
    if isinstance(fields, str):
        return fields
    assert isinstance(fields, (tuple, list))
    for name in fields:
        idx += 1
        if not name:
            continue
        astr += sep if idx > 1 else ""
        astr += f"{idx}#{name}"
    return astr


# Main script
if __name__ == "__main__":
    # import importlib; importlib.reload(wparse.train); from wparse.train import *
    main()
