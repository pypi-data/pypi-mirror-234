from dataclasses import dataclass
from typing import Optional

from LOGS.Entity.EntityRequestParameter import EntityRequestParameter


@dataclass
class FormatVendorRequestParameter(EntityRequestParameter):
    includeIcon: Optional[bool] = None
