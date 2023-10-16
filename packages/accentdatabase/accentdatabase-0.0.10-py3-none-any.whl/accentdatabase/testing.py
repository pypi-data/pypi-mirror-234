from copy import deepcopy

from pydantic import PostgresDsn
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine


async def recreate_postgres_database(
    database_url: PostgresDsn,
    maintenance_db: str = "postgres",
):
    """Drop and recreate test database, requires min of postgres v13"""

    maintenance_url = deepcopy(database_url)
    maintenance_url_str = str(maintenance_url).replace(
        maintenance_url.path,
        f"/{maintenance_db}",
    )
    test_db = str(database_url).split("/")[-1]

    engine = create_async_engine(
        maintenance_url_str,
        isolation_level="AUTOCOMMIT",
    )

    async with engine.begin() as conn:
        # drop the test database
        drop = f"DROP DATABASE IF EXISTS {test_db} WITH (FORCE);"
        await conn.execute(text(drop))
        # create the test database
        create = f"CREATE DATABASE {test_db};"
        await conn.execute(text(create))

    # dispose of the engine
    await engine.dispose()
