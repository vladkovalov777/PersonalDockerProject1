from datetime import timedelta, datetime
from fastapi import HTTPException, status


import jwt

from apps.users.models import User
from settings import settings


class AuthHandler:
    def __init__(self):
        self.secret = settings.JWT_SECRET
        self.algorithm = settings.JWT_ALGORITHM

    async def get_token_pairs(self, user: User) -> dict:
        access_token_payload = {
            'sub': user.email
        }
        refresh_token_payload = {
            'sub': user.email,
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
            print(e, 888888888888888888)
            raise HTTPException(detail=f'where have you got this token, dude',
                                status_code=status.HTTP_401_UNAUTHORIZED)


auth_handler = AuthHandler()