#!/usr/bin/env bash
# Count consecutive Asia/Calcutta days missing log/YYYY-MM-DD.md, ending today.
# Prints 0 when today is already filled.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
day="$(TZ=Asia/Calcutta date +%Y-%m-%d)"
gap=0
while [[ ! -f "$ROOT/log/${day}.md" ]]; do
  gap=$((gap + 1))
  day="$(TZ=Asia/Calcutta date -d "${day} -1 day" +%Y-%m-%d)"
  # safety: don't walk forever if log/ is empty
  if [[ "$gap" -gt 3650 ]]; then
    echo "gap: >3650 day(s) (bail)" >&2
    exit 1
  fi
done
echo "gap: ${gap} day(s)"
