from fastapi import FastAPI
from contextlib import asynccontextmanager

from common.settings import Settings
from db.database import Database
from services.performers.routers.performer import performers_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    database = Database(settings=Settings())
    yield
    await database.dispose(close=False)


app = FastAPI(lifespan=lifespan)

app.include_router(performers_router, tags=['performers'])
