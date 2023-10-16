from LOGS.Auxiliary.Decorators import FullModel
from LOGS.Entities.Format import Format
from LOGS.Entity.EntityMinimalWithStrId import EntityMinimalWithStrId


@FullModel(Format)
class FormatMinimal(EntityMinimalWithStrId[Format]):
    pass
