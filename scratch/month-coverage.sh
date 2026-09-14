#!/usr/bin/env bash
# Month coverage for log/ in Asia/Calcutta: days logged vs days elapsed this month.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
year="$(TZ=Asia/Calcutta date +%Y)"
month="$(TZ=Asia/Calcutta date +%m)"
today="$(TZ=Asia/Calcutta date +%-d)"
prefix="${year}-${month}"
logged=0
for ((d=1; d<=today; d++)); do
  day="$(printf '%s-%02d' "$prefix" "$d")"
  if [[ -f "$ROOT/log/${day}.md" ]]; then
    logged=$((logged + 1))
  fi
done
pct=$((logged * 100 / today))
echo "month ${prefix} (Asia/Calcutta)"
echo "  logged ${logged}/${today} days so far (${pct}%)"
