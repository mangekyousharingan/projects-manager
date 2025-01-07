#!/bin/bash

set -e

echo "Waiting for database to be ready..."
while ! nc -z "${POSTGRES_HOST}" "${POSTGRES_PORT}"; do
  sleep 1
done

echo "Applying database migrations..."
alembic upgrade head

echo "Starting the application..."
exec gunicorn src.main:app \
    --worker-class uvicorn.workers.UvicornWorker \
    --workers 4 \
    --bind "${HOST}:${PORT}" \
    --timeout 60
