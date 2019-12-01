# reindent.test.py  (c)2019  Henrique Moreira

"""
  reindent.test: basic reindent tester

  Compatibility: python 3.
"""

from reindent import *

#
# main_reindent.test()
#
def main_reindent_test (outFile, errFile, inArgs):
    sample = """# LIXO
if True:
  docInit = @@@Abc
Def @line3
Ghi @line4
@@@
  pass
print("Bye!")
"""
    expectedSub = """# LIXO
if True:
    docInit = @@@Abc
Def @line3
Ghi @line4
@@@
    pass
print("Bye!")
"""
    i = 0
    x = CLASS_Test_Reindenter(sample)
    aList = x.results[i]
    assert type( aList )==list
    s = "".join( aList ).replace( '\"\"\"', "@@@" )
    print("AFTER:\n{}".format( headed_blanks(s) ))
    if not s.startswith(expectedSub):
        print("---\nEXPECTED:\n{}".format( headed_blanks(expectedSub) ))
        return 1
    return 0


def headed_blanks (s, instead='.'):
    spl = s.split("\n")
    res = ""
    for x in spl:
        s = ""
        head = 0
        for c in x:
            d = c
            if head>=0:
                if c==" ":
                    head += 1
                    d = instead
                else:
                    head = -1
            s += d
        res += s + "\n"
    return res


#
# Main script
#
if __name__ == "__main__":
    import sys
    code = main_reindent_test( sys.stdout, sys.stderr, sys.argv[ 1: ] )
    assert type( code )==int
    assert code==0
