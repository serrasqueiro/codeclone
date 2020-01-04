# stdcurrency.py  (c)2020  Henrique Moreira (part of 'mlaby/stds')

"""
  stdcurrency module handles currency dictionaries.

  Compatibility: python 2 and 3.
"""


#
# test_stdcurrency()
#
def test_stdcurrency (outFile, inArgs):
    code = None
    if inArgs==[]:
        args = ["a"]
    else:
        args = inArgs
    cmd = args[0]
    param = args[1:]
    if cmd=="a":
        code = 0
    print("param:", param)
    return code


#
# Test suite
#
if __name__ == "__main__":
    import sys
    code = test_stdcurrency( sys.stdout, sys.argv[ 1: ] )
    if code is None:
        print("""stdcurrency.py
""")
        code = 0
    sys.exit( code )

