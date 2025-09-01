from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api import root_router

from app.db import engine
from app.models.user import UserDB

# Create the tables (run only once)
app = FastAPI(debug=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(UserDB.metadata.create_all)
        print("Tables created!")
        yield

app.include_router(root_router)
