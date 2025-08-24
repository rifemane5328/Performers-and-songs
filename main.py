from fastapi import FastAPI
from contextlib import asynccontextmanager

from common.settings import Settings
from db.database import Database


@asynccontextmanager
async def lifespan(app: FastAPI):
    database = Database(settings=Settings())
    yield
    await database.dispose(close=False)


app = FastAPI(lifespan=lifespan)
