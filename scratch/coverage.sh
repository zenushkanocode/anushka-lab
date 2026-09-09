#!/usr/bin/env bash
# Print Asia/Calcutta month log coverage: filled / days-so-far and percent.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
year_month="$(TZ=Asia/Calcutta date +%Y-%m)"
today_day="$(TZ=Asia/Calcutta date +%d)"
# strip leading zero for arithmetic
today_n=$((10#$today_day))
filled=0
for ((i=1; i<=today_n; i++)); do
  day="$(printf '%s-%02d' "$year_month" "$i")"
  if [[ -f "$ROOT/log/${day}.md" ]]; then
    filled=$((filled + 1))
  fi
done
pct=$((filled * 100 / today_n))
echo "coverage ${year_month}: ${filled}/${today_n} days (${pct}%)"
