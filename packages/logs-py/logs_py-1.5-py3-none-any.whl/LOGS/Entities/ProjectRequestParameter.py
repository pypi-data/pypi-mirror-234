from dataclasses import dataclass
from typing import List, Optional

from LOGS.Entity.EntityRequestParameter import EntityRequestParameter
from LOGS.Interfaces.IOwnedEntity import IOwnedEntityRequest


@dataclass
class ProjectRequestParameter(EntityRequestParameter, IOwnedEntityRequest):
    names: Optional[List[str]] = None
    notes: Optional[str] = None
    tags: Optional[List[str]] = None
