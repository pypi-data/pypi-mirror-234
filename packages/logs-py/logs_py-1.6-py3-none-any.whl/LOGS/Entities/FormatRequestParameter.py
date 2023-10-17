from dataclasses import dataclass
from typing import Optional

from LOGS.Entity.EntityRequestParameter import EntityRequestParameter


@dataclass
class FormatRequestParameter(EntityRequestParameter):
    name: Optional[str] = None
