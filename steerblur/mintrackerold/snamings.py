"""
Module for stock namings/ abbreviations/ weights.

(c)2020  Henrique Moreira (part of 'mintracker')
"""

# pylint: disable=missing-docstring, invalid-name


import sindexes.stockspt
from sindexes.stockspt import STK_W_PSI20
from sindexes.isin import ISIN_checksum, ISIN


def run_main(args):
    """
    Main basic module test.
    """
    nicks = args if args != [] else None
    do_invent = args != []
    stk_pair = (STK_W_PSI20,
                )
    for name, lines in stk_pair:
        sw = StockWeight(name, lines)
        sr = RefISIN()
        invalids = sr.add_ISIN_refs(sindexes.stockspt.STK_ISIN_PSI20)
        if invalids != []:
            print("Invalid ISIN (#{} invalid): {}".format(len(invalids), invalids))
            assert False
        if nicks is None or name in nicks:
            s_refs = StockRefs(sw)
            if do_invent:
                s_refs.add_stock("ABC", "Abc Long")
                sr.ref_isin["Abc Long"] = "ABC123XYZ00?"
            idx, f_sum = 0, 0.0
            for abbrev, any_weight in sw.abbreviations():
                idx += 1
                weight = any_weight if any_weight is not None else -1.0
                print("#{}:\t{} {:8.2f} {:.15} {}"
                      "".format(idx, name, weight, abbrev, sw.full_name(abbrev)))
                if weight > 0:
                    f_sum += weight
            print("Total weight (100%) = {:.3f}".format(f_sum))
            for abbrev, _ in sw.abbreviations():
                stock_name = sw.full_name(abbrev)
                isin = sr.ref_isin.get(stock_name)
                is_ok = isin is not None and ISIN_checksum(isin) == isin
                str_ok = "OK" if is_ok else "NotOk; ok would be '{}'".format(ISIN_checksum(isin))
                print("{}, ISIN={}, {} ({})".format(name, isin, stock_name, str_ok))
    return 0



class RefISIN():
    def __init__(self):
        self.ref_isin = dict()


    def add_ISIN_refs(self, tups):
        """
        Add a list/ tuples of pairs (name, ISIN) into the 'ref_isin' dictionary.
        Only adds valid ISIN numbers.
        :param tups: list of pairs "STOCK LONG NAME", "ISIN" (where ISIN is a 12-char/digit ISIN reference)
        :return: list, invalid ISIN
        """
        invalids = []
        if not isinstance(tups, (list, tuple)):
            return None
        for q, i in tups:
            assert isinstance(q, str)
            assert isinstance(i, str)
            if q not in self.ref_isin:
                self.ref_isin[q] = i
                isin = ISIN(i)
                if not isin.is_valid():
                    invalids.append((q, i))
        return invalids


class StockWeight():
    """
    StockWeight class, for one Stock Index
    """
    def __init__(self, name, a_text):
        assert isinstance(name, str)
        assert isinstance(a_text, str)
        self.name = name
        self._abbrevs = []
        self._abbrev2name = dict()
        self._init_from_text(a_text)


    def _init_from_text(self, lines, debug=0):
        assert lines[0] == "\n" and lines[-1] == "\n"
        spl = lines[1:-1].split("\n")
        self.head = spl[0]
        tail = spl[1:]
        for row in tail:
            trip = row.split(";")
            assert len(trip) == 3
            name, abbrev, s_weight = trip
            if debug > 0:
                print("Debug:", trip)
            weight = float(s_weight)
            self._abbrevs.append((abbrev, weight))
            assert abbrev not in self._abbrev2name
            self._abbrev2name[abbrev] = name
        return True


    def abbreviations(self):
        return self._abbrevs


    def abbrev_list(self):
        return [s for s, weight in self._abbrevs]


    def full_name(self, abbrev):
        return self._abbrev2name.get(abbrev)


    def add_stock_ref(self, nick, long_name=None, weight=None):
        if long_name is None:
            name = nick
        else:
            name = long_name
        self._abbrevs.append((nick, weight))
        if nick in self._abbrev2name:
            return False
        self._abbrev2name[nick] = name
        return True


    def validate(self):
        names = []
        for abbrev, _ in self._abbrevs:
            long_name = self.full_name(abbrev)
            if long_name is None:
                return False
            assert long_name not in names
            names.append(long_name)
        return True


class StockRefs():
    def __init__(self, local_stock=None):
        self.error_code = 0
        self.all_refs = []
        if local_stock is None:
            is_ok = True
        else:
            is_ok = local_stock.validate()
            self.add_ref_stock(local_stock)
        if not is_ok:
            self.error_code = 1  # invalid (local) stock index
        self._local = local_stock


    def current_local(self):
        return self._local

    def current_local_name(self):
        return self._local.name


    def add_ref_stock(self, stk):
        assert isinstance(stk, StockWeight)
        self.all_refs.append((stk.name, stk))


    def set_local_byname(self, name):
        for stock_name, stk in self.all_refs:
            if stock_name == name:
                self._local = stk
                return True
        return False


    def add_stock(self, nick, long_name, where=None):
        stk = None
        if where is None:
            stk = self._local
        else:
            for stock_name, this in self.all_refs:
                if stock_name == where:
                    stk = this
                    break
        if stk is None:
            return False
        weight = None
        stk.add_stock_ref(nick, long_name, weight)
        return True


def comp_name_ok(s):
    assert isinstance(s, str)

    def valid_rest(s, valids):
        for c in s:
            ok = c.isalnum() or c in valids or c == ' '
            if not ok:
                return False
        return True

    VALIDS = (".", "-", ",")
    is_ok = (s[0].upper() or s[0].isdigit()) and valid_rest(s[1:], VALIDS)
    return is_ok


 #
# Main script
#
if __name__ == "__main__":
    from sys import argv
    CODE = run_main(argv[1:])
