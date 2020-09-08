from datetime import datetime
from typing import List, Union

import aiopg.sa
from sqlalchemy import MetaData, Table, Column, String, DateTime, cast, Date
from sqlalchemy import create_engine, inspect
from sqlalchemy.dialects.postgresql import insert
import sqlalchemy.engine

from reuters_parsing.db import DBBackend
from reuters_parsing.models import News


async def get_one(conn, clause):
    cursor = await conn.execute(clause)
    result = await cursor.fetchone()
    if result is not None:
        result = dict(result)
    return result


async def get_many(conn, clause):
    cursor = await conn.execute(clause)
    records = await cursor.fetchall()
    return list(map(dict, records))


# ===========================================

class PostgresBackend(DBBackend):
    _meta = MetaData()

    _news = Table(
        'news', _meta,

        Column('guid', String(), primary_key=True),
        Column('title', String, nullable=False),
        Column('description', String, nullable=False),
        Column('link', String, nullable=False),
        Column('pub_date', DateTime, nullable=False),
        Column('text', String, nullable=False),
    )

    # -------------------------------------------

    def __init__(self, dsn: str):
        self.dsn = dsn
        self.sync_engine: sqlalchemy.engine.Engine = create_engine(dsn)
        self.engine: Union[aiopg.sa.Engine, None] = None  # async engine

    # -------------------------------------------

    def _is_empty(self):
        return not bool(inspect(self.sync_engine).get_table_names())

    def _create_tables(self):
        self._meta.create_all(bind=self.sync_engine)

    def _drop_tables(self):
        self._meta.drop_all(bind=self.sync_engine)

    # -------------------------------------------

    def ensure_schema(self, force_recreate: bool):
        if force_recreate or self._is_empty():
            if force_recreate:
                self._drop_tables()
            self._create_tables()

    def drop_schema(self):
        self._drop_tables()

    async def init_engine(self):
        self.engine = await aiopg.sa.create_engine(self.dsn)

    async def stop_engine(self):
        self.engine.close()
        await self.engine.wait_closed()

    async def append_news(self, news: List[News]):
        async with self.engine.acquire() as conn:
            for n in news:  # async engine does not support insert multiple items
                await conn.execute(
                    insert(self._news)
                        .values(n._asdict())
                        .on_conflict_do_nothing(index_elements=[self._news.c.guid])
                )

    async def get_news(self, date: datetime) -> List[News]:  # sorted by pubdate
        date = date.date()
        async with self.engine.acquire() as conn:
            result = await get_many(
                conn,
                self._news.select()
                    .where(cast(self._news.c.pub_date, Date) == date)
                    .order_by(self._news.c.pub_date)
            )
        return list(map(lambda i: News(**i), result))
