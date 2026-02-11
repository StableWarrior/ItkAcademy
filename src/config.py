import logging
import os

import structlog

logging.basicConfig(
    format="%(message)s",
    level=logging.INFO,
)


structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.add_log_level,
        structlog.processors.format_exc_info,
        structlog.processors.CallsiteParameterAdder(
            [structlog.processors.CallsiteParameter.PATHNAME]
        ),
        structlog.processors.JSONRenderer(ensure_ascii=False),
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
)


LOGGER = structlog.getLogger()
DATABASE_URL = os.getenv("DATABASE_URL")
X_API_KEY = os.getenv("X_API_KEY")
EVENTS_API_URL = os.getenv("EVENTS_API_URL")
HOSTNAME = os.getenv("HOSTNAME")
PORT = os.getenv("PORT")
