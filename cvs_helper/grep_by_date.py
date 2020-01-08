# grep_by_date.py  (c)2019  Henrique Moreira

"""
  grep_by_date: latest (by date) first
"""

import os
import datetime


def main (outFile, inFile, errFile, args):
    cmd = "order"
    param = args
    if cmd=="order":
        d = read_data(inFile, param)
        lines = d.split("\n")
        stamps = []
        for a in lines:
            pos = a.find(":")
            if pos>0:
                p = a[:pos]
                stamp = os.stat( p ).st_mtime
            else:
                stamp = -1
            stamps.append( stamp )
        show( outFile, errFile, (lines, stamps), None )
    return 0


def read_data (inFile, param):
    d = ""
    if param==[]:
        with open(inFile, "r") as f:
            d = f.read()
    for fName in param:
        with open(fName, "r") as f:
            d += f.read()
    return d


def show (outFile, errFile, tup, order=None):
    a, b = tup[0], tup[1]
    idx = 0
    for x in a:
        dt = b[ idx ]
        if dt!=-1:
            outFile.write("{} {}\n".format(fix_date_str(dt), x))
        idx += 1
    return True



def fix_date_str (stamp):
    assert stamp!=-1
    x = datetime.datetime.fromtimestamp( stamp )
    #s = x.strftime("%Y-%m-%dT%H:%M:%SZ")
    s = x.strftime("%Y-%m-%d %H:%M:%S")
    return s


#
# Main script
#
if __name__ == "__main__":
    import sys
    args = sys.argv[ 1: ]
    outFile = sys.stdout
    inFile = sys.stdin
    errFile = sys.stderr
    code = main(outFile, inFile, errFile, args)
    assert type( code )==int
    sys.exit(0)
