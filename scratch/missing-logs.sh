#!/usr/bin/env bash
# List Asia/Calcutta dates in the last N days (default 7) that lack log/YYYY-MM-DD.md.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
N="${1:-7}"
missing=0
for ((i=0; i<N; i++)); do
  d="$(TZ=Asia/Calcutta date -d "-${i} days" +%Y-%m-%d)"
  f="$ROOT/log/${d}.md"
  if [[ ! -f "$f" ]]; then
    echo "missing: $d"
    missing=$((missing + 1))
  fi
done
if [[ "$missing" -eq 0 ]]; then
  echo "ok: last ${N} day(s) all present"
fi
exit "$missing"