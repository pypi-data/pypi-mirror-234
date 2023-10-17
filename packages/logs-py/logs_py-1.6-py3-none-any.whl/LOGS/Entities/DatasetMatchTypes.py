import uuid
from typing import Any, List, Optional

from LOGS.Auxiliary.Tools import Tools
from LOGS.Entities.FileEntry import FileEntry, FileFragment
from LOGS.Entity.SerializeableContent import SerializeableClass


class MatchRequest(SerializeableClass):
    _typeMapper = {"files": FileEntry}

    def __init__(self, ref: Any = None):
        self.files: List[FileEntry] = []
        self.formatIds: Optional[List[str]] = None
        super().__init__(ref)


class DatasetForSearch(SerializeableClass):
    _typeMapper = {"files": FileEntry}

    def __init__(self, ref: Any = None):
        self.id: str = ""
        self.parserId: str = ""
        self.checkUpdatable: bool = True
        self.files: List[FileEntry] = []
        super().__init__(ref)
        self.id = uuid.uuid4().hex


class DatasetsUpdatableFiles(SerializeableClass):
    _typeMapper = {"files": FileEntry}

    def __init__(
        self,
        ref: Any = None,
        datasetId: Optional[int] = None,
        files: Optional[List[FileEntry]] = None,
    ):
        self.datasetId: int = 0
        self.files: List[FileEntry] = []
        super().__init__(ref)
        if datasetId is not None:
            self.datasetId = datasetId
        if files is not None:
            self.files = files


class DatasetSearchResult(SerializeableClass):
    _typeMapper: dict = {"files": FileEntry}

    def __init__(self, ref: Any = None):
        self.id: str = ""
        self.errors: List[str] = []
        self.logsId: Optional[int] = None
        self.isUpdateable: Optional[bool] = None
        self.files: List[FileEntry] = []
        super().__init__(ref)


class DatasetSearchRequest(SerializeableClass):
    _typeMapper = {"datasets": DatasetForSearch}

    def __init__(self, ref: Any = None):
        self.datasets: List[DatasetForSearch] = []
        super().__init__(ref)


class MatchedDataset(SerializeableClass):
    _typeMapper = {"files": FileEntry}

    def __init__(self, ref: Any = None):
        self.id: str = ""
        self.parserId: str = ""
        self.name: str = ""
        self.parentMissing: bool = False
        self.parentPath: str = ""
        self.files: List[FileEntry] = []
        super().__init__(ref)

    def __iter__(self):
        for file in self.files:
            yield file

    def __str__(self):
        if len(self.files):
            return "<%s %a %s>" % (
                type(self).__name__,
                self.parserId,
                Tools.numberPlural("file", len(self.files)),
            )
        else:
            return "<%s>" % (type(self).__name__)


class DatasetMatch(SerializeableClass):
    _typeMapper = {"datasets": MatchedDataset}

    def __init__(self, ref: Any = None):
        self.parserId: str = ""
        self.parserName: str = ""
        self.datasets: List[MatchedDataset] = []
        super().__init__(ref)

    def __iter__(self):
        for dataset in self.datasets:
            yield dataset

    def __str__(self):
        if self.parserId and len(self.datasets):
            return "<%s %a(%d)>" % (
                type(self).__name__,
                self.parserId,
                len(self.datasets),
            )
        else:
            return "<%s>" % (type(self).__name__)


class MatchResult(SerializeableClass):
    _typeMapper = {"matches": DatasetMatch, "missingFragments": FileFragment}

    def __init__(self, ref: Any = None):
        self.matches: List[DatasetMatch] = []
        self.missingFragments: List[FileFragment] = []
        super().__init__(ref)
