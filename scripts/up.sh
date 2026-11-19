#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
# 首次或 Dockerfile 变更后会构建带 IK 的镜像
docker compose up -d --build
echo "ES  : http://localhost:9200"
echo "Kibana: http://localhost:5601  (Dev Tools → Console)"
echo "Check IK: curl -s 'http://localhost:9200/_cat/plugins?v'"
