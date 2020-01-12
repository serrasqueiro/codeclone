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
        aDict = dict(ex) if ex is not None else None
        self.meta = {"EXIF": aDict,
                     "EXIF-getexif()": ex,
                     "main": dict(),
                     "info": None,
                     }
        self._base_parse( ex, self.meta )
        return True


    def get_info (self):
        assert self.meta is not None
        return self.meta["EXIF"]


    def _base_parse (self, exifInfo, outMeta):
        if exifInfo is None:
            return False
        width, height = -1, -1
        dMain = {"x": dict(),
                 "y": dict(),
                 }
        for key, val in exifInfo.items():
            if key not in ExifTags.TAGS:
                continue
            tagName = ExifTags.TAGS[key]
            xKey = tagName.lower()
            if xKey.find("width")>=0:
                dMain["x"][tagName] = val
                if xKey.startswith("exif"): width = int( val )
            elif xKey.find("height")>=0:
                dMain["y"][tagName] = val
                if xKey.startswith("exif"): height = int(val)
        dInfo = {"width": width,
                 "height": height,
                 }
        outMeta["main"] = dMain
        outMeta["info"] = dInfo
        return True


#
# No main...!
#
if __name__ == "__main__":
    print("see mempic.test.py")
