from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from core.config import settings
from core.models import Base, db_helper
from src.products.views import router as products_router
from src.users.views import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router=products_router, prefix="/products", tags=["Products"])
app.include_router(router=users_router, prefix="/users", tags=["Users"])


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
