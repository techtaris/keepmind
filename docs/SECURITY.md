# Security model

| Risk | Control | Verified by |
|---|---|---|
| Broad ingestion of private/work data | You list the folders; tiers (A own, W work, P personal, R third-party) with only A enabled; credential, app-data and cloud folders refused by the wizard | `sb doctor` (no out-of-scope paths), eval G04 |
| Secrets in the index | Never-open rules for `.env*`, keys, credential files, browser profiles, `.git`, databases, email/chat exports; content scan before indexing: high-confidence patterns quarantine the file, low-confidence spans are redacted; values are never logged | `sb quarantine`, doctor `.env` check, eval G03 + system secret test |
| Data leaving the machine | Local mode: Seatbelt denies all non-loopback network, including DNS; the code refuses non-loopback Ollama URLs | doctor: outbound to 1.1.1.1 denied; eval: non-loopback sockets = 0 |
| Writing to your sources | Seatbelt allows writes only in the instance folder | doctor: write to the first source root denied |
| Reading outside scope / via symlinks | Seatbelt denies reads in your home except the listed folders; symlinks are never followed | doctor: home listing denied, out-of-scope fixture denied; system test E23 |
| Prompt injection from indexed files | Sources wrapped as data; the answering LLM has no tools; JSON-constrained output; citations must quote the source (word-level verification); skills are imported as candidates and need human approval | eval G05 (injection fixture) |
| Model tampering | Ollama model digests recorded on first run and compared by every `doctor` | doctor checksum lines |
| Local web UI abuse (CSRF / DNS rebinding) | Bound to 127.0.0.1; Host-header allowlist; per-launch token; no CORS; no external assets | — |
| Second-opinion calls (`sb validate`) | On demand only; shows the excerpt paths and size and asks y/n; secret patterns scrubbed again; Claude Code CLI run with file, shell and web tools disallowed; Claude's quotes re-verified locally | `logs/validation.jsonl` |
| Backup / recovery | `sb backup` (tar.gz, newest 7 kept) and `sb restore-test` (hash comparison); the index is rebuildable | restore-test PASS |
| Permissions on disk | umask 077; doctor fails on any group/world-accessible file in the instance | doctor permissions line |

**Hosted backends** (Anthropic/OpenAI) trade privacy for quality: the sandbox then allows HTTPS egress, and retrieved excerpts are sent to the provider. The wizard and the system card say so explicitly.
