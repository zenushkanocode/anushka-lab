#!/usr/bin/env bash
# Asia/Calcutta month pace: weekdays logged so far vs weekdays still ahead.
# Tells you if full weekday coverage for this month is still reachable.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
year="$(TZ=Asia/Calcutta date +%Y)"
month="$(TZ=Asia/Calcutta date +%m)"
today="$(TZ=Asia/Calcutta date +%-d)"
last="$(TZ=Asia/Calcutta date -d "${year}-${month}-01 +1 month -1 day" +%-d)"
prefix="${year}-${month}"

logged=0
past_weekdays=0
ahead=0
for ((d=1; d<=last; d++)); do
  day="$(printf '%s-%02d' "$prefix" "$d")"
  dow="$(TZ=Asia/Calcutta date -d "${day}" +%u)" # 1=Mon .. 7=Sun
  if [[ "$dow" -gt 5 ]]; then
    continue
  fi
  if [[ "$d" -lt "$today" ]]; then
    past_weekdays=$((past_weekdays + 1))
    if [[ -f "$ROOT/log/${day}.md" ]]; then
      logged=$((logged + 1))
    fi
  elif [[ "$d" -eq "$today" ]]; then
    past_weekdays=$((past_weekdays + 1))
    if [[ -f "$ROOT/log/${day}.md" ]]; then
      logged=$((logged + 1))
    fi
  else
    ahead=$((ahead + 1))
  fi
done

gaps=$((past_weekdays - logged))
echo "month pace ${prefix} (Asia/Calcutta)"
echo "  logged ${logged}/${past_weekdays} weekdays through today (${gaps} gap(s))"
echo "  ${ahead} weekday(s) still ahead after today"
if [[ "$gaps" -eq 0 ]]; then
  echo "  status: clean so far — full weekday coverage still reachable"
elif [[ "$gaps" -le "$ahead" ]]; then
  echo "  status: reachable if you keep shipping (and optionally backfill ${gaps})"
else
  echo "  status: full weekday coverage needs backfill — gaps (${gaps}) exceed remaining weekdays (${ahead})"
fi