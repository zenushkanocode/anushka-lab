#!/usr/bin/env bash
# Current week so far (Mon → today, Asia/Calcutta): fill count, gaps, days left.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
today="$(TZ=Asia/Calcutta date +%Y-%m-%d)"
today_dow="$(TZ=Asia/Calcutta date +%u)" # 1=Mon .. 7=Sun
monday="$(TZ=Asia/Calcutta date -d "today -$((today_dow - 1)) days" +%Y-%m-%d)"
sunday="$(TZ=Asia/Calcutta date -d "${monday} +6 days" +%Y-%m-%d)"

echo "week so far ${monday} → ${today} (week ends ${sunday}, Asia/Calcutta)"
logged=0
through=0
for ((i=0; i<today_dow; i++)); do
  day="$(TZ=Asia/Calcutta date -d "${monday} +${i} days" +%Y-%m-%d)"
  dow="$(TZ=Asia/Calcutta date -d "${day}" +%a)"
  through=$((through + 1))
  if [[ -f "$ROOT/log/${day}.md" ]]; then
    echo "  [x] ${dow} ${day}"
    logged=$((logged + 1))
  else
    echo "  [ ] ${dow} ${day}"
  fi
done
pct=$((logged * 100 / through))
gaps=$((through - logged))
left=$((7 - today_dow))
echo "  filled ${logged}/${through} so far (${pct}%, ${gaps} gap(s))"
echo "  ${left} day(s) left in the week after today"
if [[ "$gaps" -eq 0 ]]; then
  echo "  status: clean through today"
else
  echo "  status: ${gaps} missing day(s) already this week"
fi
