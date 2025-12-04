from datetime import timedelta, datetime

import jwt

from apps.users.models import User
from settings import settings


class AuthHandler:
    def __init__(self):
        self.secret = settings.JWT_SECRET
        self.algorithm = settings.JWT_ALGORITHM

    async def get_token_pairs(self, user: User) -> dict:
        access_token_payload = {
            'id': user.id
        }
        refresh_token_payload = {
            'id': user.id,
        }
        # todo process refresh token

        return {
            "access_token": await self.generate_token(access_token_payload, timedelta(minutes=settings.ACCESS_TOKEN_LIFETIME_MINUTES)),
            "refresh_token": await self.generate_token(refresh_token_payload, timedelta(minutes=settings.REFRESH_TOKEN_LIFETIME_MINUTES))
        }

    async def generate_token(self, payload: dict, expiry: timedelta) -> str:
        now = datetime.now()
        time_payload = {
            'exp': now + expiry,
            'iat': now,
        }
        payload.update(time_payload)
        token = jwt.encode(
            payload=payload,
            key=self.secret,
            algorithm=self.algorithm

        )

        return token


auth_handler = AuthHandler()