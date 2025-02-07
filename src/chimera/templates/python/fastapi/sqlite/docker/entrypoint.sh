#!/bin/sh
set -e

# Run migrations
poetry run alembic upgrade head

# Start FastAPI
exec poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload