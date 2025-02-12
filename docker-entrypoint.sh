#!/bin/sh
set -e

# Check if template file exists
if [ ! -f /etc/caddy/Caddyfile.template ]; then
    echo "Error: Caddyfile.template not found in /etc/caddy/"
    exit 1
fi

# Check if target directory is writable
if [ ! -w /etc/caddy ]; then
    echo "Error: /etc/caddy is not writable"
    exit 1
fi

# Ensure template file is readable
chmod 644 /etc/caddy/Caddyfile.template

# Process the template file
cat /etc/caddy/Caddyfile.template | envsubst > /etc/caddy/Caddyfile

# Ensure the generated Caddyfile has correct permissions
chmod 644 /etc/caddy/Caddyfile

# Execute the CMD
exec "$@"
