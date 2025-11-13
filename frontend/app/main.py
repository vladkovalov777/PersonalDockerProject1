from fastapi import FastAPI




def get_application() -> FastAPI:
    app = FastAPI()



    return app


app = get_application()