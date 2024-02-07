"""Module for sql query builders."""
import aiosql
from aiosql.queries import Queries as AiosqlQueries
from asyncpg import Connection

from src.url.models.routers import URLID

class Queries:
    """
    SQL query builder.

    Parses file or folder with sql files.
    """

    def __init__(self) -> None:
        self._queries: AiosqlQueries | None = None

    def parse_sql(self, path: str="sql/", driver: str="asyncpg") -> None:
        """
        Parse queries to be run from .sql files.

        :param path: Path to sql file or folder with files. Default: "sql/".
        :param driver: Name of the driver used to connect to db. Default: "asyncpg".
        """
        self._queries = aiosql.from_path(path, driver)

    async def save_url(self, connection: Connection, long_url: str, short_url: URLID) -> None:
        """
        Save url to database.

        :param connection: Connection to db.
        :param long_url: Long url value.
        :param short_url: Short url id.
        """
        if not self._queries:
            self.parse_sql()

        await self._queries.save_url(
            connection,
            long_url=long_url,
            short_url=short_url,
        )

    async def get_url(self, connection: Connection, short_url: URLID) -> str:
        """
        Get long url from db.

        :param connection: Connection to db.
        :param short_url: Short url id.
        :return: Long url matching short url.
        """
        if not self._queries:
            self.parse_sql()

        long_url = await self._queries.get_url(
            connection,
            short_url=short_url,
        )
        return long_url
