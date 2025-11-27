from fastapi import FastAPI

from router_user import router_user


def get_application() -> FastAPI:
    app = FastAPI(debug=True)

    app.include_router(router_user)

    return app


app = get_application()