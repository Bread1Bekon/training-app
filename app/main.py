from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from app.api import root_router

from app.db import engine
from app.models.user import Base, UserDB

from app.db import engine
from app.models.base import Base

app = FastAPI(debug=True)
load_dotenv()
# @app.on_event("startup")
# async def startup_event():
#     # Создать таблицы, если их нет
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#     print("Tables created successfully")


app.include_router(root_router)


