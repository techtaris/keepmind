# Desktop installer

A small desktop app that runs the Second Brain setup without the terminal. It works like a Tauri app: a backend (here, Python standard library) serves an HTML interface that is shown in a native window (via [pywebview](https://pywebview.flowrl.com/) when installed) or in your browser.

## Start it
| OS | Start | Prerequisite installer |
|---|---|---|
| macOS | double-click `start-ui.command`, or `python3 install/app.py` | `install/install.sh` (Homebrew + npm + Ollama) |
| Windows | double-click `start-ui.bat`, or `py -3 install\app.py` | `install\install.bat` → `install.ps1` (winget + npm + Ollama) |
| Linux | `python3 install/app.py` | install packages with your package manager; `install.sh check` shows status |

Without pywebview the page opens in your default browser. Install it from step 1 for a native window.

## The five steps
1. **Prerequisites.** Shows the status of: Python ≥ 3.10 + SQLite FTS5, Ollama, pulled models, the macOS sandbox, git, Node.js/npm, the Claude Code CLI, the Codex CLI and pywebview. Each **Install** button runs one allow-listed component of the installer script and streams its output, including the exact command.
2. **Source folders.** **Add folder…** opens the native folder dialog. Credential, app-data and cloud-sync folders, your whole home folder and the repo itself are refused. Desktop/Documents/Downloads need a tick to include. Pick the instance folder, which must be outside the repo.
   **Notes vault:** create a new vault (default `~/SecondBrainVault`, folders 00 Home … 15 Personal + 90 Templates), use an existing one (only missing folders and templates are added, nothing is changed), or none. Choose whether client/sales notes and 15 Personal are indexed. See [Notes vault](../docs/wiki/15-notes-vault.md).
3. **Models & agents.** Choose the answer backend: local Ollama (offline), the Claude API or the OpenAI API. Hosted backends take a model id and the *name* of the environment variable with the key, never the key itself. Choose the embedding model (always local) and the optional operator agent: Claude Code CLI or Codex CLI. **Pull these Ollama models** downloads them.
4. **Review & create.** The exact READ / WRITE / NETWORK / NEVER-READ / sandbox / models / operator summary. Tick **I grant these permissions**, then **Create instance**. This runs `setup_wizard.py` non-interactively with your answers.
5. **Run.** Doctor, Ingest, Evaluate, Full pipeline (macOS/Linux), Stats, Vault index, Ask, Open instance folder, Open vault.

## Installer scripts (usable without the UI)
```bash
./install/install.sh check                     # macOS/Linux: status as JSON
./install/install.sh ollama                    # components: python ollama models git node claude codex pywebview all
./install/install.sh models --embed-model nomic-embed-text --chat-model llama3.1:8b   # leave out --chat-model for hosted answers
```
```bat
install\install.bat check
install\install.bat ollama
powershell -ExecutionPolicy Bypass -File install\install.ps1 -Component models -ChatModel llama3.1:8b
```

| Component | macOS (`install.sh`) | Windows (`install.ps1`) |
|---|---|---|
| python | `brew install python@3.12` | `winget install Python.Python.3.12` |
| ollama | `brew install ollama` | `winget install Ollama.Ollama` |
| models | `ollama pull <embed>` + `<chat>` | same |
| git / node | `brew install git` / `node` | `winget install Git.Git` / `OpenJS.NodeJS.LTS` |
| claude | `npm install -g @anthropic-ai/claude-code` | same |
| codex | `npm install -g @openai/codex` | same |
| pywebview | `python3 -m pip install --user pywebview` | `py -3 -m pip install --user pywebview` |

## Security
- **Local only:** the app listens on `127.0.0.1` on a random port, behind a per-launch token and a Host-header check.
- **Fixed dialog titles:** the folder-picker titles are chosen on the server and passed to AppleScript/PowerShell as data, never as code.
- **No free-form shell:** the page can only trigger allow-listed installer components, the setup wizard, and a fixed set of `sb` actions. Model names, environment-variable names and folders are validated on the server.
- **Same rules as the terminal:** folder rules come from `setup_wizard.classify_root`. Nothing is created without the explicit grant.

## Platform notes
- **macOS** is the reference platform. `sb` runs inside the Seatbelt sandbox, and doctor tests it.
- **Windows** is experimental. The desktop app runs Python and `src/sb.py` directly. It never goes through `.cmd` files, because cmd.exe re-parses their arguments. The wizard also writes `bin\sb.cmd` launchers for your own terminal, but there is **no OS sandbox** (doctor reports those checks as FAIL), the bash-only full pipeline is disabled, and the symlink fixture test is skipped without symlink privilege.
