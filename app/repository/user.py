from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import UserDB


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_user(self, user_data: dict) -> UserDB:
        user = UserDB(**user_data)
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def get_user_by_id(self, user_id: int) -> UserDB:
        result = await self.db.execute(select(UserDB).where(user_id == UserDB.id))
        return result.scalar_one_or_none()

    async def get_user_by_email(self, user_email: str) -> UserDB:
        result = await self.db.execute(select(UserDB).where(user_email == UserDB.email))
        return result.scalar_one_or_none()

    async def delete_user(self, user_id: int) -> bool:
        user = await self.get_user_by_id(user_id)
        if user:
            await self.db.delete(user)
            await self.db.commit()
            return True
        return False

    async def log_in(self, user_email: str):
        return await self.get_user_by_email(user_email)

    async def update_user(self, user_id: int, update_data: dict) -> UserDB | None:
        user = await self.get_user_by_id(user_id)
        for key, value in update_data.items():
                setattr(user, key, value)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def change_password(self, user_id: int, new_password: str) -> UserDB | None:
        user = await self.get_user_by_id(user_id)
        user.password = new_password
        await self.db.commit()
        await self.db.refresh(user)
        return user
