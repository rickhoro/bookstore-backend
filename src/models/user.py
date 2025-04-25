from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from enum import Enum

class Role(str, Enum):
    superuser = "superuser"
    admin = "admin"
    user = "user"

    def has_at_least(self, other: "Role") -> bool:
        hierarchy = [Role.user, Role.admin, Role.superuser]
        try:
            return hierarchy.index(self) >= hierarchy.index(other)
        except ValueError:
            return False  # or raise a meaningful error

class UserCreate(BaseModel):
    username: str | None = None
    email: EmailStr
    password: str
    role: Role


class UserInDB(UserCreate):
    hashed_password: str


class UserOut(BaseModel):
    email: EmailStr

class JWTTokenContents(BaseModel):
    pass

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
