from datetime import date
from ..database.repository.events_aggregator import EventsAggregatorRepository


class EventsAggregatorService:

    def __init__(self, repository: EventsAggregatorRepository):
        self.repository = repository

    async def get_page(
        self,
        date_from: date = date(2000, 1, 1),
        page: int = 1,
        page_size: int = 10,
    ):
        page = await self.repository.get_events(
            date_from=date_from, page=page, page_size=page_size
        )
        return page

