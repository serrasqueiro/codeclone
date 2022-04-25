#-*- coding: utf-8 -*-
# media_info.py	(c)2020  Henrique Moreira

""" media_info.py - using mutagen
"""

# pylint: disable=unused-variable, invalid-name

import sys
import mutagen


def main():
    """ Main script """
    code = run(sys.stdout, sys.stderr, sys.argv[1:])
    if code is None:
        print("""python media_info.py file [...]
""")
        code = 0
    sys.exit(code)


def run(out, err, args) -> int:
    """ Main list of '.wpl' """
    param = args
    verbose = 0
    while param and param[0].startswith("-"):
        if param[0].startswith("-v"):
            verbose += int(param[0].count("v"))
            del param[0]
            continue
        return None
    if param == []:
        return None
    opts = {"verbose": verbose,
            "n-files": len(param),
            }
    return info_files(out, param, opts)


def info_files(out, param, opts) -> int:
    verbose = opts["verbose"]
    for name in param:
        if not name:
            continue
        mfile = mutagen.File(name)
        code, infos = info_file(mfile, opts)
        if code:
            return code
        ppr, _, tags = infos
        shown = ppr.replace("\n", "; ")
        out.write(f"{name}: {shown}\n")
        if verbose > 0:
            if tags:
                out.write(f"\t{tags}\n")
            out.write("--\n")
    return 0


def info_file(mfile, opts) -> tuple:
    what = mfile.pprint()
    info = mfile.info
    tags = mfile.tags
    hint = ("{round(info.length*1000.0)}ms",
            info.sample_rate, info.channels,
            info.bits_per_sample,
            f"{info.min_blocksize}/{info.max_blocksize}",
            )
    infos = (what, hint, tags)
    return (0, infos)


# Main script
if __name__ == "__main__":
    main()
