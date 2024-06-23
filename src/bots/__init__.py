from fastapi import APIRouter

from .views import router as bots_router

router = APIRouter()
router.include_router(router=bots_router, prefix="/bots")
