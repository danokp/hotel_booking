from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import settings

if settings.MODE == "TEST":
    DATABASE_URL = settings.TEST_DATABASE_URL
    DATABASE_PARAMS = {"poolclass": NullPool}
else:
    DATABASE_URL = settings.DATABASE_URL
    DATABASE_PARAMS = {}

engine = create_async_engine(DATABASE_URL, **DATABASE_PARAMS)

async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


# NullPool is used for celery tasks
DATABASE_PARAMS_FOR_CELERY_CONNECTION = {"poolclass": NullPool}
engine_nullpool = create_async_engine(
    DATABASE_URL, **DATABASE_PARAMS_FOR_CELERY_CONNECTION
)
async_session_maker_nullpool = sessionmaker(
    engine_nullpool, class_=AsyncSession, expire_on_commit=False
)


class Base(DeclarativeBase):
    pass
