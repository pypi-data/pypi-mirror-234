from LOGS.Auxiliary.Decorators import FullModel
from LOGS.Entities.AutoloadConfiguration import AutoloadConfiguration
from LOGS.Entity.EntityMinimalWithIntId import EntityMinimalWithIntId


@FullModel(AutoloadConfiguration)
class AutoloadConfigurationMinimal(EntityMinimalWithIntId[AutoloadConfiguration]):
    pass
