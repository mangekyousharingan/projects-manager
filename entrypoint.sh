#!/bin/bash

set -e

echo "Waiting for database to be ready..."
while ! nc -z projects-db 5432; do
  sleep 1
done

#echo "Applying database migrations..."
#alembic upgrade head

echo "Starting the application..."
exec "$@"
