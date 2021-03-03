"""
Module for textual TSV and related files

(c)2020  Henrique Moreira (part of 'draftdb', teq)
"""

# pylint: disable=missing-docstring

import sys
import util.strlist
import teq.ttext as ttext
from util.strlist import expand_list
from util.osindependent import TaPath
from waxpage.redit import char_map


def run_main(args):
    """
    Main ttext.py tests!
    """
    code = 0
    opts = {"ext": None,
            }
    param = args
    while param and param[0].startswith("-"):
        if param[0] == "--ext":
            opts["ext"] = param[1]
            del param[:2]
            continue
        return None

    notes = dict()
    for d in param:
        code = run_test_cat(notes, opts, d)
        if code != 0:
            break
    if code != 0:
        print("TESTS failed, code:", code)
    ksimple, _ = util.strlist.dict_order(notes)
    if ksimple:
        print("The following tables were shown simpler:\n{}"
              "".format(expand_list(ksimple, "\t-")))
    return code


def run_test_cat(notes, opts, d):
    debug = 1
    tap = TaPath(d)
    if not tap.ok_path():
        print("Invalid path:", tap)
        return 1
    if not tap.is_dir():
        print("Not a directory:", tap)
    if tap.path.startswith("../"):
        pass
    else:
        tap.cd_path()
    print("Dir: {}, abs_path: {}".format(tap, tap.abs_path))
    ttb = ttext.TsvBase("any-db")
    if opts["ext"]:
        ttb.ext = opts["ext"]
    rel_names = ttb.scan_tsv(tap.path)
    tbl = ttb.get_multiple_subnames()
    assert not tbl
    fails = ttb.read_files(rel_names, debug=debug)
    print("ttb.read_files(rel_names={}) returned fails={}".format(rel_names, fails))
    if not ttb.names:
        print("No files found: {} (ext: {}).".format(d, opts["ext"]))
        return 2
    print("Tables:")
    print(expand_list(ttb.names, "\t- ", 1))
    print(expand_list(util.strlist.dict_order(ttb.names, "z")[0], "\t=", post=" (reverse order)\n"))
    for name in ttb.names:
        cont = ttb.get_content(name)
        tbl = ttb.get_table(name)
        shown = [astr.split("\t") for astr in cont]
        flown = flow_list(shown)
        s_str = char_map.simpler_ascii(flown)
        if s_str != flown:	# ...except UnicodeEncodeError (Avoid that!)
            notes[name] = flown
        msgs = tbl[3]
        print("Error msgs ({}): {}\n...\n".format(type(msgs), msgs))
    return 0


def flow_list(a_list):
    s = ""
    for elem in a_list:
        s += "{}\n".format(elem)
    return s


#
# Main script
#
if __name__ == "__main__":
    CODE = run_main(sys.argv[1:])
    if CODE is None:
        print("""ttext.test.py [options] path [path...]

Options are:
   --ext X        Use X as extension
""")
        CODE = 0
    sys.exit(CODE)
