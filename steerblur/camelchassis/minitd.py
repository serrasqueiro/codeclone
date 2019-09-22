# minitd.py  (c)2019  Henrique Moreira (part of 'camelchassis')

"""
  minitd - Mini Table database

  Compatibility: python 3.
"""

try:
  import fcntl
except ImportError:
  pass


#
# test_minitd()
#
def test_minitd (outFile, errFile, inArgs):
  code = None
  try:
    cmd = inArgs[ 0 ]
  except:
    return None
  param = inArgs[ 1: ]
  if cmd=="test":
    tdb = MiniTD()
  if cmd=="show":
    fn = param[ 0 ]
    tdb = MiniTD()
    err = tdb.set_file( fn )
    code = err[0]
    isOk = code==0
    if not isOk:
      errFile.write("Error {}, cannot read '{}': {}".format( code, fn, err[1] ))
      return 2
    full = tdb.read_to_mem()
    tdb.unlock()
    idx = 0
    cont = full[ 1 ]
    for r in cont:
      idx += 1
      outFile.write("{}: {}\n".format( idx, r ))
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
    return True


  def lock_handle (self):
    # fcntl.lockf(self.ioPtr, fcntl.LOCK_EX | fcntl.LOCK_NB)
    return True


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
  def __init__ (self):
    self.init_anytd()
    self.locked = None


  def set_file (self, aName, lockMethod=None):
    assert type( aName )==str
    self.filename = aName
    self.ioPtr = None
    try:
      self.ioPtr = open( aName, "rb" )
    except Exception as ex:
      return self.fine_error( ex )
    self.lock_handle()
    return (0, ".")


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
# Test suite
#
if __name__ == "__main__":
  import sys
  args = sys.argv[ 1: ]
  code = test_minitd( sys.stdout, sys.stderr, args )
  if code is None:
    print("""minitd.py command

Commands are:
  test            Testing this package.

  show file       Show tdb file.
""")
  sys.exit( code )

