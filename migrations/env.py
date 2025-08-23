import asyncio
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from sqlalchemy.engine import URL, Connection
from alembic import context
from pydantic import computed_field
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel

from models import Performer, Album, Song
from common.settings import DatabaseConnectionSettings


class DatabaseMigrationSettings(DatabaseConnectionSettings):
    @computed_field  # type: ignore
    @property
    def url(self) -> URL:
        return self.database.get_url()


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = SQLModel.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    context.configure(
        url=DatabaseMigrationSettings().url.render_as_string(hide_password=False),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    conn_config = DatabaseMigrationSettings()
    engine = create_async_engine(
        url=conn_config.url,
        poolclass=pool.NullPool,
        echo=conn_config.database.debug,
        echo_pool="debug" if conn_config.database.debug else None
    )

    async with engine.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await engine.dispose()


def run_migrations_online():
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
