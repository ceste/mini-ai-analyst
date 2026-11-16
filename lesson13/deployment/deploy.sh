#!/usr/bin/env bash
set -Eeuo pipefail

IMAGE="ghcr.io/ceste/mini-ai-analyst"
VERSION="${1:?Usage: ./deploy.sh <git-commit-sha>}"

CONTAINER="ai-analyst-release"
PORT=8010

NEW_IMAGE="${IMAGE}:${VERSION}"

echo "================================"
echo "Deploying Mini AI Analyst"
echo "Version: ${VERSION}"
echo "================================"

# 1. Download the requested release
# echo "[1/5] Pulling image..."
# docker pull "$NEW_IMAGE"

echo "[1/5] Preparing image..."

if [ "$VERSION" = "broken-test" ]; then
    echo "Using local test image."
    docker image inspect "$NEW_IMAGE" >/dev/null
else
    docker pull "$NEW_IMAGE"
fi

# 2. Remember the currently deployed image
PREVIOUS_IMAGE=""

if docker container inspect "$CONTAINER" >/dev/null 2>&1; then
    PREVIOUS_IMAGE="$(
        docker inspect "$CONTAINER" --format '{{.Image}}'
    )"
fi

# 3. Stop the previous deployment
echo "[2/5] Preparing deployment..."

docker rm -f "$CONTAINER" >/dev/null 2>&1 || true

# 4. Start the requested version
echo "[3/5] Starting container..."

docker run -d \
    --name "$CONTAINER" \
    --read-only \
    --tmpfs /tmp:rw,noexec,nosuid,size=16m \
    --cap-drop ALL \
    --security-opt no-new-privileges:true \
    --pids-limit 100 \
    --memory 256m \
    --cpus 1 \
    -p "127.0.0.1:${PORT}:8000" \
    "$NEW_IMAGE"

# 5. Verify application health
echo "[4/5] Checking health..."

HEALTHY=false

for attempt in $(seq 1 10); do
    if curl --noproxy '*' \
        --fail --silent --show-error \
        --connect-timeout 2 --max-time 3 \
        "http://127.0.0.1:${PORT}/health" \
        2>/dev/null | grep -q '"status":"healthy"'; then

        HEALTHY=true
        break
    fi

    echo "Waiting for application... attempt ${attempt}/10"
    sleep 2
done

if [ "$HEALTHY" = true ]; then
    echo "[5/5] Deployment successful!"
    echo "Running version: ${VERSION}"
    exit 0
fi

echo "Deployment failed health check."
echo "Attempting rollback..."

docker logs --tail 30 "$CONTAINER" || true
docker rm -f "$CONTAINER" >/dev/null 2>&1 || true

if [ -n "$PREVIOUS_IMAGE" ]; then
    echo "Restoring previous image: ${PREVIOUS_IMAGE}"

    docker run -d \
        --name "$CONTAINER" \
        --read-only \
        --tmpfs /tmp:rw,noexec,nosuid,size=16m \
        --cap-drop ALL \
        --security-opt no-new-privileges:true \
        --pids-limit 100 \
        --memory 256m \
        --cpus 1 \
        -p "127.0.0.1:${PORT}:8000" \
        "$PREVIOUS_IMAGE"

    echo "Previous image restarted. Verifying rollback..."

    ROLLBACK_HEALTHY=false

    for attempt in $(seq 1 10); do
        if curl --noproxy '*' \
            --fail --silent \
            --connect-timeout 2 \
            --max-time 3 \
            "http://127.0.0.1:${PORT}/health" \
            2>/dev/null | grep -q '"status":"healthy"'; then

            ROLLBACK_HEALTHY=true
            break
        fi

        echo "Waiting for rollback... attempt ${attempt}/10"
        sleep 2
    done

    if [ "$ROLLBACK_HEALTHY" = true ]; then
        echo "ROLLBACK SUCCESSFUL"
        echo "Previous healthy release restored."
    else
        echo "CRITICAL: ROLLBACK FAILED"
        docker logs --tail 30 "$CONTAINER" || true
        exit 2
    fi
else
    echo "No previous deployment available for rollback."
fi

exit 1
