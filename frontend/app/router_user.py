from fastapi import Request, APIRouter, Form, status, Depends
from fastapi.responses import RedirectResponse
import httpx

from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

router_user = APIRouter()


async def get_user_info(access_token: str) -> dict:
    headers_user_info = {
        "Content-Type": "application/json",
        "Authorization": f'Bearer {access_token}'
    }
    async with httpx.AsyncClient() as client:
        response_user_info = await client.get("http://backend:20001/users/my-info", headers=headers_user_info)
        return response_user_info.json()


async def get_user(request: Request) -> dict:
    access_token = request.cookies.get('access_token')
    if not access_token:
        return {}
    user = await get_user_info(access_token)
    return user


@router_user.get("/")
async def index(request: Request, user: dict = Depends(get_user)):
    context = {
        "request": request,
        "title": "Головна сторінка сайту",
        "user": user
    }

    response = templates.TemplateResponse('pages/index.html', context=context)

    return response


@router_user.get("/register")
@router_user.post("/register")
async def user_register(request: Request, email: str = Form(''), username: str = Form(''), password: str = Form('')):
    context = {
        "request": request,
        "title": "Register",
        "user": {},
        "email": email,
        "username": username,
        "error": ""
    }
    if request.method == "GET":
        response = templates.TemplateResponse('pages/register.html', context=context)
        return response

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

        if response.status_code == status.HTTP_409_CONFLICT:
            context['error'] = f"Користувач {email} вже зареєстрований"
            response = templates.TemplateResponse('pages/register.html', context=context)
            return response

    response = RedirectResponse(request.url_for('index'), status_code=status.HTTP_303_SEE_OTHER)
    return response


@router_user.get("/login")
@router_user.post("/login")
async def user_login(request: Request, email: str = Form(''), password: str = Form(''), user: dict = Depends(get_user)):
    if user:
        redirect_url = request.url_for('index')
        response = RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)
        return response

    context = {
        "request": request,
        "title": "Login",
        "user": user,
        "email": email,
        "error": ""
    }
    if request.method == "GET":
        response = templates.TemplateResponse('pages/login.html', context=context)
        return response

    async with httpx.AsyncClient() as client:
        # get token
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        data = {
            'username': email,
            'password': password
        }
        response = await client.post("http://backend:20001/users/login", data=data, headers=headers)
        tokens = response.json()
        print(tokens)
        access_token = tokens['access_token']
        user_info = await get_user_info(access_token)

    context['user'] = user_info

    redirect_url = request.url_for('index')
    response = RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key='access_token', value=access_token, httponly=True, max_age=14 * 60)
    return response


@router_user.get("/logout")
async def logout(request: Request):
    redirect_url = request.url_for('index')
    response = RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie('access_token')
    return response