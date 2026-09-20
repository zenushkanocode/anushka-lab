#!/usr/bin/env bash
# Asia/Calcutta full-month fill: every calendar day logged vs days still ahead.
# Tells you if a perfect month (log every day) is still reachable.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
year="$(TZ=Asia/Calcutta date +%Y)"
month="$(TZ=Asia/Calcutta date +%m)"
today="$(TZ=Asia/Calcutta date +%-d)"
last="$(TZ=Asia/Calcutta date -d "${year}-${month}-01 +1 month -1 day" +%-d)"
prefix="${year}-${month}"

logged=0
through=0
ahead=0
for ((d=1; d<=last; d++)); do
  day="$(printf '%s-%02d' "$prefix" "$d")"
  if [[ "$d" -le "$today" ]]; then
    through=$((through + 1))
    if [[ -f "$ROOT/log/${day}.md" ]]; then
      logged=$((logged + 1))
    fi
  else
    ahead=$((ahead + 1))
  fi
done

gaps=$((through - logged))
echo "month fill ${prefix} (Asia/Calcutta)"
echo "  logged ${logged}/${through} days through today (${gaps} gap(s))"
echo "  ${ahead} day(s) still ahead after today"
if [[ "$gaps" -eq 0 ]]; then
  echo "  status: clean so far — perfect month still reachable"
elif [[ "$gaps" -le "$ahead" ]]; then
  echo "  status: reachable if you keep shipping (and optionally backfill ${gaps})"
else
  echo "  status: perfect month needs backfill — gaps (${gaps}) exceed remaining days (${ahead})"
fi
