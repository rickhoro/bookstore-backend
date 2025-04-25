from fastapi import FastAPI
from routes import auth
from contextlib import asynccontextmanager
from db.mongo import connect_to_mongo, close_mongo_connection
from db.init_superuser import create_initial_user
import uvicorn

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    await connect_to_mongo()
    await create_initial_user()
    yield
    # Shutdown logic
    await close_mongo_connection()

app = FastAPI(lifespan=lifespan)

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])

@app.get("/")
async def root():
    return {"message": "Hello from FastAPI!"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    # uvicorn.run(app, host="0.0.0.0", port=8000)
