# six_rsa.py  (c)2019  Henrique Moreira (part of 'mlaby')

"""
  six_rsa module: Simple and eXtended RSA functions.

  Compatibility: python 2 and 3.
"""


from base64 import b64decode, b64encode


#
# test_six_rsa()
#
def test_six_rsa (out, inArgs):
  code = 0
  verbose = 1
  args = ["host-priv", "/etc/ssh/ssh_host_rsa_key"] if inArgs==[] else inArgs
  cmd = args[ 0 ]
  try:
    a = args[ 1 ]
  except:
    a = "/tmp/rsa_key"
  if cmd=="host-priv":
    print("Host private key:", a)
    pKey = HostPrivateKey( a )
    isOk = pKey.is_ok()
    print( "{"+str( pKey )+"}", "(OK)" if isOk else "(NotOk)")
    textEnc = pKey.textual_encoding()
    if verbose>0:
      print("MIME64 size:", pKey.mime64Size, "Max.bin.size:", pKey.mime64Size * 3/4.0, "; key bin size:", len(pKey.key))
      print("---> textual_encoding() as follow --->")
      print( textEnc )
    if not isOk:
      print("\nERRORs follow:", pKey.errors)
  return code


"""
RFC 7468 clarifies the PKCS#8/PrivateKeyInfo

-----BEGIN RSA PRIVATE KEY-----
<<1616 MIME64 chars, separated in 64 column lines>>
-----END RSA PRIVATE KEY-----
"""


#
# CLASS AnyPrivKey
#
class AnyPrivKey:
  def init_any_priv_key (self):
    self.errors = []
    self.key = b''


  def is_ok (self):
    return len( self.errors )==0 and len( self.key )>=512


  pass


#
# CLASS HostPrivateKey -- handles host private key files
#
class HostPrivateKey(AnyPrivKey):
  def __init__ (self, fileOrCont):
    self.init_any_priv_key()
    self.orig64 = []
    self.mime64Size = 0
    self.init_private_key( fileOrCont )


  def init_private_key (self, fileOrCont):
    if type( fileOrCont )==str:
      tup = self.read_from_file( fileOrCont )
    else:
      assert False


  def read_from_file (self, path, sep=" PRIVATE "):
     assert type( path )==str
     p = open( path, "r" )
     cont = p.read()
     spl = cont.split( sep  )
     for tuk in spl:
       lines = tuk.split( "\n" )
       for item in lines:
         aLen = len( item )
         if aLen<=0:
           continue
         isMIME = item.find( "-" )==-1
         if isMIME:
           self.orig64.append( item )
           self.mime64Size += aLen
         else:
           try:
             which = ["KEY-----",
                      "-----BEGIN RSA",
                      "-----END RSA"].index( item )
           except:
             self.errors.append( "Invalid key: '{}'".format( item ) )
     self.set_from_mime64()
     return (True, self.key)


  def textual_encoding (self, head="RSA PRIVATE KEY"):
    # RFC7468, section 2 (General Considerations)
    s1 = "-----BEGIN {}-----".format( head )
    s2 = "-----END {}-----".format( head )
    y = b64encode( self.key ).decode()
    if head and len( head )>0:
      s = s1 + "\n" + mime_lines( y ) + s2
    else:
      s = mime_lines( y )
    return s


  def mime64_str (self):
    return '\n'.join( self.orig64 ).strip( "\n" )


  def __str__ (self):
    return self.mime64_str()


  def set_from_mime64 (self):
    b = self.mime64_str()
    self.key = b64decode( b )


#
# mime_lines()
def mime_lines (sInput, maxColumns=64):
  idx = 0
  s = ""
  while idx < len( sInput ):
    now = idx + maxColumns
    s += sInput[ idx:now ] + "\n"
    idx = now
  return s


#
# Test suite
#
if __name__ == "__main__":
  import sys
  outFile = sys.stdout;
  code = test_six_rsa( outFile, sys.argv[ 1: ] )
  sys.exit( code )

