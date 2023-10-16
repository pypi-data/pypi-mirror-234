from dataclasses import dataclass
from typing import List, Optional, Union
from uuid import UUID

from LOGS.Entity.SerializeableContent import SerializeableClass


@dataclass
class EntitiesRequestParameter(SerializeableClass):
    _noSerialize = ["asString"]
    uids: Optional[List[Union[str, UUID]]] = None
    names: Optional[List[str]] = None
