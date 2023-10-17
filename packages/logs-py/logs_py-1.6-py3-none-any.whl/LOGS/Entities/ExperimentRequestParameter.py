from dataclasses import dataclass
from typing import List, Optional

from LOGS.Entity.EntityRequestParameter import EntityRequestParameter
from LOGS.Interfaces.IOwnedEntity import IOwnedEntityRequest


@dataclass
class ExperimentRequestParameter(EntityRequestParameter, IOwnedEntityRequest):
    name: Optional[str] = None
    methodIds: Optional[List[int]] = None
