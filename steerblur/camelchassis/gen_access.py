"""
 gen_access.py -- basic methods for file access
"""


from os import name, stat
from os.path import isdir, isfile
from getpass import getuser

try:
 import pwd
except ModuleNotFoundError:
 import winpwd as pwd


#
# test_gen_access()
#
def test_gen_access (inArgs):
  code = 0
  wa = wideAccess
  isOk = wa.store_user()
  assert isOk
  args = inArgs
  if args==[]:
    args = ["/var/run/widedbz", "/var/run/widedbz/"+wa.user]
  print("Who am I:", wa.user)
  for a in args:
    d = wa.is_dir( a )
    f = wa.is_file( a )
    p = wa.lastPath
    print("Is dir:", p, "? " + "Yes" if d else "No")
    print("Is file:", a, "? " + "Yes" if f else "No")
    wa.a_stat( p )
    mode = wa.fileStat.st_mode
    print("Owner is:", wa.stat_user( wa.fileStat ), ";", "octal:", wa.ux_octal_str( mode ))
    print("")
  return code


#
# CLASS WideAccess
#
class WideAccess:
  def __init__ (self, storeUser=False):
    self.myOS = name
    self.lastPath = None
    self.user = "nobody"
    if storeUser:
      self.store_user()
    self.fileStat = None


  def is_win (self):
    return name=="nt"


  def is_dir (self, p):
    path = self.os_path( p )
    return isdir( path )

  def is_file (self, p):
    path = self.os_path( p )
    return isfile( path )


  def os_path (self, path):
    if path.find( "file:///" )==0:
      p = path[ len( "file:///" ): ]
    else:
      p = path
    if p!="/":
      while p.endswith( "/" ):
        p = p[ :-1 ]
    self.lastPath = p
    if self.is_win():
      s = p.replace( "/", "\\" )
    else:
      s = p
    return s


  def store_user (self):
    w = getuser()
    if w is None:
      return False
    self.user = w
    return True


  def a_stat (self, path):
    p = self.os_path( path )
    self.fileStat = stat( p )
    return self.fileStat


  def stat_user (self, aStat):
    userInfo = pwd.getpwuid( aStat.st_uid )
    print("userInfo:", userInfo)
    return userInfo.pw_name


  def ux_octal_str (self, mode):
    if type( mode )==int:
      s = "{0:03o}".format( mode & 0o777 )
    else:
      assert False
    return s


#
# Global
#
wideAccess = WideAccess()


#
# Test suite
#
if __name__ == "__main__":
  import sys
  args = sys.argv[ 1: ]
  code = test_gen_access( args )
  sys.exit( code )
