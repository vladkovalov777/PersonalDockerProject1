from apps.auth.auth_handler import auth_handler
from apps.core.base_model import async_session_maker
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from apps.users.crud import user_manager
from apps.users.models import User


class SecurityHandler:
    oauth2_schema = OAuth2PasswordBearer(tokenUrl="/users/login")


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_current_user(
        token: str = Depends(SecurityHandler.oauth2_schema),
        session: AsyncSession = Depends(get_async_session)
) -> User:
    payload = await auth_handler.decode_token(token)

    user: User = await user_manager.get(session=session, model_field=User.email, value=payload['sub'])
    if not user:
        raise HTTPException(detail=f'User with email {payload["sub"]} not found',
                            status_code=status.HTTP_404_NOT_FOUND)
    return user