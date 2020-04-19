# tinytext.py  (c)2020  Henrique Moreira (part of 'jworks')

"""
  tinytext module handles basic best-effort text classes

  Compatibility: python 3.
"""

# pylint: disable=invalid-name

from os.path import realpath
try:
    from redito import xCharMap
except ModuleNotFoundError:
    xCharMap = None


class LocalCharMap():
    """ Basic local charmap, whenever xCharMap is not available """
    _map = None

    def __init__(self):
        self._map = {128: "EUR",
                     }

    def simpler_ascii(self, s):
        """ Simplified simple string """
        if isinstance(s, str):
            return self._get_simpler_str(s)
        if not isinstance(s, list):
            return None
        res = []
        for a in s:
            res.append(self.simpler_ascii(a))
        return res

    def _get_simpler_str(self, s, basic_q="?"):
        """ Internal simplified string """
        assert isinstance(s, str)
        res = ""
        for c in s:
            d = ord(c)
            if c in ("\t", "\n",):
                u_str = c
            elif d < 32:
                u_str = basic_q
            elif d in self._map:
                u_str = self._map[d]
            else:
                u_str = c
            res += u_str
        return res


def simpler_ascii(s):
    """ Basic function for displaying a simpler string """
    return char_map.simpler_ascii(s)


def neat_filename(s, simplify=""):
    """ Simply substitute backslashses.
    It simplify paths if requested.
     """
    assert isinstance(s, str)
    assert isinstance(simplify, str)
    if simplify == "r":
        res = realpath(s)
    else:
        res = s
    res = res.replace("\\", "/")
    return res


char_map = LocalCharMap() if xCharMap is None else xCharMap


#
# No main...!
#
if __name__ == "__main__":
    print("Import tinytext instead!")
