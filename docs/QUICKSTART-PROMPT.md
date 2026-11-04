# Quick-start prompt (checklist)

A short prompt for Claude Code, Codex or a local agent: it checks the prerequisites, installs only what you approve, creates the notes vault where you choose, sets up the second brain and reports a checklist. For the full plan-then-execute version, see [PROMPT.md](PROMPT.md).

Fill in the four lines at the top, then paste everything below the line.

---

```text
Set up my Second Brain with the repository at: <REPO_FOLDER>
Notes vault location (new or existing folder, any drive):   <VAULT_FOLDER>
Other folders to index, read-only (optional):                 <FOLDER_1>, <FOLDER_2>
Answer engine: local Ollama model | Claude API | OpenAI API.   Agent CLI to manage it: none | claude-code | codex

Rules: read only the folders above; never touch credentials, ~/.ssh, ~/.config, app data or cloud-sync folders;
never open .env or key files; ask me before installing anything, downloading models, or using a new path.
Never print secret values. Stop and tell me if something needs a folder I did not list.
Keep your notes, logs and audit files in the instance folder, never in the repository (it is public: no local paths there).

Work through this checklist and mark each line ✅ / ❌ / ⏭ with one line of evidence:

1. Prerequisites: run `install/install.sh check` (macOS/Linux) or `install\install.bat check` (Windows).
   Required: Python ≥ 3.10 with SQLite FTS5, Ollama running on 127.0.0.1:11434.
   Optional: git, Obsidian, Node.js + Claude Code / Codex CLI, pywebview.
2. Install what is missing, one component at a time, after I approve:
   `install/install.sh <python|ollama|git|node|claude|codex|pywebview>` (Windows: `install\install.bat <component>`).
3. Models: check my RAM and suggest a chat model from docs/REQUIREMENTS.md (fast and fits in memory).
   After I approve: `install/install.sh models --embed-model nomic-embed-text --chat-model <model>`
   (leave out `--chat-model` when answers come from the Claude or OpenAI API: only the embedding model is needed).
4. Vault preview: `python3 vault_init.py "<VAULT_FOLDER>" --dry-run`. Show me what would be created
   (00 Home … 15 Personal, 90 Templates); nothing existing is ever changed.
5. Create the instance (config, index, logs) outside the repo, e.g. ~/SecondBrain-Instance:
   run `./setup.sh` (it picks a Python ≥ 3.10 with FTS5; plain `python3` may be an older system Python; on Windows `py -3 setup_wizard.py`) and answer with my choices above (vault = new or existing,
   15 Personal not indexed unless I say so). Show me its permission summary before I accept.
6. Health: `<instance>/bin/sb-sandboxed doctor --record` (Windows: `<instance>\bin\sb.cmd doctor --record`).
   Every line PASS; on Windows/Linux only the sandbox lines may FAIL (no OS sandbox there).
7. Index and test: `sb ingest`, then `sb eval --system`, then one real question with `sb ask "..."`:
   the answer must cite a file, or say "Not in the second brain."
8. Daily use: tell me how to add notes (Obsidian or any editor → `sb ingest`), ask within a folder
   (`sb ask "..." --in decisions,meetings`), and open the local web UI (`sb serve`).
9. If I chose an agent CLI: show me the rule files it got in `<instance>/agent/` and start it from there.

Finish with the checklist table, the instance and vault paths, and anything that still needs me.
```

Tip: the desktop installer (`install/start-ui.command` on macOS, `install\start-ui.bat` on Windows) does steps 1–7 with buttons instead.
