#!/bin/bash
# Entry point: finds a suitable Python (>= 3.10 with SQLite FTS5) and starts the setup wizard.
set -euo pipefail
cd "$(dirname "$0")"
for PY in "${SB_PYTHON:-}" /opt/homebrew/bin/python3.12 /opt/homebrew/bin/python3 /usr/local/bin/python3 python3.12 python3.11 python3.10 python3; do
  [ -n "$PY" ] || continue; command -v "$PY" >/dev/null 2>&1 || continue
  if "$PY" -c 'import sys,sqlite3; assert sys.version_info >= (3,10); sqlite3.connect(":memory:").execute("create virtual table t using fts5(x)")' 2>/dev/null; then
    exec "$PY" -I -B setup_wizard.py "$@"
  fi
done
echo "No Python >= 3.10 with SQLite FTS5 found. Install one (macOS: brew install python@3.12) and re-run, or set SB_PYTHON=/path/to/python3." >&2
exit 1
