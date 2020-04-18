# edates.py  (c)2020  Henrique Moreira (part of 'jworks')

"""
  edates module handles strictly needed date conversions for EXIF data

  Compatibility: python 3.
"""

# pylint: disable=unused-argument, invalid-name

import datetime

# dttm = datetime.datetime.strptime("2015:01:26 18:32:33", "%Y:%m:%d %H:%M:%S")
# is: datetime.datetime(2015, 1, 26, 18, 32, 33)


def basic_test():
    """ Only a few basic tests. """
    dt = datetime.datetime.now()
    tup = (dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
    s = exif_str_date(dt)
    back = exif_date(s)
    print("now={},\n"
          "exif_str_date('{}')={}\n"
          "{}".format(tup, dt, s, back))
    #print("Invalid date:", exif_date(None))
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
        assert False
    a_str = dt.strftime(fmt)
    return a_str


#
# No main...!
#
if __name__ == "__main__":
    print("Import edates instead!")
    basic_test()
