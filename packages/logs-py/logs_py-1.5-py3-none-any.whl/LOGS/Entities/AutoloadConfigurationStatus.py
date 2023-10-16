from datetime import datetime
from typing import List, Optional

from LOGS.Entities.AutoloadStatus import AutoloadStatus
from LOGS.Entity.SerializeableContent import SerializeableClass


class AutoloadConfigurationStatus(SerializeableClass):
    isConnected: Optional[bool] = None
    nextScheduledDate: Optional[datetime] = None
    lastClientStatus: Optional[AutoloadStatus] = None
    statusHistory: Optional[List[AutoloadStatus]] = None
