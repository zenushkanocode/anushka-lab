#!/usr/bin/env bash
# Next calendar week (Mon → Sun after this week's Sunday), Asia/Calcutta.
# Companion to week-summary.sh (current) and prev-week.sh (last).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
today_dow="$(TZ=Asia/Calcutta date +%u)" # 1=Mon .. 7=Sun
# Days until next Monday: if today is Sun (7) → 1, else 8 - today_dow
if [[ "$today_dow" -eq 7 ]]; then
  days_to_next_mon=1
else
  days_to_next_mon=$((8 - today_dow))
fi
next_monday="$(TZ=Asia/Calcutta date -d "today +${days_to_next_mon} days" +%Y-%m-%d)"
next_sunday="$(TZ=Asia/Calcutta date -d "${next_monday} +6 days" +%Y-%m-%d)"

echo "next week ${next_monday} → ${next_sunday} (Asia/Calcutta)"
filled=0
for i in 0 1 2 3 4 5 6; do
  day="$(TZ=Asia/Calcutta date -d "${next_monday} +${i} days" +%Y-%m-%d)"
  dow="$(TZ=Asia/Calcutta date -d "${day}" +%a)"
  if [[ -f "$ROOT/log/${day}.md" ]]; then
    echo "  [x] ${dow} ${day}"
    filled=$((filled + 1))
  else
    echo "  [ ] ${dow} ${day}"
  fi
done
echo "  pre-filled ${filled}/7 (should be 0 unless you backfilled ahead)"
