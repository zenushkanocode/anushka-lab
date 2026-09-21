#!/usr/bin/env bash
# Last complete Mon–Sun week (Asia/Calcutta): fill count, gaps, percent.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
today_dow="$(TZ=Asia/Calcutta date +%u)" # 1=Mon .. 7=Sun
# Monday of this week, then back 7 days = last week's Monday
this_monday="$(TZ=Asia/Calcutta date -d "today -$((today_dow - 1)) days" +%Y-%m-%d)"
last_monday="$(TZ=Asia/Calcutta date -d "${this_monday} -7 days" +%Y-%m-%d)"
last_sunday="$(TZ=Asia/Calcutta date -d "${last_monday} +6 days" +%Y-%m-%d)"

echo "prev week ${last_monday} → ${last_sunday} (Asia/Calcutta)"
logged=0
for i in 0 1 2 3 4 5 6; do
  day="$(TZ=Asia/Calcutta date -d "${last_monday} +${i} days" +%Y-%m-%d)"
  dow="$(TZ=Asia/Calcutta date -d "${day}" +%a)"
  if [[ -f "$ROOT/log/${day}.md" ]]; then
    echo "  [x] ${dow} ${day}"
    logged=$((logged + 1))
  else
    echo "  [ ] ${dow} ${day}"
  fi
done
pct=$((logged * 100 / 7))
gaps=$((7 - logged))
echo "  filled ${logged}/7 (${pct}%)"
if [[ "$logged" -eq 7 ]]; then
  echo "  status: clean week — no gaps"
elif [[ "$logged" -eq 0 ]]; then
  echo "  status: empty week — nothing logged"
else
  echo "  status: ${gaps} gap(s) last week"
fi
