from datetime import datetime
from .events_provider import EventsProviderService


class EventsPaginatorService:
    def __init__(
            self,
            service: EventsProviderService
    ):
        self.service = service
        self.current_events = []
        self.next_page = ""
        self.previous_page = ""
        self._changed_at = "2000-01-01"

    async def get_changed_at(self):
        return self._changed_at

    async def set_changed_at(self, value):
        try:
            dt = datetime.fromisoformat(value)
        except ValueError:
            dt = datetime.strptime(value, "%Y-%m-%d")

        self._changed_at = dt.strftime("%Y-%m-%d")

    def __aiter__(self):
        return self

    async def __anext__(self):
        async with self.service as session:
            if self.next_page:
                response = await session.get_page(url=self.next_page)
            elif self.next_page is None:
                raise StopAsyncIteration
            else:
                response = await session.get_first_page(
                    changed_at=await self.get_changed_at()
                )

        self.next_page = response["next"]
        self.previous_page = response["previous"]
        self.current_events = response["results"]
        return self.current_events
