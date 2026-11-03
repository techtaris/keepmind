# Requirements

## Required

| Tool | Version | Why | Install (macOS) |
|---|---|---|---|
| Python | ≥ 3.10 with SQLite **FTS5** | Runs `sb` and the wizard (standard library only, no pip packages) | `brew install python@3.12` (Apple's `/usr/bin/python3` also works if it is ≥ 3.10) |
| Ollama | recent | Local embeddings in every mode; local chat in `ollama` mode. Must listen on `127.0.0.1:11434` | ollama.com, then `ollama pull nomic-embed-text` and a chat model |
| `sandbox-exec` | built into macOS | OS-enforced read/write/network boundary | — |
| `lsof`, `curl` | built into macOS | `doctor` checks, setup checks | — |

## Optional

| Tool | When | Notes |
|---|---|---|
| git | Versioning this repo | — |
| Claude Code (`claude`) | Operator agent = `claude-code`, or `sb validate` second opinions | The wizard writes `agent/CLAUDE.md` + `agent/.claude/settings.json` |
| Codex CLI (`codex`) | Operator agent = `codex` | The wizard writes `agent/AGENTS.md` + `codex-config.example.toml` |
| Anthropic / OpenAI API key | Hosted answer backend | Exported in your shell; the wizard stores only the variable **name** |

## Hardware guidance (local mode)

| Unified memory | Suggested local chat model |
|---|---|
| 8 GB | 3–4B (e.g. `llama3.2:3b`, `gemma3:4b`) |
| 16 GB | 7–8B (e.g. `llama3.1:8b`, `qwen3:8b`) |
| 24–32 GB | 12–14B (e.g. `gemma4:12b`, `qwen3:14b`) |

Plan for ~0.3 GB for the embedding model and < 1 GB of index per ~10k files. Linux works without the OS sandbox: `doctor` reports it as FAIL.
