#!/usr/bin/env bash
# Print newest log date, age vs Asia/Calcutta today, and whether today is filled.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
today="$(TZ=Asia/Calcutta date +%Y-%m-%d)"
latest="$(ls -1 "$ROOT"/log/*.md 2>/dev/null | xargs -n1 basename | sed 's/\.md$//' | sort | tail -1 || true)"
if [[ -z "${latest}" ]]; then
  echo "latest: none"
  echo "today (${today}): missing"
  exit 1
fi
# age in whole days: today - latest (GNU date)
today_epoch="$(TZ=Asia/Calcutta date -d "$today" +%s)"
latest_epoch="$(TZ=Asia/Calcutta date -d "$latest" +%s)"
age_days=$(( (today_epoch - latest_epoch) / 86400 ))
echo "latest: ${latest} (${age_days} day(s) behind today)"
if [[ -f "$ROOT/log/${today}.md" ]]; then
  echo "today (${today}): filled"
else
  echo "today (${today}): missing"
fi
