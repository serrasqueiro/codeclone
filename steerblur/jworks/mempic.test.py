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
            print("Bin, read exif")
            isOk = pm.read( name )
            assert isOk
            ed = pm.meta[ "EXIF" ]
            if verbose>0:
                dump_exif_details(outFile, name, ed)
            else:
                dump_exif_details(outFile, name, ed, fieldStarList )
        if verbose>0:
            if sPreHeader:
              print("{}: {}[]".format( name, sPreHeader ))
        code = 0
    return code


#
# dump_exif_details()
#
def dump_exif_details (outFile, name, img_exif_dict, filter=None):
    res = []
    ed = img_exif_dict
    showAll = filter is None
    maxShownLen = 60
    for key, val in ed.items():
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
                s = y[:maxShownLen] if len(y) > maxShownLen else y
                post = "(...)" if len(y) > maxShownLen else ""
                doShow = showAll
                shown = f"{x}: {s}{post}"
                if doShow:
                    outFile.write( "{}\n".format( shown ) )
                    res.append( shown )
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
