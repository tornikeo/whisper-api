#!/bin/bash
set -e
docker compose build
docker tag backend_web:latest gcr.io/tornikeo/backend_web
docker push gcr.io/tornikeo/backend_web
gcloud run deploy gcr.io/tornikeo/backend_web