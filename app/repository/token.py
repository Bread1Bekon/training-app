from config import Settings
from datetime import datetime, timezone, timedelta
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.token import TokenDB

class TokenRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add_tokens(self, refresh_token: str) -> TokenDB:
        settings = Settings()
        token = TokenDB(refresh_token=refresh_token, is_valid=True, refresh_expires=datetime.now(timezone.utc) + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_DAYS))
        self.db.add(token)
        await self.db.commit()
        await self.db.refresh(token)
        return token

    async def get_token(self, refresh_token: str) -> TokenDB:
        result = await self.db.execute(select(TokenDB).where(refresh_token == TokenDB.refresh_token))
        return result.scalar_one_or_none()

    async def revoke_token(self, refresh_token: str) -> TokenDB:
        db_token = await self.get_token(refresh_token)
        if db_token:
            db_token.is_valid = False
            await self.db.commit()
            await self.db.refresh(db_token)
            return True
        return False
