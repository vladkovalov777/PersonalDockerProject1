from fastapi import Request, APIRouter, Form, status
from fastapi.responses import RedirectResponse
import httpx

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

    """
    curl -X 'POST' \
      'http://localhost:19999/users/create' \
      -H 'accept: application/json' \
      -H 'Content-Type: application/json' \
      -d '{
      "email": "user@example.com",
      "name": "string",
      "password": "string"
    }'
    """
    async with httpx.AsyncClient() as client:
        headers = {
            "Content-Type": "application/json",
        }
        payload = {
            "email": email,
            "name": username,
            "password": password
        }
        response = await client.post("http://backend:20001/users/create", json=payload, headers=headers)



    response = RedirectResponse(request.url_for('index'), status_code=status.HTTP_303_SEE_OTHER)
    return response