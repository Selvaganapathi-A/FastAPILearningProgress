from collections.abc import AsyncGenerator
from pathlib import Path
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncEngine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm.decl_api import declarative_base, DeclarativeMeta


_sqlite_file = Path(__file__).parent / 'db.db3'
_sqlite_url = f'sqlite+aiosqlite:///{_sqlite_file}'
_sqlite_connect_args = {
    'check_same_thread': False,
}
#

BASE: DeclarativeMeta = declarative_base()
ASYNCENGINE: AsyncEngine = create_async_engine(
    _sqlite_url, connect_args=_sqlite_connect_args, echo=True
)
SESSIONLOCAL: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=ASYNCENGINE
)


async def createTables():
    global BASE, ASYNCENGINE
    async with ASYNCENGINE.connect() as con:
        await con.run_sync(BASE.metadata.create_all)


async def dropTables():
    global BASE, ASYNCENGINE
    async with ASYNCENGINE.connect() as con:
        await con.run_sync(BASE.metadata.drop_all)


async def session_dependency() -> AsyncGenerator[AsyncSession, None]:
    global SESSIONLOCAL
    session = SESSIONLOCAL()
    try:
        yield session
        await session.commit()
    except Exception as e:
        await session.rollback()
        await session.commit()
        print(e)
    finally:
        await session.aclose()
