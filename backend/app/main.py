from fastapi import FastAPI

from apps.users.routers import users_router
from settings import settings


def get_application() -> FastAPI:
    app = FastAPI(debug=settings.DEBUG)

    app.include_router(users_router, prefix='/users', tags=['Users', "Auth"])

    return app


app = get_application()