# dictplay.py  (c)2019  Henrique Moreira

"""
  dictplay: dictionary for my playlists
"""

dict_MyPlaylists = {
    "k": "6895831904",
    "yes": "6417264184",
    "20thB": "6995293744",
    "another": "5930226904",
    "sombras": "6359769584",
    "autumn": "6656722524",
    "ultimate": "6996072584",
    "verao": "6290445124",
    "brasil": "7010440444",
    "trance": "4680320448",
    }


#
# Main script
#
if __name__ == "__main__":
    for k, val in dict_MyPlaylists.items():
        print("{:.<12} {}".format( k, val ))
        assert type( k )==str
        assert type( val )==str
        assert len( k )<=12
        assert k[0].isalnum()
        assert len(val)>=2 and len(val)<30
        assert val.isdigit() or val.isalpha()
