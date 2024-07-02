from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from core.models import db_helper
from . import crud
from .schemas import Product, ProductCreate, ProductUpdate, ProductUpdatePartial
from .dependencies import product_by_id

router = APIRouter(tags=["Products"])


@router.get("/",
            response_model=list[Product],
            operation_id="list_products",
            )
async def get_products(session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return await crud.get_products(session=session)


@router.post("/",
             response_model=Product,
             status_code=status.HTTP_201_CREATED,
             operation_id="create_product",
             )
async def create_product(
        product_in: ProductCreate,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return await crud.create_product(
        session=session,
        product_in=product_in)


@router.get("/{product_id}/",
            response_model=Product,
            operation_id="get_product",
            )
async def get_product(product: Product = Depends(product_by_id)):
    return product


@router.put("/{product_id}/", operation_id="update_product")
async def update_product(
        product_update: ProductUpdate,
        product: Product = Depends(product_by_id),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return await crud.update_product(
        session=session,
        product=product,
        product_update=product_update)


@router.patch("/{product_id}/", operation_id="partial_update_product")
async def update_product_partial(
        product_update: ProductUpdatePartial,
        product: Product = Depends(product_by_id),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return await crud.update_product(
        session=session,
        product=product,
        product_update=product_update,
        partial=True)


@router.delete("/{product_id}/",
               status_code=status.HTTP_204_NO_CONTENT,
               operation_id="delete_product")
async def delete_product(
        product: Product = Depends(product_by_id),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)) -> None:
    await crud.delete_product(
        session=session,
        product=product)
