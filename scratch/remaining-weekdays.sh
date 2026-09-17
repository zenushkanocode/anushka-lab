#!/usr/bin/env bash
# Weekdays left vs logged in the current Asia/Calcutta month.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
year="$(TZ=Asia/Calcutta date +%Y)"
month="$(TZ=Asia/Calcutta date +%m)"
today="$(TZ=Asia/Calcutta date +%-d)"
last="$(TZ=Asia/Calcutta date -d "${year}-${month}-01 +1 month -1 day" +%-d)"
prefix="${year}-${month}"
logged=0
remaining=0
for ((d=1; d<=last; d++)); do
  day="$(printf '%s-%02d' "$prefix" "$d")"
  dow="$(TZ=Asia/Calcutta date -d "${day}" +%u)" # 1=Mon .. 7=Sun
  [[ "$dow" -le 5 ]] || continue
  if [[ -f "$ROOT/log/${day}.md" ]]; then
    logged=$((logged + 1))
  elif [[ "$d" -ge "$today" ]]; then
    remaining=$((remaining + 1))
  fi
done
echo "remaining weekdays ${prefix} (Asia/Calcutta)"
echo "  logged ${logged} weekday(s) so far"
echo "  ${remaining} weekday slot(s) still open (from today through month end)"
