# mjd_helper.py  (c)2020  Henrique Moreira

"""
  Dates and Modified Julian Dates
  (instead of 'adates.py' classes!
"""

import datetime
# pylint: disable=invalid-name, missing-function-docstring
# pylint: disable=chained-comparison, attribute-defined-outside-init


def date_to_MJD(dttm) -> int:
    """ Converts a date to MJD """

    def nys_date_to_MJD(year, month, day):
        """
        Normative Year Stamp to MJD
        :param year: year
        :param month: month value
        :param day: day of month
        :return: MJD, the Julian Date
        """
        y = int(year)
        m = int(month)
        assert isinstance(day, int)
        """ Taken from:     icnames/ntp_analyst.cpp
        long nys_DateToMjd (int y, int m, int day)
        {
         if ( y>=1858 && m>=1 && m<=12 && day>=1 && day<=31 ) {
            return
                367 * y
                - 7 * (y + (m + 9) / 12) / 4
                - 3 * ((y + (m - 9) / 7) / 100 + 1) / 4
                + 275 * m / 9
                + day
                + 1721028
                - 2400000;
         }
         return 0;
        }
        """
        if y >= 1858 and m >= 1 and m <= 12 and day >= 1 and day <= 31:
            return 367 * y \
              - int( (7 * (y + int((m + 9) / 12))) / 4 ) \
              - 3 * int((int(int((y + (m - 9) / 7)) / 100) + 1) / 4) \
              + int( 275 * m / 9) \
              + day \
              + 1721028 \
              - 2400000
        return 0


        if isinstance(xDate, str):
            isOk = len(xDate) >= 8
            if isOk:
                try:
                    v = int(xDate)
                except ValueError:
                    v = 0
            return self.from_xdate(v)
        assert isinstance(xDate, int)
        isOk = xDate >= self.firstValidDate
        year = int(xDate / (10**4))
        month = int((xDate-year * 10**4) / 100)
        day = xDate % 100
        if isOk and self.check_ymd( year, month, day ):
            self.xdate = xDate
            return (True, (year, month, day))
        self.xdate = 0
        return (False, (0, 0, 0))

    if isinstance(dttm, datetime.datetime):
        year, month, day = dttm.year, dttm.month, dttm.day
    elif isinstance(dttm, str):
        a_str = dttm.replace("-", " ").replace("/", " ").replace(".", " ")
        tups = []
        for this in a_str.split(" "):
            num = int(this)
            tups.append(num)
        if len(tups) < 3:
            return -1
        year, month, day = tups[0], tups[1], tups[2]
    else:
        return -1
    mjd = nys_date_to_MJD(year, month, day)
    return mjd


#
# Test suite
#
if __name__ == "__main__":
    print("Import this module!")
