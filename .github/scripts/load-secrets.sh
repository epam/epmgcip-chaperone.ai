#!/bin/bash
set -e

if [[ -z "$ENVIRONMENT" ]]; then
  echo "ENVIRONMENT variable is not set. Exiting."
  exit 1
fi

VARIABLES=("AZURE_CLIENT_ID" "AZURE_CLIENT_SECRET" "AZURE_SUBSCRIPTION_ID" "AZURE_TENANT_ID")

for VAR in "${VARIABLES[@]}"; do
  SECRET_NAME="${ENVIRONMENT}_${VAR}"
  SECRET_VALUE="${!SECRET_NAME}"

  if [[ -z "$SECRET_VALUE" ]]; then
    echo "Missing value for secret: $SECRET_NAME"
    exit 1
  fi

  echo "$VAR=$SECRET_VALUE" >> $GITHUB_ENV
done
