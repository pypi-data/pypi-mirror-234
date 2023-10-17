from datetime import datetime
from typing import Optional

from LOGS.Auxiliary.Decorators import Endpoint
from LOGS.Entity.EntityMinimalWithIntId import EntityMinimalWithIntId
from LOGS.Entity.EntityWithIntId import EntityWithIntId
from LOGS.Interfaces.ICreationRecord import ICreationRecord
from LOGS.Interfaces.IModificationRecord import IModificationRecord
from LOGS.Interfaces.INamedEntity import INamedEntity


@Endpoint("lab_notebook_entries")
class LabNotebookEntry(
    INamedEntity, EntityWithIntId, ICreationRecord, IModificationRecord
):
    _version: Optional[int] = None
    _labNotebook: Optional[EntityMinimalWithIntId] = None
    _labNotebookExperiment: Optional[EntityMinimalWithIntId] = None
    _entryDate: Optional[datetime] = None
    _isDeleted: Optional[bool] = None

    def fromDict(self, ref, formatDict=None) -> None:
        if isinstance(ref, dict):
            if "name" in ref:
                ref["name"] = ref["name"].replace(" > ", "_")

        super().fromDict(ref, formatDict)
