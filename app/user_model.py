from pydantic import BaseModel

class User(BaseModel):
    name: str | None = None
    email: str
    id: int

class UserBase(BaseModel):
    name:  str | None = None
    email: str

class UserCreate(UserBase):
    pass                         # same fields we allow on create

class UserOut(UserBase):
    id: int