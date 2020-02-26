# zdoc.py  (c)2020  Henrique Moreira

"""
  Transcode word docs

  Compatibility: python 3.
"""

# pylint: disable=no-self-use

from redito import xCharMap
import docx2txt


def bare_test(args):
    """
    Main (bare) module tests
    :param args: system args
    :return: int, 0
    """
    for name in args:
        d_text = DocText(name)
        d_text.read()
        for line in d_text.content:
            s = xCharMap.simpler_ascii(line)
            print(s)
    return 0


class DocText():
    """
    DocText -- word documents text handleprocessor
    """
    def __init__(self, path=None):
        self.filename = path
        self.content = []


    def read(self, opts=None):
        """
        Read document
        :param opts: unused
        :return: ToDo
        """
        assert opts is None
        if self.filename is None:
            return False
        s_text = docx2txt.process(self.filename)
        self.content = self._post_processed(s_text, opts).split("\n")
        return True


    def _post_processed(self, s, opts):
        assert isinstance(s, str)
        if opts is None:
            spl = s.split("\n\n\n\n")
            res = "\n###\n".join(spl)
        else:
            res = s
        return res


if __name__ == "__main__":
    from sys import argv
    print("Module, please import it!")
    bare_test(argv[1:])
