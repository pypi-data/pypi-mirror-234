from LOGS.Auxiliary.Decorators import Endpoint
from LOGS.Entities.AutoloadSource import AutoloadSource
from LOGS.Entities.AutoloadSourceRequestParameter import AutoloadSourceRequestParameter
from LOGS.Entity.EntityIterator import EntityIterator


@Endpoint("autoload_sources")
class AutoloadSources(EntityIterator[AutoloadSource, AutoloadSourceRequestParameter]):
    """LOGS connected class AutouploadSource iterator"""

    _generatorType = AutoloadSource
    _parameterType = AutoloadSourceRequestParameter
