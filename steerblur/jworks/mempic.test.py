# mempic.test.py  (c)2020  Henrique Moreira (part of 'jworks')

"""
  mempic.test - test module for mempic

  Compatibility: python 3.
"""

from redito import xCharMap
from mempic import *


#
# run_main()
#
def run_main (outFile, errFile, inArgs):
    code = None
    verbose = 0
    sPreHeader = None
    fieldStarList = ("DateTime*",
                     "Model",)
    # Processing
    if inArgs==[]:
        return run_main(outFile, errFile, ["a", "-v", "mem_test.txt"])
    cmd = inArgs[ 0 ]
    param = inArgs[ 1: ]
    # Checking options
    while len( param )>0 and param[ 0 ].startswith("-"):
        if param[ 0 ].startswith( "-v" ):
            verbose += param[ 0 ].count( "v" )
            del param[ 0 ]
            continue
        print("Wrong option:", param[ 0 ])
        return None
    # Work the commands
    if cmd=="a":  # Dump basic file characteristics
        name = param[ 0 ]
        pm = PicMem()
        with open(name, "rb") as f:
            for tSize in (20, 8):
                try:
                    data = f.read(tSize)
                except:
                    data = None
                if data is not None: break
        if data is None:
            print("{}: too short".format( name ))
            return 3
        if data.isascii():
            decoded = data.decode("latin-1")
            sPreHeader = xCharMap.simpler_ascii( decoded.replace("\n","\\n") )
        else:
            print("Bin, read exif:", name)
            isOk = pm.read( name )
            assert isOk
            x = pm.meta["info"]["width"]
            y = pm.meta["info"]["height"]
            if verbose>0:
                print("\tx={}: {}; y={}: {}".format(x, pm.meta["main"]["x"], y, pm.meta["main"]["y"]))
                infos = dump_exif_details(outFile, name, pm)
            else:
                infos = dump_exif_details(outFile, name, pm, fieldStarList )
            bKind = data[6:11]
            isOk = type(bKind)==bytes
            assert isOk
            sExifOffset = infos[1]["ExifOffset"]
            sPreHeader = "({}), ExifOffset={}".format( bKind, sExifOffset )
        if verbose>0:
            if sPreHeader:
                print("{}: [{}]".format( name, sPreHeader ))
        code = 0
    return code


#
# dump_exif_details()
#
def dump_exif_details (outFile, name, pm, filter=None):
    res, desc = list(), list()
    myDict = dict()
    ed = pm.meta["EXIF"]
    showAll = filter is None
    maxShownLen = 60
    showEmpty = "-"
    # for key, val in ed.items(): -- would not be sorted by the EXIF id
    orderedKeys = list( ed.keys() )
    orderedKeys.sort()
    for key in orderedKeys:
        val = ed[key]
        if key in ExifTags.TAGS:
            x = ExifTags.TAGS[key]
            if type(val)==bytes:
                y = repr(val)
            elif type(val)==int:
                y = "(int) {}".format( val )
            else:
                y = val
            if x not in ("MakerNote",
                         ):
                if type(y)==str and y.strip()=="":
                    s = showEmpty
                else:
                    s = y[:maxShownLen] if len(y) > maxShownLen else y
                post = "(...)" if len(y) > maxShownLen else ""
                doShow = showAll
                shown = f"{x}: {s}{post}"
                if doShow:
                    if outFile is not None: outFile.write( "{}\n".format( shown ) )
                    desc.append( shown )
                myDict[ x ] = val
    res = (desc, myDict)
    return res


#
# Main script
#
if __name__ == "__main__":
    import sys
    code = run_main(sys.stdout, sys.stderr, sys.argv[ 1: ])
    if code is None:
        code = 0
        print("""mempic.test [command]

Tests mempic module.""")
    assert type( code )==int
    sys.exit( code )
