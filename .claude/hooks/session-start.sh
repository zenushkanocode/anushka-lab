#!/bin/bash
# Prepares Anushka's edit studio in Claude Code cloud sessions: the video-edit engine's Python venv
# (faster-whisper, Pillow), sound effects, yt-dlp for references, and a local copy of GSAP for reel builds.
# Idempotent: a second run only checks. Cloud only; on a laptop the skill's own first-run setup handles this.
set -euo pipefail

if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

ROOT="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "$0")/../.." && pwd)}"
VE="$ROOT/.claude/skills/video-edit"
ST="$ROOT/.claude/skills/anushka-edit"

python3 "$VE/scripts/setup.py" | grep -E "STATUS|READY" || true

PY="$VE/.venv/bin/python"
if [ -x "$PY" ] && ! "$PY" -c "import yt_dlp" 2>/dev/null; then
  "$PY" -m pip install -q yt-dlp || echo "yt-dlp install skipped (offline?)"
fi

if [ ! -f "$ST/tools/vendor/gsap.min.js" ]; then
  mkdir -p "$ST/tools/vendor"
  tmp=$(mktemp -d)
  (cd "$tmp" && npm pack -q gsap@3 >/dev/null 2>&1 && tar xzf gsap-*.tgz && cp package/dist/gsap.min.js "$ST/tools/vendor/") \
    || echo "gsap download skipped (offline?)"
  rm -rf "$tmp"
fi

echo "edit studio ready"
