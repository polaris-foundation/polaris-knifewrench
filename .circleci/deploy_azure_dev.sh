#!/usr/bin/env bash

set -eux

source /usr/local/bin/deployment-helpers-v1.sh

# login to AKS
authenticateToAKS

# Loop over the subfolders
for SERVICE_FOLDER in ${SERVICE_FOLDERS}; do
    K8S_DEV_DEPLOYMENT_NAME=${K8S_DEV_DEPLOYMENT_PREFIX}-${SERVICE_FOLDER}-${K8S_DEV_DEPLOYMENT_SUFFIX}
    FULL_PROJECT_NAME=${CIRCLE_PROJECT_REPONAME}-${SERVICE_FOLDER}

    # Iterate through the deployment names (strings delimited by ;) and set image.
    deployFromACR
done
