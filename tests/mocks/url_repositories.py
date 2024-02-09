from src.url.models.routers import URL, URLID


class URLRepositoryMock:
    def __init__(self) -> None:
        self.data: dict[URLID, URL] = {}

    async def save_url(self, url: URL) -> None:
        self.data[url.short] = url

    async def get_url(self, short_url_id: URLID) -> URL:
        return self.data.get(short_url_id)


class URLCacheRepositoryMock:
    def __init__(self) -> None:
        self.data: dict[str, dict[str, URL | float]] = {}

    async def save_url(self, url: URL, ttl: float = -1) -> None:
        self.data[url.short] = {"value": URL, "ttl": ttl}

    async def get_url(self, short_url_id: URLID) -> URL | None:
        return self.data.get(short_url_id, {}).get("value")
