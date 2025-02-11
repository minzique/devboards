#!/bin/sh
set -e

# Replace environment variables in Caddyfile
envsubst < /etc/caddy/Caddyfile.template > /etc/caddy/Caddyfile

# Execute CMD
exec "$@"
