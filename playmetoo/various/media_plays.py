# media_plays.py  (c)2020, 2022  Henrique Moreira

""" media_plays: basic playlist readers
"""

# pylint: disable=missing-function-docstring, invalid-name, unidiomatic-typecheck

import sys
import pargs
from wparse.mediaelems import MediaElem, TextualSeq


def main():
    code = script(sys.stdout, sys.stderr, sys.argv[1:])
    if code is None:
        print("""media_plays command [options] [args]

media-list      List of media description with links.
""")
        code = 0
    assert code <= 127
    sys.exit(code)


def script(out, errfile, inArgs):
    code = None
    if not inArgs:
        return None
    cmd, param = inArgs[0], inArgs[1:]
    verbose = 0
    eq = {
        "s": ("--strict", ),
    }
    opts = pargs.arg_parse(param, eq)
    if opts is None:
        return None
    if "-v" in opts:
        verbose = opts[ "-v" ]
        assert verbose <= 3
    else:
        opts["-v"] = 0
    if "-s" not in opts:
        opts[ "-s" ] = 0
    if verbose < 0:
        print("param:", param)
        for k, val in opts.items():
            print("option {}: {}".format( k, val ))
        return 0
    out_streams = (out, errfile)
    if cmd == "media-list":
        code = media_list(out_streams, opts, param)
        if verbose > 0:
            errfile.write("Exit-code: {}\n".format(code))
    return code

def media_list(out_streams, opts, param):
    """ Media list """
    for fname in param:
        dump_textual(out_streams, fname, opts)
    return 0


def dump_textual(out_streams, fname, opts):
    out, errfile = out_streams
    verbose = opts["-v"]
    strict_level = opts["-s"]

    textseq = TextualSeq(strict_level=strict_level)
    isOk = textseq.load(fname)
    textseq.trim_input(True)
    assert isOk
    errCode, tups = parse_input(errfile, textseq)
    bugs = 0
    if strict_level > 0:
        for mElem in tups:
            assert mElem.header
            assert len(mElem.urls) >= 1
            isOk = mElem.valid_url()
            if not isOk:
                bugs += 1
                errfile.write("Line {}: invalid mElem: {}\n".
                              format(mElem.ref, ";".join(mElem.urls)))

    hdr = textseq.get_header()
    s_extra = "" if bugs == 0 else " (bugs: {})".format(bugs)
    if verbose > 0:
        if hdr.startswith("#"):
            hdr = hdr[1:].strip()
        out.write("# {}{}\n\n".format(hdr, s_extra))
    for mElem in tups:
        astr = f"{mElem}\n"
        out.write(astr)
        if verbose > 0:
            out.write("--\n")
        out.write("\n")
    if errCode != 0:
        return 1
    return 0


def parse_input(errfile, textseq):

    def flush(moves, tups, lineNr, numLines=2):
        opt_comments = None
        if numLines > 0:
            isOk = len(moves) >= 2
            opt_comments = moves[2:]
        else:
            isOk = True
        if isOk:
            mElem = MediaElem(moves[0], moves[1], opt_comments)
            mElem.ref = lineNr
            tups.append(mElem)
        return isOk

    numSep = 2
    maxLines = 2
    tups = []
    start_line = textseq.original_start
    lines = textseq.lines()
    # Start checking algorithm
    middle = []
    line, moves = "", []
    for line, instr in enumerate(lines, start_line):
        s = instr.strip("\t ")
        if s != instr:
            errfile.write("Line {}: Trailing or leading Blanks/ tabs\n".format(line))
            return (1, [])
        if not s:
            if not middle:
                if moves:
                    isOk = flush(moves, tups, line, maxLines)
                    if not isOk:
                        errfile.write(
                            "Line {}: invalid pairs.\n(num={}): {}".format(
                                line,
                                len(moves),
                                '@'.join(moves),
                            )
                        )
                        return (1, [])
                    moves = []
            middle.append(s)
            if len(middle) > 2:
                errfile.write("Line {}: Too many empty lines ({}).\n".
                              format(line, len(middle)))
                return (1, [])
        else:
            if middle and len(tups) > 0:
                if textseq.level > 0:
                    #print("Check lines in between:", len(middle), "s:", s)
                    if len(middle) != numSep:
                        errfile.write("Line {}: Few empty lines ({}), expected {}.\n".
                                      format(line, len(middle), numSep))
                        return (1, [])
            middle = []
            moves.append(s)
    if moves:
        isOk = flush(moves, tups, line)
        if not isOk:
            return (1, [])
    return (0, tups)


#
# Main script
#
if __name__ == "__main__":
    main()
