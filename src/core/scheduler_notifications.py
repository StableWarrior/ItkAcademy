import asyncio
from zoneinfo import ZoneInfo

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from .tasks import sync_notifications


async def main():
    scheduler = AsyncIOScheduler(timezone=ZoneInfo("Asia/Vladivostok"))

    scheduler.add_job(
        sync_notifications,
        CronTrigger(minute="*/1"),
        id="sync_notifications",
        max_instances=1,
        coalesce=True,
    )

    scheduler.start()
    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
