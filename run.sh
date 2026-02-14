#!/bin/sh

set -e

alembic -c src/alembic.ini upgrade head

python -m src.scheduler &
uvicorn src.main:app --host 0.0.0.0 --port 8000 &

wait
