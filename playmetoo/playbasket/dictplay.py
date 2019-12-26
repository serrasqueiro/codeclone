# dictplay.py  (c)2019  Henrique Moreira

"""
  dictplay: dictionary for my playlists
"""

dict_MyPlaylists = {
    "k": "6895831904",
    "yes": "6417264184",
    }


#
# Main script
#
if __name__ == "__main__":
    for k, val in dict_MyPlaylists.items():
        print("{:.<12} {}".format( k, val ))
        assert type( k )==str
        assert type( val )==str
