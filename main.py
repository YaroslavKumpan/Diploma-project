from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI


from src.products.views import router as products_router
from src.users.views import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI):

    yield



app = FastAPI(
    title="Telegram Bots Marketplace",
    description="API for managing Telegram bots and other products",
    version="1.0.0",
    openapi_tags=[
        {"name": "Products", "description": "Operations with products"},
        {"name": "Users", "description": "Operations with users"}
    ],
    lifespan=lifespan
)


app.include_router(router=products_router, prefix="/products", tags=["Products"])
app.include_router(router=users_router, prefix="/users", tags=["Users"])

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
