from typing import List, Optional, TypeVar, Union, cast

from LOGS.Entities.DatasetRequestParameter import ParsingStates
from LOGS.Entities.Datatrack import Datatrack
from LOGS.Entities.DatatrackNumericArray import DatatrackNumericArray
from LOGS.Entities.HierarchyNode import HierarchyNode
from LOGS.Entities.ParserLog import ParserLog
from LOGS.Entities.Track import Track
from LOGS.Entities.TrackXY import TrackXY
from LOGS.Entity.SerializeableContent import SerializeableContent

TRACKS = Union[Track, TrackXY]
DATATRACKS = Union[Datatrack, DatatrackNumericArray]
_T = TypeVar("_T", Track, TrackXY)


class DatasetInfo(SerializeableContent):
    _name: Optional[str] = None
    _type: Optional[str] = None
    _formatVersion: Optional[int] = None
    _parsingState: Optional[ParsingStates] = None
    _parserLogs: Optional[List[ParserLog]] = None
    _tracks: Optional[List[TRACKS]] = None
    _datatracks: Optional[List[DATATRACKS]] = None
    _tracksHierarchy: Optional[HierarchyNode] = None

    @property
    def name(self) -> Optional[str]:
        return self._name

    @name.setter
    def name(self, value):
        self._name = self.checkAndConvertNullable(value, str, "name")

    @property
    def type(self) -> Optional[str]:
        return self._type

    @type.setter
    def type(self, value):
        self._type = self.checkAndConvertNullable(value, str, "type")

    @property
    def parsingState(self) -> Optional[ParsingStates]:
        return self._parsingState

    @parsingState.setter
    def parsingState(self, value):
        self._parsingState = cast(
            ParsingStates, self.checkAndConvertNullable(value, str, "parsingState")
        )

    @property
    def formatVersion(self) -> Optional[int]:
        return self._formatVersion

    @formatVersion.setter
    def formatVersion(self, value):
        self._formatVersion = self.checkAndConvertNullable(value, int, "formatVersion")

    @property
    def parserLogs(self) -> Optional[List[ParserLog]]:
        return self._parserLogs

    @parserLogs.setter
    def parserLogs(self, value):
        self._parserLogs = self.checkListAndConvertNullable(
            value, ParserLog, "parserLogs"
        )

    @classmethod
    def _trackConverter(cls, value: dict) -> TRACKS:
        if isinstance(value, dict) and "type" in value:
            if value["type"] == "XY_real":
                return TrackXY(value)
            else:
                return Track(value)
        else:
            return Track(value)

    @classmethod
    def _datatrackConverter(cls, value: dict) -> DATATRACKS:
        if isinstance(value, dict) and "type" in value:
            if value["type"] == "numeric_array":
                return DatatrackNumericArray(value)
            else:
                return Datatrack(value)
        else:
            return Datatrack(value)

    @property
    def tracks(self) -> Optional[List[Track]]:
        return self._tracks

    @tracks.setter
    def tracks(self, value):
        self._tracks = self.checkListAndConvertNullable(
            value, Track, "tracks", converter=self._trackConverter
        )

    @property
    def datatracks(self) -> Optional[List[Datatrack]]:
        return self._datatracks

    @datatracks.setter
    def datatracks(self, value):
        self._datatracks = self.checkListAndConvertNullable(
            value, Datatrack, "datatracks", converter=self._datatrackConverter
        )

    @property
    def tracksHierarchy(self) -> Optional[HierarchyNode]:
        return self._tracksHierarchy

    @tracksHierarchy.setter
    def tracksHierarchy(self, value):
        self._tracksHierarchy = self.checkAndConvertNullable(
            value, HierarchyNode, "tracksHierarchy"
        )
