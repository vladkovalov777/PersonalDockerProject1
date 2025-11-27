from fastapi import Request, APIRouter

from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

router_user = APIRouter()


@router_user.get("/")
async def index(request: Request):
    context = {
        "request": request,
        "title": "Головна сторінка сайту"
    }

    response = templates.TemplateResponse('pages/index.html', context=context)

    return response