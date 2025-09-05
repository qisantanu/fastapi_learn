#!/bin/bash

# Start Redis server (if not running)
redis-server --daemonize yes

# Start Celery worker in background
celery -A celery_app worker --loglevel=info &

# Start Celery beat scheduler
celery -A celery_app beat --loglevel=info
