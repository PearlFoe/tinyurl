from src.url.models.routers import URL, URLID


class URLRepositoryMock:
    def __init__(self) -> None:
        self.data: dict[URLID, URL] = {}

    async def save_url(self, url: URL) -> None:
        self.data[url.short] = url

    async def get_url(self, short_url_id: URLID) -> URL:
        return self.data.get(short_url_id)
