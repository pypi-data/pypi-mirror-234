from datetime import datetime
from typing import Optional

from LOGS.Entity.SerializeableContent import SerializeableClass


class AutoloadFileInfo(SerializeableClass):
    name: Optional[str] = None
    fullPath: Optional[str] = None
    size: Optional[int] = None
    modTime: Optional[datetime] = None
    isDir: Optional[bool] = None
