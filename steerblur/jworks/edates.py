# edates.py  (c)2020  Henrique Moreira (part of 'jworks')

"""
  edates module handles strictly needed date conversions for EXIF data

  Compatibility: python 3.
"""

# pylint: disable=unused-argument, invalid-name

import datetime
from jworks.mjd_helper import date_to_MJD

MMJD_REF = 51544	# Modern MJD (MJD: Modified Julian Date), 1st January 2000!

### Examples:
# dttm = datetime.datetime.strptime("2015:01:26 18:32:33", "%Y:%m:%d %H:%M:%S")
# is: datetime.datetime(2015, 1, 26, 18, 32, 33)


def basic_test():
    """ Only a few basic tests. """
    dt = datetime.datetime.now()
    tup = (dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
    s = exif_str_date(dt)
    back = exif_date(s)
    n_date = norm_date(dt, True)
    print("now={} = {},\n"
          "exif_str_date('{}')={}\n"
          "{}".format(tup, n_date, dt, s, back))
    #print("Invalid date:", exif_date(None))
    mjd = date_to_MJD(dt)
    print("MJD (Modified Julian Day):", mjd)
    return 0


def exif_date(s, has_seconds=":%S"):
    """
    Converts an EXIF date (YYYY:MM:DD HH:MM:SS) into a datetime.
    :param s: input string
    :param has_seconds: use '' to parse no seconds
    :return: datetime
    """
    assert isinstance(has_seconds, str)
    if s is None:
        return None
    in_date_format = "%Y:%m:%d %H:%M" + has_seconds
    try:
        dttm = datetime.datetime.strptime(s, in_date_format)
    except ValueError:
        dttm = None
    return dttm


def eu_date(s, has_time=False, has_seconds=True):
    """
    Converts a date in european format (ISO-like), YYYY-MM-DD into a datetime.
    :param s: input string, e.g. '1971-12-23' or '2020-09-19 23:58:59'
    :param has_time: input string has not only year date but also time
    :param has_seconds: input string has seconds (must put 'has_time'=True too!)
    :return: datetime
    """
    assert isinstance(s, str)
    assert isinstance(has_seconds, bool)
    if s is None:
        return None
    if has_time:
        in_date_format = "%Y-%m-%d %H:%M" + has_seconds
    else:
        in_date_format = "%Y-%m-%d"
    try:
        dttm = datetime.datetime.strptime(s, in_date_format)
    except ValueError:
        dttm = None
    return dttm


def pt_date(s, has_time=False, has_seconds=True):
    """
    Converts a date in portuguese format (DD-MM-YYYY) into a datetime.
    :param s: input string, e.g. '23-12-1971' or '19-09-2020 23:58:59'
    :param has_time: input string has not only year date but also time
    :param has_seconds: input string has seconds (must put 'has_time'=True too!)
    :return: datetime
    """
    assert isinstance(s, str)
    assert isinstance(has_seconds, bool)
    if s is None:
        return None
    if has_time:
        in_date_format = "%d-%m-%Y %H:%M" + has_seconds
    else:
        in_date_format = "%d-%m-%Y"
    try:
        dttm = datetime.datetime.strptime(s, in_date_format)
    except ValueError:
        dttm = None
    return dttm


def mjd_from(s, country_fmt="eu"):
    """ Returns the MJD (Modified Julian Date) from the string date provided 's'
    """
    if country_fmt == "eu":
        dttm = eu_date(s)
    elif country_fmt == "pt":
        dttm = pt_date(s)
    else:
        dttm = None
    if dttm is None:
        return -1
    mjd = date_to_MJD(dttm)
    return mjd


def exif_str_date(dttm, iso_format=None):
    """
    Returns the regular ISO date into a string.
    :param dttm: datetime
    :param iso_format: which format (None: default)
    :return: string, the date
    """
    if iso_format is None:
        fmt = "%Y:%m:%d %H:%M:%S"
    elif iso_format == "ISO":
        fmt = "%Y-%m-%d %H-%M-%S"
    else:
        fmt = iso_format
    if isinstance(dttm, datetime.datetime):
        dt = dttm
    elif isinstance(dttm, int):
        a_val = dttm
        dt = datetime.datetime.fromtimestamp(a_val)
    else:
        return "-"
    a_str = dt.strftime(fmt)
    return a_str


def norm_date(s, has_seconds=False) -> str:
    """ Shows a basic ISO-date:		YYYY-MM-DD HH:MM(:SS)
    """
    # datetime.datetime.isoformat(dttm) = '2020-09-19T17:43:58.638106'
    # datetime.datetime.isoformat(dttm, timespec='seconds') = '2020-09-19T17:43:58'
    fmt = "%Y-%m-%d %H:%M"
    if has_seconds:
        fmt += ":%S"
    if isinstance(s, str):
        res = pt_date(s, has_seconds)
    elif isinstance(s, datetime.datetime):
        dttm = s
        res = datetime.datetime.strftime(dttm, fmt)
    else:
        assert False
    return res


#
# No main...!
#
if __name__ == "__main__":
    print("Import edates instead!")
    basic_test()
