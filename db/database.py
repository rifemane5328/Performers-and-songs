from types import TracebackType
from typing import Optional, Dict, Self, AsyncIterator
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession, async_sessionmaker

from common.settings import Settings


class Database:
    def __init__(self, db_url: Optional[str | URL] = None,
                 engine_args: Optional[Dict] = None,
                 custom_engine: Optional[AsyncEngine] = None,
                 settings: Optional[Settings] = None
                 ):
        engine_args = engine_args or {}

        self._settings = settings or Settings()

        if custom_engine:
            self._engine = custom_engine
        else:
            if not db_url:
                db_url = self._settings.database.get_url()
                if not engine_args:
                    engine_args = dict(
                        echo=self._settings.database.debug
                    )
                self._engine = create_async_engine(db_url, **engine_args)  # type: ignore

            self._session_maker = async_sessionmaker(
                self._engine, class_=AsyncSession, expire_on_commit=False
            )

    @property
    def engine(self) -> AsyncEngine:
        return self._engine

    @property
    def session_maker(self) -> async_sessionmaker:
        return self._session_maker

    async def dispose(self, close: bool = True) -> None:
        await self.engine.dispose(close=close)


class DatabaseSession:
    def __init__(self, commit_on_exit: bool = False, session_maker: Optional[async_sessionmaker] = None):
        self.commit_on_exit = commit_on_exit
        if session_maker is None:
            self._session_maker = Database().session_maker
        else:
            self._session_maker = session_maker
        self._session = None

    @property
    def session(self) -> AsyncSession:
        return self._session

    async def __aenter__(self) -> Self:
        self._session = self._session_maker()  # type: ignore
        return self

    async def __aexit__(self, exc_type: type[BaseException] | None, exc_value: BaseException | None,
                        traceback: TracebackType | None) -> None:
        try:
            if exc_type is not None:
                await self.session.rollback()  # type: ignore
            elif self.commit_on_exit:
                await self.session.commit()  # type: ignore
        finally:
            await self.session.close()


async def get_async_session() -> AsyncIterator[AsyncSession]:
    async with DatabaseSession() as db:
        yield db.session
