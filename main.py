from fastapi import FastAPI
from contextlib import asynccontextmanager

from common.settings import Settings
from db.database import Database
from services.performers.routers.performer import performers_router
from services.albums.routers.album import albums_router
from services.songs.routers.song import songs_router
from services.users.routers.users import users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    database = Database(settings=Settings())
    yield
    await database.dispose(close=False)


app = FastAPI(lifespan=lifespan)

app.include_router(performers_router, tags=['performers, performer, performer_by_id, performer_by_id'])
app.include_router(albums_router, tags=['albums, album, album_by_id, album_by_id'])
app.include_router(songs_router, tags=['songs, song, song_by_id, song_by_id'])
app.include_router(users_router, tags=['users'])
