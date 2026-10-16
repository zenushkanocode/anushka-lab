# Anushka's house style

The default for every edit. Any other `.md` file in this folder overrides it where they disagree, and whatever
Anushka asks for in the chat overrides both. When she gives a note that applies to every video (not just this one),
add it to "Learned from feedback" at the bottom and commit it.

## Who it's for
Anushka Tyagi, Instagram @zenushkascut. Startup marketing, content and distribution for founders (Reddit, Twitter,
Instagram). Talking-head reels shot on a DJI Osmo Pocket 3, usually against a plain grey wall, often in D-Log M.

## Cutting
- Use the last clean take of every line. Repeated starts inside a take are not allowed: run `tools/find_repeats.py`
  on every EDL before assembling. Whisper merges repeats ("each bot... each bot... each bot has") into one line,
  so never trust a whole-segment transcript for this.
- Zero dead air between lines. Cut in ~0.05s before the first word, out at the silence after the last.
- Alternate wide shots with 1.4x punch-ins cropped from the 4K source. Frame punch-ins on her face, which usually
  sits right of centre in her setup (measure it; she was at cx 0.58, cy 0.50).
- Never clip the end of the CTA. Let the last word finish, keep ~0.3s of room tone, fade audio over 0.2s.

## Captions
- **Three words max on screen at any moment.** Split every line into chunks of 1-3 words that replace each other.
  Never put a full sentence ("knows my personal food preferences") up at once.
- Put text in the empty space. On wide shots that's the wall above her head (y ~300-480 in 1080x1920). On
  punch-ins, a small line at the top (y ~246) and punch words tucked behind her head.
- Names and key nouns go behind the head (cutout on top), sized so at least ~70% of every letter shows.
- Inter Tight 900, lowercase, white with a firm shadow; punch words in butter yellow `#FAE67A` at ~170px.
- Captions say exactly what she said (fix Whisper on names: "Grok bot by SpaceX AI" is correct as spoken).
  No em dashes on screen.
- Everything inside the Reels safe zone: top 220, nothing below y 1470, sides 35, right 100 from y 1155.
- Darken the top of the frame slightly so white text reads on her light grey wall.

## Motion
- The frame is never still: a quick punch on every cut (scale 1.06 → 1 over 0.3s) then a slow push-in across the
  shot (1 → 1.045).
- Signature move, the **slide-and-stack**: on a key line the frame slides right (scale 1.3, x +150) and the words
  stack vertically on the free left side; on the next beat it slides left (x -136) and the words stack on the
  right. Used on "I read 26 books" / "by the end of 2026". Use it once or twice per reel on the strongest lines.

## Sound
- Subtle: soft whooshes when a new idea or character is introduced and on the slides, small pops on punch words.
  Always under the voice (template SFX_GAIN 0.75).
- **Nothing under the CTA.** The CTA voice must be completely clean.

## Colour
- D-Log M footage gets converted and graded; never deliver log unless it's the intentional "before" half of a
  transition.
- Looks on hand (`grades/`):
  - `ghibli`: Megan Tan's Ghibli grade, well-exposed recipe. Creamy wall, peachy natural skin, pastel hair,
    soft contrast, fine 16mm grain.
  - `dreamy`: the "One Day Off" K-drama look. Greener tint, golden sunlit highlights, olive shadows, lifted
    blacks, soft highlight glow (halation 0.42) + grain.
- The **lens switch**: when she covers the camera (a lens, a ring, her hand), stay in log before and switch to the
  grade on the darkest covered frame (`tools/find_switch.py`). Soft click as it touches + light sparkle on reveal.
- Skin must stay natural: if hair or skin goes orange, pull orange saturation, not the whole image.

## Delivery
- Talking-head reels: 9:16 1080x1920. Cinematic / grade clips: keep the source format (often 16:9 4K).
- Always send a phone copy and a full-quality copy under 30 MB (`tools/deliver.sh`). Keep the masters.
- Trim where she says to trim, to the exact frame (e.g. "end when I look sideways" = the first sideways frame).

## Learned from feedback
- v1 of her first reel scored 3/10: too many words on screen, repeats left in, static frame, SFX muddying the CTA.
  v2 fixed all four and is the reference for what "good" looks like.
