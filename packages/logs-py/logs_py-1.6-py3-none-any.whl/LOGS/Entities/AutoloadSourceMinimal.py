from LOGS.Auxiliary.Decorators import FullModel
from LOGS.Entities.AutoloadSource import AutoloadSource
from LOGS.Entity.EntityMinimalWithIntId import EntityMinimalWithIntId


@FullModel(AutoloadSource)
class AutoloadSourceMinimal(EntityMinimalWithIntId[AutoloadSource]):
    pass
