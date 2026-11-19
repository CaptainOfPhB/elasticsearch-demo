#!/usr/bin/env bash
# Wipe ES volume and restart (all indices gone)
set -euo pipefail
cd "$(dirname "$0")/.."
docker compose down -v
docker compose up -d
echo "Volumes removed. Cluster restarting from empty state."
