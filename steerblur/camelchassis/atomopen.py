"""
 atomopen.py -- locks files before using them.
"""


import os
from sys import stderr
from time import sleep

global_atom_debug=0
global_atom_encoding=""


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
    return isOk


def file_size (f):
  size = os.path.getsize( os.path.realpath(f.name) )
  return size


#
# test_atomopen()
#
def test_atomopen (inArgs):
  global global_atom_debug
  cmd = inArgs[ 0 ]
  args = inArgs[ 1: ]
  code = 0
  if cmd=="lock":
    doAny = True
    while len( args )>0 and doAny:
      doAny = False
      if args[ 0 ]=='-v':
        doAny = True
        global_atom_debug = 9
        del args[ 0 ]
        continue
    name = args[ 0 ]
    del args[ 0 ]
    with AtomicOpen( name, "a" ) as aop:
      if aop.errorCode!=0:
        print("Bogus:", name)
      for line in args:
        if line=="":
          continue
        if line.find( "sleep:" )==0:
          slp = float( line.split( ":" )[ 1 ] )
          print("sleeping...", slp)
          try:
            sleep( slp )
          except:
            print("Breaked by user.")
          continue
        if aop.file:
          aop.file.write( line + "\n" )
        else:
          print("Did not write:", line)
      #print("Ending AtomicOpen:", name)
      pass
  if cmd=="unlock":
    global_atom_debug = 9
    isOk = False
    name = args[ 0 ]
    if name:
      print("unlock_file():", name)
      f = open( name, "r" )
      with GenHandler( f ) as handler:
        isOk = unlock_file( handler.file, 1, stderr )
    code = 0 if isOk else 1
  return code


#
# CLASS GenHandler
#
class GenHandler:
  def __init__ (self, f, comment=""):
    self.errorCode = 0
    self.file = f
    if comment!="":
      self.comment = comment
    else:
      self.comment = f.name if f else "."
    pass


  def close (self):
    global global_atom_debug
    if self.file:
      if global_atom_debug>=9:
        print("Closed:", self.comment)
      self.file.close()
      self.file = None
      return True
    return False


  def __enter__ (self, *args, **kwargs):
    return self


  def __exit__ (self, exc_type=None, exc_value=None, traceback=None):
    global global_atom_debug
    if self.file:
      if global_atom_debug>=9:
        print("Closing handler:", self.comment)
      self.file.close()
      self.file = None
    return True


  def __str__ (self):
    return self.comment


#
# CLASS GenOpen
#
class GenOpen:
  def init_info (self, infoFile):
    self.info = infoFile


  def init_file (self, f):
    self.bogus = 0
    isOk = False
    self.handler = GenHandler( f )
    if f:
      isOk = True
      self.fileSize = file_size( f )
    else:
      self.fileSize = -1
    return isOk


  pass


# Class for ensuring that all file operations are atomic, treat 
# initialization like a standard call to 'open' that happens to be atomic.
# This file opener *must* be used in a "with" block.
class AtomicOpen(GenOpen):
  # Open the file with arguments provided by user. Then acquire 
  # a lock on that file object (WARNING: Advisory locking).
  def __init__ (self, path, *args, **kwargs):
    global global_atom_debug
    self.init_info( stderr if global_atom_debug>0 else None )
    # Open the file and acquire a lock on the file before operating
    if global_atom_debug>=9:
      print("args:", type(args), len(args), "; are:", args)
      print("kwargs:", kwargs)
      for key, val in kwargs.items():
        print("key:", key, "val:", val)
    if path!="":
      try:
        f = open(path, *args, **kwargs)
      except:
        f = None
      self.init_file( f )
      if f:
        lock_file( self.handler.file, self.fileSize, self.info )
      else:
        self.handler.errorCode = 1
        if global_atom_debug>0:
          stderr.write("Uops, errorCode="+str(self.handler.errorCode)+ ": " + path + "\n")
    else:
      self.init_file( None )
    pass


  def __enter__ (self, *args, **kwargs):
    return self.handler


  def __exit__ (self, exc_type=None, exc_value=None, traceback=None):
    # Flush to make sure all buffered contents are written to file.
    if self.handler.file:
      self.handler.file.flush()
      os.fsync(self.handler.file.fileno())
      # Release the lock on the file.
      unlock_file( self.handler.file, self.fileSize, self.info )
      self.handler.file.close()
      # Handle exceptions that may have come up during execution, by
      # default any exceptions are raised to the user.
      if (exc_type != None):
        return False
      else:
        return True
    pass


  pass


#
# Test suite
#
if __name__ == "__main__":
  import sys
  args = sys.argv[ 1: ]
  code = test_atomopen( args )
  sys.exit( code )
