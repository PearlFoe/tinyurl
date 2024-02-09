from src.url.url_handlers import URLHandler
from src.url.models.routers import URL, ShortenUrlRequest

# TODO: test db errors processing

class TestURLHandler:
    async def test_save_url(
            self,
            monkeypatch,
            url_handler: URLHandler,
            shoten_url_request: ShortenUrlRequest,
            url: URL,
        ):
        with monkeypatch.context() as context:
            context.setattr(
                "src.url.models.routers.random.choices",
                lambda _, k: list(url.short)
            )

            await url_handler.save_url(shoten_url_request)

            assert url.short in url_handler._db.data

    async def test_save_url__new_url_id_generates(
            self,
            url_handler: URLHandler,
            shoten_url_request: ShortenUrlRequest,
        ):
        url1 = await url_handler.save_url(shoten_url_request)
        url2 = await url_handler.save_url(shoten_url_request)

        assert url1.short != url2.short

    async def test_get_url(
            self,
            url_handler: URLHandler,
            url: URL,
        ):
        url_handler._db.data[url.short] = url
        saved_url = await url_handler.get_url(url.short)
        assert saved_url == url

    async def test_get_url__url_doesnt_exist(
            self,
            url_handler: URLHandler,
            url: URL,
        ):
        saved_url = await url_handler.get_url(url.short)
        assert saved_url is None
