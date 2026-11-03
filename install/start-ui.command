#!/bin/bash
# macOS: double-click to start the Second Brain desktop installer.
cd "$(dirname "$0")"
for p in /opt/homebrew/bin/python3.12 /opt/homebrew/bin/python3 /usr/local/bin/python3 python3; do
  if command -v "$p" >/dev/null 2>&1 || [ -x "$p" ]; then exec "$p" app.py "$@"; fi
done
echo "Python 3 not found: run ./install.sh python"; read -r -p "Press Enter to close"
