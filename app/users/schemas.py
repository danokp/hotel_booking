from pydantic import BaseModel, EmailStr


class UserAuthSchema(BaseModel):
    email: EmailStr
    password: str


class GetUserSchema(BaseModel):
    id: int
    email: EmailStr
