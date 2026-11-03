# Interfaces: CLI & web UI

[← Wiki home](../README.md)

Always use the sandboxed launcher: `SB=<instance>/bin/sb-sandboxed`. The exception is `sb-validate`, which runs outside the sandbox (see [Second opinion](07-second-opinion.md)).

| Command | Purpose |
|---|---|
| `$SB ask "question" [--json] [--eval]` | Grounded answer with sources, or "Not in the second brain." |
| `$SB query "terms" [--eval]` | Retrieval only: scores, paths, lines, snippets |
| `$SB serve` | Web UI on `http://127.0.0.1:8765/?t=<token>` |
| `$SB ingest [--full] [--no-embed] [--eval]` · `$SB embed` | Index / embed |
| `$SB inventory` · `$SB knowledge map\|cards\|system` | [Knowledge](08-knowledge.md) |
| `$SB skills import\|list\|show\|approve\|run` | [Skills](09-skills.md) |
| `$SB doctor [--record]` | [Health and security checks](11-doctor.md) |
| `$SB eval [--system] [--only IDS]` | [Evaluation](12-evaluation.md) |
| `$SB quarantine` · `$SB stats [--eval]` | Quarantined files · index statistics |
| `$SB backup` · `$SB restore-test` | [Backup & restore](13-logs-backup.md) |
| `<instance>/bin/sb-validate [--last N\|--query Q] [--dry-run] [--yes]` | [Second opinion](07-second-opinion.md) |
| `bash <instance>/bin/run-all.sh [--from STEP]` | Whole pipeline, logged |

## Web UI security
- Binds only to `127.0.0.1` (refuses any other host in config).
- Rejects requests whose `Host` header is not `127.0.0.1:<port>` or `localhost:<port>` (DNS-rebinding defence).
- Requires the per-launch random token (URL for the page, `X-SB-Token` header for the API); restarting `serve` rotates it.
- No CORS, a Content-Security-Policy header, no external fonts or scripts; snippets are HTML-escaped.
