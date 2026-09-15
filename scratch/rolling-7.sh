#!/usr/bin/env bash
# Last 7 Asia/Calcutta days: which ones already have a log file.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
echo "rolling 7 (Asia/Calcutta)"
now_s="$(TZ=Asia/Kolkata date +%s)"
for i in 6 5 4 3 2 1 0; do
  day="$(TZ=Asia/Kolkata date -d "@$((now_s - i * 86400))" +%Y-%m-%d)"
  if [[ -f "$ROOT/log/${day}.md" ]]; then
    mark="ok"
  else
    mark="--"
  fi
  echo "  ${day}  ${mark}"
done
