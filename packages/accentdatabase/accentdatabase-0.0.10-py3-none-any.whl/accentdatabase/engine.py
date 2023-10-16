from sqlalchemy.ext.asyncio import create_async_engine

from accentdatabase.config import config

engine = create_async_engine(
    str(config.url),
    json_serializer=config.json_serializer,
    future=config.future,
    echo=config.echo,
)
