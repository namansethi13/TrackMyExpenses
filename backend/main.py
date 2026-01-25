from fastapi import FastAPI
from middleware.auth import AuthMiddleware
from routers.routes import router

app = FastAPI()

app.add_middleware(AuthMiddleware)
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)