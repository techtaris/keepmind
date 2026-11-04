# keepmind

**Local-first second brain for your notes:** a ready-made Markdown vault (Obsidian or any editor), any LLM or agent CLI, and answers that cite your files or say "Not in the second brain."

A private, searchable "second brain" over folders **you** choose. It answers questions with citations to your own files, or says **"Not in the second brain."**

- **Local by default:** Ollama runs the LLM and the embeddings on `127.0.0.1`, and a macOS sandbox blocks the internet.
- **Optional hosted answers:** Claude (Anthropic API) or OpenAI (the provider behind Codex), with a clear disclosure.
- **Optional operator agent:** Claude Code or Codex can use the brain through the `sb` command, under generated permission rules.
- **Notes vault:** one folder of Markdown notes (Obsidian or any editor) with category folders (00 Home … 15 Personal) and templates; you write, the second brain reads it as knowledge. See [Notes vault](docs/wiki/15-notes-vault.md).
- **Optional second opinion:** `sb validate` asks Claude (your own Claude Code login, on demand) whether a "Not in the second brain" answer was right.

🔒 **Security:** macOS is the reference platform (OS sandbox enforced and tested by `sb doctor`). Linux and Windows run without an OS sandbox; Windows is experimental. See [docs/SECURITY.md](docs/SECURITY.md), including known limitations.

📚 **Documentation wiki:** [docs/README.md](docs/README.md), including [the Judgment Call](docs/wiki/06-judgment-call.md) and interactive [diagrams](docs/README.md#diagrams).
- **No personal data in this repo.** Your configuration, index and logs live in a separate *instance* folder created by the setup wizard.

## Easiest: desktop installer

macOS: double-click `install/start-ui.command`. Windows: double-click `install\start-ui.bat`. It walks you through prerequisites, folder selection, models/agents and permissions. See [install/README.md](install/README.md).

## Quick start (macOS, terminal)

```bash
# 0. Get the code
git clone https://github.com/techtaris/keepmind.git && cd keepmind

# 1. Install the required tools (see docs/REQUIREMENTS.md), then pull two models:
ollama pull nomic-embed-text          # embeddings (always local)
ollama pull llama3.1:8b               # or any local chat model you prefer

# 2. Run the wizard: it asks for your folders, notes vault, backend, operator agent and permissions
./setup.sh

# 3. First run (paths are printed by the wizard)
~/SecondBrain-Instance/bin/sb-sandboxed doctor --record
bash ~/SecondBrain-Instance/bin/run-all.sh
~/SecondBrain-Instance/bin/sb-sandboxed ask "What is project X about?"

# 4. Write notes in ~/SecondBrainVault (Obsidian or any editor), then pick them up:
~/SecondBrain-Instance/bin/sb-sandboxed ingest
```

## What the wizard asks

| Question | Default |
|---|---|
| Answer backend | `ollama` (local). Also `anthropic` or `openai` (hosted) |
| Operator agent | `none`. Also `claude-code` or `codex` (generates `CLAUDE.md` + settings or `AGENTS.md`) |
| Instance folder | `~/SecondBrain-Instance` (must be outside this repo) |
| Source folders | You list them. Credential, app-data and cloud-sync folders are refused; Desktop/Documents/Downloads need confirmation |
| Models | Embedding model + local chat model (or a hosted model id + the *name* of the environment variable holding the API key) |
| Notes vault | `new` = create `~/SecondBrainVault` with folders 00 Home … 15 Personal + 90 Templates and note templates; or use an existing vault; or none |
| Permissions | A summary of READ / WRITE / NETWORK / NEVER-READ / sandbox; nothing is created until you say yes |

## Layout

| Path | Contents |
|---|---|
| `setup.sh`, `setup_wizard.py` | Setup (terminal) |
| `install/` | Desktop installer (`app.py` + `ui/index.html`) and prerequisite scripts (`install.sh`, `install.ps1`, `install.bat`) |
| `vault_init.py`, `templates/vault/` | Notes vault starter: category folders, note templates, Obsidian settings (never overwrites) |
| `src/sb.py` | The engine: ingest, search, ask, serve, doctor, eval, knowledge, skills, backup (Python standard library only) |
| `templates/` | Config, exclusions, sandbox profile, prompts, launchers, eval fixtures, operator-agent files |
| `docs/` | [Wiki home](docs/README.md) · `wiki/` feature pages · `diagrams/` (Archify HTML) · `REQUIREMENTS.md`, `SECURITY.md`, `AGENTS.md`, `RUNBOOK.md` |
| `docs/QUICKSTART-PROMPT.md` | A short checklist prompt: prerequisites, installs, vault creation in the folder you choose, setup, health check |
| `docs/PROMPT.md` | A ready-to-use prompt that has an AI agent plan and set up a second brain with this repo |

## License

[MIT](LICENSE) © 2026 TECHTARIS. Diagrams embed third-party components: see [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

### Local Gemma validation

The answer engine is `gemma4:12b` through Ollama on `127.0.0.1:11434`. No OpenAI account, API key, or credit purchase is needed for Second Brain answers. The old `validate-openai.py` helper is retired and will not prompt for a key.

```bash
# Resume any incomplete embeddings, then validate locally:
/Users/tarisadmin/sandbox/SB-Instance/bin/sb-sandboxed embed
/opt/homebrew/bin/python3.12 -I -B /Users/tarisadmin/sandbox/SB-Instance/bin/validate-local.py
```

The validation helper checks that all chunks have vectors, runs `sb eval --system`, checks the report, and asks which answer model is configured. Initial parsing found 45 unparsed files and quarantined 9 files; see AUDIT.md. Do not start another embed process while the current run is active.

Generated operator files are `/Users/tarisadmin/sandbox/SB-Instance/agent/AGENTS.md` and `codex-config.example.toml`. The example configuration is not automatically applied. Start Codex yourself from that agent folder, as requested. Codex remains a separate hosted operator even though Second Brain answers are local.
