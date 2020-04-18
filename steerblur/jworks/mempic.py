# mempic.py  (c)2020  Henrique Moreira (part of 'jworks')

"""
  mempic module handles basic text memory files.

  Compatibility: python 3.
"""

# pylint: disable=missing-function-docstring, invalid-name

from PIL import Image, ExifTags
from jworks.edates import exif_date, exif_str_date


class TagsExif():
    """
    TagsExif class -- has dual id to string and string to id
    """
    str_to = None
    thisExifInfo = None
    _exif_tags = None

    def __init__(self):
        self._exif_tags = ExifTags.TAGS
        self.str_to = self._init_tags()

    def get_index(self, s):
        if isinstance(s, str):
            i_val = self.str_to.get(s)
        else:
            assert False
        if i_val is None:
            return -1
        assert isinstance(i_val, int)
        return i_val

    def get_info(self, idx):
        assert isinstance(idx, int)
        assert self.thisExifInfo is not None
        return self.thisExifInfo[idx]

    def what_date(self, keyName=""):
        assert isinstance(keyName, str)
        if keyName == "":
            k = "DateTime"
        else:
            k = keyName
        idx = self.get_index(k)
        return self.get_info(idx)

    def _init_tags(self):
        dct = dict()
        for i_val, s in self._exif_tags.items():
            if s != "":
                dct[s] = i_val
        return dct


class RawPic:
    """ Abstract class RawPic """
    _ibuf = None

    def __init__ (self, img_buf=None):
        self._ibuf = img_buf

    def buffer(self):
        return self._ibuf


class PicMem(RawPic):
    """ Picture Memory """
    pict = None
    meta = dict()

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
        self._base_parse(ex)
        return True


    def get_info (self):
        assert self.meta is not None
        return self.meta["EXIF"]


    def has_exif (self):
        sizeX, sizeY = self.meta["info"]["width"], self.meta["info"]["height"]
        if sizeX == -1:
            assert sizeY == -1
        return sizeX > 0


    def _base_parse (self, exifInfo):
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
            if xKey.find("width") >= 0:
                dMain["x"][tagName] = val
                if xKey.startswith("exif"):
                    width = int( val )
            elif xKey.find("height") >= 0:
                dMain["y"][tagName] = val
                if xKey.startswith("exif"):
                    height = int(val)
        controlTagsExif.thisExifInfo = exifInfo
        sDate = controlTagsExif.what_date("DateTime")
        assert sDate is not None
        dttm = exif_date(sDate)
        dInfo = {"width": width,
                 "height": height,
                 "DateTime": dttm,
                 "DateISO": exif_str_date(dttm, "ISO"),
                 }
        self.meta["main"] = dMain
        self.meta["info"] = dInfo
        return True


class Pict():
    """ Pict class, for pictures/ images """
    img = None

    def __init__ (self, img=None):
        self.img = img
        self._parse_picture( img )


    def _parse_picture (self, img):
        """
        Parses PIL image
        :param img:
        :return: bool (whether image is correct)
        """
        if img is None:
            return False
        #  See also:
        #	https://stackoverflow.com/questions/6444548/how-do-i-get-the-picture-size-with-pil
        self.size = img.size  # size[0]=x, size[1]=y
        return True


    def width (self):
        return self.size[0]


    def height (self):
        return self.size[1]


controlTagsExif = TagsExif()

#
# No main...!
#
if __name__ == "__main__":
    print("see mempic.test.py")
