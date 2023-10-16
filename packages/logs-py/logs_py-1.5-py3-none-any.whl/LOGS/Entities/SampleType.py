from LOGS.Auxiliary.Decorators import Endpoint
from LOGS.Entities.CustomSchema import CustomSchema


@Endpoint("sample_types")
class SampleType(CustomSchema):
    pass
