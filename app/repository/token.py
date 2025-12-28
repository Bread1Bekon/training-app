from config import settings
from app.redis_db import redis_db
from app.models.token import TokenDB

SECONDS_IN_DAY = 86400
SECONDS_IN_MINUTE = 60

class TokenRepository:
    def __init__(self):
        self.redis_client = redis_db

    async def add_access_token(self, token: str):
        self.redis_client.setex(token, settings.ACCESS_TOKEN_EXPIRE_MINUTES*SECONDS_IN_MINUTE,)
        return True

    async def add_refresh_token(self, token: str):
        self.redis_client.setex(token, settings.REFRESH_TOKEN_EXPIRE_DAYS*SECONDS_IN_DAY,)
        return True

    async def check_token(self, token: str) -> TokenDB:
        return self.redis_client.exists(token)
