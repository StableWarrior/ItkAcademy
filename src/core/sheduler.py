import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from zoneinfo import ZoneInfo

from .tasks import sync_metadata


async def main():
    scheduler = AsyncIOScheduler(
        timezone=ZoneInfo("Asia/Vladivostok")
    )

    scheduler.add_job(
        sync_metadata,
        CronTrigger(hour=0, minute=0),
        id="sync_metadata",
        replace_existing=True,
        max_instances=1,
        coalesce=True,
    )

    scheduler.start()
    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
