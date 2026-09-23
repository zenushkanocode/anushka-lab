#!/usr/bin/env bash
# Remaining weekdays this month after today (Asia/Calcutta) — month closeout checklist.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
year="$(TZ=Asia/Calcutta date +%Y)"
month="$(TZ=Asia/Calcutta date +%m)"
today="$(TZ=Asia/Calcutta date +%-d)"
last="$(TZ=Asia/Calcutta date -d "${year}-${month}-01 +1 month -1 day" +%-d)"
prefix="${year}-${month}"

echo "month remaining ${prefix} (Asia/Calcutta, after day ${today})"
left=0
for ((d=today + 1; d<=last; d++)); do
  day="$(printf '%s-%02d' "$prefix" "$d")"
  dow="$(TZ=Asia/Calcutta date -d "${day}" +%u)" # 1=Mon .. 7=Sun
  if [[ "$dow" -gt 5 ]]; then
    continue
  fi
  left=$((left + 1))
  name="$(TZ=Asia/Calcutta date -d "${day}" +%a)"
  if [[ -f "$ROOT/log/${day}.md" ]]; then
    echo "  [x] ${name} ${day}"
  else
    echo "  [ ] ${name} ${day}"
  fi
done

if [[ "$left" -eq 0 ]]; then
  echo "  no weekdays left after today — month closeout is today or done"
else
  echo "  ${left} weekday(s) still to ship before ${prefix} ends"
fi
