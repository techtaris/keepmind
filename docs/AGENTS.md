# Agent options

Two independent choices: **who writes the answers** (backend) and **who operates the brain** (optional operator agent).

## Answer backend

| Backend | Data leaves the machine? | Pros | Cons |
|---|---|---|---|
| `ollama` (default) | **No**: internet blocked by the sandbox | Private, offline, free | Slower; quality depends on model size and RAM |
| `anthropic` (Claude API) | **Yes**: retrieved excerpts of your files go to Anthropic | Strong grounding and writing | Needs an API key; sandbox must allow HTTPS egress |
| `openai` (Codex's provider) | **Yes**: retrieved excerpts go to OpenAI | Strong models | Same as above |

In every mode, **embeddings and the index stay local**. Only the top retrieved excerpts for a question are sent to a hosted backend.

## Operator agent (optional)

The operator is an AI assistant that *uses* the second brain on your behalf: it asks `sb`, reads cited files, and drafts from them.

| Operator | Files the wizard generates in `<instance>/agent/` | Boundary |
|---|---|---|
| `none` | — | You use `sb` / the web UI directly |
| `claude-code` | `CLAUDE.md` (rules), `.claude/settings.json` (allow `sb` commands, read the source folders, deny secrets, curl/wget/rm and web tools, ask before edits) | Claude Code permission rules + the sb sandbox |
| `codex` | `AGENTS.md` (rules), `codex-config.example.toml` (read-only sandbox, on-request approvals) | Codex sandbox + the sb sandbox |

## Second opinion (`sb validate`)

Independent of the backend: an on-demand review of "Not in the second brain" answers by Claude through the Claude Code CLI (your own login). See [wiki/07-second-opinion.md](wiki/07-second-opinion.md).

Anything the operator reads is sent to its provider. The generated rules keep it to `sb` output and cited files.
