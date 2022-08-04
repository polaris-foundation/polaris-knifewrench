#!/usr/bin/env bash

set -eux

for SERVICE_FOLDER in ${SERVICE_FOLDERS}; do
    mkdir -p ${SERVICE_FOLDER}/${COVERAGE_REPORT_DIR}
    tox -c ${SERVICE_FOLDER} -e py39
done
