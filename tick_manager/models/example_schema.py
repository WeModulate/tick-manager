from pydantic import BaseModel, Field


class OperationRequest(BaseModel):
    """
    OperationRequest model to represent the request body for operations.

    Attributes:
        a (float): The first operand.
        b (float): The second operand.
    """

    a: float = Field(..., description="First operand")
    b: float = Field(..., description="Second operand")


class OperationResponse(BaseModel):
    """
    OperationResponse model to represent the response body for operations.

    Attributes:
        result (float): The result of the operation.
    """

    result: float = Field(..., description="Result of the operation")
