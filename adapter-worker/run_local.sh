#!/bin/bash

export DHOS_KNIFEWRENCH_API_HOST=localhost
export RABBITMQ_HOST=localhost
export RABBITMQ_USERNAME=user
export RABBITMQ_PASSWORD=bitnami

# Logs
export LOG_LEVEL=${LOG_LEVEL:-DEBUG}
export LOG_FORMAT=${LOG_FORMAT:-COLOUR}

python -m dhos_knifewrench_adapter_worker
