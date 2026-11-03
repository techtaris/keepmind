# Second Brain instance

| | |
|---|---|
| Instance (config, index, logs) | `{{INSTANCE}}` |
| Answer backend | `{{PROVIDER}}` |
| Operator agent | `{{OPERATOR}}` |

**Source folders (read-only):**
{{ROOTS}}

**Contents of this instance:** your index, your logs and generated summaries of your files. **Don't commit it or share it.**

```bash
{{SB}} doctor --record      # first run: health, boundary tests, record model digests
bash {{INSTANCE}}/bin/run-all.sh   # index + eval + backup, logged to logs/run-all.log
{{SB}} ask "question"       # answer with sources, or "Not in the second brain."
{{SB}} serve                # local web UI on 127.0.0.1:8765
```
