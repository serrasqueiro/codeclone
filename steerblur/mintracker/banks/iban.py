# -*- coding: iso-8859-1 -*-
# iban.py  (c)2020  Henrique Moreira (part of 'mintracker')

""" Module for IBAN, and NIB
"""

# pylint: disable=missing-docstring


import banks.names
import banks.ibanpt as ibanpt
from waxpage.redit import char_map


def run_main(args):
    """ Main basic module test.
    """
    aformat = CountryFormats()
    ibn = IBAN()
    abbrev = None if args == [] else args[0]
    print("IBAN format, abbrev='{}': {}"
          "".format(abbrev, ibn.gen_format(abbrev)))
    dct = banks.names.BANK_NAMES
    keys = dct.keys()
    for bkey in keys:
        yyyy = bkey[:4]
        s = banks.names.get_original_name(bkey)
        if aformat.simple_latin1:
            original_name = char_map.simpler_ascii(s)
        else:
            original_name = s
        print("Bank code: {} (IBAN yyyy='{}', ccode={}): {}"
              "".format(bkey, yyyy, bkey[4:], original_name))
        num = int(bkey[4:])
        valid = num > 0
        assert valid
    assert check_country_accs()
    return 0


def check_country_accs() -> bool:
    alist = ibanpt.bank_accounts()
    idx = 0
    for entry in alist:
        idx += 1
        shown = char_map.simpler_ascii(entry)
        print("\n#{}/{}:\n>>>{}<<<"
              "".format(idx, len(alist), shown))
        assert shown.strip('\n') == shown
        assert shown.replace("  ", " ") == shown
    return True


class CountryFormats():
    """ Country IBAN formats
    """
    GEN_FORMATS = {"PT": (50, "BBBB AAAA CCCCCCCCCCC XX"),
                  }
    _DEF_COUNTRY_ABBREV = "PT"
    simple_latin1 = True

    def default_country_abbrev(self):
        return self._DEF_COUNTRY_ABBREV


class IBAN(CountryFormats):
    """ Simple IBAN class
    """
    def __init__(self, s=None, iban_len=25):
        self.iban_lengths = (iban_len,) if isinstance(iban_len, int) else iban_len
        self._own_set(s)
        self._pair = self._update()

    def _own_set(self, s):
        if s is None:
            ibn = None
        elif isinstance(s, str):
            ibn = s
        elif isinstance(s, (list, tuple)):
            ibn = "".join(s)
        else:
            assert ibn
        self.iban = ibn
        return ibn and len(ibn) == 25

    def _update(self):
        if self.iban and len(self.iban) in self.iban_lengths:
            tup = (self.iban[:4], self.iban[4:])
        else:
            tup = ("", "")
        return tup

    def gen_format(self, country_abbrev=None):
        if country_abbrev is None:
            abbrev = self.default_country_abbrev()
        else:
            abbrev = country_abbrev
        return self.GEN_FORMATS[abbrev]

    def string(self):
        assert self.iban and len(self.iban) in self.iban_lengths
        assert len(self._pair) == 2
        return self._pair[0]+self._pair[1]


if __name__ == "__main__":
    import sys
    print("Module, no run!")
    run_main(sys.argv[1:])
