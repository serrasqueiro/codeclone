# (c)2020  Henrique Moreira
"""
secstext - show textual seconds
"""


import sys


def show_seconds_text(args):
    """ Few tests """
    if args ==  []:
        vals = ("0", 13, 69, 3602, 86463, -3604,)
    else:
        vals = args
    # python secstext.py , 3602
    # is: seconds_to_text(secs=3602): 1h,0m,2s
    first = vals[0]
    for p in vals if first.isdigit() else vals[1:]:
        secs = int(p)
        s = seconds_to_text(secs, ",")
        print("seconds_to_text(secs={}): {}".format(secs, s))


def seconds_to_text(secs, sep="", zeroed="0s"):
    """ Returns the textual string of the time elapsed; e.g. 'uptime' """
    if secs < 0:
        return "-" + seconds_to_text(-secs, sep, zeroed)
    if secs == 0:
        return zeroed
    res, count = "", 0
    days = secs // 86400
    hours = (secs - days * 86400) // 3600
    minutes = (secs - days * 86400 - hours * 3600) // 60
    seconds = secs - days * 86400 - hours * 3600 - minutes * 60
    # res = ("{}d".format(days) if days else "") + \
    #      ("{}h".format(hours) if hours else "") + \
    #      ("{}m".format(minutes) if minutes else "") + \
    #      ("{}s".format(seconds) if seconds else "")
    for tic in ("d", "h", "m", "s"):
        val = days if tic == "d" else hours if tic == "h" else minutes if tic == "m" else seconds
        if val == 0 and count <= 0:
            continue
        count += 1
        if res:
            res += sep
        res += f"{val}{tic}"
    return res


# A few tests
if __name__=="__main__":
    show_seconds_text(sys.argv[1:])
