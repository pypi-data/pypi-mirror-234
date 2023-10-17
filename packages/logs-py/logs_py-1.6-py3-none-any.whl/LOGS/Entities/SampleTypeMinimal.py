from LOGS.Auxiliary.Decorators import FullModel
from LOGS.Entities.SampleType import SampleType
from LOGS.Entity.EntityMinimalWithStrId import EntityMinimalWithStrId


@FullModel(SampleType)
class SampleTypeMinimal(EntityMinimalWithStrId[SampleType]):
    pass
