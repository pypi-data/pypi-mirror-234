import os
from datetime import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Sequence, Union, cast

from LOGS.Auxiliary.Constants import Constants
from LOGS.Auxiliary.Decorators import Endpoint, UiEndpoint
from LOGS.Auxiliary.Exceptions import (
    EntityFetchingException,
    EntityIncompleteException,
    LOGSException,
)
from LOGS.Auxiliary.MinimalModelGenerator import (
    AutoloadSourceMinimalFromDict,
    DatasetTypeMinimalFromDict,
    ExperimentMinimalFromDict,
    FormatMinimalFromDict,
    InstrumentMinimalFromDict,
    MethodMinimalFromDict,
    MinimalFromList,
    SampleMinimalFromDict,
)
from LOGS.Auxiliary.Tools import Tools
from LOGS.Entities.DatasetInfo import DatasetInfo
from LOGS.Entities.DatasetRelations import DatasetRelations
from LOGS.Entities.DatasetRequestParameter import ParsingStates
from LOGS.Entities.DatasetTypeMinimal import DatasetTypeMinimal
from LOGS.Entities.Datatrack import Datatrack
from LOGS.Entities.FileEntry import FileEntry
from LOGS.Entities.HierarchyNode import HierarchyNode
from LOGS.Entities.ParserLog import ParserLog
from LOGS.Entities.Track import Track
from LOGS.Entity.EntityWithIntId import EntityWithIntId
from LOGS.Entity.SerializeableContent import SerializeableContent
from LOGS.Interfaces.INamedEntity import INamedEntity
from LOGS.Interfaces.IOwnedEntity import IOwnedEntity
from LOGS.Interfaces.IUniqueEntity import IUniqueEntity
from LOGS.LOGSConnection import LOGSConnection, ResponseTypes

if TYPE_CHECKING:
    from LOGS.Entities.AutoloadSourceMinimal import AutoloadSourceMinimal
    from LOGS.Entities.EquipmentMinimal import EquipmentMinimal
    from LOGS.Entities.ExperimentMinimal import ExperimentMinimal
    from LOGS.Entities.FormatMinimal import FormatMinimal
    from LOGS.Entities.InstrumentMinimal import InstrumentMinimal
    from LOGS.Entities.MethodMinimal import MethodMinimal
    from LOGS.Entities.PersonMinimal import PersonMinimal
    from LOGS.Entities.ProjectMinimal import ProjectMinimal
    from LOGS.Entities.SampleMinimal import SampleMinimal


class ParsedMetadata(SerializeableContent):
    Parameters: bool = False
    Tracks: bool = False
    TrackCount: int = False
    TrackViewerTypes: List[str] = []


@Endpoint("datasets")
@UiEndpoint("#data")
class Dataset(
    INamedEntity,
    IUniqueEntity,
    IOwnedEntity,
    EntityWithIntId,
):
    _noInfo = True
    _noParameters = True

    _datasetType: Optional[DatasetTypeMinimal]
    _format: Optional["FormatMinimal"]
    _acquisitionDate: Optional[datetime]
    _path: Optional[str]
    _method: Optional["MethodMinimal"]
    _experiment: Optional["ExperimentMinimal"]
    _claimed: Optional[bool]
    _notes: Optional[str]
    _dateAdded: Optional[datetime]
    _isDeleted: Optional[bool]
    _other: Optional[str]
    _instrument: Optional["InstrumentMinimal"]
    _sample: Optional["SampleMinimal"]
    _autoloadSource: Optional["AutoloadSourceMinimal"]
    _operators: Optional[List["PersonMinimal"]]
    _equipments: Optional[List["EquipmentMinimal"]]
    _projects: Optional[List["ProjectMinimal"]]
    _customFields: Optional[Dict[str, Any]]
    _parsingState: Optional[ParsingStates]
    _relations: Optional[DatasetRelations]
    _parsedMetadata: Optional[ParsedMetadata]
    _parameters: Optional[Dict[str, Any]]
    _formatVersion: Optional[int]
    _parserLogs: Optional[List[ParserLog]]
    _tracks: Optional[List[Track]]
    _datatracks: Optional[List[Datatrack]]
    _tracksHierarchy: Optional[HierarchyNode]
    _files: Optional[List[FileEntry]]
    _formatId: Optional[str]

    def __init__(
        self,
        ref=None,
        id: Optional[int] = None,
        connection: Optional[LOGSConnection] = None,
        files: Optional[Sequence[Constants.FILE_TYPE]] = None,
        format: Optional[Union[str, "FormatMinimal"]] = None,
    ):
        self._datasetType = None
        self._format = None
        self._acquisitionDate = None
        self._path = None
        self._method = None
        self._experiment = None
        self._claimed = None
        self._notes = None
        self._dateAdded = None
        self._isDeleted = None
        self._other = None
        self._instrument = None
        self._sample = None
        self._autoloadSource = None
        self._operators = None
        self._equipments = None
        self._projects = None
        self._customFields = None
        self._parsingState = None
        self._relations = None
        self._parsedMetadata = None
        self._parameters = None
        self._formatVersion = None
        self._parserLogs = None
        self._tracks = None
        self._datatracks = None
        self._tracksHierarchy = None
        self._files = None

        super().__init__(ref=ref, id=id, connection=connection)
        self._noSerialize += [
            "parameters",
            "formatVersion",
            "parserLogs",
            "tracks",
            "datatracks",
            "tracksHierarchy",
        ]

        if isinstance(ref, Dataset):
            self._format = ref._format

        if format:
            self.format = cast(Any, format)

        if files:
            if not self._format or not self._format.id:
                raise LOGSException(
                    "Cannot create %s object from files parameter without a format"
                    % type(self).__name__
                )

            self._files = FileEntry.entriesFromFiles(files)

    def fromDict(self, ref, formatDict=None) -> None:
        if isinstance(ref, dict):
            if "parameters" in ref:
                self._parameters = self.checkAndConvertNullable(
                    ref["parameters"], dict, "parameters"
                )
                self._noParameters = False
                self._noParameters = False
            if "formatVersion" in ref:
                self._formatVersion = self.checkAndConvertNullable(
                    ref["formatVersion"], int, "formatVersion"
                )
                self._noInfo = False
            if "parserLogs" in ref:
                self._parserLogs = self.checkListAndConvertNullable(
                    ref["parserLogs"], ParserLog, "parserLogs"
                )
                self._noInfo = False
            if "tracks" in ref:
                self._tracks = self.checkListAndConvertNullable(
                    ref["tracks"], Track, "tracks"
                )
                self._noInfo = False
            if "datatracks" in ref:
                self._datatracks = self.checkListAndConvertNullable(
                    ref["datatracks"], Datatrack, "datatracks"
                )
                self._noInfo = False
            if "tracksHierarchy" in ref:
                self._tracksHierarchy = self.checkAndConvertNullable(
                    ref["tracksHierarchy"], HierarchyNode, "tracksHierarchy"
                )
                self._noInfo = False

        super().fromDict(ref=ref, formatDict=formatDict)

    # def _getConnectionData(self):
    #     if not self._endpoint:
    #         raise NotImplementedError(
    #             "Endpoint missing for of entity type %a."
    #             % (
    #                 type(self).__name__
    #                 if type(self).__name__ != Entity.__name__
    #                 else "unknown"
    #             )
    #         )

    #     if not self.id:
    #         raise EntityNotFoundException(self)

    #     return self._getConnection(), self._endpoint, self.id

    def fetchParameters(self):
        connection, endpoint, id = self._getConnectionData()

        parameters, errors = connection.getEndpoint(endpoint + [id, "parameters"])
        if errors:
            raise EntityFetchingException(entity=self, errors=errors)

        if isinstance(parameters, dict):
            if "url" in parameters:
                del parameters["url"]
            self._parameters = parameters
        else:
            self._parameters = {}
        self._noParameters = False

    def fetchInfo(self: "Dataset"):
        connection, endpoint, id = self._getConnectionData()

        data, errors = connection.getEndpoint(endpoint + [id, "info"])
        if errors:
            raise EntityFetchingException(entity=self, errors=errors)

        info = DatasetInfo(data)
        self._formatVersion = info.formatVersion
        self._parserLogs = info.parserLogs
        self._tracks = info.tracks
        self._datatracks = info.datatracks
        self._tracksHierarchy = info.tracksHierarchy

        trackLookup: Dict[str, Datatrack] = {}
        if self._datatracks:
            for datatrack in self._datatracks:
                datatrack.connection = self.connection
                datatrack._endpoint = endpoint + [str(id), "datatrack"]
                if datatrack.id:
                    trackLookup[datatrack.id] = datatrack

        if self._tracks:
            for track in self._tracks:
                track.connection = self.connection
                if track._dataIds:
                    track.datatracks = cast(
                        Any,
                        {
                            k: (trackLookup[v] if v in trackLookup else None)
                            for k, v in track._dataIds.items()
                        },
                    )
        self._noInfo = False

    def fetchFull(self):
        self.fetchParameters()
        self.fetchInfo()

    def download(
        self,
        directory: Optional[str] = None,
        fileName: Optional[str] = None,
        overwrite=False,
    ):
        connection, endpoint, id = self._getConnectionData()

        if not directory:
            directory = os.curdir

        if not fileName:
            fileName = self.name if self.name and self.name != "" else "Dataset"
            fileName += ".zip"

        path = os.path.join(directory, Tools.sanitizeFileName(fileName=fileName))

        if overwrite:
            if os.path.exists(path) and not os.path.isfile(path):
                raise LOGSException("Path %a is not a file" % path)
        else:
            if os.path.exists(path):
                raise LOGSException("File %a already exists" % path)

        data, errors = connection.getEndpoint(
            endpoint + [id, "files", "zip"], responseType=ResponseTypes.RAW
        )
        if errors:
            raise EntityFetchingException(entity=self, errors=errors)

        with open(path, mode="wb") as localfile:
            localfile.write(cast(bytes, data))

        return path

    @property
    def datasetType(self) -> Optional[DatasetTypeMinimal]:
        return self._datasetType

    @datasetType.setter
    def datasetType(self, value):
        self._datasetType = DatasetTypeMinimalFromDict(
            value, "datasetType", connection=self.connection
        )

    @property
    def format(self) -> Optional["FormatMinimal"]:
        return self._format

    @format.setter
    def format(self, value):
        self._format = FormatMinimalFromDict(
            value, "format", connection=self.connection
        )

    @property
    def acquisitionDate(self) -> Optional[datetime]:
        return self._acquisitionDate

    @acquisitionDate.setter
    def acquisitionDate(self, value):
        self._acquisitionDate = self.checkAndConvertNullable(
            value, datetime, "acquisitionDate"
        )

    @property
    def path(self) -> Optional[str]:
        return self._path

    @path.setter
    def path(self, value):
        self._path = self.checkAndConvertNullable(value, str, "path")

    @property
    def claimed(self) -> Optional[bool]:
        return self._claimed

    @claimed.setter
    def claimed(self, value):
        self._claimed = self.checkAndConvertNullable(value, bool, "claimed")

    @property
    def notes(self) -> Optional[str]:
        return self._notes

    @notes.setter
    def notes(self, value):
        self._notes = self.checkAndConvertNullable(value, str, "notes")

    @property
    def dateAdded(self) -> Optional[datetime]:
        return self._dateAdded

    @dateAdded.setter
    def dateAdded(self, value):
        self._dateAdded = self.checkAndConvertNullable(value, datetime, "dateAdded")

    @property
    def isDeleted(self) -> Optional[bool]:
        return self._isDeleted

    @isDeleted.setter
    def isDeleted(self, value):
        self._isDeleted = self.checkAndConvertNullable(value, bool, "isDeleted")

    @property
    def other(self) -> Optional[str]:
        return self._other

    @other.setter
    def other(self, value):
        self._other = self.checkAndConvertNullable(value, str, "other")

    @property
    def customFields(self) -> Optional[Dict[str, Any]]:
        return self._customFields

    @customFields.setter
    def customFields(self, value):
        self._customFields = self.checkAndConvertNullable(value, dict, "customFields")

    @property
    def parsingState(self) -> Optional[ParsingStates]:
        return self._parsingState

    @parsingState.setter
    def parsingState(self, value):
        self._parsingState = cast(
            ParsingStates, self.checkAndConvertNullable(value, str, "parsingState")
        )

    @property
    def relations(self) -> Optional[DatasetRelations]:
        return self._relations

    @relations.setter
    def relations(self, value):
        if value:
            self._relations = self.checkAndConvert(value, DatasetRelations, "relations")

    @property
    def parsedMetadata(self) -> Optional[ParsedMetadata]:
        return self._parsedMetadata

    @parsedMetadata.setter
    def parsedMetadata(self, value):
        self._parsedMetadata = self.checkAndConvertNullable(
            value, ParsedMetadata, "parsedMetadata"
        )

    @property
    def parameters(self) -> Optional[Dict[str, Any]]:
        if self._noParameters:
            raise EntityIncompleteException(self)
        return self._parameters

    @property
    def formatVersion(self) -> Optional[int]:
        if self._noInfo:
            raise EntityIncompleteException(self)
        return self._formatVersion

    @property
    def parserLogs(self) -> Optional[List[ParserLog]]:
        if self._noInfo:
            raise EntityIncompleteException(self)
        return self._parserLogs

    @property
    def tracks(self) -> Optional[List[Track]]:
        if self._noInfo:
            raise EntityIncompleteException(self)
        return self._tracks

    @property
    def datatracks(self) -> Optional[List[Datatrack]]:
        if self._noInfo:
            raise EntityIncompleteException(self)
        return self._datatracks

    @property
    def tracksHierarchy(self) -> Optional[HierarchyNode]:
        if self._noInfo:
            raise EntityIncompleteException(self)
        return self._tracksHierarchy

    @property
    def autoloadSource(self) -> Optional["AutoloadSourceMinimal"]:
        return self._autoloadSource

    @autoloadSource.setter
    def autoloadSource(self, value):
        self._autoloadSource = AutoloadSourceMinimalFromDict(
            value, "autoloadSource", connection=self.connection
        )

    @property
    def autoloadSourceId(self) -> Optional[int]:
        return self._autoloadSource.id if self._autoloadSource else None

    @autoloadSourceId.setter
    def autoloadSourceId(self, value):
        self._autoloadSource = AutoloadSourceMinimalFromDict(
            value, "autoloadSource", connection=self.connection
        )

    @property
    def equipments(self) -> Optional[List["EquipmentMinimal"]]:
        return self._equipments

    @equipments.setter
    def equipments(self, value):
        self._equipments = MinimalFromList(
            value, "EquipmentMinimal", "equipments", connection=self.connection
        )

    @property
    def equipmentIds(self) -> Optional[List[int]]:
        if self._equipments is None:
            return None
        return [e.id for e in self._equipments]

    @equipmentIds.setter
    def equipmentIds(self, value):
        self._equipments = MinimalFromList(
            value, "EquipmentMinimal", "equipments", connection=self.connection
        )

    @property
    def method(self) -> Optional["MethodMinimal"]:
        return self._method

    @method.setter
    def method(self, value):
        self._method = MethodMinimalFromDict(
            value, "method", connection=self.connection
        )

    @property
    def methodId(self) -> Optional[int]:
        return self._method.id if self._method else None

    @methodId.setter
    def methodId(self, value):
        self._method = MethodMinimalFromDict(
            value, "method", connection=self.connection
        )

    @property
    def experiment(self) -> Optional["ExperimentMinimal"]:
        return self._experiment

    @experiment.setter
    def experiment(self, value):
        self._experiment = ExperimentMinimalFromDict(
            value, "experiment", connection=self.connection
        )

    @property
    def sample(self) -> Optional["SampleMinimal"]:
        return self._sample

    @sample.setter
    def sample(self, value):
        self._sample = SampleMinimalFromDict(
            value, "sample", connection=self.connection
        )

    @property
    def sampleId(self) -> Optional[int]:
        return self._sample.id if self._sample else None

    @sampleId.setter
    def sampleId(self, value):
        self._sample = SampleMinimalFromDict(
            value, "sample", connection=self.connection
        )

    @property
    def operators(self) -> Optional[List["PersonMinimal"]]:
        return self._operators

    @operators.setter
    def operators(self, value):
        self._operators = MinimalFromList(
            value, "PersonMinimal", "operators", connection=self.connection
        )

    @property
    def operatorIds(self) -> Optional[List[int]]:
        if self._operators is None:
            return None
        return [e.id for e in self._operators]

    @operatorIds.setter
    def operatorIds(self, value):
        self._operators = MinimalFromList(
            value, "PersonMinimal", "operators", connection=self.connection
        )

    @property
    def projects(self) -> Optional[List["ProjectMinimal"]]:
        return self._projects

    @projects.setter
    def projects(self, value):
        self._projects = MinimalFromList(
            value, "ProjectMinimal", "projects", connection=self.connection
        )

    @property
    def projectIds(self) -> Optional[List[int]]:
        if self._projects is None:
            return None
        return [e.id for e in self._projects]

    @projectIds.setter
    def projectIds(self, value):
        self._projects = MinimalFromList(
            value, "ProjectMinimal", "projects", connection=self.connection
        )

    @property
    def instrument(self) -> Optional["InstrumentMinimal"]:
        return self._instrument

    @instrument.setter
    def instrument(self, value):
        self._instrument = InstrumentMinimalFromDict(
            value, "instrument", connection=self.connection
        )

    @property
    def instrumentId(self) -> Optional[int]:
        return self._instrument.id if self._instrument else None

    @instrumentId.setter
    def instrumentId(self, value):
        self._instrument = InstrumentMinimalFromDict(
            value, "instrument", connection=self.connection
        )
