from dataclasses import dataclass
from typing import List, Optional

from LOGS.Entity.EntityRequestParameter import EntityRequestParameter


@dataclass
class AutoloadConfigurationRequestParameter(EntityRequestParameter):
    names: Optional[List[str]] = None
    enabled: Optional[bool] = None
    autoloadSourceIds: Optional[List[int]] = None
    formats: Optional[List[str]] = None
    directories: Optional[List[str]] = None
    methodIds: Optional[List[int]] = None
    instrumentIds: Optional[List[int]] = None
    sourceHostnames: Optional[List[str]] = None
    sourceIpAddresses: Optional[List[str]] = None
