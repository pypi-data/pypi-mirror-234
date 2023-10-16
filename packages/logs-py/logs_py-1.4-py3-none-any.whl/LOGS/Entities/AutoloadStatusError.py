from typing import Optional

from LOGS.Entity.SerializeableContent import SerializeableClass


class AutoloadStatusError(SerializeableClass):
    message: Optional[str] = None
