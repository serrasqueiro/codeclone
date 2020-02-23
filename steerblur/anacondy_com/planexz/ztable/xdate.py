# xdate.py  (c)2020  Henrique Moreira

"""
  MS dates

  Compatibility: python 3.
"""

import datetime

XCEL_NUM_START, XCEL_ORD_START = 42139, 735733
#
#	Excel date starts as: 42139 being 2015-05-15 00:00:00
#	timetuple():
#		time.struct_time(tm_year=2015, tm_mon=5, tm_mday=15, tm_hour=0, tm_min=0, tm_sec=0, tm_wday=4, tm_yday=135, tm_isdst=-1)
#	norm = datetime.datetime(2015, 5, 15); norm.toordinal() == 735733

WEEK_DAYS = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun", "-")


class MsDate():
    """
    MS Date, used in xcel
    """
    def __init__ (self, s=""):
        self.dttm = None
        is_ok, val = self._set_from_date(s)
        if is_ok:
            self.jDate = val
        else:
            self.jDate = None


    def _set_from_date (self, s):
        v = -1
        dt = None
        if isinstance(s, str):
            if s.isdigit() and len(s) == 5:
                try:
                    v = int( s )
                except:
                    v = None
            elif len(s) == 10:
                latin = s[2]+s[5] == "--"  # dd-mm-YYYY
                if latin:
                    try:
                        dt = datetime.datetime.strptime(s, "%d-%m-%Y")
                    except ValueError:
                        pass
                elif s[4]+s[7] == "--":  # YYYY-mm-dd (kind of ISO, or really ISO)
                    try:
                        dt = datetime.datetime.strptime(s, "%Y-%m-%d")
                    except ValueError:
                        pass
                if dt is None:
                    is_ok = False
                else:
                    days = dt.toordinal()
                    is_ok = days >= XCEL_ORD_START
                    self.dttm = dt
                if is_ok:
                    # what is the number in xcel days value?
                    v = XCEL_NUM_START + days - XCEL_ORD_START
        elif isinstance(s, int):
            v = s
        elif isinstance(s, float):
            v = int(s)
            if float(v)!=s:
                v = None
        is_ok = v is not None and v >= XCEL_NUM_START and v <= 99999
        return is_ok, v


    def _to_str (self, j):
        dt = datetime.datetime.fromordinal(datetime.datetime(1900, 1, 1).toordinal() + j - 2)
        tt = dt.timetuple()
        return "{:4}-{:02}-{:02}".format( tt.tm_year, tt.tm_mon, tt.tm_mday )


    def __str__(self):
        return self._to_str(self.jDate if self.jDate is not None else "-")


    def days_from_stamp(self, stamp=-1):
        if stamp < 1431648000:	# 2015-05-15
            return 0
        days = int(stamp / 86400) + 719163
        return days


    def weekday_str(self):
        if self.jDate is None:
            wd = None
        else:
            days = self.jDate - XCEL_NUM_START + XCEL_ORD_START
            dt = datetime.datetime.fromordinal(days)
            wd = dt.weekday()
        if wd is None:
            return WEEK_DAYS[7]
        return WEEK_DAYS[wd]


class MsTime():
    """
    MS Time, used in xcel
    """
    def __init__(self, s=""):
        is_ok, val = self._set_from_time( s )
        if is_ok:
            self.jTime = val
        else:
            self.jTime = None


    def _set_from_time(self, s):
        is_ok = False
        r, h = None, None
        comp = None
        if isinstance(s, float):
            h = s * 24.0
        elif isinstance(s, str):
            if s.count(":")==1:
                comp = s
            else:
                if s!="":
                    h = float(s) * 24.0
        if comp:
            is_ok = True
            r = comp
        else:
            if h is not None:
                is_ok = True
                v = float(int(h))
                halves = float(h - v) * 60.0 / 100.0
                v += halves
                r = "{:.2f}".format(v).replace(".", ":")
        return is_ok, r


    def __str__(self):
        x = self.jTime
        if x is None:
            return "-"
        return x


#
# Test suite
#
if __name__ == "__main__":
    print("Module, please import it!")
    m = MsDate(XCEL_NUM_START)
    s = str(m)
    print(m, "Ok?", s == "2015-05-15")
