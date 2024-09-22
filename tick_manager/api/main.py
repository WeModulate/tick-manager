from fastapi import FastAPI, HTTPException

from tick_manager.models.schema import OperationRequest, OperationResponse
from tick_manager.operations.core import add, divide, multiply, subtract

# Create a FastAPI instance with a title
app = FastAPI(title="Tick Manager API")


@app.get("/")
def read_root() -> dict:
    """
    Root endpoint that returns a welcome message.

    Returns:
        dict: A dictionary containing a welcome message.
    """
    return {"message": "Welcome to Tick Manager API"}


@app.post("/add", response_model=OperationResponse)
def add_endpoint(request: OperationRequest) -> OperationResponse:
    """
    Endpoint to add two numbers.

    Args:
        request (OperationRequest): The request body containing two numbers.

    Returns:
        OperationResponse: The result of the addition.
    """
    result = add(request.a, request.b)
    return OperationResponse(result=result)


@app.post("/subtract", response_model=OperationResponse)
def subtract_endpoint(request: OperationRequest) -> OperationResponse:
    """
    Endpoint to subtract two numbers.

    Args:
        request (OperationRequest): The request body containing two numbers.

    Returns:
        OperationResponse: The result of the subtraction.
    """
    result = subtract(request.a, request.b)
    return OperationResponse(result=result)


@app.post("/multiply", response_model=OperationResponse)
def multiply_endpoint(request: OperationRequest) -> OperationResponse:
    """
    Endpoint to multiply two numbers.

    Args:
        request (OperationRequest): The request body containing two numbers.

    Returns:
        OperationResponse: The result of the multiplication.
    """
    result = multiply(request.a, request.b)
    return OperationResponse(result=result)


@app.post("/divide", response_model=OperationResponse)
def divide_endpoint(request: OperationRequest) -> OperationResponse:
    """
    Endpoint to divide two numbers.

    Args:
        request (OperationRequest): The request body containing two numbers.

    Returns:
        OperationResponse: The result of the division.

    Raises:
        HTTPException: If division by zero occurs.
    """
    try:
        result = divide(request.a, request.b)
        return OperationResponse(result=result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from None


if __name__ == "__main__":
    import uvicorn

    # Run the FastAPI application using Uvicorn
    uvicorn.run(app, host="localhost", port=8000)
