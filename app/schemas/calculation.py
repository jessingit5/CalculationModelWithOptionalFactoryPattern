# app/schemas/calculation.py

from pydantic import BaseModel, model_validator, computed_field
from enum import Enum
from typing import Optional

from ..core.factory import CalculationFactory # We'll create this next

# Use an Enum to define the allowed calculation types
class CalculationType(str, Enum):
    ADD = "add"
    SUBTRACT = "subtract"
    MULTIPLY = "multiply"
    DIVIDE = "divide"

# Schema for creating a new calculation (input)
class CalculationCreate(BaseModel):
    a: float
    b: float
    type: CalculationType

    # Pydantic v2 validator to check for division by zero
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
        """Computes the result of the calculation."""
        try:
            operation = CalculationFactory.get_operation(self.type)
            return operation(self.a, self.b).execute()
        except (ValueError, KeyError):
            # This case should ideally not be hit if DB data is clean
            return float('nan') # Not a Number

    class Config:
        # For Pydantic v1, use orm_mode = True
        # For Pydantic v2, this is the way
        from_attributes = True