#!/bin/zsh
SCRIPT_DIR="$(cd "$(dirname "$(readlink -f "$0" || echo "$0")")" && pwd)"
python3 "$SCRIPT_DIR/../../src/scp.py" "$@"
