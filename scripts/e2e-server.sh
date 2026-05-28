#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PORT="${E2E_PORT:-4173}"
TMPDIR="${E2E_TMPDIR:-$(mktemp -d)}"
CONFIG="$TMPDIR/config.yaml"

mkdir -p "$TMPDIR/data"

cat > "$CONFIG" <<EOF
storage_path: $TMPDIR/data
instance_id: e2e-test
host: 127.0.0.1
port: $PORT
EOF

cd "$ROOT/frontend"
npm run build

cd "$ROOT"
exec uv run doggy-dog-diary start --config "$CONFIG"
