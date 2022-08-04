#!/usr/bin/env bash

set -eux

cd api/dhos_knifewrench_ui

# Add in a .env file to disable a react-scripts check
cat << EOF > .env
SKIP_PREFLIGHT_CHECK=true

EOF

yarn install --frozen-lockfile
yarn run prettier src/**/*.ts* --check
yarn run eslint src/**/*.ts*
yarn run test --watchAll=false
