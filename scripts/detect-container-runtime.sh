#!/bin/bash
#
# Detect Container Runtime (Podman or Docker)
# Returns the command to use: "podman" or "docker"
#

set -e

# Check for Podman first (preferred)
if command -v podman >/dev/null 2>&1; then
    echo "podman"
    exit 0
fi

# Fall back to Docker
if command -v docker >/dev/null 2>&1; then
    echo "docker"
    exit 0
fi

# Neither found
echo "Error: Neither podman nor docker found" >&2
exit 1

