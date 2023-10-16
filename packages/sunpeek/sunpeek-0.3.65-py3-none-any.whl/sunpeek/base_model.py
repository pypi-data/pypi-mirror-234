from pydantic import BaseModel as PydanticBaseModel
from pydantic import validator
import pint


class BaseModel(PydanticBaseModel):
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
        fields = {
            'class_': 'class'
        }

    @validator('*', pre=True)
    def make_strings(cls, v):
        if isinstance(v, pint.Unit):
            v = str(v)
            return v
        # elif isinstance(v, pint.Quantity):
        #     return str(v.units)
        # elif isinstance(v, cmp.Collector):
        #     return v.name
        return v

    @validator('units', 'native_unit', pre=True, check_fields=False)
    def validate_units(cls, v):
        if isinstance(v, pint.Quantity):
            return str(v.units)
        return v
