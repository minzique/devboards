#!/bin/sh

# Start FastAPI server
uvicorn src.main:app --host 0.0.0.0 --port 8000 &

# Start scraper scheduler
while true
do
  poetry run python -m src.scrapers.main
  sleep $(( ${SCRAPER_SCHEDULE:-60} * 60 ))  # Default to 60 minutes
done