#!/usr/bin/env bash
set -euo pipefail

if [ -f ".env" ]; then
  set -a
  source .env
  set +a
fi

REQUIRED_VARS=(TELEGRAM_TOKEN OPENAI_API_KEY)
for var in "${REQUIRED_VARS[@]}"; do
  if [ -z "${!var:-}" ]; then
    echo "Missing required environment variable: $var"
  fi
done

mkdir -p /workspace logs
python -m playwright install --with-deps chromium || true
python -m app.main
