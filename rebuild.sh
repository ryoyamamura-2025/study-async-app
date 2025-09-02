#!/usr/bin/env bash
set -euo pipefail

IMAGE_NAME="study-async-app"
TAG="dev"
CONTAINER_NAME="${IMAGE_NAME}-container"

echo ">>> Building Docker image ${IMAGE_NAME}:${TAG} ..."
docker buildx build \
  -f Dockerfile.dev \
  -t ${IMAGE_NAME}:${TAG} \
  .

# 古いコンテナがあれば削除
if docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
  echo ">>> Removing old container..."
  docker rm -f ${CONTAINER_NAME}
fi

echo ">>> Starting new container..."
docker run -it \
  --name ${CONTAINER_NAME} \
  -p 3232:8080 \
  -v "$PWD":/workspace \
  -w /workspace/app \
  ${IMAGE_NAME}:${TAG}

