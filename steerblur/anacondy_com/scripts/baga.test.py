# baga.test.py  (c)2020  Henrique Moreira

"""
  baga.test: basic tester of baga

  Compatibility: python 3.
"""

# pylint: disable=invalid-name, pointless-string-statement

import commands
from baga import MediaFile


def main_baga_test(outFile, errFile, inArgs):
    """
    Main tests for module baga
    :param outFile: output stream
    :param errFile: error stream
    :param inArgs: system args
    :return: int, error-code
    """
    if inArgs == []:
        args = ["a"]
    else:
        args = inArgs
    cmd = args[0]
    param = args[1:]
    if cmd == "a":
        code = run_test_a(outFile, errFile, param)
    else:
        code = None
    return code


def run_test_a(outFile, errFile, param):
    """
    Run test 'a'
    :return: 0
    """
    assert outFile is not None
    assert errFile is not None
    listed = param
    for name in listed:
        p = commands.safe_name(name)
        print(p)
        mf = MediaFile(p)
        assert mf is not None
    return 0


#
# Main script
#
if __name__ == "__main__":
    import sys
    CODE = main_baga_test(sys.stdout, sys.stderr, sys.argv[1:])
    if CODE is None:
        print("""
baga.test a|b|...

Default: test 'a'
""")
        CODE = 0
    assert isinstance(CODE, int)
    assert CODE == 0


"""
import glob
import os
from mutagen.flac import FLAC

for filename in glob.glob('*.flac'):
    artist, title = os.path.splitext(filename)[0].split(' - ', 1)
    audio = FLAC(filename)
    audio.clear()
    audio['artist'] = artist
    audio['title'] = title
    audio.save()
"""
