#!/usr/bin/env bash
set -euo pipefail
if [ -f /proc/self/cmdline ]; then
  if curl -sf http://localhost:8000/health >/dev/null 2>&1; then
    exit 0
  fi
fi
exit 1
