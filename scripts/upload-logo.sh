#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <company-slug> <logo-file>"
    exit 1
fi

COMPANY=$1
LOGO_FILE=$2
CONTAINER_NAME="devboards-logos-1"

# Validate file exists
if [ ! -f "$LOGO_FILE" ]; then
    echo "Error: Logo file not found"
    exit 1
fi

# Extract file extension
EXT="${LOGO_FILE##*.}"

# Copy file to container
docker cp "$LOGO_FILE" "$CONTAINER_NAME:/logos/${COMPANY,,}.$EXT"

echo "Logo uploaded successfully: ${COMPANY,,}.$EXT"
