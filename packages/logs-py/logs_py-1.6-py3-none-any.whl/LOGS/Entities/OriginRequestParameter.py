from dataclasses import dataclass
from typing import List, Optional, Sequence, Union
from uuid import UUID

from LOGS.Entity.EntityRequestParameter import EntityRequestParameter


@dataclass
class OriginRequestParameter(EntityRequestParameter):
    names: Optional[List[str]] = None
    urls: Optional[List[str]] = None
    uids: Optional[Sequence[Union[UUID, str]]] = None
