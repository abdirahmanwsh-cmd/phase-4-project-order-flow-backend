from fastapi import FastAPI
from app.api.router import api_router

app = FastAPI(title="Order Flow API")

app.include_router(api_router)

@app.get("/")
def root():
    return {"message": "Order Flow API is running"}
