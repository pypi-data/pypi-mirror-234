from datetime import datetime
from typing import List, Optional
from uuid import UUID

from LOGS.Entities.AutoloadSourceType import AutoloadSourceType
from LOGS.Entities.AutoloadStatusError import AutoloadStatusError
from LOGS.Entities.RunState import RunState
from LOGS.Entity.SerializeableContent import SerializeableClass


class AutoloadStatus(SerializeableClass):
    type: Optional[AutoloadSourceType]
    uuid: Optional[UUID]
    lastUpdated: Optional[datetime]
    counter: Optional[int]
    autoloadConfigurationId: Optional[int]
    runState: Optional[RunState]
    startedOn: Optional[datetime]
    duration: Optional[str]
    errors: Optional[List[AutoloadStatusError]]
    info: Optional[dict]
