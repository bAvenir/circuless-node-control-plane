#!/bin/sh

# Exit on error
set -e

echo "Running database migrations..."
cd /code/migrations
alembic upgrade head

echo "Starting FastAPI application..."
cd /code
exec fastapi run src/main.py --port 3000
