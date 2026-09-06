#!/usr/bin/env bash
# Count consecutive Asia/Calcutta days with a log/YYYY-MM-DD.md, ending today.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
day="$(TZ=Asia/Calcutta date +%Y-%m-%d)"
streak=0
while [[ -f "$ROOT/log/${day}.md" ]]; do
  streak=$((streak + 1))
  day="$(TZ=Asia/Calcutta date -d "${day} -1 day" +%Y-%m-%d)"
done
echo "streak: ${streak} day(s)"
