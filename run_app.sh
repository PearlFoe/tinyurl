#!/bin/bash
alembic upgrade head  # run migrations
gunicorn "main:get_app()" --chdir src/ --bind 0.0.0.0:8000 --worker-class uvicorn.workers.UvicornWorker