import aiohttp

from ..config import EVENTS_API_URL, X_API_KEY


class EventsProviderService:
    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            headers={
                "x-api-key": X_API_KEY,
            }
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def get_first_page(self, changed_at: str):
        async with self.session.get(
            f"{EVENTS_API_URL}/api/events/?changed_at={changed_at}"
        ) as response:
            page = await response.json()
        return page

    async def get_page(self, url: str):
        async with self.session.get(url) as response:
            page = await response.json()
        return page
