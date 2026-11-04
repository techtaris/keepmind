# Runbook

`SB=<instance>/bin/sb-sandboxed` (always use the sandboxed launcher).

| Task | Command |
|---|---|
| Ask with sources | `$SB ask "question"` (`--json` for machine-readable output) |
| Search only | `$SB query "terms"` |
| Web UI | `$SB serve`, then open the printed `http://127.0.0.1:8765/?t=…` link |
| Pick up changes | `$SB ingest` (incremental, idempotent); `--full` to re-parse everything |
| Health + security | `$SB doctor` (every line should PASS); first time: `doctor --record` |
| Notes vault | Write notes in the vault with Obsidian or any editor, then `$SB ingest`. Ask within folders: `$SB ask "…" --in decisions,meetings`. Vault index: `$SB knowledge vault`. Add missing folders/templates: `python3 vault_init.py <vault> --dry-run` (run outside the sandbox) |
| Maps & system card | `$SB knowledge map` · `$SB knowledge system` · `$SB knowledge cards --limit 3` (then `$SB ingest`) |
| Evaluation | `$SB eval --system` → `<instance>/eval/results/<date>.md` |
| Quarantined files | `$SB quarantine` (path + rule + line, never values) |
| Skills | `$SB skills import` · `list` · `show <id>` · `approve <id>` · `run <id> --input f.md --context-query "..."` |
| Backup / restore check | `$SB backup` · `$SB restore-test` |
| Second opinion on abstentions (Claude, on demand) | `<instance>/bin/sb-validate [--last N] [--dry-run]` (outside the sandbox; asks before sending) |
| Run selected eval questions | `$SB eval --only ID1,ID2` |
| Whole pipeline | `bash <instance>/bin/run-all.sh [--from STEP]` |

## Changing things

| Change | Steps |
|---|---|
| Add or remove a folder | Edit `roots` in `config/secondbrain.json` **and** the read rule in `config/seatbelt/secondbrain.sb` (or re-run `./setup.sh` with a new instance), then `$SB ingest` and `$SB doctor` |
| Vault settings | Edit `vaults` in `config/secondbrain.json` (`include_personal`, `include_clients`, `folder_map`), then `$SB ingest` (only vault notes are re-read) |
| Enable a tier | Add it to `enabled_tiers`, then `$SB ingest` |
| New chat model | `ollama pull <model>`; set `ollama.chat_model`; remove its entry in `models/ollama-models.json`; `$SB doctor --record`; `$SB eval --system` |
| New embedding model | As above for `embed_model`, then delete `index/brain.sqlite` and run `$SB ingest` (full re-embed) |

## Troubleshooting

| Symptom | Check |
|---|---|
| "Not in the second brain." for something indexed | `<instance>/bin/sb-validate --query "…"` for a second opinion; `$SB query "terms"`; `logs/llm.jsonl` (`content_chars` 0 or `done_reason` "length" means a thinking model ran out of budget: keep `ollama.think` false) |
| Doctor network FAIL in local mode | The sandbox profile must not contain `(allow network* (local ip ...))`: that matches every outbound socket |
| Slow answers | Use a smaller chat model, or lower `retrieval.top_n` / `context_token_budget` |
