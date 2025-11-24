from fastapi import APIRouter, status, Depends

from apps.auth.password_handler import PasswordHandler
from apps.core.dependencies import get_async_session
from apps.users.crud import user_manager
from apps.users.schemas import SavedUserSchema, RegisterUserSchema
from sqlalchemy.ext.asyncio import AsyncSession

users_router = APIRouter()


@users_router.post('/create', status_code=status.HTTP_201_CREATED)
async def create_user(
        user_data: RegisterUserSchema,
        session: AsyncSession = Depends(get_async_session)
) -> SavedUserSchema:
    """create user based on name email password"""
    hashed_password = await PasswordHandler.get_password_hash(user_data.password)
    # is_valid = await PasswordHandler.verify_password(user_data.password, hashed_password)
    saved_user = await user_manager.create(
        session=session,
        name=user_data.name,
        email=user_data.email,
        hashed_password=hashed_password,
    )

    return saved_user