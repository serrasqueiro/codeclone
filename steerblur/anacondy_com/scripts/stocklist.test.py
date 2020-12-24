"""
Module for testing 'mintracker' related modules

(c)2020  Henrique Moreira
"""

# pylint: disable=missing-function-docstring

import sys
from sys import stdout, stderr
from snamings import comp_name_ok
from sindexes.stockspt import STK_ISIN_PSI20
from sindexes.isin import ISIN_checksum


def test_stocklist(out_file, err_file, in_args):
    """
    Main tests
    :param out_file: output stream
    :param err_file: error stream
    :param in_args: system args
    :return: int, or None, if parameters are wrong.
    """
    assert out_file is not None
    assert err_file is not None
    param = in_args
    is_ok = True
    if param == []:
        is_ok = test_pair_list(out_file, STK_ISIN_PSI20)
    else:
        for s_isin in param:
            if s_isin.isalpha():
                print("Skipped:", s_isin)
                continue
            tup = (("Any Name", s_isin),)
            is_ok = test_pair_list(out_file, tup)
            assert is_ok
    print("See also: https://github.com/serrasqueiro/codeclone/tree/master/steerblur/anacondy_com/common_dict/wstocks/")
    assert is_ok
    return 0


def test_pair_list(out_file, pair_list):
    assert out_file is not None
    all_ok = True
    for name, s_isin in pair_list:
        s = ISIN_checksum(s_isin)
        is_ok = s == s_isin
        s_ok = "OK" if is_ok else "NotOk"
        print("{:_<20} {} {}".format(name, s, s_ok))
        is_name_ok = comp_name_ok(name)
        assert is_name_ok
        if not is_ok:
            all_ok = False
    return all_ok


#
# Main script
#
if __name__ == "__main__":
    CODE = test_stocklist(stdout, stderr, sys.argv[1:])
    if CODE is None:
        print("""stocklist.test.py test-name [options...]

Test names are:
     a        Basic tests
""")
        CODE = 0
    else:
        assert CODE == 0
    sys.exit(CODE)
