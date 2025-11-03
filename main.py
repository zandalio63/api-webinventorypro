from fastapi import FastAPI
from contextlib import asynccontextmanager

from db.connnection import db_management

@asynccontextmanager
async def lifespan(app : FastAPI):
    await db_management.connect_to_db()
    yield
    await db_management.disconnect_from_db()

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def main():
    return {"hello" : "World"}