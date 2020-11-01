# six_rsa.py  (c)2019  Henrique Moreira (part of 'mlaby')

"""
  six_rsa module: Simple and eXtended RSA functions.

  Compatibility: python 2 and 3.
"""

# pylint: disable=missing-function-docstring

import sys
from base64 import b64decode, b64encode
from mlaby.amath import calcNum


def main():
    """ Main script """
    outFile = sys.stdout;
    code = test_six_rsa(outFile, sys.argv[ 1: ])
    sys.exit(code)


def test_six_rsa (out, inArgs):
    assert out
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
        print("{"+str( pKey )+"}", "(OK)" if isOk else "(NotOk)")
        textEnc = pKey.textual_encoding()
        if verbose>0:
            print("MIME64 size:", pKey.mime64Size,
                  "Max.bin.size:", pKey.mime64Size * 3/4.0,
                  "; key bin size:", len(pKey.key))
            print("---> textual_encoding() as follow --->")
            print(textEnc)
        if not isOk:
            print("\nERRORs follow:", pKey.errors)
    if cmd=="raw-hash":
        pKey = HostPrivateKey( a )
        assert pKey.is_ok()
        for k in pKey.orig64:
            h = calcNum.hash1000( k )
            print("{:03d} {}".format( h, k ))
    if cmd=="raw-hex":
        pKey = HostPrivateKey( a )
        assert pKey.is_ok()
        pKey.to_hex()
        h = pKey.hex
        x = pKey.magic_hash()
        print("pKey.hex, len:", len(pKey.key), "(OK)" if 2*len(pKey.key)==len( h ) else "NotOk")
        print(h)
        print("---\n\npKey.magic_hash():", x)
    return code


"""
RFC 7468 clarifies the PKCS#8/PrivateKeyInfo

-----BEGIN RSA PRIVATE KEY-----
<<1616 MIME64 chars, separated in 64 column lines>>
-----END RSA PRIVATE KEY-----
"""


class AnyPrivKey:
    """ Any Private Key """
    def init_any_priv_key (self):
        self.errors = []
        self.key = b''
        self.hex = None

    def is_ok (self):
        return len( self.errors )==0 and len( self.key )>=512


class HostPrivateKey(AnyPrivKey):
    """ Handles host private key files """
    def __init__ (self, fileOrCont):
        self.init_any_priv_key()
        self.orig64 = []
        self.mime64Size = 0
        tup = self._init_private_key( fileOrCont )
        assert tup is not None


    def _init_private_key (self, fileOrCont):
        if isinstance(fileOrCont, str):
            return self.read_from_file( fileOrCont )
        return None


    def read_from_file (self, path, sep=" PRIVATE "):
        p = open(path, "r")
        cont = p.read()
        spl = cont.split(sep)
        for tuk in spl:
            lines = tuk.split("\n")
            for item in lines:
                aLen = len(item)
                if aLen <= 0:
                    continue
                isMIME = item.find("-")==-1
                if isMIME:
                    self.orig64.append(item)
                    self.mime64Size += aLen
                else:
                    try:
                        which = ["KEY-----",
                                 "-----BEGIN RSA",
                                 "-----END RSA"].index( item )
                    except:
                        self.errors.append("Invalid key: '{}'".format( item ))
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


    def to_hex (self):
        h = ""
        for num in self.key:
            nibble = "{0:02x}".format( num )
            h += nibble
        self.hex = h
        return h


    def magic_hash (self):
        if self.hex is None:
            to_hex()
        subj = self.hex[ :64 ] + self.hex[ 80:86 ]
        num = calcNum.hash1000( subj, 9 )
        s = "0x{0:08x}".format( num )
        # s += " {:d}d".format( num )
        return s


def mime_lines (sInput, maxColumns=64):
    """ Basic MIME lines """
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
    main()
