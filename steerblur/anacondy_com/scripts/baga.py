# baga.py  (c)2020  Henrique Moreira

"""
  baga: basic tester of tinytag

  Compatibility: python 3.
"""

from tinytag import TinyTag
import os.path


#
# main_baga()
#
def main_baga(outFile, errFile, inArgs):
    """
    Main function.
    :param outFile: output file
    :param errFile: error file
    :param inArgs: parameters
    :return: an error-code
    """
    return 0


#
# CLASS MediaFile
#
class MediaFile():
    def __init__(self, p=None):
        self.path = p
        self.size = -1
        self.handler = None
        self.tiny = None
        if p is not None:
            self._read_tags(p)


    def _read_tags(self, p, debug=1):
        size = os.path.getsize(p)
        with open(p, "rb") as handler:
            self.tiny = TinyTag(p, size).get(p)
            self.handler = handler
        if debug>0:
            print("read_tags({}), size={}".format(p, size))
        return 0


#
# Main script
#
if __name__ == "__main__":
    import sys
    CODE = main_baga(sys.stdout, sys.stderr, sys.argv[1:])
    if CODE is None:
        print("""
baga
""")
        CODE = 0
    assert isinstance(CODE, int)
    assert CODE == 0
