from fastapi import FastAPI
from contextlib import asynccontextmanager

from db.connnection import db_management
from api.routers import auth, user

@asynccontextmanager
async def lifespan(app : FastAPI):
    await db_management.connect_to_db()
    yield
    await db_management.disconnect_from_db()

app = FastAPI(lifespan=lifespan)

app.include_router(auth.router)
app.include_router(user.router)

@app.get("/")
async def main():
    return {"hello" : "World"}