# Overview & components

[← Wiki home](../README.md) · [Interactive diagram](../diagrams/architecture.html)

The second brain is a small set of local programs. It reads folders you choose, builds a private search index, and answers questions **only** from what it finds, citing file paths and lines.

## Components

| Component | What it does | Code |
|---|---|---|
| **Setup wizard** | Asks for your folders, answer backend, operator agent, models and permissions; creates an *instance folder* | `setup.sh`, `setup_wizard.py` |
| **Instance folder** | Your config, sandbox profile, index (`index/brain.sqlite`), logs, generated knowledge, skills, backups. Always **outside** the repo | Created by the wizard |
| **sb engine** | Ingests files, retrieves evidence, makes the [Judgment Call](06-judgment-call.md), runs checks and evaluations | `src/sb.py` (Python standard library only) |
| **sb CLI + web UI** | `sb ask`, `sb query`… and a localhost web page | `bin/sb`, `bin/sb-sandboxed`, `sb serve` |
| **Ollama** | Runs the embedding model (always) and the local chat model (local mode) on `127.0.0.1:11434` | External app |
| **Seatbelt sandbox** | macOS OS-level boundary around `sb`: read only your folders, write only the instance, network loopback-only | `config/seatbelt/secondbrain.sb` (from `templates/seatbelt*.sb`) |
| **Hosted LLM API** *(optional)* | Anthropic or OpenAI as the answer backend; excerpts leave the machine | `answer_backend` in config |
| **sb validate** *(optional)* | Second opinion from Claude Code CLI on "Not in the second brain" answers | `bin/sb-validate` → [page](07-second-opinion.md) |
| **Operator agent** *(optional)* | Claude Code or Codex using the brain through `sb`, under generated rules | `agent/CLAUDE.md` or `agent/AGENTS.md` → [Agent options](../AGENTS.md) |

## Design principles
1. **Local by default.** No data leaves the machine unless you choose a hosted backend or run `sb validate`.
2. **Read-only sources.** Nothing in your folders is ever written, moved or deleted.
3. **Prove or abstain.** An answer must cite verifiable quotes; otherwise the system says "Not in the second brain."
4. **Content is data.** Instructions inside your files never change the system's behaviour.
5. **No personal data in the repo.** Everything personal lives in the instance folder.
6. **Standard library only.** No pip packages, so offline installs are trivial and auditable.

## The life of a question
1. You ask (`sb ask "…"` or the web UI).
2. [Retrieval](05-retrieval.md) finds the 8 most relevant chunks (keyword + semantic).
3. The [Judgment Call](06-judgment-call.md) decides: answer with verified citations, or abstain.
4. The answer is printed with its sources (path, lines, project, modified date) and logged to `logs/query.jsonl`.
5. If it abstained and you want a check, run [`sb validate`](07-second-opinion.md).
