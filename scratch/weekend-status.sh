#!/usr/bin/env bash
# Asia/Calcutta weekend pair (Sat + Sun of this week): logged or still open.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
today_dow="$(TZ=Asia/Calcutta date +%u)" # 1=Mon .. 7=Sun
# Saturday of this week = today - (dow - 6) when dow>=6, else today + (6 - dow)
if [[ "$today_dow" -ge 6 ]]; then
  sat="$(TZ=Asia/Calcutta date -d "today -$((today_dow - 6)) days" +%Y-%m-%d)"
else
  sat="$(TZ=Asia/Calcutta date -d "today +$((6 - today_dow)) days" +%Y-%m-%d)"
fi
sun="$(TZ=Asia/Calcutta date -d "${sat} +1 day" +%Y-%m-%d)"

echo "weekend pair (Asia/Calcutta)"
filled=0
for day in "$sat" "$sun"; do
  dow="$(TZ=Asia/Calcutta date -d "${day}" +%a)"
  if [[ -f "$ROOT/log/${day}.md" ]]; then
    echo "  [x] ${dow} ${day}"
    filled=$((filled + 1))
  else
    echo "  [ ] ${dow} ${day}"
  fi
done
case "$filled" in
  0) echo "  status: both weekend slots still open" ;;
  1) echo "  status: half done — one weekend slot still open" ;;
  2) echo "  status: weekend pair complete" ;;
esac