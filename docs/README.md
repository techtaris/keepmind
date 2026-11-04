# Second Brain — documentation wiki

A local-first, agent-agnostic "second brain": it indexes folders you choose and answers questions with citations to your own files, or says **"Not in the second brain."**

## Start here
| Page | What it covers |
|---|---|
| [Overview & components](wiki/01-overview.md) | What the system is, its parts, and how they connect ([diagram](diagrams/architecture.html)) |
| [Setup wizard](wiki/02-setup-wizard.md) | What `./setup.sh` asks, checks, refuses and writes ([diagram](diagrams/setup-wizard.html)) |
| [Notes vault](wiki/15-notes-vault.md) | One folder of Markdown notes (Obsidian or any editor) with category folders and templates, read as knowledge |
| [Desktop installer](wiki/14-desktop-installer.md) | Point-and-click setup: prerequisites, folder picker, models/agents, create, run |
| [Requirements](REQUIREMENTS.md) | Tools to install, models, hardware guidance |
| [Quick-start prompt (checklist)](QUICKSTART-PROMPT.md) | Short prompt: prerequisites, installs, vault in the folder you choose, setup and health check |
| [Setup prompt for an AI agent](PROMPT.md) | Copy-paste prompt that has Claude Code, Codex or a local agent plan and run the setup |

## How it works
| Page | What it covers |
|---|---|
| [Sources, tiers & exclusions](wiki/03-sources-tiers-exclusions.md) | What can be read, what is never opened, tiers A/W/P/R/X/D |
| [Ingestion pipeline](wiki/04-ingestion.md) | Walk → parse → secret scan → chunk → embed → store ([diagram](diagrams/ingestion.html)) |
| [Retrieval](wiki/05-retrieval.md) | Hybrid BM25 + vectors, RRF, Spanish questions, self-questions |
| [**The Judgment Call**](wiki/06-judgment-call.md) | How each answer is decided: answer with sources, or abstain ([diagram](diagrams/judgment-call.html)) |
| [Second opinion with Claude](wiki/07-second-opinion.md) | `sb validate`: an on-demand check of abstentions |
| [Knowledge maps & system card](wiki/08-knowledge.md) | Project map, project cards, vault index, the system card (laid out as a vault) |
| [Skills](wiki/09-skills.md) | Turning SKILL.md / prompt files into reviewed local procedures |

## Operating it
| Page | What it covers |
|---|---|
| [Interfaces: CLI & web UI](wiki/10-interfaces.md) | Every `sb` command, the localhost web UI |
| [Security model](SECURITY.md) · [Health checks](wiki/11-doctor.md) | Threats and controls; what `sb doctor` verifies |
| [Evaluation](wiki/12-evaluation.md) | Test questions, system tests, metrics, adding your own |
| [Logs, backup & restore](wiki/13-logs-backup.md) | Every log file; backup and restore test |
| [Agent options](AGENTS.md) | Answer backends (local / Claude / OpenAI) and operator agents (Claude Code / Codex) |
| [Runbook](RUNBOOK.md) | Day-to-day commands, changes, troubleshooting |

## Diagrams
Interactive, standalone HTML files made with [Archify](https://github.com/tt-a1i/archify). Open them in a browser; each box links to the source lines it is based on.

| Diagram | Type |
|---|---|
| [Components](diagrams/architecture.html) | Architecture |
| [The Judgment Call](diagrams/judgment-call.html) | Workflow |
| [Ingestion pipeline](diagrams/ingestion.html) | Data flow |
| [Setup wizard](diagrams/setup-wizard.html) | Workflow |

Line references in this wiki and in the diagrams point to `src/sb.py`, `setup_wizard.py` and `templates/` as of the commit that added them; use the function names if lines have moved.
