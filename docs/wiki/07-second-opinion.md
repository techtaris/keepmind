# Second opinion with Claude (`sb validate`)

[← Wiki home](../README.md) · Code: `validate()` in `src/sb.py`, `bin/sb-validate` · Related: [The Judgment Call](06-judgment-call.md)

An **on-demand** check: was "Not in the second brain" the right call, or did the local model miss an answer that was in its own excerpts?

```bash
<instance>/bin/sb-validate                       # the most recent abstention
<instance>/bin/sb-validate --last 5              # the 5 most recent
<instance>/bin/sb-validate --query "question"    # ask locally first; validate if it abstains or is partial
<instance>/bin/sb-validate --dry-run             # show exactly what would be sent; send nothing
<instance>/bin/sb-validate --yes                 # skip the y/n confirmation
```

## How it works
1. **Select** abstentions from `logs/query.jsonl` (or run `--query` first).
2. **Rebuild** the same top-8 excerpts the local model saw, from the index (≤ 2,500 characters each), and **scrub** secret patterns again.
3. **Show** the question, the excerpt paths and the total size; **ask** y/n.
4. **Send** via the Claude Code CLI with your own login: `claude -p --output-format json --max-turns 1`, with file, shell and web tools disallowed, from an empty working folder.
5. Claude returns `verdict` (`correct_abstention` | `missed_answer` | `partial`), `answer`, `citations`, `missing`, `search_hints`, `notes`.
6. **Verify locally:** Claude's quotes are checked against the excerpts with the same rule as layer 3. A missed/partial verdict without verifiable quotes is marked **UNVERIFIED**.
7. **Record:** `logs/validation.jsonl`, a readable report `eval/validation/<date>.md`, and — for a verified miss — a proposed question in `eval/validation/eval-candidates.json`.

## Boundaries and privacy
- This is the **only** command that runs outside the offline sandbox: the CLI needs the network and its login files. Under `sb-sandboxed` it refuses with guidance.
- `sb` itself reads only the instance's index and logs here; only the question and the shown excerpts are sent — never whole files.
- Requires the Claude Code CLI (`claude`) in `PATH`, or `validation.claude_bin` in config. Optional `validation.model`.

## Turning findings into improvements
Review `eval-candidates.json`, add good items to `eval/questions.json` with `expect_terms`, and re-run `sb eval`. If Claude's `search_hints` point to content that exists but was not retrieved, adjust tiers, exclusions or retrieval settings.
