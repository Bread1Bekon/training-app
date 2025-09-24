from pydantic import BaseModel, ConfigDict

class UserBase(BaseModel):
    name: str
    email: str
    password: str

class UserCreate(UserBase):
    pass

class UserOut(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int