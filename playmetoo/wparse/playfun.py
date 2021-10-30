#-*- coding: utf-8 -*-
# playfun.py  (c)2021  Henrique Moreira

"""
Playlist functions
"""

# pylint: disable=unused-argument, line-too-long

VPL_HEADER = "#VUPlayer playlist"

from wparse.vpl import IDX_KEYS_VPL, VUPlayerControl

#	IDX_KEYS_VPL = '1#NAME 2#ATST 3#ALBM 4#TRKN 5#TYPE 6#RATE 7#FREQ 8#CHNL 9#SIZE 10#TIME 11#CUE1 12#CUE0 13#GENR 14#YEAR'

def main_test():
    """ Just basic tests """
    payload = []
    fields = [item.split("#", maxsplit=1) for item in IDX_KEYS_VPL.split(" ")]
    for item in fields:
        print(item)
    fname = "list.vpl"
    lines = from_vpl_string(open(fname, "r", encoding="ISO-8859-1").read())
    for line in lines:
        first, rest = line[0], line[1:]
        if first == VPL_HEADER:
            assert not rest
            continue
        path = first.replace("\\", "/")
        print(path, rest)
        payload.append((path, rest))
    vcontrol = VUPlayerControl()
    assert vcontrol.valid_vpl(payload)

def from_vpl_string(data:str) -> list:
    """ Converts a VPL playlist into a list of lines (of dictionary) """
    lines = [item.strip('\r').split('\x01') for item in data.split("\n") if len(item) > 1]
    return lines

# Main script
if __name__ == "__main__":
    print("Import, or see main at playfun_list.py")
    main_test()
