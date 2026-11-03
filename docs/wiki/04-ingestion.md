# Ingestion pipeline

[← Wiki home](../README.md) · [Interactive diagram](../diagrams/ingestion.html) · Code: `ingest()`, `walk()`, `parse()`, `secret_scan()`, `chunk()`, `embed_missing()` in `src/sb.py`

```bash
sb-sandboxed ingest            # incremental (default), embeds new chunks automatically
sb-sandboxed ingest --full     # re-parse everything
sb-sandboxed ingest --no-embed # full-text only (e.g. Ollama not running)
```

## Stages
| Stage | What happens |
|---|---|
| **1. Discover** | `walk()` lists files with `lstat` only. It prunes excluded folders, skips symlinks, applies tiers and [exclusions](03-sources-tiers-exclusions.md), and records the nearest Git repo (by the presence of `.git`, never read) |
| **2. Change check** | Unchanged size + mtime → skipped. Otherwise SHA-256: same hash → metadata update only |
| **3. Parse** | Markdown/text/code as text; notebooks (outputs stripped); HTML (scripts/styles removed); CSV/TSV as schema + 5 sample rows; DOCX/PPTX/XLSX via their XML; PDF via a basic text extractor (scanned PDFs are logged as "unparsed") |
| **4. Secret scan** | Quarantine or redact (see [exclusions](03-sources-tiers-exclusions.md#content-scan-after-parsing-before-indexing)) |
| **5. Chunk** | Markdown/docs: split on H1–H3, packed to ≤ 800 tokens with ~15 % overlap, each chunk prefixed with `project › file › heading`. Code: 100-line windows, 20-line overlap, snapped to blank lines |
| **6. Store** | `chunks` table + FTS5 index (`unicode61 remove_diacritics 2`, so Spanish accents match) in `index/brain.sqlite` |
| **7. Embed** | Chunks without a vector are embedded by Ollama (`search_document:` prefix), normalized, and stored as float32 blobs |
| **8. Tombstone** | Files that vanished, became excluded or whose tier was switched off are marked `deleted` and their chunks removed |

## Metadata kept per chunk
Path, project (`root/first-folder`), Git sub-project, tier, namespace (`main`, `derived`, `eval`), file type, language (en/es heuristic), line range, heading path, content hashes, modified date.

## Properties
- **Idempotent:** a second run with no file changes reports 0 added / 0 changed.
- **Never writes to sources.**
- Every run is logged to `logs/ingest.jsonl` with counts per skip reason.
