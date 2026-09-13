#!/usr/bin/env bash
# Snapshot: first/last log date, total days, live streak ending today (Asia/Calcutta).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
shopt -s nullglob
logs=("$ROOT"/log/[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9].md)
if ((${#logs[@]} == 0)); then
  echo "no logs yet"
  exit 0
fi
# basenames sorted lexicographically = chronological for YYYY-MM-DD
mapfile -t names < <(printf '%s\n' "${logs[@]}" | xargs -n1 basename | sed 's/\.md$//' | sort)
first="${names[0]}"
last="${names[-1]}"
total="${#names[@]}"

day="$(TZ=Asia/Calcutta date +%Y-%m-%d)"
streak=0
while [[ -f "$ROOT/log/${day}.md" ]]; do
  streak=$((streak + 1))
  day="$(TZ=Asia/Calcutta date -d "${day} -1 day" +%Y-%m-%d)"
done

echo "first:  ${first}"
echo "last:   ${last}"
echo "total:  ${total} day(s)"
echo "streak: ${streak} day(s) (ending today, Asia/Calcutta)"
