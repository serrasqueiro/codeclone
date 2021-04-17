# (c)2019, 2021  Henrique Moreira

"""
 cchome.py -- basic methods for home vars
"""

import sys
import os
from os.path import isdir, isfile
import base64

def main():
    """ Main tests """
    args = sys.argv[1:]
    code = test_cchome(sys.stdout, sys.stderr, args)
    sys.exit(code)


#
# test_cchome()
#
def test_cchome (outFile, errFile, inArgs):
    code = 0
    showPassword = True
    bHome = BasicHome( ".gpconfig" )
    print("bHome, homeDir:", bHome.homeDir, "; config:", bHome.configFileName)
    hasConfig = bHome.hasConfig
    print("configs{}:".format( " (has no config)" if not hasConfig else "" ))
    for k, val in bHome.configs.items():
        print("key='{}': {}".format( k, val ))
    hashedConfig = ConfigLines( [], bHome.configs )
    hashedConfig.mini_hash()
    for item in ( "user",
                  ):
        print("List item:", item)
        d = hashedConfig.items[ item ]
        for k, val in d.items():
            s = val
            if k=="password" and showPassword:
                s = hashedConfig.string_password( val )
            assert type( s )==str
            print("sub-item {}.{}: {}".format( item, k, s ))
    return code


#
# CLASS BasicHome
#
class BasicHome:
    def __init__ (self, basicConfig=".cchome.txt", autoRead=True):
        self.isWin = os.name=="nt"
        self.homeDir = None
        self.set_home()
        assert self.homeDir is not None
        self.hasConfig = self.set_config( self.homeDir, basicConfig )
        if self.hasConfig:
            self.configs = self.get_config( self.configFileName )
        else:
            self.configs = {"user":[]}
        assert "user" in self.configs


    def set_home (self):
        try:
            userProfile = os.environ[ "USERPROFILE" ]
        except:
            userProfile = None
        if userProfile is None:
            userProfile = os.environ[ "HOME" ]
        isDir = isdir( userProfile )
        isOk = isDir
        if isDir:
            self.homeDir = userProfile
        return isOk


    def set_config (self, hDir, bConfigName):
        assert type( bConfigName )==str
        isOk = False
        if bConfigName.find( "/" )>=0 or bConfigName.find( "\\" )>=0:
            p = bConfigName
        else:
            p = os.path.join( self.homeDir, bConfigName )
        isOk = isfile( p )
        self.configFileName = p
        return isOk


    def get_config (self, bConfigName):
        op = open( bConfigName, "r" )
        lines = op.read().split("\n")
        confLines = ConfigLines( lines )
        return confLines.parse_config()


#
# CLASS ConfigLines
#
class ConfigLines:
    def __init__ (self, lines=[], fullConfig={}):
        self.lines = lines
        self.fullConfig = fullConfig


    def parse_config (self):
        dct = self.feed_config( self.lines )
        return dct


    def feed_config (self, lines):
        lastKey = None
        dct = dict()
        for x in lines:
            if x.startswith("[") and x.endswith("]"):
                k = x[1:-1].strip()
                lastKey = k
                dct[ k ] = []
            elif x=="":
                pass
            else:
                if lastKey is not None:
                    assert x==x.strip()
                    dct[ lastKey ].append( x )
        return dct


    def mini_hash (self):
        self.items = dict()
        for k, aList in self.fullConfig.items():
            self.items[ k ] = dict()
            # k='user', list is e.g. [email=a, password=b]
            for e in aList:
                pos = e.find( "=" )
                if pos>0:
                    left = e[ :pos ].strip()
                    right = e[ pos+1: ].strip()
                    self.items[ k ][ left ] = right
                else:
                    self.items[ k ][ e ] = "TRUE"
        return True


    def string_password (self, sBase64):
        if type( sBase64 )==str:
            aBin = bytes( sBase64, "ascii" )
        else:
            aBin = None
        assert aBin is not None
        b = self.decode_base64( aBin )
        s = b.decode( "ascii" )
        return s


    def decode_base64 (self, aBin):
        assert type( aBin )==bytes
        b = base64.b64decode( aBin )
        return b


#
# Test suite
#
if __name__ == "__main__":
    main()
