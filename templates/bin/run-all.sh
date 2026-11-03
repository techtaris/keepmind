#!/bin/bash
# Full pipeline for this instance, fully logged: checks, boundary, ingest, knowledge, eval, skills, backup, doctor.
# Usage: bash <instance>/bin/run-all.sh [--from STEP]
set -u; umask 077
INST="$(cd "$(dirname "$0")/.." && pwd)"; X="$INST/bin/sb-sandboxed"
LOG="$INST/logs/run-all.log"; ST="$INST/logs/run-all-status.jsonl"
FROM=""; [ "${1:-}" = "--from" ] && FROM="${2:-}"; REACHED=0; [ -z "$FROM" ] && REACHED=1
cd "$INST" || exit 1
[ -z "$FROM" ] && : > "$ST"
echo "=== run-all $( [ -n "$FROM" ] && echo "resumed from [$FROM]" || echo started ) $(date '+%F %T %z') ===" | tee -a "$LOG"
step() {
  local id="$1" fatal="$2" desc="$3"; shift 4
  [ "$id" = "$FROM" ] && REACHED=1; [ "$REACHED" = "1" ] || return 0
  local t0=$(date +%s); echo "" | tee -a "$LOG"; echo "##### [$id] $desc" | tee -a "$LOG"
  "$@" 2>&1 | tee -a "$LOG"; local rc=${PIPESTATUS[0]}
  printf '{"step":"%s","desc":"%s","rc":%d,"secs":%d,"ts":"%s"}\n' "$id" "$desc" "$rc" "$(( $(date +%s) - t0 ))" "$(date '+%F %T')" >> "$ST"
  echo "----- [$id] exit $rc" | tee -a "$LOG"
  if [ "$rc" -ne 0 ] && [ "$fatal" = "1" ]; then echo "STOPPED at [$id]" | tee -a "$LOG"; exit 1; fi
}
step B1 1 "Sandbox starts"                         -- "$X" stats
step B2 0 "Doctor + record model digests"          -- "$X" doctor --record
step I1 1 "Eval fixtures ingest"                   -- "$X" ingest --eval
step I2 1 "Inventory (metadata only)"              -- "$X" inventory
step I3 1 "Ingest + embeddings"                    -- "$X" ingest
step I4 0 "Idempotency re-run (expect 0 changes)"  -- "$X" ingest
step I5 0 "Quarantine list (paths + rule only)"    -- "$X" quarantine
step K1 0 "Project map + system card"              -- bash -c "'$X' knowledge map && '$X' knowledge system && '$X' ingest"
step E1 0 "Eval + system tests"                    -- "$X" eval --system
step S1 0 "Skill candidates"                       -- "$X" skills import
step R1 0 "Backup"                                 -- "$X" backup
step R2 0 "Restore test"                           -- "$X" restore-test
step D1 0 "Final doctor"                           -- "$X" doctor
echo "=== run-all finished $(date '+%F %T %z') ===" | tee -a "$LOG"
