"""
Module for ISIN, basic class and checks

Follows:
- ISO 6166: International Securities Identification Number (ISIN)

(c)2020  Henrique Moreira (part of 'mintracker')
"""

# pylint: disable=invalid-name, no-self-use

import string


class ISIN():
    """
    ISIN class
    """
    def __init__(self, s_isin=None):
        self.isin_str = s_isin


    def checksum_digit(self, s):
        """
        Calculate ISIN checksum digit (and 12 alpha-digit string)
        :param s: input ISIN
        :return: pair (tuple): checksum digit, and 12 alpha-digit string
        """
        assert isinstance(s, str)
        if len(s) != 12:
            return -1, None
        cs_digit = _ISIN_checksum_digit(s)
        s_isin = "{}{}".format(s[:-1], cs_digit)
        return cs_digit, s_isin


    def is_valid(self):
        """
        Checks whether ISIN is valid
        :return: bool, True iff ISIN is valid
        """
        _, s_isin = self.checksum_digit(self.isin_str)
        if s_isin is None:
            return False
        return s_isin == self.isin_str


    def __str__(self):
        is_ok = is_valid()
        if is_ok:
            return self.isin_str
        return "-"


def _ISIN_checksum_digit(isin):
    def digit_sum(n):
        return (n // 10) + (n % 10)

    assert len(isin) == 12
    # See: https://stackoverflow.com/questions/46061228/calculating-isin-checksum
    all_uppercase = string.ascii_uppercase
    alphabet = {letter: value for (value, letter) in
                enumerate(''.join(str(n) for n in range(10)) + all_uppercase)}
    checksum_digit = abs(- sum(digit_sum(2 * int(c))
                               if i % 2 == 1
                               else int(c) for (i, c) in enumerate(
        reversed(''.join(str(d) for d in (alphabet[v] for v in isin[:-1]))), 1)) % 10)
    return checksum_digit


#    sample = "US0378331005"
#    tic = sample[:-1] + "$"
#    z = ISIN(tic)
#    print("isin_checksum_digit('{}') = {}".format(tic, z.isin_str))
