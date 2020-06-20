#-*- coding: utf-8 -*-
# misc.py  (c)2020  Henrique Moreira

"""
Misceleaneous text functions
"""

# pylint: disable=no-self-use, unused-argument

from waxpage.redit import char_map


_QUOTE_UNQUOTED = 0
_QUOTE_STAT_DBL = 1
_QUOTE_STAT_SINGLE = 2
_QUOTE_SINGLE_WITHIN_DQ = 3
_QUOTE_STAT_LAST = 4


def simpler_str(s, subst_chr="?"):
    """ Simpler ASCII string """
    return char_map.simpler_ascii(s)


def latin1_chr(c, subst_chr="?"):
    """ Latin-1 (ISO-8859-1) char """
    assert isinstance(c, str)
    if len(c) != 1:
        return c
    deci = ord(c)
    if deci == 0x7F:
        res = "$"
    elif 0xA0 <= deci <= 0xFF:
        res = c
    elif 32 <= deci < 0x7F:
        res = c
    else:
        res = subst_chr
    return res


class HtmlText():
    """ HTML Text """
    _cont = ""
    _stream = None
    _n_bytes = 0
    quote_count = [0] * _QUOTE_STAT_LAST  # 1st: double-quote; 2nd: single quote
    _keep_comments = False
    lines = []

    def __init__(self, in_file=""):
        """ Initializer """
        if in_file:
            self._stream = self._reader(in_file)


    def parse_lines(self):
        """ Parse HTML lines """
        self.lines = self.html_split(self._cont)
        return 0


    def _reader(self, in_file):
        """ Text file reader """
        assert isinstance(in_file, str)
        with open(in_file, "r", encoding="utf-8") as f_in:
            self._cont = f_in.read()
        return f_in


    def size(self):
        """ Just returns the size (i.e. number of chars.) """
        return self._n_bytes


    def html_split(self, a_str):
        """ Split HTML text into lines """
        assert isinstance(a_str, str)

        def flush(s, listed):
            new_s = ""
            if s:
                new_s = s.strip()
                if not self._keep_comments and new_s.startswith("<!--"):
                    new_s = ""
            if new_s:
                listed.append(new_s)
                self._n_bytes += len(new_s)
            return ""

        res = []
        quote, last = '', ''
        for c in a_str:
            unquote, c_str = False, c
            if c == "'":
                if quote == "'":
                    unquote = True
                else:
                    quote = c
            elif c == '"':
                if quote == '"':
                    unquote = True
                else:
                    quote = c
            else:
                c_str = simpler_str(c)
            if unquote:
                quote = ""
                pos = _QUOTE_STAT_DBL if c == '"' else _QUOTE_STAT_SINGLE
                self.quote_count[pos] += 1
            if not quote:
                if c == "<":
                    last = flush(last, res)
            last += c_str
        flush(last, res)
        self.quote_count[_QUOTE_UNQUOTED] = 1 if quote else 0
        return res


def find_sub(lines, sub):
    """ Find 'sub' string(s) within list of 'lines'.
    """
    res, idx = list(), 0
    if isinstance(lines, (list, tuple)):
        for line in lines:
            pos = line.find(sub)
            if pos >= 0:
                tup = (idx, line)
                res.append(tup)
    return res


# Main script
if __name__ == "__main__":
    print("Module, to import!")
