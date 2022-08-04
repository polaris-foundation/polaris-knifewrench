#!/bin/bash
SERVER_PORT=${1-5000}
export SERVER_PORT=${SERVER_PORT}

export PROXY_URL=http://localhost
export HS_KEY=secret
export ENVIRONMENT=DEVELOPMENT
export IGNORE_JWT_VALIDATION=True
export FLASK_APP=dhos_knifewrench_api/autoapp.py

# Postgres
export DATABASE_HOST=localhost
export DATABASE_PORT=5432
export DATABASE_USER=dhos-knifewrench-api
export DATABASE_PASSWORD=dhos-knifewrench-api
export DATABASE_NAME=dhos-knifewrench-api

# Redis
export REDIS_HOST=localhost
export REDIS_PORT=6379
export REDIS_PASSWORD=

# Logs
export LOG_LEVEL=${LOG_LEVEL:-DEBUG}
export LOG_FORMAT=${LOG_FORMAT:-COLOUR}

flask db upgrade

python -m dhos_knifewrench_api
