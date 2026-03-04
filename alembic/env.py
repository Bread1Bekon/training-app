from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

from config import settings

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
from app.models.base import Base
from app.models.form import Form
from app.models.skill import Skill
from app.models.user import UserDB

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""

    context.configure(
        url=settings.DATABASE_URL.replace("db:6000", "localhost:6000"),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""

    # Get the configuration section
    configuration = config.get_section(config.config_ini_section) or {}

    # Convert async URL to sync URL for Alembic
    if settings.DATABASE_URL.startswith('postgresql+asyncpg://'):
        sync_url = settings.DATABASE_URL.replace('postgresql+asyncpg://', 'postgresql://')
        sync_url = sync_url.replace("db:6000", "localhost:6000")
    elif settings.DATABASE_URL.startswith('postgresql://'):
        sync_url = settings.DATABASE_URL
        sync_url = sync_url.replace("db:6000", "localhost:6000")
    else:
        sync_url = settings.DATABASE_URL
        sync_url = sync_url.DATABASE_URL.replace("db:6000", "localhost:6000")

    # Set the SQLAlchemy URL in configuration
    configuration["sqlalchemy.url"] = sync_url

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()