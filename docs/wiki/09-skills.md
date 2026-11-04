# Skills

[← Wiki home](../README.md) · Code: `skills_import()`, `skills_cmd()` in `src/sb.py`

Turns reusable procedures already in your folders (`SKILL.md`, prompt files, workflow docs) into **reviewed, local** prompts that the local model can run.

```bash
sb-sandboxed skills import            # create candidates from indexed Tier A files
sb-sandboxed skills list              # candidates and approved skills (also skills/SKILLS_INDEX.md)
sb-sandboxed skills show <id>         # read the converted prompt
sb-sandboxed skills approve <id>      # human review → moves to skills/approved/
sb-sandboxed skills run <id> --input task.md --context-query "topic"
```

## Import
- **Which files:** SQL LIKE patterns in `skills.path_patterns` (config). Defaults: `%/SKILL.md`, `%.prompt.md`, `%/prompts/%.md`, `%/workflows/%.md`, `%/.claude/commands/%.md`, `%/.github/prompts/%.md`. Add your own folders. Note: `.claude`, `.codex` and `.cursor` folders are not entered by default (see [Sources & exclusions](03-sources-tiers-exclusions.md)), so skills inside them are imported only after you allow that folder.
- **Dedupe:** by content hash (duplicated agent folders are common). An id clash with a different source gets an 8-character hash suffix.
- **Per skill:** `skill.json` (id, name, description, source path + SHA-256, license, `offline_ok`, `requires_unavailable_tools`, `status: candidate`), `prompt.md` (procedure + `{{input}}` and `{{context}}` slots), `SOURCE.md`.
- **Tool translation:** references to Claude/Codex tools (Bash, WebFetch, MCP, sub-agents, slash commands…) are flagged; such skills are `offline_ok: false` and the prompt tells the operator to do those steps manually or with `sb ask` / `sb query`.

## Safety
Skills are instructions, so imported text is **never** executed or promoted automatically: only `approved` skills can run, and approval is a human action. Context passed to a skill is wrapped as data.
