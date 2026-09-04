#!/usr/bin/env bash
# Exit 0 if log/YYYY-MM-DD.md exists for today in Asia/Calcutta; else exit 1.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TODAY="$(TZ=Asia/Calcutta date +%Y-%m-%d)"
LOG="$ROOT/log/${TODAY}.md"
if [[ -f "$LOG" ]]; then
  echo "present: $LOG"
  exit 0
fi
echo "missing: $LOG"
exit 1
