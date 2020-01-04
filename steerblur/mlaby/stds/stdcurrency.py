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
    if code is not None:
        if param:
            print("Remaining params:", param)
    return code


#
# slim_dict()
#
def slim_dict (resDict, fields, fieldTypes={}, defVal=""):
    assert type(fieldTypes)==dict
    if type( fields )==list or type( fields )==tuple:
        for f in fields:
            notThere = f not in resDict
            if notThere:
                resDict[ f ] = defVal
                print("NAME:", resDict["CtryNm"], "f:", f, "TYP:", fieldTypes)
                if f in fieldTypes:
                    resDict[ f ] = fieldTypes[ f ]
    else:
        assert False
    return True


#
# Test suite
#
if __name__ == "__main__":
    import sys
    code = test_stdcurrency( sys.stdout, sys.argv[ 1: ] )
    if code is None:
        print("""stdcurrency.py command [options]
Lists currencies.

a       Basic dump.

""")
        code = 0
    sys.exit( code )
