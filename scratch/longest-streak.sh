#!/usr/bin/env bash
# Longest consecutive Asia/Calcutta day run with a log/YYYY-MM-DD.md in history.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
mapfile -t days < <(find "$ROOT/log" -maxdepth 1 -type f -name '*.md' -printf '%f\n' | sed 's/\.md$//' | sort)
if [[ ${#days[@]} -eq 0 ]]; then
  echo "longest streak: 0 day(s)"
  exit 0
fi
best=1
cur=1
prev="${days[0]}"
for ((i = 1; i < ${#days[@]}; i++)); do
  day="${days[i]}"
  expect="$(TZ=Asia/Calcutta date -d "${prev} +1 day" +%Y-%m-%d)"
  if [[ "$day" == "$expect" ]]; then
    cur=$((cur + 1))
    if [[ "$cur" -gt "$best" ]]; then
      best=$cur
    fi
  else
    cur=1
  fi
  prev="$day"
done
echo "longest streak: ${best} day(s)"
