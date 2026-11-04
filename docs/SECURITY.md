# Security model

| Risk | Control | Verified by |
|---|---|---|
| Broad ingestion of private/work data | You list the folders; tiers (A own, W work, P personal, R third-party) with only A enabled; credential, app-data and cloud folders refused by the wizard | `sb doctor` (no out-of-scope paths), eval G04 |
| Terminal output | Escape sequences and control characters from indexed files are stripped before printing | — |
| Secrets in the index | Never-open rules for `.env*`, keys, credential files, browser profiles, `.git`, databases, email/chat exports; content scan before indexing (raw bytes and extracted text, so Office/PDF files are covered): high-confidence patterns quarantine the file, low-confidence spans are redacted; values are never logged | `sb quarantine`, doctor `.env` check, eval G03 + system secret test |
| Data leaving the machine | Local mode: Seatbelt denies all non-loopback network, including DNS; the code refuses non-loopback Ollama URLs | doctor: outbound to 1.1.1.1 denied; eval: non-loopback sockets = 0 |
| Writing to your sources | Seatbelt allows writes only in the instance folder | doctor: write to the first source root denied |
| Reading outside scope / via symlinks | Seatbelt denies reads in your home except the listed folders; symlinks are never followed | doctor: home listing denied, out-of-scope fixture denied; system test E23 |
| Launching other programs (e.g. a shell command, `open` on a file or URL) | Seatbelt allows only bash/env/dirname/lsof and the instance's own Python to run, and blocks the macOS service that opens apps and URLs | doctor: launching other programs denied |
| Notes vault | Read-only like every source: Seatbelt denies writes; `vault_init.py` only adds missing files, never overwrites, and refuses to write through a symlinked folder; 15 Personal off by default, client/sales notes switchable; templates/assets never indexed | doctor: vault readable, sandboxed write to vault denied |
| Questions about your own folders ("my Documents folder") | If that folder is not an indexed root, `sb` answers "Not in the second brain." without asking the model, so a note that merely mentions a folder of the same name is not passed off as its contents | eval G07 |
| Prompt injection from indexed files | Sources wrapped as data; the answering LLM has no tools; JSON-constrained output; citations must quote the source (word-level verification); skills are imported as candidates and need human approval | eval G05 (injection fixture) |
| Model tampering | Ollama model digests recorded on first run and compared by every `doctor` | doctor checksum lines |
| Local web UI abuse (CSRF / DNS rebinding) | Bound to 127.0.0.1; Host-header allowlist; per-launch token; no CORS; no external assets | — |
| Second-opinion calls (`sb validate`) | On demand only; shows the excerpt paths and size and asks y/n; secret patterns scrubbed again; Claude Code CLI run with no built-in tools (`--tools ""`), no MCP servers (`--strict-mcp-config` + empty config) and `--permission-mode dontAsk`; Claude's quotes re-verified locally | `logs/validation.jsonl` |
| Debug mode | Off by default. `SB_DEBUG=1` saves the full prompt (excerpts of your files) and raw model replies to `logs/debug/` (mode 0600, included in backups); delete them when done | — |
| Backup / recovery | `sb backup` (tar.gz, newest 7 kept) and `sb restore-test` (hash comparison); the index is rebuildable | restore-test PASS |
| Permissions on disk | umask 077; doctor fails on any group/world-accessible file in the instance | doctor permissions line |

**Hosted backends** (Anthropic/OpenAI) trade privacy for quality: the sandbox then allows HTTPS egress, and retrieved excerpts are sent to the provider. The wizard and the system card say so explicitly.

## Known limitations
These were found in the project's own security assessment and are accepted for now. Each has a planned fix.

| Area | Limitation | Mitigation today |
|---|---|---|
| Platforms | **macOS is the reference platform.** Linux and Windows have **no OS sandbox**: the read/write/network rules are enforced in code only, and `doctor` reports the sandbox checks as FAIL. Windows support is experimental and not yet tested on a real machine | Use macOS for private data; on other systems keep the source folders narrow and the backend local |
| Hosted backends | Seatbelt filters by address and port, not by hostname, so in hosted mode HTTPS to any server is allowed, not only the provider's | Use the local backend for private data |
| Access tokens | The web UI and installer tokens are part of the URL, so they appear in the terminal, browser history and screenshots | Loopback only, Host-header check, a new token at every start; don't share screenshots of the address bar |
| Installer | The installer runs the launcher of any folder that contains `config/secondbrain.json`; installs (npm, pip, brew, winget) are not version-pinned; model digests are trusted on first download | Token-gated, local only; run `doctor --record` only after a pull you started yourself |
| Data at rest | The index, the logs (question text on by default) and the backups are not encrypted (mode 0600) | Turn on FileVault (macOS) or BitLocker (Windows); set `logs.query_log_text` to `false` to log question hashes only |
| Sandbox scope | The macOS profile denies reads and writes in your home folder and on external drives (`/Volumes`), then re-allows only the source folders, the instance and the code. System folders outside those (e.g. `/etc`, `/usr`) stay readable, as programs need them | Keep secrets in your home folder or on encrypted volumes, not in system folders |
| File races | A file swapped for a symlink between the check and the read, or a hard link inside a source folder, could pull in content from outside | Needs write access to a source folder first; symlinks are otherwise never followed |
| Prompt injection | A planted sentence in an indexed file can be quoted with a valid citation: the check proves the quote exists, not that it is true | The answering model has no tools; content is wrapped as data |
