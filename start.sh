#!/bin/sh
set -eu

python initialize_db.py

exec gunicorn app:app \
  --bind "0.0.0.0:${PORT:-5000}" \
  --workers 1 \
  --timeout 180