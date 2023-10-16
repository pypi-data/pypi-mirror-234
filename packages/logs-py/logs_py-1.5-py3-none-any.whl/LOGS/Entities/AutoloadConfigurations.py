from LOGS.Auxiliary.Decorators import Endpoint
from LOGS.Entities.AutoloadConfiguration import AutoloadConfiguration
from LOGS.Entities.AutoloadConfigurationRequestParameter import (
    AutoloadConfigurationRequestParameter,
)
from LOGS.Entity.EntityIterator import EntityIterator


@Endpoint("autoload_configurations")
class AutoloadConfigurations(
    EntityIterator[AutoloadConfiguration, AutoloadConfigurationRequestParameter]
):
    """LOGS connected class AutouploadSource iterator"""

    _generatorType = AutoloadConfiguration
    _parameterType = AutoloadConfigurationRequestParameter
