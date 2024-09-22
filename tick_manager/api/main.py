from fastapi import FastAPI

app = FastAPI(title="Tick Manager API")

@app.get('/')
def read_root():
    return {"message": "Welcome to Tick Manager API"}

