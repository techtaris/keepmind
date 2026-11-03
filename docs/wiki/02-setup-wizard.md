# Setup wizard

[← Wiki home](../README.md) · [Interactive diagram](../diagrams/setup-wizard.html) · Code: `setup.sh`, `setup_wizard.py`

`./setup.sh` finds a Python ≥ 3.10 with SQLite FTS5 and starts `setup_wizard.py`. Nothing is created until you confirm the permission summary.

## Steps
| # | Step | Details |
|---|---|---|
| 0 | **Agent & backend** | Answer backend: `ollama` (local, default), `anthropic`, or `openai`. Operator agent: `none`, `claude-code`, `codex` |
| 1 | **Tools check** | Python + FTS5, Ollama on 127.0.0.1:11434, `curl`, `lsof`, `sandbox-exec` (macOS); optional git, `claude`, `codex`. Missing required tools are listed with install hints |
| 2 | **Locations** | Instance folder (refused if inside the repo). Source folders, each validated: must exist, no symlinks, not your whole home, not credential/app-data/cloud folders (`~/.ssh`, `~/.aws`, `~/Library`, `~/.config`, `~/.claude`, `~/.ollama`, …). Desktop/Documents/Downloads need an extra yes |
| 3 | **Models** | Lists installed Ollama models; asks for the embedding model (default `nomic-embed-text`) and local chat model. Hosted: model id + the **name** of the env var holding the API key (the key is never stored) |
| 4 | **Permission summary** | READ / WRITE / NETWORK / NEVER-READ / OS sandbox / operator; you answer yes or no |
| 2b | **Notes vault** | new (default `~/SecondBrainVault`) / existing / none; index 15 Personal? (default no); index client & sales notes? (default yes). The vault is added to the source folders; see [Notes vault](15-notes-vault.md) |
| 5 | **Create instance** | `umask 077`; writes config, Seatbelt profile, launchers, eval questions + fixtures, agent files, `README-INSTANCE.md` |

## What the instance contains
```
<instance>/
  config/   secondbrain.json · source-register.json · exclusions.json · prompts/ · seatbelt/secondbrain.sb · env.sh
  bin/      sb · sb-sandboxed · sb-validate · run-all.sh
  index/    brain.sqlite (main) · eval.sqlite (fixtures)
  knowledge/ 00 Home/ · 06 Projects/ · 11 Decisions/   (generated, indexed as "derived"; opens as an Obsidian vault)
  skills/   candidates/ · approved/
  eval/     questions.json · fixtures/ · results/ · validation/
  logs/  models/  backups/  tmp/  agent/
```

## Non-interactive use
For scripted or agent-driven setup:
```bash
SB_NONINTERACTIVE=1 SB_INSTANCE=~/SecondBrain-Instance SB_ROOTS="$HOME/Code:$HOME/Notes" \
SB_PROVIDER=ollama SB_CHAT_MODEL=llama3.1:8b SB_OPERATOR=none SB_ACCEPT=yes ./setup.sh
```
Other variables: `SB_EMBED_MODEL`, `SB_HOSTED_MODEL`, `SB_API_KEY_ENV`, `SB_ALLOW_SENSITIVE`, `SB_CONTINUE_MISSING`.

## After setup
```bash
<instance>/bin/sb-sandboxed doctor --record   # boundary tests + record model checksums
bash <instance>/bin/run-all.sh                # index, eval, skills, backup — logged to logs/run-all.log
```
