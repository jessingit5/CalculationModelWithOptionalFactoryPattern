from pydantic import BaseModel, model_validator, computed_field
from enum import Enum
from typing import Optional

from ..core.factory import CalculationFactory 
class CalculationType(str, Enum):
    ADD = "add"
    SUBTRACT = "subtract"
    MULTIPLY = "multiply"
    DIVIDE = "divide"

class CalculationCreate(BaseModel):
    a: float
    b: float
    type: CalculationType

    @model_validator(mode='after')
    def check_division_by_zero(self) -> 'CalculationCreate':
        if self.type == CalculationType.DIVIDE and self.b == 0:
            raise ValueError("Division by zero is not allowed.")
        return self

class CalculationRead(BaseModel):
    id: int
    a: float
    b: float
    type: CalculationType
    user_id: int

    @computed_field
    @property
    def result(self) -> float:
        try:
            operation = CalculationFactory.get_operation(self.type)
            return operation(self.a, self.b).execute()
        except (ValueError, KeyError):
            return float('nan') 

    class Config:
        from_attributes = True