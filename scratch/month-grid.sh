#!/usr/bin/env bash
# Print every day of the current Asia/Calcutta month and which have a log.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
year_month="$(TZ=Asia/Calcutta date +%Y-%m)"
days_in_month="$(TZ=Asia/Calcutta date -d "${year_month}-01 +1 month -1 day" +%d)"
echo "month ${year_month} (Asia/Calcutta)"
for d in $(seq -w 1 "$days_in_month"); do
  day="${year_month}-${d}"
  dow="$(TZ=Asia/Calcutta date -d "${day}" +%a)"
  if [[ -f "$ROOT/log/${day}.md" ]]; then
    echo "  [x] ${dow} ${day}"
  else
    echo "  [ ] ${dow} ${day}"
  fi
done
