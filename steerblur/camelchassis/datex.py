# datex.py  (c)2018  Henrique Moreira (part of 'camelchassis')

"""
  datex - Common date functions.

  Compatibility: python 2 and 3.
"""

""" obsolete by adate.py

#
# test_datex()
#
def test_datex (outFile, inArgs):
  code = 0
  args = inArgs
  isOk = dateStyle.is_english_style()==False
  if len( args )<=0:
    return test_datex( outFile, ["31/12"] )
  smallDate = args[ 0 ]
  dt = ShortDate( smallDate )
  print(dt, "dt.dateOk?", dt.dateOk)
  if dt.month==2:
    for y in [2018, 2016]:
      isOk = dt.set_year( y )
      print("Trying year", y, "for", dt, "Ok?", isOk, "dateOk?", dt.dateOk)
  if True:
    euroDate = EuDate( args[ 0 ] )
    ed = euroDate
    print(ed, "ed.dateOk?", ed.dateOk)
  return code



#
# CLASS DateStylex() -- type of dates, depending on your preference
#
class DateStylex:
  def __init__ (self):
    self.dateOk = False
    self.dateDDMMYY = 1
    self.monthDays = (0, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
    assert len(self.monthDays)==12+1


  def set_english_style (self):
    self.dateDDMMYY = 0


  def is_english_style (self):
    isEnglish = self.dateDDMMYY==0
    if isEnglish:
      return True
    assert self.dateDDMMYY<=2
    return False


  def is_leap_year (self, year):
    isLeap = ((year % 4 == 0) and (year % 100 != 0)) or (year % 400 == 0)
    print("year", year, "isLeap?", isLeap)
    return isLeap


  pass


#
# CLASS AnyDate (abstract)
#
class AnyDate:
  def __init__ (self, s=""):
    self.aString = ""
    self.mjd = -1	# modified Julian Date
    self.day = 0
    self.month = 0
    self.year = 1900
    self.mainSeparator = '/'
    self.separators = ['/', '-', '.']
    code = self.date_init( s )
    pass


  def basic_dm_check (self, dStr, mStr, yStr=""):
    d = -1
    m = -1
    badTuple = (False, d, m)
    try:
      d = int( dStr )
      m = int( mStr )
    except:
      return badTuple
    isOk = m>=1 and m<=12 and (d>=1 and d<=dateStyle.monthDays[ m ])
    if isOk==False:
      return badTuple
    if yStr=="" or m!=2:
      return (True, d, m)
    # Check leap-years
    dOfMonth = dateStyle.monthDays[ 2 ] - int( dateStyle.is_leap_year( int( yStr ) )==False )
    isOk = d<=dOfMonth
    return (isOk, d if isOk else dOfMonth, m)


  pass


#
# CLASS ShortDate
#
class ShortDate(AnyDate):
  def date_init (self, s):
    if type( s )==list:
      aStr = self.mainSeparator.join( s )
      if len( s )>0 and len( aStr )>0:
        return self.date_init( aStr )
      return -1
    self.dateOk = self.try_date( s )
    return 0


  def __str__ (self):
    assert self.year>=1900
    s = format( self.year, "04d" ) + self.mainSeparator + format( self.month, "02d" ) + self.mainSeparator + format( self.day, "02d" )
    return s


  def try_date (self, s):
    assert type( s )==str
    for tryLen in [3, 2]:
      for sep in self.separators:
        spl = s.split( sep )
        if len( spl )!=tryLen:
          continue
        isEnglish = dateStyle.is_english_style()
        if isEnglish:
          m = spl[ 0 ]
          d = spl[ 1 ]
        else:
          d = spl[ 0 ]
          m = spl[ 1 ]
        tup = self.basic_dm_check( d, m )
        isOk = tup[ 0 ]
        if isOk:
          self.day = tup[ 1 ]
          self.month = tup[ 2 ]
          return True
    return False


  def set_year (self, aYear):
    assert aYear>=1900
    isOk = aYear<=2999
    if isOk==False:
      return False
    tup = self.basic_dm_check( self.day, self.month, str(aYear) )
    isOk = tup[ 0 ]
    if isOk==False:
      return False
    self.year = aYear
    return True


  pass


#
# CLASS EuDate
class EuDate(AnyDate):
  def date_init (self, s):
    self.leadYear = -1
    if type( s )==list:
      aStr = self.mainSeparator.join( s )
      if len( s )>0 and len( aStr )>0:
        return self.date_init( aStr )
      return -1
    self.dateOk = self.try_date( s )
    return 0


  def try_date (self, s):
    assert type( s )==str
    for tryLen in [3]:
      for sep in self.separators:
        spl = s.split( sep )
        if len( spl )!=tryLen:
          continue
        isEnglish = dateStyle.is_english_style()
        yStr = spl[ 2 ]
        if isEnglish:
          m = spl[ 0 ]
          d = spl[ 1 ]
        else:
          # Check whether it is YYYY-mm-dd or dd-mm-YYYY
          d = spl[ 0 ]
          m = spl[ 1 ]
          if len( d )==4:
            self.leadYear = 1
            yStr = d
            d = spl[ 2 ]
          elif len( yStr )==4:
            self.leadYear = 3
            pass
        tup = self.basic_dm_check( d, m, yStr )
        isOk = tup[ 0 ]
        if isOk:
          y = int( yStr )
          self.year = y
        if isOk:
          self.day = tup[ 1 ]
          self.month = tup[ 2 ]
          print("Ok, yStr:", yStr, "day:", self.day, "month:", self.month, "year:", self.year)
          return True
    return False


  def __str__ (self):
    assert self.year>=1900
    dayStr = format( self.day, "02d" )
    monthStr = format( self.month, "02d" )
    if self.year<=1900:
      s = "--/--/----"
      return s
    yearStr = format( self.year, "04d" )
    s = dayStr + self.mainSeparator + monthStr + self.mainSeparator + yearStr
    return s


  pass


#
# GLOBAL singleton
#
dateStyle = DateStylex()

"""


#
# Test suite
#
if __name__ == "__main__":
  print("Obsolete module.")
  #import sys
  #args = sys.argv[ 1: ]
  #code = test_datex( sys.stdout, args )
  pass

