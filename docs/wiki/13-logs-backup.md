# Logs, backup & restore

[← Wiki home](../README.md)

## Logs (`<instance>/logs/`, JSON Lines, rotated at 10 MB × 5)
| File | Contents |
|---|---|
| `ingest.jsonl` | Each run: added / changed / unchanged / deleted / quarantined, skip counts by reason; skipped symlinks; permission denials |
| `quarantine.jsonl` | Path, rule, line, file hash — never the matched value |
| `query.jsonl` | Question (or its hash if `logs.query_log_text` is false), status, retrieved chunk ids, citations, model, latency, abstain reason |
| `llm.jsonl` | Model output size, thinking size, token counts, duration, stop reason; rejected citations |
| `validation.jsonl` | `sb validate` verdicts, verified citations, characters sent |
| `doctor.jsonl` | Every doctor run and backup / restore-test event |
| `errors.jsonl` | Parser, network and other errors |
| `run-all.log`, `run-all-status.jsonl` | Full pipeline output and per-step exit codes |

## Backup & restore
```bash
sb-sandboxed backup         # backups/sb-backup-<timestamp>.tar.gz (newest 7 kept, mode 0600)
sb-sandboxed restore-test   # extract the latest into tmp/restore-test/ and compare file hashes
```
A backup holds config, launchers, agent files, skills, knowledge, eval questions/results/validation, model manifest, logs and instance docs. The **index is not backed up**: it is rebuilt from your sources with `sb ingest --full`. Store copies off-machine according to your own policy; encrypt them if they leave the machine.
