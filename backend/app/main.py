from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, create_engine
from sqlalchemy.orm import sessionmaker
from .models import User, Base

# Get the DATABASE_URL from the environment
DATABASE_URL = os.environ["DATABASE_URL"]

# Create an async engine
engine = create_engine(
    DATABASE_URL,
    echo=True,  # print SQL statements
)

# Create a session maker
async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_db():
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()

# Create the tables (run only once)
@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app = FastAPI()

# ... (rest of the code remains the same)