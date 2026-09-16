#!/usr/bin/env bash
# Weekday (Mon–Fri) log rate for the current Asia/Calcutta month so far.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
year="$(TZ=Asia/Calcutta date +%Y)"
month="$(TZ=Asia/Calcutta date +%m)"
today="$(TZ=Asia/Calcutta date +%-d)"
prefix="${year}-${month}"
weekdays=0
logged=0
for ((d=1; d<=today; d++)); do
  day="$(printf '%s-%02d' "$prefix" "$d")"
  dow="$(TZ=Asia/Calcutta date -d "${day}" +%u)" # 1=Mon .. 7=Sun
  if [[ "$dow" -le 5 ]]; then
    weekdays=$((weekdays + 1))
    if [[ -f "$ROOT/log/${day}.md" ]]; then
      logged=$((logged + 1))
    fi
  fi
done
if [[ "$weekdays" -eq 0 ]]; then
  echo "weekday rate ${prefix} (Asia/Calcutta): no weekdays yet"
  exit 0
fi
pct=$((logged * 100 / weekdays))
echo "weekday rate ${prefix} (Asia/Calcutta)"
echo "  logged ${logged}/${weekdays} weekdays so far (${pct}%)"