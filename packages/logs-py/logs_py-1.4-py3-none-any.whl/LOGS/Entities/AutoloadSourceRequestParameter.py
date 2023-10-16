from dataclasses import dataclass
from typing import List, Optional

from LOGS.Entity.EntityRequestParameter import EntityRequestParameter


@dataclass
class AutoloadSourceRequestParameter(EntityRequestParameter):
    names: Optional[List[str]] = None
    hostnames: Optional[List[str]] = None
    usernames: Optional[List[str]] = None
    ipAddresses: Optional[List[str]] = None
    configurationIds: Optional[List[int]] = None
