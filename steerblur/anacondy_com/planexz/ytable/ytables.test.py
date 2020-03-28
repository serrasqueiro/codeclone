# ytables.test.py  (c)2020  Henrique Moreira

"""
  ytables tests

  Compatibility: python 3.
"""

# pylint: disable=import-error, invalid-name, line-too-long

from sys import stdout, argv
from ytable.ytables import XcelTable
from ytable.ysheet import XcelSheet


def main():
    """
    Main test.
    """
    code = run_tests(stdout, argv[1:])
    assert isinstance(code, int)
    assert code == 0


def run_tests(out_file, in_args):
    """
    Basic tests for this module
    :param out_file: output stream
    :param inArgs: system args.
    :return: void
    """
    assert out_file is not None
    if in_args == []:
        args = ["a.xlsx"]
    else:
        args = in_args
    filename = args[0]
    param = args[1:]
    print("Reading {}, params: {}".format(filename, param))
    xt = XcelTable(filename, param)
    names = xt.get_sheet_names()
    idx = 0
    last = None
    for title in names:
        idx += 1
        sheet = xt.content(title)
        xs = XcelSheet(sheet, title)
        cols = xs.get_column_names()
        hdr = xs.get_header_numbers()
        print("idx={}, title={}, {}; header: {}, columns: {}".format(idx, title, sheet, hdr, cols))
        print("get_header_columns(): {}, get_header_column_names(): {}".format(xs.get_header_columns(), xs.get_header_column_names()))
        print("get_bold_headers(): {}".format(xs.get_bold_headers()))
        if sheet is None:
            return 1
        ir = sheet.iter_rows()
        y = 0
        for row in ir:
            y += 1
            shown = row
            last = (row, row[0] if row else "?")
            print("row#{}, #cols={}".format(y, len(row)), shown)
        print("---")
    if last is None:
        return 2
    row, elem = last[0], last[1]
    print("Last row:", row)
    print("Last row, 1st element ({}): {}".format(type(elem), elem))
    return 0


if __name__ == "__main__":
    main()
