# mempic.test.py  (c)2020  Henrique Moreira (part of 'jworks')

"""
  mempic.test - test module for mempic

  Compatibility: python 3.
"""

# pylint: disable=unused-argument, invalid-name

import sys
from jworks.mempic import PicMem, ExifTags
from jworks.tinytext import simpler_ascii, neat_filename


def main():
    """ Main script! """
    code = run_main(sys.stdout, sys.stderr, sys.argv[1:])
    if code is None:
        print("""mempic.test [command]

Tests mempic module.

Commands are:
   a      Dump EXIF descriptions. 
""")
        code = 0
    assert isinstance(code, int)
    sys.exit(code)


def run_main (outFile, errFile, inArgs):
    """ Main run. """
    code = None
    verbose = 0
    # Processing
    if inArgs == []:
        files = ["mem_test.txt"]
        args = ["a", "-v"] + files
    else:
        args = inArgs
    cmd = args[0]
    param = args[1:]
    # Checking options
    while len(param) > 0 and param[0].startswith("-"):
        if param[ 0 ].startswith( "-v" ):
            verbose += param[0].count( "v" )
            del param[0]
            continue
        print("Wrong option:", param[ 0 ])
        return None
    # Options
    opts = {"verbose": verbose,
            }
    # Work the commands
    if cmd == "a":
        code = dump_basic_pics(outFile, errFile, param, opts)
    return code


def dump_basic_pics(outFile, errFile, param, opts):
    """
    Dump basic file characteristics
    :param outFile: output stream
    :param errFile: error stream
    :param param: parameters
    :param opts: options dict.
    :return: int, code
    """
    for name in param:
        # Main test
        code = dump_basic_pic(outFile, errFile, name, len(param), opts)
        if code != 0:
            errFile.write("Bogus: {}\n".format(name))
            return code
    return 0


def dump_basic_pic(outFile, errFile, name, n, opts):
    """ Simple single basic pic """
    assert errFile is not None
    verbose = opts["verbose"]
    fieldStarList = ("DateTime*",
                     "Model",)
    pm = PicMem()
    with open(name, "rb") as f:
        for tSize in (20, 8):
            data = f.read(tSize)
    if len(data) < 8:
        print("{}: too short".format(name))
        return 3
    try:
        is_asc = data.isascii()
    except AttributeError:
        is_asc = False
    if is_asc:
        decoded = data.decode("latin-1")
        sPreHeader = simpler_ascii(decoded.replace("\n", "\\n"))
        print("sPreHeader={}".format(sPreHeader))
    else:
        bKind = data[6:11]
        isOk = isinstance(bKind, bytes)
        assert isOk
        print("Bin, read exif: {} ({})".format(name, bKind))
        isOk = pm.read(name)
        assert isOk
        x = pm.meta["info"]["width"]
        y = pm.meta["info"]["height"]
        dates = (pm.meta["info"]["DateTime"], pm.meta["info"]["DateISO"])
        if verbose > 0:
            infos = dump_exif_details(outFile, name, pm)
        else:
            infos = dump_exif_details(outFile, name, pm, fieldStarList)
        sExifOffset = infos[1].get("ExifOffset")
        if sExifOffset is None:
            sExifOffset = "."
        sPreHeader = " ExifOffset={}".format(sExifOffset)
        sizeXDict = pm.meta["main"]["x"]
        sizeYDict = pm.meta["main"]["y"]
        if len(sizeXDict) <= 0:
            sizeXDict, sizeYDict = "()", "()"
        sizeX = pm.pict.width()
        sizeY = pm.pict.height()
        sExtra = "" if n <= 1 and verbose == 0 else ", file={}".format(neat_filename(name))
        if verbose > 0:
            if pm.has_exif():
                print("\tx={}={}: {}; y={}={}: {}{}{}"
                      "".format(x, sizeX, sizeXDict,
                                y, sizeY, sizeYDict,
                                sPreHeader, sExtra))
            else:
                print("\tx={}, y={}; NO EXIF{}".format(sizeX, sizeY, sExtra))
            print("DateTime({}): {}, DateISO: {}".format(type(dates[0]), dates[0], dates[1]))
    return 0


def dump_exif_details (outFile, name, pm, xfilter=None):
    """ Dump EXIF details """
    res, desc = list(), list()
    myDict = dict()
    ed = pm.meta["EXIF"]
    showAll = xfilter is None
    maxShownLen = 60
    showEmpty = "-"
    # for key, val in ed.items(): -- would not be sorted by the EXIF id
    orderedKeys = list( ed.keys() )
    orderedKeys.sort()
    for key in orderedKeys:
        val = ed[key]
        if key in ExifTags.TAGS:
            x = ExifTags.TAGS[key]
            if isinstance(val, bytes):
                y = repr(val)
            elif isinstance(val, int):
                y = "(int) {}".format(val)
            else:
                y = val
            if x not in ("MakerNote",
                         ):
                if isinstance(y, str) and y.strip() == "":
                    s = showEmpty
                else:
                    s = y[:maxShownLen] if len(y) > maxShownLen else y
                post = "(...)" if len(y) > maxShownLen else ""
                doShow = showAll
                # not compatible with older Pythons... shown = f"{x}: {s}{post}"
                shown = "{}: {}{}".format(x, s, post)
                if doShow:
                    if outFile is not None:
                        outFile.write("{}\n".format(shown))
                    desc.append( shown )
                myDict[x] = val
    res = (desc, myDict)
    return res


#
# Main script
#
if __name__ == "__main__":
    main()
