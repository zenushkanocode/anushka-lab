# anushka-lab

Anushka's personal lab: daily logs (`log/`), experiments (`scratch/`) and her video edit studio.

## Video editing
Anushka (@zenushkascut) edits her videos by directing Claude. For any video request (a Drive link, "edit this",
"colour grade", notes on a version), use the `anushka-edit` skill in `.claude/skills/anushka-edit/`. It reads her
style files in `.claude/skills/anushka-edit/style/` and drives the `video-edit` engine next to it.

- The session-start hook (`.claude/hooks/session-start.sh`) prepares the engine (~40s on a fresh container).
- Edit projects live in `~/reel-edits/<project>/`, outside the repo. Never commit footage or renders.
- Commit studio improvements (style notes, new looks, tool fixes) so the next session has them.
