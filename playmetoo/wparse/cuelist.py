# -*- coding: utf-8 -*-
# (c)2020 Henrique Moreira,
#	original cueparser.py from github, at artur-shaik/CueParser.git

""" cuelist -- CUE sheet handling
Handling CUE playlists as text.

See also:	https://en.wikipedia.org/wiki/Cue_sheet_(computing)
"""

import sys
import re
import math
from datetime import timedelta

# pylint: disable=invalid-name, no-self-use, unused-argument
# pylint: disable=missing-function-docstring


def main():
    """ Simplified main. Import this module instead. """
    args = sys.argv[1:]
    if args:
        print("\nBasic output follows\n")
        dump_cue(args[0], args[1:])


def dump_cue(cueFile, options):
    assert not options
    cuesheet = CueSheet(open(cueFile, "r").read())
    cuesheet.parse()
    print(cuesheet)


class PlayFormat():
    """ Playlist Formats """
    defOutputFormat = """
%performer% - %title%
File: %file%
%tracks%
""".strip('\n')
    defTrackOutputFormat = "%performer% - %title%"

    def setOutputFormat(self, outputFormat, trackOutputFormat="") -> bool:
        # pylint: disable=attribute-defined-outside-init
        self.outputFormat = outputFormat
        if trackOutputFormat:
            self.trackOutputFormat = trackOutputFormat
        return self.validFormats()

    def validFormats(self) -> bool:
        return True


class CueSheet(PlayFormat):
    """ CUE playlist """
    _fields = [
        "file",
        "performer",
        "songwriter",
        "title",
        "flags",
        "isrc"
    ]

    def __init__(self, optData=""):
        self.data = ""
        self.rem = None
        self.performer = None
        self.songwriter = None
        self.title = None
        self.file = None
        self.aformat = None
        self.tracks = []
        self.outputFormat = PlayFormat.defOutputFormat
        self.trackOutputFormat = PlayFormat.defTrackOutputFormat
        self.iterator = 0
        self.flags, self.isrc = None, None
        if optData:
            self.setData(optData)

    def setData(self, data):
        self.data = data.splitlines()

    def __next__(self):
        if self.iterator < len(self.data):
            ret = self.data[self.iterator]
            self.iterator += 1
            return ret.strip()
        return None

    def back(self):
        self.iterator -= 1

    def parse(self) -> bool:
        line = next(self)
        if not line:
            return True

        if not self.rem:
            match = re.match('^REM .(.*).$', line)
            rem_tmp = ''
            while match:
                rem_tmp += match.group(0) + '\n'
                line = next(self)
                match = re.match('^REM .(.*).$', line)
            if rem_tmp:
                self.rem = rem_tmp.strip()

        for field in ["performer", "songwriter", "title"]:
            if not getattr(self, field):
                match = re.match("^{} .(.*).$".format(field.upper()), line)
                if match:
                    setattr(self, field, match.group(1))
                    line = next(self)

        if not self.file:
            match = re.match('^FILE .(.*). (.*)$', line)
            if match:
                self.file = match.group(1)
                self.aformat = match.group(2)
                line = next(self)

        match = re.match('^TRACK.*$', line)
        if match:
            cuetrack = CueTrack()
            cuetrack.setOutputFormat(self.trackOutputFormat)
            cuetrack.number = len(self.tracks) + 1
            self.track(cuetrack)
            if len(self.tracks) > 0:
                previous = self.tracks[len(self.tracks) - 1]
                offset = offsetToTimedelta(cuetrack.offset)
                previosOffset = offsetToTimedelta(previous.offset)
                previous.duration = offset - previosOffset
            self.tracks.append(cuetrack)
        return self.parse()

    def track(self, track):
        line = next(self)
        if not line:
            return

        for field in CueSheet._fields:
            match = re.match("^{} .(.*).$".format(field.upper()), line)
            if match:
                setattr(track, field, match.group(1))
                self.track(track)

        match = re.match('^INDEX (.*) (.*)$', line)
        if match:
            track.index = match.group(1)
            track.offset = match.group(2)
            self.track(track)
        self.back()

    def output(self):
        return self.__repr__()

    def getTrackByNumber(self, number):
        return self.tracks[number - 1] if self.tracks[number - 1] else None

    def getTrackByTime(self, time):
        for track in reversed(self.tracks):
            trackOffset = offsetToTimedelta(track.offset)
            if time > trackOffset:
                return track
        return None

    def __repr__(self):
        return self._to_string()

    def _to_string(self):
        ret = self.outputFormat
        for field in CueSheet._fields:
            value = getattr(self, field)
            if value:
                ret = ret.replace(f"%{field}%", value)
        trackOutput = ""
        for track in self.tracks:
            track.setOutputFormat(self.trackOutputFormat)
            astr = track.output()
            trackOutput += f"{astr}\n"
        ret = ret.replace("%tracks%", trackOutput)
        return ret


class CueTrack():
    """ CUE track (item) """
    _fields = [
        "performer",
        "songwriter",
        "title",
        "index",
        "offset"
    ]

    def __init__(self):
        self.performer = None
        self.songwriter = None
        self.title = None
        self.flags = None
        self.isrc = None
        self.index = None
        self.offset = None
        self.outputFormat = None
        self.duration = None
        self.number = None

    def setOutputFormat(self, outputFormat):
        self.outputFormat = outputFormat

    def output(self):
        return self.__repr__()

    def __repr__(self):
        ret = self.outputFormat

        for field in CueTrack._fields:
            if getattr(self, field):
                ret = ret.replace("%{}%".format(field), getattr(self, field))

        if self.number:
            ret = ret.replace("%number%", "%02d" % self.number)
        if self.duration:
            minutes = math.floor(self.duration.seconds / 60)
            ret = ret.replace("%duration%", "%02d:%02d" %
                              (minutes, self.duration.seconds - 60 * minutes))
        else:
            ret = ret.replace("%duration%", "")

        return ret


def offsetToTimedelta(offset):
    offset = offset.split(':')
    if len(offset) == 1:
        offset = timedelta(minutes=int(offset[0]))
    elif len(offset) == 2:
        offset = timedelta(minutes=int(offset[0]), seconds=int(offset[1]))
    elif len(offset) == 3:
        if len(offset[2]) < 3:
            offset[2] += "0"
        offset = timedelta(minutes=int(offset[0]), seconds=int(offset[1]),
                           milliseconds=int(offset[2]))
    else:
        print("Wrong offset value")
        sys.exit(0)
    return offset


def print_all_tracks(cuesheet, i=0):
    for track in cuesheet.tracks:
        i += 1
        print("{}: {}".format(i, track))


# Main script
if __name__ == '__main__':
    print(f"Import wparse.{__file__} !")
    #cuesheet = CueSheet(); cuesheet.setData(data); cuesheet.parse()
    #	... print(cuesheet) or print(cuesheet.output())
    main()
