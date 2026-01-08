from fastapi import APIRouter, status, Depends, HTTPException, Header, Form, UploadFile, File

from apps.auth.auth_handler import auth_handler
from apps.auth.password_handler import PasswordHandler
from apps.core.dependencies import get_async_session, get_current_user
from apps.products.crud import product_manager
from apps.products.models import Product
from apps.products.schemas import SavedProductSchema
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm

products_router = APIRouter()


@products_router.post('/create', status_code=status.HTTP_201_CREATED)
async def create_product(
        title: str = Form(),
        description: str = Form(default=""),
        price: int = Form(gt=0),
        main_image: UploadFile = File(),
        images: list[UploadFile] = File(default=None, max_length=5),
        session: AsyncSession = Depends(get_async_session)
) -> SavedProductSchema:

    maybe_product = await product_manager.get(
        session=session,
        model_field=Product.title,
        value=title,
    )
    if maybe_product:
        raise HTTPException(detail=f'Product with title {maybe_product.title} already exists',
                            status_code=status.HTTP_409_CONFLICT)

    created_product = await product_manager.create(
        session=session,
        title=title,
        description=description,
        price=price,
        main_image='mmmmmm',
        # images=
    )

    return created_product