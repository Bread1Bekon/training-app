import json

from app.schemas.user import UserOut
from config import settings
from app.redis_db import redis_db

SECONDS_IN_DAY = 86400
SECONDS_IN_MINUTE = 60

class TokenRepository:
    def __init__(self):
        self.redis_client = redis_db

    async def add_access_token(self, user: UserOut, token: str):
        token_expiration = settings.ACCESS_TOKEN_EXPIRE_MINUTES*SECONDS_IN_MINUTE
        user_data = user.model_dump_json()
        await self.redis_client.setex(token, token_expiration, user_data)
        return True

    async def add_refresh_token(self, user: UserOut, token: str):
        token_expiration = settings.REFRESH_TOKEN_EXPIRE_DAYS*SECONDS_IN_DAY
        user_data = user.model_dump_json()
        await self.redis_client.setex(token, token_expiration, user_data)
        return True

    async def check_token(self, token: str):
        data = await self.redis_client.get(token)

        if data is None:
            return None

        return json.loads(data)
