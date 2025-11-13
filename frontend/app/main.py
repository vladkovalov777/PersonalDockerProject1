from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")


def get_application() -> FastAPI:
    app = FastAPI(debug=True)

    @app.get("/")
    async def index(request: Request):
        context = {
            "request": request,
            "title": "Головна сторінка сайту"
        }

        response = templates.TemplateResponse('pages/index.html', context=context)

        return response


    return app


app = get_application()