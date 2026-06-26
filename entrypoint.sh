#!/bin/sh

echo "Waiting for database..."
sleep 5


echo "Running migrations..."

alembic upgrade head



echo "Starting FastAPI..."


exec "$@"