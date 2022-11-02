from fastapi_users import models
from pydantic import EmailStr


class User(models.BaseModel):
    # Сам пользователь
    username: str
    phone: str


class UserCreate(models.BaseUserCreate):
    # Создание пользователя
    username: str
    email: EmailStr
    password: str
    phone: str


class UserUpdate(User, models.BaseUserUpdate):
    # Обновление пользователя
    username: str


class UserDB(User, models.BaseUserDB):
    # Вывод пользователя
    username: str
