#!/bin/sh

# Start all services using supervisor
exec supervisord -c supervisord.conf