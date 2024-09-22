from pydantic import BaseModel, Field

class OperationRequest(BaseModel):
    a: float = Field(..., description="First operand")
    b: float = Field(..., description="Second operand")

class OperationResponse(BaseModel):
    result: float = Field(..., description="Result of the operation")

