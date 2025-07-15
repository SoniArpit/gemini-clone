#!/bin/bash
set -e

# Run Alembic migrations
alembic upgrade head

# Start FastAPI server
uvicorn app.main:app --host 0.0.0.0 --port 10000
