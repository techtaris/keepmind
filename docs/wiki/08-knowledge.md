# Knowledge maps, project cards & system card

[← Wiki home](../README.md) · Code: `inventory()`, `knowledge_map()`, `knowledge_cards()`, `knowledge_system()` in `src/sb.py`

Generated Markdown lives in `<instance>/knowledge/` and is indexed in the **derived** namespace (tier D). Answers cite original files first; derived pages are marked `derived` when cited. JSON twins (`project-map.json`, `inventory.json`) are written for tools but never indexed.

| Command | Output | How |
|---|---|---|
| `sb inventory` | `knowledge/maps/inventory.{md,json}` | Metadata only: files that pass all rules, skip counts by reason, files per project |
| `sb knowledge map` | `knowledge/maps/project-map.{md,json}` | Deterministic, no LLM: per project the indexed file count, last modified, Git repositories, stack files (package.json, pyproject.toml…), README first line; plus a **Git repositories by root folder** list |
| `sb knowledge cards [--project P] [--limit N]` | `knowledge/projects/<root>--<project>.md` | The local LLM writes Purpose / Stack / Status / Key decisions / Open items / Key files from the project's README and docs, every bullet citing `[S#]`; front matter has `reviewed: false` until you check it |
| `sb knowledge system` | `knowledge/maps/system-card.md` | Deterministic description of the second brain itself (below) |

Run `sb ingest` afterwards so new pages become searchable.

## System card
A one-page, always-current description of **this** second brain, so questions about the system itself get cited answers (see [Retrieval → questions about the system](05-retrieval.md#questions-about-the-system-itself)):
- chat and embedding models with Ollama digests, parameter size, quantization;
- Ollama version, Python version, answer and retrieval settings, web UI address;
- the security boundary (network, reads, writes, never-indexed list) and the answer backend (local or hosted);
- source roots, enabled tiers, index size, last ingest, last evaluation summary.

`sb doctor` regenerates it on every run.
