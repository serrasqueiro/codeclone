#-*- coding: utf-8 -*-
# vpl.py  (c)2021  Henrique Moreira

"""
VUPlayer playlist handling (classes)
"""

# pylint: disable=unused-argument, line-too-long

from wparse.playlist import GenericPlaylist, \
     safe_path, \
     unencode

DEF_ENC_VPL = "ISO-8859-1"

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
        self.content = VPL._entries(cont[start:])
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
    def _entries(bytelist, encoding:str=DEF_ENC_VPL, debug=0) -> list:
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
            if debug > 0:
                print("Debug: idx:", idx, "; FIELDS:",
                      [entry.decode("ascii") for entry in fields])
            VPL.fields_from(fields[1:], encoding, entry)
            res.append(entry)
        return res

    @staticmethod
    def fields_from(fields:list, encoding:str, entry:dict) -> list:
        """ Updates 'entry' dictionary with the binary fields """
        assert line >= -1
        res = []
        for attr in fields:
            astr = attr.decode(encoding)
            assign = astr.split("=", maxsplit=1)
            assert len(assign) == 2, f"Unable to split: '{astr}'"
            key, value = assign
            entry[key] = value
            res.append(tuple(assign))
        return res

class VUPlayerControl():
    """ Basic abstract class """
    _fields = None

    def __init__(self):
        """ Init. """
        # VUPlayer playlist fields
        self._fields = {
            'NAME': 'name',	# song name
            'ATST': 'artist',
            'ALBM': 'album',
            'GENR': 'genre',
            'YEAR': 'year',
            'TRKN': 'track-number',
            'TYPE': 'type',	# file-type
            'RATE': 'rate',
            'FREQ': 'frequency',
            'CHNL': 'channels',	# number of channels
            'SIZE': 'size',
            'TIME': 'time',
            'CUE1': 'cue1',
            'CUE0': 'cue0',
        }

    def fields(self):
        return self._fields

    def valid_vpl(self, alist:list) -> bool:
        """ Returns True if 'list' is a valid VPL playlist! """
        for row in alist:
            path, rest = row
            for field in rest:
                tup = field.split("=", maxsplit=1)
                key, value = tup
                if key not in self._fields:
                    return False
        return True

def simpler_entry(ubytes) -> str:
    """ Uncoding bytes and split """
    astr = unencode(ubytes)
    return tuple(astr.split('\x01'))


# Main script
if __name__ == "__main__":
    print("Import, or see main at vpl_list.py")
