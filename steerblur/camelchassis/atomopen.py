"""
 atomopen.py -- locks files before using them.
"""


import os
from sys import stderr
from time import sleep


try:
  # Posix based file locking (Linux, Ubuntu, MacOS, etc.)
  import fcntl
  def lock_file (f, fSize=0, info=None):
    if info:
      info.write("Locking: " + f.name + "\n")
    fcntl.lockf(f, fcntl.LOCK_EX)
    return True
  def unlock_file (f, fSize=0, info=None):
    fcntl.lockf(f, fcntl.LOCK_UN)
    if info:
      info.write("Unlocked: " + f.name + "\n")
    return True
except ModuleNotFoundError:
  # Windows file locking
  import msvcrt
  def lock_file (f, fSize, info=None):
    if info:
      info.write("Locking: " + f.name + "\n")
    msvcrt.locking(f.fileno(), msvcrt.LK_RLCK, 1)
    return True
  def unlock_file (f, fSize, info=None):
    try:
      msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)
      isOk = True
    except:
      isOk = False
    if info and isOk:
      info.write("Unlocked: " + f.name + "\n")
    return True


def file_size (f):
  size = os.path.getsize( os.path.realpath(f.name) )
  print("Size:", f.name, "is:", size)
  return size


#
# test_atomopen()
#
def test_atomopen (inArgs):
  cmd = inArgs[ 0 ]
  args = inArgs[ 1: ]
  if cmd=="lock":
    name = args[ 0 ]
    del args[ 0 ]
    with AtomicOpen( name, "a" ) as aop:
      for line in args:
        if line.find( "sleep:" )==0:
          slp = float( line.split( ":" )[ 1 ] )
          print("sleeping...", slp)
          try:
            sleep( slp )
          except:
            print("Breaked by user.")
          continue
        aop.write( line + "\n" )
      print("Ending AtomicOpen:", name)
  if cmd=="unlock":
    name = args[ 0 ]
    ao = AtomicOpen( name )
  return 0


#
# CLASS GenOpen
#
class GenOpen:
  def init_info (self, infoFile):
    self.info = infoFile


  def init_file (self, f):
    assert f
    self.file = f
    self.fileSize = file_size( f )


  pass


# Class for ensuring that all file operations are atomic, treat 
# initialization like a standard call to 'open' that happens to be atomic.
# This file opener *must* be used in a "with" block.
class AtomicOpen(GenOpen):
  # Open the file with arguments provided by user. Then acquire 
  # a lock on that file object (WARNING: Advisory locking).
  def __init__ (self, path, *args, **kwargs):
    self.init_info( stderr )
    # Open the file and acquire a lock on the file before operating
    self.init_file( open(path, *args, **kwargs) )
    # Lock the opened file
    lock_file( self.file, self.fileSize, self.info )


  def __enter__ (self, *args, **kwargs):
    return self.file


  def __exit__ (self, exc_type=None, exc_value=None, traceback=None):
    # Flush to make sure all buffered contents are written to file.
    self.file.flush()
    os.fsync(self.file.fileno())
    # Release the lock on the file.
    unlock_file( self.file, self.fileSize, self.info )
    self.file.close()
    # Handle exceptions that may have come up during execution, by
    # default any exceptions are raised to the user.
    if (exc_type != None):
      return False
    else:
      return True


  pass


#
# Test suite
#
if __name__ == "__main__":
  import sys
  args = sys.argv[ 1: ]
  code = test_atomopen( args )
  sys.exit( code )
