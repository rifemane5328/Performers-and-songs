from fastapi import FastAPI
from contextlib import asynccontextmanager

from common.settings import Settings
from db.database import Database
from services.performers.routers.performer import performers_router
from services.albums.routers.album import albums_router
from services.songs.routers.song import songs_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    database = Database(settings=Settings())
    yield
    await database.dispose(close=False)


app = FastAPI(lifespan=lifespan)

app.include_router(performers_router, tags=['performers, performer'])
app.include_router(albums_router, tags=['albums, album'])
app.include_router(songs_router, tags=['songs, song'])
