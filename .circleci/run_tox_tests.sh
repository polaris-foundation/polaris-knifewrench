#!/usr/bin/env bash

set -eux

for SERVICE_FOLDER in ${SERVICE_FOLDERS}; do
    tox -c ${SERVICE_FOLDER} -e py39
done
