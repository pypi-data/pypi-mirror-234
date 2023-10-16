from LOGS.Auxiliary.Decorators import FullModel
from LOGS.Entities.DatasetType import DatasetType
from LOGS.Entity.EntityMinimalWithStrId import EntityMinimalWithStrId


@FullModel(DatasetType)
class DatasetTypeMinimal(EntityMinimalWithStrId[DatasetType]):
    pass
