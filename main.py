from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from src.core.models import db_helper, Base
from src.users.views import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(users_router, tags=["Users"])

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
