from pydantic import BaseModel, EmailStr
from typing import Optional

# ----------------- User Create -----------------
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    role: Optional[str] = "user"
    password: str

# ----------------- User Login -----------------
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# ----------------- User Response -----------------
class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str
    status: str
    created_at: str

    class Config:
        orm_mode = True
