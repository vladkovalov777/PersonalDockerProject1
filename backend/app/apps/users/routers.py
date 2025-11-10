from fastapi import APIRouter, status

from apps.auth.password_handler import PasswordHandler
from apps.users.schemas import UserBaseFieldsSchema, RegisterUserSchema

users_router = APIRouter()


@users_router.post('/create', status_code=status.HTTP_201_CREATED)
async def create_user(user_data: RegisterUserSchema) -> UserBaseFieldsSchema:
    """create user based on name email password"""
    print(user_data.password, 8888888888888)
    hp = await PasswordHandler.get_password_hash(user_data.password)
    print(hp)

    is_valid = await PasswordHandler.verify_password(user_data.password, hp)

    print(is_valid, 9999999999999999999999999999999)

    return user_data