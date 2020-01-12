# mempic.py  (c)2020  Henrique Moreira (part of 'jworks')

"""
  mempic module handles basic text memory files.

  Compatibility: python 3.
"""

from PIL import Image, ExifTags

#
# abstract CLASS RawPic
#
class RawPic:
    def __init__ (self, imgBuf=None):
        self.iBuf = imgBuf
        self.meta = None


#
# CLASS PicMem:
#
class PicMem(RawPic):
    def read (self, name):
        img = Image.open( name )
        ex = img.getexif()
        self.meta = {"EXIF": dict( ex ),
                     }
        return True


#
# No main...!
#
if __name__ == "__main__":
    print("see mempic.test.py")
