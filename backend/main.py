from fastapi import FastAPI
from middleware.auth import AuthMiddleware
app = FastAPI()

app.add_middleware(AuthMiddleware)

@app.get("/")
async def root():
    return {"message": "Hello World"}