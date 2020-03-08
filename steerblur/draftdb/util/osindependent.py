"""
OS independent functions

(c)2020  Henrique Moreira (part of 'draftdb', util)
"""

# pylint: disable=missing-function-docstring, no-member


import os
from sys import stderr
from util.strlist import any_of

_ISO_ASCII_127UP = (">", 126)
_ISO_ASCII_32DN = ("<", 32)


class GenericPath():
    """
    Abstract class: Generic path functions (get)
    """
    def __str__(self):
        return self._get_str()


class TaPath(GenericPath):
    """
    Picky OS independent paths
    """
    def __init__(self, s=None, filename=None):
        self.err_stream = stderr
        if s is None:
            self.path = ""
        else:
            self.path = unslashed_path(s)
        self.abs_path, self.filename = None, filename

    def _get_str(self):
        assert self.path is not None
        if self.path == "":
            return "."
        return self.path

    def ok_path(self):
        return self.is_ok_path(self.path)

    def is_ok_path(self, s):
        assert isinstance(s, str)
        detect = any_of(s, ("\\", "|", "~", _ISO_ASCII_32DN, _ISO_ASCII_127UP))
        if detect != -1:
            info = smooth_char(detect)
            if self.err_stream:
                self.err_stream.write("Detected: {}, invalid '{}'\n".format(info, s))
            return False
        return s == "" or s[-1] != "/"

    def is_dir(self, s=None):
        if s is None:
            w = self.path
        else:
            w = s
        return os.path.isdir(w)

    def is_file(self, s=None):
        if s is None:
            w = self.path
        else:
            w = s
        return os.path.isfile(w)


    def cd_path(self):
        self.abs_path = None
        if not os.path.isdir(self.path):
            return False
        os.chdir(self.path)
        self.abs_path = unslashed_path(os.getcwd())
        return True


def unslashed_path(s):
    """
    Return path without any slashes
    :param s: input string
    :return: string
    """
    return s.replace("\\", "/")


def smooth_char(d):
    if isinstance(d, int):
        return "'{}'".format(chr(d)) if d < 127 else "{}d".format(d)
    return d


def list_dir(d):
    if isinstance(d, str):
        ta = TaPath(d)
    elif isinstance(d, TaPath):
        ta = d
    else:
        assert False
    if not ta.ok_path():
        return None
    ls = os.listdir(ta.path)
    return ls


#
# Main script
#
if __name__ == "__main__":
    print("Module, no run!")
