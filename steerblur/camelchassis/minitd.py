# minitd.py  (c)2019  Henrique Moreira (part of 'camelchassis')

"""
  minitd - Mini Table database

  Compatibility: python 3.
"""

import os
try:
  import fcntl
except ImportError:
  import msvcrt


#
# test_minitd()
#
def test_minitd (outFile, errFile, inFile, inArgs):
  code = None
  verbose = 0
  try:
    cmd = inArgs[ 0 ]
  except:
    return None
  param = inArgs[ 1: ]
  while len( param )>0 and param[ 0 ].startswith( "-" ):
    if param[ 0 ].startswith( "-v" ):
      verbose += param[ 0 ].count( "v" )
      del param[ 0 ]
      continue
    print("Invalid option:", param[0])
    return None
  if cmd=="test":
    tdb = MiniTD()
    isOk = tdb.locked==None
    assert isOk
    code = 0
  if cmd=="show":
    fn = param[ 0 ]
    tdb = MiniTD()
    err = tdb.set_file( fn )
    code = err[0]
    isOk = code==0
    if not isOk:
      errFile.write("Error {}, cannot read '{}': {}\n".format( code, fn, err[1] ))
      return 2
    full = tdb.read_to_mem()
    tdb.unlock()
    idx = 0
    cont = full[ 1 ]
    for r in cont:
      idx += 1
      outFile.write("{}: {}\n".format( idx, r ))
  if cmd=="lock":
    fn = param[ 0 ]
    tdb = MiniTD( fn )
    if tdb.ioPtr is None:
      return 2
    print("File locked {}: {}".format( tdb.filename, tdb.locked ))
    while True:
      c = inFile.read( 1 )
      if c.startswith( "." ):
        break
    tdb.close()
    code = 0
  if verbose>0:
    errFile.write("minitd returns: {}\n".format( code ))
  return code


#
# CLASS AnyTD
#
class AnyTD:
  def init_anytd (self):
    self.filename = None
    self.ioPtr = None


  def close (self, debug=0):
    if self.ioPtr is not None:
      if debug>0:
        print("Closing:", self.filename)
      self.ioPtr.close()
      self.locked = None
    return True


  def lock_handle (self, who="me", lockMethod="L", debug=0):
    isOk = True
    assert lockMethod=="L"
    self.locked = who
    if is_win_env():
      file_lock( self.ioPtr, self.filename )
    else:
      try:
        fcntl.flock(self.ioPtr.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
      except Exception as ex:
        self.locked = "failed:{}".format( ex )
        isOk = False
    return isOk


  def unlock (self):
    # from filelock import FileLock --> https://stackoverflow.com/questions/489861/locking-a-file-in-python
    self.locked = None
    return self.close()


  def fine_error (self, ex=None):
    # ex is the exception error
    if ex is None or ex.errno==0:
      return (0, "")
    s = ex.strerror
    tup = (ex.errno, s if s!="" else "?")
    return tup


#
# CLASS MiniTD
#
class MiniTD(AnyTD):
  def __init__ (self, aName=None, doRead="r"):
    self.init_anytd()
    self.locked = None
    if aName is not None:
      self.set_file( aName, "L" )
    pass


  def set_file (self, aName, lockMethod=None):
    assert type( aName )==str
    self.filename = aName
    self.ioPtr = None
    try:
      self.ioPtr = open( aName, "rb" )
    except Exception as ex:
      return self.fine_error( ex )
    if lockMethod is not None:
      if not self.lock_handle( "me", lockMethod ):
        return (11, "Temp. unavailable")
    return (0, ".")


  def append (self):
    assert self.filename is not None
    assert self.locked is None
    self.ioPtr = open(self.filename, "ab")
    return self.lock_handle()


  def read_to_mem (self):
    assert self.ioPtr is not None
    buf = self.ioPtr.read().decode( "ascii" )
    cont = buf.split( "\n" )
    while len( cont )>0:
      s = cont[ -1 ]
      if s=="":
        del cont[ -1 ]
      else:
        break
    head = ""
    if len( cont )>0:
      head = cont[ 0 ] if cont[ 0 ].startswith( "#" ) else ""
      if head!="":
        payload = cont[ 1: ]
      else:
        payload = cont
    res = ({"head":head,
            }, payload )
    return res


  def __del__ (self):
    self.close()


#
# is_win_env()
#
def is_win_env ():
  return os.name=="nt"


#
# file_lock()
#
def file_lock (fileStream, aFilename):
  """
    LK_UNLCK = 0  # unlock the file region
    LK_LOCK = 1  # lock the file region
    LK_NBLCK = 2  # non-blocking lock
    LK_RLCK = 3  # lock for writing
    LK_NBRLCK = 4  # non-blocking lock for writing
  """
  LK_LOCK = 1
  if is_win_env():
    msvcrt.locking(fileStream.fileno(), LK_LOCK, os.path.getsize(aFilename))
  return True


#
# file_unlock()
#
def file_unlock (fileStream, aFilename):
  LK_UNLOCK = 0
  if is_win_env():
    msvcrt.locking(fileStream.fileno(), LK_UNLOCK, os.path.getsize(aFilename))
  return True


#
# Test suite
#
if __name__ == "__main__":
  import sys
  args = sys.argv[ 1: ]
  code = test_minitd( sys.stdout, sys.stderr, sys.stdin, args )
  if code is None:
    print("""minitd.py command

Commands are:
  test            Testing this package.

  show file       Show tdb file.
""")
  sys.exit( code )

