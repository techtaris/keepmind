# Desktop installer

[← Wiki home](../README.md) · Code: `install/app.py`, `install/ui/index.html`, `install/install.sh`, `install/install.ps1`, `install/install.bat`

A point-and-click alternative to `./setup.sh`, built Tauri-style: a Python backend serves one HTML page to a native window (pywebview) or to your browser. See [install/README.md](../../install/README.md) for start-up commands, the full component table and platform notes.

| Step | What you do | What runs |
|---|---|---|
| 1 Prerequisites | Check status; click **Install** per component | `install.sh <component>` or `install.ps1 -Component <component>` |
| 2 Source folders | **Add folder…** (native dialog) per vault; choose the instance folder | `setup_wizard.classify_root` (refuses unsafe folders) |
| 3 Models & agents | Local Ollama / Claude API / OpenAI API; embedding model; Claude Code or Codex operator | `install … models` to pull models |
| 4 Review & create | Read the permission summary, grant, create | `setup_wizard.py` with `SB_NONINTERACTIVE=1` and your answers |
| 5 Run | Doctor, Ingest, Evaluate, Full pipeline, Stats, Ask | `<instance>/bin/sb-sandboxed …` (Windows: `bin\sb.cmd …`) |

Security: binds to 127.0.0.1 with a per-launch token, a Host-header check and allow-listed actions only; nothing is installed or created without a click.
