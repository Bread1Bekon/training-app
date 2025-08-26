from fastapi.responses import Response
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.schemas import UserCreate, UserOut
from app.models import UserDB
from app.db import get_db

user_router = APIRouter(
    prefix="/user",
    tags=["user"]
)

@user_router.post("/", response_model=UserOut, status_code=201)
async def create_user(
    payload: UserCreate,
    db: AsyncSession = Depends(get_db)  # <-- Still Depends on get_db
):
    async with db as session:  # <--- ENTER THE ASYNC CONTEXT HERE
        user = UserDB(**payload.dict())
        session.add(user)      # Now 'session' is the real AsyncSession
        await session.commit()
        await session.refresh(user)
        return user                  # Pydantic's orm_mode will convert it


@user_router.delete("/{user_id}", status_code=204)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(UserDB).where(UserDB.id == user_id))
    user_obj = result.scalar_one_or_none()
    if user_obj is None:
        raise HTTPException(status_code=404, detail="User not found")
    await db.delete(user_obj)
    await db.commit()
    return Response(status_code=204)