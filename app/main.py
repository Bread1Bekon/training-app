import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, status, HTTPException
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, create_engine
from sqlalchemy.orm import sessionmaker
from app.db_model import UserDB
from app.user_model import UserCreate, UserOut, User

print(os.listdir('.'))

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
@asynccontextmanager
async def get_db():
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()

# Create the tables (run only once)
app = FastAPI()
@app.on_event("startup")
@asynccontextmanager
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(UserDB.metadata.create_all)


# --- POST /users ---
@app.post("/users", response_model=UserOut, status_code=201)
async def create_user(payload: UserCreate, db: AsyncSession = Depends(get_db)):
    new_user = User(**payload.dict(), id=None)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


# --- DELETE /users/{user_id} ---
@app.delete("/users/{user_id}", status_code=204)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    user_obj = result.scalar_one_or_none()
    if user_obj is None:
        raise HTTPException(status_code=404, detail="User not found")

    await db.delete(user_obj)
    await db.commit()
    return Response(status_code=204)