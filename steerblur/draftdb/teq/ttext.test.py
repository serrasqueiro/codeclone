"""
Module for textual TSV and related files

(c)2020  Henrique Moreira (part of 'draftdb', teq)
"""

# pylint: disable=missing-docstring

import sys
from util.osindependent import TaPath
from teq.ttext import TsvBase


def run_main(args):
    """
    Main ttext.py tests!
    """
    code = 0
    param = args
    for d in param:
        ta = TaPath(d)
        if not ta.ok_path():
            print("Invalid path:", ta)
            return 1
        if not ta.is_dir():
            print("Not a directory:", ta)
        ta.cd_path()
        print("Dir: {}, abs_path: {}".format(ta, ta.abs_path))
        tb = TsvBase("any-db")
        rel_names = tb.scan_tsv(ta.path)
        is_ok = tb.read_files(rel_names)
        print("tb.read_files(rel_names={}) returned {}".format(rel_names, is_ok))
        for name in tb.names:
            cont = tb.get_content(name)
            tbl = tb.get_table(name)
            shown = [s.split("\t") for s in cont]
            print("{}: {} line(s)\n{}<<<".format(name, len(cont), flow_list(shown)))
            print("Error msgs: {}\n...\n", tbl[3])
    if code != 0:
        print("TESTS failed, code:", code)
    return code


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
    sys.exit(CODE)
