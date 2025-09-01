from fastapi import HTTPException
from app.repository.user import UserRepository
from app.schemas.user_schemas import UserCreate, UserOut

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def create_user(self, user_create: UserCreate) -> UserOut:
        user_db = await self.user_repository.create_user(user_create.model_dump())
        return UserOut.model_validate(user_db)

    async def delete_user(self, user_id: int) -> None:
        deleted = await self.user_repository.delete_user(user_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="User not found")

## get excercises/
## get excercises/{excercise_id}
## put excercises/{excercise_id}
##