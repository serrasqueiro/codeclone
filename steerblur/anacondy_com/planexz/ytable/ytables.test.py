# ytables.test.py  (c)2020  Henrique Moreira

"""
  ytables tests

  Compatibility: python 3.
"""

from sys import stdout, argv
from ytables import XcelTable


def run_tests(out_file, inArgs):
    """
    Basic tests for this module
    :param out_file: output stream
    :param inArgs: system args.
    :return: void
    """
    if inArgs == []:
        args = ["a.xlsx"]
    else:
        args = inArgs
    filename = args[0]
    param = args[1:]
    nums, idx = [], 0
    for name in param:
        idx += 1
        print("#{}\t{} . {}".format(idx, filename, name))
        nums.append(idx)
    xt = XcelTable(filename, param)
    if nums == []:
        nums = [1]
    for idx in nums:
        sheet = xt.content(idx)
        print("idx:", idx, sheet)
        if sheet is None:
            return 1
        ir = sheet.iter_rows()
        for row in ir:
            print(row)
        print("---")
    return 0


if __name__ == "__main__":
    CODE = run_tests(stdout, argv[1:])
    assert isinstance(CODE, int) and CODE == 0
