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
        self.pict = Pict( img )
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


    def has_exif (self):
        sizeX, sizeY = self.meta["info"]["width"], self.meta["info"]["height"]
        if sizeX==-1:
            assert sizeY==-1
        return sizeX>0


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
# CLASS Pict
#
class Pict():
    def __init__ (self, img=None):
        self.img = img
        self._parse_picture( img )


    def _parse_picture (self, img):
        """
        Parses PIL image
        :param img:
        :return: bool (whether image is correct)
        """
        if img is None: return False
        """
        See also:
		https://stackoverflow.com/questions/6444548/how-do-i-get-the-picture-size-with-pil
        """
        self.size = img.size  # size[0]=x, size[1]=y
        return True


    def width (self):
        return self.size[0]


    def height (self):
        return self.size[1]


#
# No main...!
#
if __name__ == "__main__":
    print("see mempic.test.py")
