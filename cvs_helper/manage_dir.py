# manage_dir.py  (c)2020  Henrique Moreira

"""
Manages dirs recursively
"""

import sys
import os
import tconfig.archs.dirs as dirs

_MAX_REC_LEVEL = 255
_OS_DIR_NEMPTY = 39

# class os.OSError:
#	OSError(39, 'Directory not empty')

def main():
    """ Main script """
    code = run_main(sys.stdout, sys.stderr, sys.argv[1:])
    if code is None:
        print(f"""{__file__} command [arg ...]

Commands are:
    lsdir              lists directories (recursively)
    rmdir NAME         removes directory NAME (recursively)

Examples:

    Remove all CVS/ directories within ~/abc:
        rmdir --at ~/abc --name CVS
""")
    sys.exit(0 if code is None else code)


def run_main (out, err, args):
    """ Main runner """
    opts = {"verbose": 0,
            "debug": 0,
            "at": "",
            "names": [],
            }
    if not args:
        return None
    cmd = args[0]
    param = args[1:]
    while param and param[0].startswith("-"):
        if param[0] == "--at":
            if opts["at"]:
                return None
            opts["at"] = param[1]
            del param[:2]
            continue
        if param[0] == "--name":
            opts["names"].append(param[1])
            del param[:2]
            continue
        break
    if cmd == "lsdir":
        return do_lsdir(out, param, opts)
    if cmd == "rmdir":
        return do_rmdir(err, param, opts)
    return None


def do_lsdir(out, names, opts) -> int:
    """ List dirs """
    dir_at = opts["at"]
    if dir_at:
        os.chdir(dir_at)
    if names:
        paths = names
    else:
        paths = ["."]
    for name in paths:
        listed = folded(name, 0)
        if not listed:
            return 2
        for path in listed:
            out.write(f"{path}\n")
    return 0


def do_rmdir(err, names, opts) -> int:
    """ Remove dirs """

    def remove_dir(a_dir) -> bool:
        nempty = False
        try:
            os.rmdir(a_dir)
        except OSError as ex:
            nempty = ex.errno == _OS_DIR_NEMPTY
        return not nempty

    errs = 0
    dir_at = opts["at"]
    if dir_at:
        os.chdir(dir_at)
    if names:
        paths = names
    else:
        paths = ["."]
    for name in paths:
        listed = folded(name, 0)
        print(":::", listed)
        if not listed:
            err.write(f"None found at: {name}\n")
            return 2
        for a_dir in listed:
            cur = f"({os.getcwd()})"
            if matches_names(a_dir, opts["names"]):
                full = os.path.join(cur, a_dir)
                print(f"# Removing {cur}: {a_dir}")
                is_ok = remove_dir(a_dir)
                if not is_ok:
                    err.write(f"Non-empty directory: {a_dir}\n")
                    print(f"rm -rf {full}")
                    errs += 1
    return int(errs != 0)	# returns 0 if all ok


def matches_names(a_dir, names) -> bool:
    if not a_dir:
        return False
    base = os.path.basename(a_dir)
    return base in names


def folded(s_path, level) -> list:
    """ Recursive path list """
    res, there = [], []
    if level >= _MAX_REC_LEVEL:
        return list()
    dlist = dirs.DirList(s_path)
    for dname in dlist.folders:
        is_link = False
        if s_path == ".":
            
            path = dname
        else:
            path = os.path.join(s_path, dname)
            is_link = os.path.islink(path)
            #print(":::", path, "Is Link?", is_link)
        if not is_link:
            there.append(path)
    #print("folded:", s_path, f"; there(#{len(there)}): ", there)
    for path in there:
        res.append(path)
        within = folded(path, level+1)
        if within:
            res += within
    return res


#
# Main script
#
if __name__ == "__main__":
    main()
