from fastapi import Request, APIRouter, Form, status
from fastapi.responses import RedirectResponse

from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

router_user = APIRouter()


@router_user.get("/")
async def index(request: Request):
    context = {
        "request": request,
        "title": "Головна сторінка сайту",
        "user": {}
    }

    response = templates.TemplateResponse('pages/index.html', context=context)

    return response


@router_user.get("/register")
@router_user.post("/register")
async def user_register(request: Request, email: str = Form(''), username: str = Form(''), password: str = Form('')):
    context = {
        "request": request,
        "title": "Register",
        "user": {}
    }
    if request.method == "GET":

        response = templates.TemplateResponse('pages/register.html', context=context)
        return response

    response = RedirectResponse(request.url_for('index'), status_code=status.HTTP_303_SEE_OTHER)
    return response