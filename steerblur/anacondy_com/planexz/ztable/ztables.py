# ztables.py  (c)2020  Henrique Moreira

"""
  Text tables, OS-independent

  Compatibility: python 3.
"""

import os
from sys import stdout, stderr


class Tabular():
    """
    Tabular/ text tables
    """
    def __init__ (self, name=None, opt_stream=None):
        self.filename = name
        self._stream = opt_stream
        self.content_size = 0
        assert name is None or (name is not None and opt_stream is not None)


    def rewrite(self, encoding=None, force=False):
        self.content_size = -1
        if os.name != "nt" and not force:
            return False
        return self._rewrite(encoding)


    def _rewrite (self, encoding=None):
        if self._stream in (stdout, stderr):
            return False
        if self._stream is not None:
            self._stream.close()
        assert self.filename is not None
        temp = open(self.filename, "r")
        data = temp.read()
        temp.close()
        self._stream = open(self.filename, "wb")
        if encoding is None:
            encoding = "ISO-8859-1"
        self._stream.write(data.encode(encoding))
        self.content_size = len(data)
        return True


if __name__ == "__main__":
    print("Module, please import it!")

