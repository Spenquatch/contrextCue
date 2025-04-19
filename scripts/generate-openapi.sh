#!/usr/bin/env bash
set -e

# Ensure sidecar spec is up to date
pushd sidecar
uv run start --reload &   # or however you spin it up
PID=$!
sleep 2                    # wait for the server
popd

# Dump the spec
curl http://localhost:8000/api/v1/openapi.json -o docs/openapi.json

# Kill the sidecar
kill $PID

# Generate the TS client
pushd frontend
npx openapi-generator-cli generate \
  -i ../docs/openapi.json \
  -g typescript-axios \
  -o src/api-client \
  --additional-properties=supportsES6=true,withSeparateModelsAndApi=true,apiPackage=api,modelPackage=models
popd
