"""
Module for stock namings/ abbreviations/ weights.

(c)2020  Henrique Moreira (part of 'mintracker')
"""

# pylint: disable=missing-docstring


import sindexes.weight_stocks
from sindexes.weight_stocks import STK_W_PSI20
from sindexes.isin import ISIN


def run_main(args):
    """
    Main basic module test.
    """
    nicks = args if args != [] else None
    stk_pair = (STK_W_PSI20,
                )
    for name, lines in stk_pair:
        sw = StockWeight(name, lines)
        sr = RefISIN()
        invalids = sr.add_ISIN_refs(sindexes.weight_stocks.STK_ISIN_PSI20)
        if invalids != []:
            print("Invalid ISIN (#{} invalid): {}".format(len(invalids), invalids))
            assert False
        if nicks is None or name in nicks:
            idx, f_sum = 0, 0.0
            for abbrev, weight in sw.abbreviations():
                idx += 1
                print("#{}:\t{} {:8.2f} {:.15} {}"
                      "".format(idx, name, weight, abbrev, sw.full_name(abbrev)))
                f_sum += weight
            print("Total weight (100%) = {:.3f}".format(f_sum))
            for abbrev, _ in sw.abbreviations():
                name = sw.full_name(abbrev)
                print("ISIN={}, {}".format(sr.ref_isin.get(name), name))
    return 0



class RefISIN():
    def __init__(self):
        self.ref_isin = dict()


    def add_ISIN_refs(self, tups):
        """
        Add a list/ tuples of pairs (name, ISIN) into the 'ref_isin' dictionary.
        :param tups: list
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


    def full_name(self, abbrev):
        return self._abbrev2name.get(abbrev)



#
# Main script
#
if __name__ == "__main__":
    from sys import argv
    CODE = run_main(argv[1:])
