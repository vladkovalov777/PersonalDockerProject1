from datetime import timedelta, datetime
from uuid import uuid4

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

import jwt

from apps.users.crud import user_manager
from apps.users.models import User
from services.redis_service import redis_service
from settings import settings


class AuthHandler:
    def __init__(self):
        self.secret = settings.JWT_SECRET
        self.algorithm = settings.JWT_ALGORITHM

    async def get_token_pairs(self, user: User) -> dict:
        access_token_payload = {
            'sub': user.email
        }

        refresh_key = uuid4().hex
        refresh_token_payload = {
            'sub': user.email,
            'key': refresh_key
        }
        redis_service.set_key(F"refresh_token_key:{refresh_key}", '1', settings.REFRESH_TOKEN_LIFETIME_MINUTES * 60)

        return {
            "access_token": await self.generate_token(access_token_payload,
                                                      timedelta(minutes=settings.ACCESS_TOKEN_LIFETIME_MINUTES)),
            "refresh_token": await self.generate_token(refresh_token_payload,
                                                       timedelta(minutes=settings.REFRESH_TOKEN_LIFETIME_MINUTES))
        }

    async def generate_token(self, payload: dict, expiry: timedelta) -> str:
        now = datetime.now()
        time_payload = {
            'exp': now + expiry,
            'iat': now,
        }
        payload.update(time_payload)
        token = jwt.encode(
            payload,
            self.secret,
            algorithm=self.algorithm

        )

        return token

    async def decode_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, self.secret, [self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(detail=f'token expired',
                                status_code=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError as e:
            raise HTTPException(detail=f'where have you got this token, dude',
                                status_code=status.HTTP_401_UNAUTHORIZED)

    async def get_token_pairs_by_refresh_token(self, refresh_token: str, session: AsyncSession) -> dict:
        payload = await self.decode_token(refresh_token)
        refresh_token_key = payload.get("key")
        if not refresh_token_key:
            raise HTTPException(detail=f'Invalid refresh', status_code=status.HTTP_401_UNAUTHORIZED)

        refresh_token_key_in_redis = redis_service.get(F"refresh_token_key:{refresh_token_key}")
        if not refresh_token_key_in_redis:
            raise HTTPException(detail=f'Redis token was used already',
                                status_code=status.HTTP_401_UNAUTHORIZED)

        redis_service.delete(F"refresh_token_key:{refresh_token_key}")

        user: User = await user_manager.get(session=session, model_field=User.email, value=payload['sub'])
        if not user:
            raise HTTPException(detail=f'User with email {payload["sub"]} not found',
                                status_code=status.HTTP_404_NOT_FOUND)
        token_pair = await self.get_token_pairs(user)
        return token_pair


auth_handler = AuthHandler()