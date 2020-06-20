#-*- coding: utf-8 -*-
# misc.test.py  (c)2020  Henrique Moreira

"""
Test misc.py
"""

# pylint: disable=no-self-use, unused-argument

import sys
from wparse.misc import \
     HtmlText


def main():
    """ Main script """
    code = run_test(sys.stdout, sys.stderr, sys.argv[1:])
    if code is None:
        print("""python misc.py file [...]
""")
        code = 0
    sys.exit(code)


def run_test(out, err, args):
    """ Main test """
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
    for arg in param:
        idx = 0
        h_text = HtmlText(arg)
        code = h_text.parse_lines()
        assert code == 0
        for line in h_text.lines:
            idx += 1
            if verbose > 0:
                print(f"{idx}: {line}")
            else:
                print(line)
        err.write(f"""
Stats: {h_text.size()} bytes; \
Quotes wrong: {h_text.quote_count[0]}, \
Double-quotes: {h_text.quote_count[1]}, \
Single-quotes: {h_text.quote_count[2]}
""")
    return code


# Main script
if __name__ == "__main__":
    main()
