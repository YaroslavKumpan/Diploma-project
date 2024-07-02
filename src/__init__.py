from fastapi import APIRouter

from .products.views import router as products_router
from .users.views import router as users_router

router = APIRouter()
router.include_router(router=products_router, prefix="/products")
router.include_router(router=users_router, prefix="/users")
