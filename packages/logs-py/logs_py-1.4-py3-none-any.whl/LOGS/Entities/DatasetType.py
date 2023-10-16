from LOGS.Auxiliary.Decorators import Endpoint
from LOGS.Entities.CustomSchema import CustomSchema


@Endpoint("dataset_types")
class DatasetType(CustomSchema):
    pass
