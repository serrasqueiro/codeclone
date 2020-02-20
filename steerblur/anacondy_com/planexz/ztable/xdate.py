# xdate.py  (c)2020  Henrique Moreira

"""
  MS dates

  Compatibility: python 3.
"""


import datetime


#
#	Excel date starts as: 42139 being 2015-05-15 00:00:00
#	timetuple():
#		time.struct_time(tm_year=2015, tm_mon=5, tm_mday=15, tm_hour=0, tm_min=0, tm_sec=0, tm_wday=4, tm_yday=135, tm_isdst=-1)


#
# CLASS MsDate
#
class MsDate():
    def __init__ (self, s=""):
        isOk, val = self._set_from_date( s )
        if isOk:
            self.jDate = val
        else:
            self.jDate = None


    def _set_from_date (self, s):
        v = -1
        if type( s )==str:
            if s.isdigit() and len( s )==5:
                try:
                    v = int( s )
                except:
                    v = None
        elif type( s )==int:
            v = s
        elif type( s )==float:
            v = int( s )
            if float( v )!=s: v = None
        isOk = v is not None and v>=42139 and v<=99999
        return isOk, v


    def _to_str (self, j):
        dt = datetime.datetime.fromordinal(datetime.datetime(1900, 1, 1).toordinal() + j - 2)
        tt = dt.timetuple()
        return "{:4}-{:02}-{:02}".format( tt.tm_year, tt.tm_mon, tt.tm_mday )


    def __str__ (self):
        return self._to_str( self.jDate if self.jDate is not None else "-" )



    def days_from_stamp (self, stamp=-1):
        if stamp<1431648000:	# 2015-05-15
            return 0
        days = int( stamp / 86400 ) + 719163
        return days



#
# CLASS MsTime
#
class MsTime():
    def __init__ (self, s=""):
        isOk, val = self._set_from_time( s )
        if isOk:
            self.jTime = val
        else:
            self.jTime = None


    def _set_from_time (self, s):
        isOk = False
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
            isOk = True
            r = comp
        else:
            if h is not None:
                isOk = True
                v = float(int(h))
                halves = float(h - v) * 60.0 / 100.0
                v += halves
                r = "{:.2f}".format(v).replace(".", ":")
        return isOk, r


    def __str__ (self):
        x = self.jTime
        if x is None:
            return "-"
        return x


#
# Test suite
#
if __name__ == "__main__":
    print("Module, please import it!")
    m = MsDate( 42139 )
    print(m)

