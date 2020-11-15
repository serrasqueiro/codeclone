#-*- coding: utf-8 -*-
# playlist.py  (c)2020  Henrique Moreira

"""
Generic playlist classes.
"""

# pylint: disable=missing-function-docstring

DOS_CR_LF = "\r\n"
UNIX_LF = "\n"
_LATIN_1 = "ISO-8859-1"


class GenericPlaylist:
    """ Abstract class for generic playlists """
    _data = b''
    _path = ""
    _headerline = None
    _line_sep = DOS_CR_LF
    _decode_path = _LATIN_1
    content = list()

    def get_headerline(self) -> str:
        return self._headerline

    def set_unix(self):
        self._line_sep = UNIX_LF


def safe_path(astr) -> str:
    res = astr.replace("\\", "/")
    return res

def unencode(ubytes, origin=_LATIN_1):
    if isinstance(ubytes, bytes):
        return ubytes.decode(origin)
    if isinstance(ubytes, (tuple, list)):
        res = [unencode(elem) for elem in ubytes]
        return res
    if isinstance(ubytes, (float, int)):
        return ubytes
    if isinstance(ubytes, str):
        return ubytes
    print(f"unencode({type(ubytes)}: {ubytes}")
    assert False
    return None

def fields_comp(known, new) -> tuple:
    assert isinstance(known, list)
    assert isinstance(new, list)
    added = 0
    res = known
    bogus = ""
    for key in new:
        if key not in known:
            added += 1
            res.append(key)
    if added:
        for key in known:
            if key not in new:
                return [], key
    if len(known) >= len(res):
        return [], bogus
    return res, bogus


# Main script
if __name__ == "__main__":
    print("Import wparse.playlist !")
