#!/bin/bash

GRAFANA_URL="http://grafana:3000"
USERNAME="admin"
PASSWORD="admin"

# JSON payload for the contact point
payload='{
  "name": "webhook_contact",
  "type": "webhook",
  "settings": {
    "url": "http://magic:6790/alert",
    "httpMethod": "POST",
    "title": "predict drift alert",
    "message": "prediction drift detected"
  }
}'

# Create the contact point with the X-Disable-Provenance header
curl -X POST "${GRAFANA_URL}/api/v1/provisioning/contact-points" \
     -H "Content-Type: application/json" \
     -H "X-Disable-Provenance: true" \
     --user ${USERNAME}:${PASSWORD} \
     -d "${payload}"
