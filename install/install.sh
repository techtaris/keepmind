#!/bin/bash
# Second Brain prerequisites for macOS (Homebrew) and Linux (manual hints).
# Usage: ./install.sh [check|python|ollama|models|git|node|claude|codex|pywebview|all] [--chat-model M] [--embed-model M]
set -euo pipefail
COMP="${1:-check}"; shift || true
CHAT="llama3.1:8b"; EMBED="nomic-embed-text"
while [ $# -gt 0 ]; do case "$1" in --chat-model) CHAT="$2"; shift 2;; --embed-model) EMBED="$2"; shift 2;; *) shift;; esac; done
run() { echo ">> $*"; "$@"; }
has() { command -v "$1" >/dev/null 2>&1; }
OS="$(uname -s)"
need_brew() { [ "$OS" = "Darwin" ] || { echo "Automatic install is macOS-only; on Linux use your package manager."; exit 2; }
  has brew || { echo "Homebrew is required: see https://brew.sh (the installer asks for your password)."; exit 2; }; }
find_py() { for p in /opt/homebrew/bin/python3.12 /opt/homebrew/bin/python3 /usr/local/bin/python3 python3.12 python3; do
  has "$p" || [ -x "$p" ] || continue
  if "$p" -c 'import sys,sqlite3; assert sys.version_info>=(3,10); sqlite3.connect(":memory:").execute("create virtual table t using fts5(x)")' 2>/dev/null; then echo "$p"; return; fi; done; }
status() {
  local py ol pys; py="$(find_py || true)"; pys="missing"; [ -n "$py" ] && pys="ok ($py)"; ol="$(curl -s --noproxy '*' --max-time 3 http://127.0.0.1:11434/api/version 2>/dev/null || true)"
  printf '{\n "python": "%s",\n "ollama": "%s",\n "git": "%s",\n "node": "%s",\n "claude": "%s",\n "codex": "%s",\n "sandbox": "%s"\n}\n' \
    "$pys" "$( [ -n "$ol" ] && echo "ok $ol" || (has ollama && echo 'installed, not running' || echo missing) )" \
    "$(has git && echo ok || echo 'missing (optional)')" "$(has npm && echo ok || echo 'missing (needed for claude/codex CLIs)')" \
    "$(has claude && echo ok || echo 'missing (optional)')" "$(has codex && echo ok || echo 'missing (optional)')" \
    "$( [ -x /usr/bin/sandbox-exec ] && echo 'ok (Seatbelt)' || echo 'not available on this OS')"
}
case "$COMP" in
  check)     status ;;
  python)    need_brew; run brew install python@3.12 ;;
  ollama)    need_brew; run brew install ollama; echo "Start it with: brew services start ollama  (or open the Ollama app)" ;;
  git)       need_brew; run brew install git ;;
  node)      need_brew; run brew install node ;;
  models)    has ollama || { echo "Install Ollama first."; exit 2; }; run ollama pull "$EMBED"; [ -n "$CHAT" ] && run ollama pull "$CHAT" ;;
  claude)    has npm || { echo "Install Node.js first (./install.sh node)."; exit 2; }; run npm install -g @anthropic-ai/claude-code ;;
  codex)     has npm || { echo "Install Node.js first (./install.sh node)."; exit 2; }; run npm install -g @openai/codex ;;
  pywebview) PY="$(find_py)"; [ -n "$PY" ] || { echo "Install Python first."; exit 2; }; run "$PY" -m pip install --user pywebview ;;
  all)       need_brew; run brew install python@3.12 ollama git; echo "Next: brew services start ollama && ./install.sh models" ;;
  *)         echo "unknown component: $COMP"; exit 2 ;;
esac
