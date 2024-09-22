from fastapi import FastAPI, HTTPException

from tick_manager.models.schemas import OperationRequest, OperationResponse
from tick_manager.operations.core import add, divide, multiply, subtract

app = FastAPI(title="Tick Manager API")


@app.get("/")
def read_root() -> dict:
    return {"message": "Welcome to Tick Manager API"}


@app.post("/add", response_model=OperationResponse)
def add_endpoint(request: OperationRequest) -> OperationResponse:
    result = add(request.a, request.b)
    return OperationResponse(result=result)


@app.post("/subtract", response_model=OperationResponse)
def subtract_endpoint(request: OperationRequest) -> OperationResponse:
    result = subtract(request.a, request.b)
    return OperationResponse(result=result)


@app.post("/multiply", response_model=OperationResponse)
def multiply_endpoint(request: OperationRequest) -> OperationResponse:
    result = multiply(request.a, request.b)
    return OperationResponse(result=result)


@app.post("/divide", response_model=OperationResponse)
def divide_endpoint(request: OperationRequest) -> OperationResponse:
    try:
        result = divide(request.a, request.b)
        return OperationResponse(result=result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from None


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
