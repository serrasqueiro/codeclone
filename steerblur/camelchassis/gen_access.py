"""
 gen_access.py -- basic methods for file access
"""


from os import name, stat
from os.path import isdir, isfile
from getpass import getuser

try:
 import pwd
except ModuleNotFoundError:
 import winx_kernel as winpwd


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
    mode = wa.fileTrip[1].st_mode
    owner = wa.stat_user( wa.fileTrip )
    print("Owner is:", owner, ";", "octal:", wa.ux_octal_str( mode ))
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
    self.fileTrip = None


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
    self.fileTrip = (p, stat( p ), 0)
    return self.fileTrip


  def stat_user (self, aStat):
    if type( aStat )==tuple:
      assert len( aStat )==3
      fName = aStat[ 0 ]
      if self.is_win():
        pSD = winpwd.get_file_security( fName )
        uName = pSD.get_owner()[ 0 ]
      else:
        userInfo = pwd.getpwuid( aStat[ 1 ].st_uid )
        uName = userInfo.pw_name
    else:
      assert False
    return uName


  def ux_octal_str (self, mode):
    if type( mode )==int:
      if self.is_win():
        m = mode & 0o664
      else:
        m = mode
      s = "{0:03o}".format( m & 0o777 )
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
