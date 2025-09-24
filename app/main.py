from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api import root_router

from app.db import engine
from app.models.user import Base, UserDB

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        print(UserDB.__table__.columns)
        yield

app = FastAPI(debug=True, lifespan=lifespan)

app.include_router(root_router)


