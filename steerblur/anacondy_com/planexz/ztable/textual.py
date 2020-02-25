# textual.py  (c)2020  Henrique Moreira

"""
  Simplified text, useful functions.

  Compatibility: python 3.
"""

# pylint: disable=missing-docstring


OPT_STRIP_LEFT = 1
OPT_STRIP_RIGHT = 2
OPT_STRIP_BOTH = OPT_STRIP_LEFT | OPT_STRIP_RIGHT


def trim_text (s, opts=None):
    """ Returns a simpler string.

    See also cut_excess().
    """
    i_strip = 0
    if isinstance(opts, dict):
        i_strip = int(opts.get("strip")) if "strip" in opts else 0
    else:
        assert opts is None
    cutWhat = (("  ", " "), ("\t", " "))
    if isinstance(s, str):
        if i_strip:
            if i_strip & OPT_STRIP_LEFT != 0:
                s = s.lstrip()
            if i_strip & OPT_STRIP_RIGHT != 0:
                s = s.rstrip()
        q = s
        for this, by in cutWhat:
            if this == "" or this == by:
                break
            count = 10**4
            while count > 0:
                count -= 1
                r = q.replace(this, by)
                if q == r:
                    break
                q = r
            assert count > 0
        res = q
    elif isinstance(s, (list, tuple)):
        res = []
        for q in s:
            r = trim_text(q, opts)
            res.append(r)
    else:
        assert False
    return res


if __name__ == "__main__":
    print("Module, please import it!")
