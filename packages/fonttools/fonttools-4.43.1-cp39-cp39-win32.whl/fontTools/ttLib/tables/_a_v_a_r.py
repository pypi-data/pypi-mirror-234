from fontTools.misc import sstruct
from fontTools.misc.fixedTools import (
    fixedToFloat as fi2fl,
    floatToFixed as fl2fi,
    floatToFixedToStr as fl2str,
    strToFixedToFloat as str2fl,
)
from fontTools.misc.textTools import bytesjoin, safeEval
from fontTools.ttLib import TTLibError
from . import DefaultTable
from . import otTables
import struct
import logging


log = logging.getLogger(__name__)

from .otBase import BaseTTXConverter


class table__a_v_a_r(BaseTTXConverter):
    """Axis Variations Table

    This class represents the ``avar`` table of a variable font. The object has one
    substantive attribute, ``segments``, which maps axis tags to a segments dictionary::

        >>> font["avar"].segments   # doctest: +SKIP
        {'wght': {-1.0: -1.0,
          0.0: 0.0,
          0.125: 0.11444091796875,
          0.25: 0.23492431640625,
          0.5: 0.35540771484375,
          0.625: 0.5,
          0.75: 0.6566162109375,
          0.875: 0.81927490234375,
          1.0: 1.0},
         'ital': {-1.0: -1.0, 0.0: 0.0, 1.0: 1.0}}

    Notice that the segments dictionary is made up of normalized values. A valid
    ``avar`` segment mapping must contain the entries ``-1.0: -1.0, 0.0: 0.0, 1.0: 1.0``.
    fontTools does not enforce this, so it is your responsibility to ensure that
    mappings are valid.
    """

    dependencies = ["fvar"]

    def __init__(self, tag=None):
        super().__init__(tag)
        self.segments = {}

    def compile(self, ttFont):
        axisTags = [axis.axisTag for axis in ttFont["fvar"].axes]
        if not hasattr(self, "table"):
            self.table = otTables.avar()
        if not hasattr(self.table, "Reserved"):
            self.table.Reserved = 0
        self.table.Version = (getattr(self, "majorVersion", 1) << 16) | getattr(
            self, "minorVersion", 0
        )
        self.table.AxisCount = len(axisTags)
        self.table.AxisSegmentMap = []
        for axis in axisTags:
            mappings = self.segments[axis]
            segmentMap = otTables.AxisSegmentMap()
            segmentMap.PositionMapCount = len(mappings)
            segmentMap.AxisValueMap = []
            for key, value in sorted(mappings.items()):
                valueMap = otTables.AxisValueMap()
                valueMap.FromCoordinate = key
                valueMap.ToCoordinate = value
                segmentMap.AxisValueMap.append(valueMap)
            self.table.AxisSegmentMap.append(segmentMap)
        return super().compile(ttFont)

    def decompile(self, data, ttFont):
        super().decompile(data, ttFont)
        assert self.table.Version >= 0x00010000
        self.majorVersion = self.table.Version >> 16
        self.minorVersion = self.table.Version & 0xFFFF
        axisTags = [axis.axisTag for axis in ttFont["fvar"].axes]
        for axis in axisTags:
            self.segments[axis] = {}
        for axis, segmentMap in zip(axisTags, self.table.AxisSegmentMap):
            segments = self.segments[axis] = {}
            for segment in segmentMap.AxisValueMap:
                segments[segment.FromCoordinate] = segment.ToCoordinate

    def toXML(self, writer, ttFont):
        writer.simpletag(
            "version",
            major=getattr(self, "majorVersion", 1),
            minor=getattr(self, "minorVersion", 0),
        )
        writer.newline()
        axisTags = [axis.axisTag for axis in ttFont["fvar"].axes]
        for axis in axisTags:
            writer.begintag("segment", axis=axis)
            writer.newline()
            for key, value in sorted(self.segments[axis].items()):
                key = fl2str(key, 14)
                value = fl2str(value, 14)
                writer.simpletag("mapping", **{"from": key, "to": value})
                writer.newline()
            writer.endtag("segment")
            writer.newline()
        if getattr(self, "majorVersion", 1) >= 2:
            if self.table.VarIdxMap:
                self.table.VarIdxMap.toXML(writer, ttFont, name="VarIdxMap")
            if self.table.VarStore:
                self.table.VarStore.toXML(writer, ttFont)

    def fromXML(self, name, attrs, content, ttFont):
        if not hasattr(self, "table"):
            self.table = otTables.avar()
        if not hasattr(self.table, "Reserved"):
            self.table.Reserved = 0
        if name == "version":
            self.majorVersion = safeEval(attrs["major"])
            self.minorVersion = safeEval(attrs["minor"])
            self.table.Version = (getattr(self, "majorVersion", 1) << 16) | getattr(
                self, "minorVersion", 0
            )
        elif name == "segment":
            axis = attrs["axis"]
            segment = self.segments[axis] = {}
            for element in content:
                if isinstance(element, tuple):
                    elementName, elementAttrs, _ = element
                    if elementName == "mapping":
                        fromValue = str2fl(elementAttrs["from"], 14)
                        toValue = str2fl(elementAttrs["to"], 14)
                        if fromValue in segment:
                            log.warning(
                                "duplicate entry for %s in axis '%s'", fromValue, axis
                            )
                        segment[fromValue] = toValue
        else:
            super().fromXML(name, attrs, content, ttFont)
