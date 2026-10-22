#!/usr/bin/env bash
set -euo pipefail
DATA_URL="${DATA_URL:-TODO}"
if [ "$DATA_URL" = "TODO" ]; then
  echo "Set DATA_URL before running this script." >&2
  exit 2
fi
curl -L "$DATA_URL" -o data/raw.zip
