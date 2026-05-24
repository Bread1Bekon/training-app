import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
from app.api import root_router
from fastapi.middleware.cors import CORSMiddleware

from app.db import engine
from app.models.user import Base, UserDB

from app.db import engine
from app.models.base import Base
from app.errors import AppError


app = FastAPI(debug=True)

@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})

@app.get("/")
async def read_root():
    return {"status": "online", "message": "MentorFlow Backend API is fully active!"}

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#load_dotenv()
# @app.on_event("startup")
# async def startup_event():
#     # Создать таблицы, если их нет
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#     print("Tables created successfully")


app.include_router(root_router)


