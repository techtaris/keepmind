# Retrieval

[← Wiki home](../README.md) · Code: `retrieve()`, `_retrieve_ml()`, `_retrieve()`, `fts_query()` in `src/sb.py`

## Hybrid search
1. **Keywords (BM25):** stop-words are removed and the remaining terms are OR-ed into an FTS5 query over chunk text, headings and path tokens (camelCase/snake_case split). Top 40.
2. **Meaning (vectors):** the question is embedded (`search_query:` prefix) and compared by cosine similarity with every chunk vector. Top 40. Brute force is fast enough for tens of thousands of chunks.
3. **Fusion:** Reciprocal Rank Fusion (k = 60) merges both lists.
4. **Diversity:** at most 3 chunks per file; top 8 overall, within a ~5,000-token context budget.

Settings: `retrieval` in `config/secondbrain.json` (`bm25_k`, `vec_k`, `rrf_k`, `top_n`, `per_file_max`, `context_token_budget`, `min_vec_cos`).

## Spanish questions
If a question looks Spanish (accents/¿¡ or common Spanish words), the local chat model translates it to English, both versions are searched, and the results are fused. This compensates for an English-centred embedding model while keeping everything local.

## Questions about the system itself
Questions like "what model is this agent using?", "which LLM are you running?" or "¿qué modelo usa este segundo cerebro?" match `SELF_RX`. For these, the [system card](08-knowledge.md#system-card) is always placed first in the results, so it is not outranked by notes that merely talk about agents or models.

## Inspecting retrieval
```bash
sb-sandboxed query "terms"    # shows scores, paths and line ranges — no LLM call
```
