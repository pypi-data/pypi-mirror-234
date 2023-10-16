from dataclasses import dataclass
from typing import List, Optional

from LOGS.Entity.EntityRequestParameter import EntityRequestParameter


@dataclass
class LabNotebookEntryRequestParameter(EntityRequestParameter):
    isSoftDeleted: Optional[bool] = None
    datasetIds: Optional[List[int]] = None
    personIds: Optional[List[int]] = None
    sampleIds: Optional[List[int]] = None
