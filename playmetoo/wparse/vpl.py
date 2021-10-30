#-*- coding: utf-8 -*-
# vpl.py  (c)2021  Henrique Moreira

"""
VUPlayer playlist handling (classes)
"""

# pylint: disable=unused-argument, line-too-long

from wparse.playlist import GenericPlaylist, \
     safe_path, \
     unencode


IDX_KEYS_VPL = '1#NAME 2#ATST 3#ALBM 4#TRKN 5#TYPE 6#RATE 7#FREQ 8#CHNL 9#SIZE 10#TIME 11#CUE1 12#CUE0 13#GENR 14#YEAR'


class VPL(GenericPlaylist):
    """ VUPlayer playlist class """
    def __init__(self, name=""):
        self._path = name
        self._headerline = "#VUPlayer playlist"
        self._line_sep = "\r\n"
        self.content = list()
        if name:
            self._data = open(name, "rb").read()
        else:
            self._data = bytes(self._headerline + self._line_sep, encoding="ascii")

    def data(self) -> bytes:
        """ Bytes read-out """
        return self._data

    def listed(self) -> list:
        """ Returns as list """
        line_sep = bytes(self._line_sep, encoding="ascii")
        lines = self._data.split(line_sep)
        return [simpler_entry(line) for line in lines]

    def text(self) -> str:
        """ Textual representation """
        data = unencode(self._data)
        astr = data.replace('\r', '\n').replace('\x01', '\n')
        return astr.lstrip(self._headerline+"\n")

    def parse(self, start=1) -> int:
        """ Parses '_data' content, and returns 0 if all ok! """
        is_ok = True
        line_sep = bytes(self._line_sep, encoding="ascii")
        cont = self._data.split(line_sep)
        if not cont:
            return 2
        first = cont[0]
        if start == 1:
            if unencode(first) != self._headerline:
                start = 0
                is_ok = False
        listed = VPL._entries(cont[start:])
        self.content = listed
        code = int(not is_ok)	# non-zero means an error
        return code

    def linear(self, start=1) -> list:
        """ Returns a plain list of (linear) content.
        """
        res = list()
        line_sep = bytes(self._line_sep, encoding="ascii")
        cont = self._data.split(line_sep)
        if unencode(cont[0]) != self._headerline:
            start = 0
        for item in cont[start:]:
            if not item:
                continue
            there = unencode(item.split(b'\x01'))
            res.append(there)
        return res

    @staticmethod
    def _entries(bytelist) -> list:
        """ Return entries from a byte list """
        res = list()
        idx = 0
        for bline in bytelist:
            if not bline:
                continue
            fields = bline.split(b'\x01')
            if len(fields) < 2:
                continue
            idx += 1
            path = safe_path(unencode(fields[0]))
            entry = {
                "!path": path,
                "#index": idx,
            }
            for attr in fields[1:]:
                astr = attr.decode("ascii")
                assign = astr.split("=", maxsplit=1)
                assert len(assign) == 2
                entry[assign[0]] = assign[1]
            res.append(entry)
        return res


def simpler_entry(ubytes) -> str:
    """ Uncoding bytes and split """
    astr = unencode(ubytes)
    return tuple(astr.split('\x01'))


# Main script
if __name__ == "__main__":
    print("Import, or see main at vpl_list.py")
