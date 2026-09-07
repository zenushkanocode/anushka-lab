#!/usr/bin/env bash
# Print Mon–Sun (Asia/Calcutta) for the current week and which days have a log.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
# GNU date: find Monday of this week in Asia/Calcutta
today_dow="$(TZ=Asia/Calcutta date +%u)" # 1=Mon .. 7=Sun
monday="$(TZ=Asia/Calcutta date -d "today -$((today_dow - 1)) days" +%Y-%m-%d)"
echo "week starting ${monday} (Asia/Calcutta)"
for i in 0 1 2 3 4 5 6; do
  day="$(TZ=Asia/Calcutta date -d "${monday} +${i} days" +%Y-%m-%d)"
  dow="$(TZ=Asia/Calcutta date -d "${day}" +%a)"
  if [[ -f "$ROOT/log/${day}.md" ]]; then
    echo "  [x] ${dow} ${day}"
  else
    echo "  [ ] ${dow} ${day}"
  fi
done
