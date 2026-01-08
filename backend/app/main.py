from fastapi import FastAPI

from apps.users.routers import users_router
from apps.products.routers import products_router
from settings import settings


def get_application() -> FastAPI:
    app = FastAPI(debug=settings.DEBUG)

    app.include_router(users_router, prefix='/users', tags=['Users', "Auth"])
    app.include_router(products_router, prefix='/products', tags=["Products"])

    return app


app = get_application()