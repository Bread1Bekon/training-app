from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.profile import ProfileDB


class ProfileRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_profile(self, user_id: int) -> ProfileDB:
        profile = ProfileDB(user_id=user_id)
        self.db.add(profile)
        await self.db.commit()
        await self.db.refresh(profile)
        return profile

    async def get_profile_by_user_id(self, user_id: int) -> ProfileDB | None:
        result = await self.db.execute(select(ProfileDB).where(ProfileDB.user_id == user_id))
        return result.scalar_one_or_none()

    async def update_profile(self, user_id: int, update_data: dict) -> ProfileDB | None:
        profile = await self.get_profile_by_user_id(user_id)
        for key, value in update_data.items():
         setattr(profile, key, value)
        await self.db.commit()
        await self.db.refresh(profile)
        return profile
