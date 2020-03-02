# baga.py  (c)2020  Henrique Moreira

"""
  baga: basic tester of tinytag

  Compatibility: python 3.
"""

# pylint: disable=invalid-name

import os.path
from tinytag import TinyTag


class MediaFile():
    """
    MediaFile class
    """
    def __init__(self, p=None):
        self.path = p
        self.size = -1
        self.handler = None
        self.tiny = None
        if p is not None:
            self._read_tags(p)


    def _read_tags(self, p, debug=0):
        size = os.path.getsize(p)
        with open(p, "rb") as handler:
            self.tiny = TinyTag(p, size).get(p)
            self.handler = handler
        if debug > 0:
            print("read_tags({}), size={}".format(p, size))
        return 0


    def path_name(self):
        """
        Returns the pathname
        :return: string
        """
        return self.path


    def path_exists(self):
        """
        Returns true if pathname exists
        :return: bool
        """
        return os.path.isfile(self.path)


#
# Main script
#
if __name__ == "__main__":
    print("See baga.test.py for this module tests!")
