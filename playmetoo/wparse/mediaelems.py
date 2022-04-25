#-*- coding: utf-8 -*-
# mediaelems.py	(c)2020  Henrique Moreira

""" mediaelems.py - textual bimbos list
"""

# pylint: disable=missing-function-docstring

DEF_INPUT_ENC = "ISO-8859-1"


class TextualSeq():
    """ Textual Sequence - text file with media elements. """
    def __init__(self, encoding=DEF_INPUT_ENC, strict_level=2):
        assert isinstance(encoding, str)
        self._header = ""
        self.comments = []
        self.level = strict_level
        self._encoding = encoding
        self._lines = []
        self.original_start = 0

    def load(self, fname:str) -> bool:
        input_encoding = self._encoding
        with open(fname, "r", encoding=input_encoding) as f_in:
            self._lines = f_in.read().splitlines()
        self.original_start = 1
        if not self._lines:
            return False
        hdr = self._lines[0]
        if hdr.startswith("#"):
            self._header = hdr
            del self._lines[0]
            self.original_start += 1
        return True

    def get_header(self):
        return self._header

    def lines(self) -> list:
        return self._lines

    def trim_input(self, accept_comments=False) -> int:
        trims = 0
        if not self._lines:
            return 0
        if not self._lines[-1]:
            trims += 1
            del self._lines[-1]
        if not accept_comments:
            return trims
        if self._lines[0].startswith("#"):
            self.comments.append(self._lines[0])
            del self._lines[0]
            self.original_start += 1
            trims += 1
        return trims


class MediaElem():
    """ MediaElem - e.g.  """
    def __init__(self, header=None, url=None, comments=None):
        self.ref = -1
        self.header = header
        self.urls = [] if url is None else [url]
        self.comments = comments
        assert isinstance(comments, list) or comments is None

    def set_from_list(self, alist, a_ref=-1):
        """  Sets data-members from a plain list
        Example (two elements):
		Relax: 1984, Frankie Goes to Hollywood
		https://www.youtube.com/watch?v=poRM75mb4YQ
        """
        assert isinstance(alist, (list, tuple))
        self.header = alist[0]
        self.urls = alist[1:]
        self.ref = int(a_ref)
        self.comments = None
        return True

    def __str__(self):
        n_urls = len(self.urls)
        if n_urls <= 1:
            ustr = self.urls[0]
        else:
            ustr = "{} ...".format(self.urls[0])
        astr = "{}\n{}".format(self.header, ustr)
        return astr

    def valid_url(self, s=None):
        valid_protos = ("file", "http", "https")
        if type( s )==list:
            for a in s:
                isOk = self.valid_url(a)
                if not isOk: return False
            return True
        elif isinstance(s, str):
            isOk = s.find("://") > 1
        elif s is None:
            assert isinstance(self.urls, list)
            return self.valid_url(self.urls)
        else:
            assert False, f"valid_url(): '{s}'"
        if isOk:
            spl = split_first(s, "://")
            prot = spl[0]
            isOk = len(spl) == 2 and prot in valid_protos
        else:
            isOk = self.valid_ref(s)
        return isOk

    def valid_ref(self, s):
        assert isinstance(s, str)
        if not s:
            return True
        isOk = s.isdigit() or (s[0].isalpha() and s.isalnum())
        return isOk


def split_first(astr, split_by):
    return astr.split(split_by, maxsplit=1)


# Main script
if __name__ == "__main__":
    # called by media_plays.py
    print("Please import me!")
