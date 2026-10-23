"""Render a two-host lesson script to one MP3 with Microsoft Edge neural voices.

Same script format and finish as claudemy's render_audio.py (it reuses that
module's parsing, ffmpeg polish and card stamping); only the voices differ,
since this machine has neither an ElevenLabs key nor macOS `say`.

Each turn is synthesized on its own, with a short pause between turns. The
Edge service drops requests at random ("No audio was received"), so a turn is
retried, and split into sentences if it keeps failing.

Voices: CLAUDEMY_EDGE_A (default ru-RU-SvetlanaNeural), CLAUDEMY_EDGE_B
(default fr-FR-RemyMultilingualNeural, speaking Russian; the learner picked it
from samples). ru-RU-DmitryNeural is not the default: in a test it returned no
audio for 7 of 15 ordinary sentences, and six retries did not fix them.
Rate: CLAUDEMY_EDGE_RATE (default +5%).
Pause between turns: CLAUDEMY_EDGE_GAP seconds (default 0.3).

Usage: <venv>/bin/python render_edge.py <script.txt> <out.mp3>
"""
import asyncio, importlib.util, os, re, subprocess, sys, tempfile, time
from pathlib import Path

import edge_tts

PLUGIN = Path("/home/andrew/.claude/plugins/cache/claudemy/claudemy/0.3.2/skills/claudemy/scripts/render_audio.py")
spec = importlib.util.spec_from_file_location("render_audio", PLUGIN)
ra = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ra)

VOICES = {"A": os.environ.get("CLAUDEMY_EDGE_A", "ru-RU-SvetlanaNeural"),
          "B": os.environ.get("CLAUDEMY_EDGE_B", "fr-FR-RemyMultilingualNeural")}
RATE = os.environ.get("CLAUDEMY_EDGE_RATE", "+5%")
GAP = float(os.environ.get("CLAUDEMY_EDGE_GAP", "0.3"))


def duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                          str(path)], capture_output=True, text=True).stdout.strip()
    return float(out or 0)


def synth_once(text, voice, out):
    asyncio.run(edge_tts.Communicate(text, voice, rate=RATE).save(str(out)))
    # The service sometimes returns a fraction of a second for a whole sentence;
    # Russian speech runs about 15 characters a second, so anything far under is cut off.
    return out.exists() and duration(out) >= len(text) / 40


def synth(text, voice, out, tries=4):
    for i in range(tries):
        try:
            if synth_once(text, voice, out):
                return [out]
        except edge_tts.exceptions.NoAudioReceived:
            pass
        time.sleep(1.5 * (i + 1))
    sentences = [s for s in re.split(r"(?<=[.!?…])\s+", text) if s.strip()]
    if len(sentences) < 2:
        sys.exit(f"Edge TTS gave no audio after {tries} tries: {text[:80]!r}")
    parts = []
    for j, s in enumerate(sentences):
        parts += synth(s, voice, out.with_name(f"{out.stem}_{j}.mp3"), tries)
    return parts


def silence(tmp):
    path = tmp / "gap.mp3"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono",
                    "-t", str(GAP), "-c:a", "libmp3lame", "-b:a", "48k", str(path)], check=True)
    return path


def main(script_path, out_path):
    turns = ra.parse_turns(Path(script_path).read_text())
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        gap, parts = silence(tmp), []
        for i, (who, said) in enumerate(turns):
            clean = re.sub(r"\[[^\]]+\]", "", said).strip()
            if parts:
                parts.append(gap)
            parts += synth(clean, VOICES[who], tmp / f"turn{i:03d}.mp3")
        ra.stitch(parts, tmp, out_path)
    card = Path(script_path).with_name("card.md")
    length = ra.stamp_card(card, out_path)
    # stamp_card's trailing \s*$ also eats the blank line after the Listen line,
    # which glues the next section onto it in rendered markdown; put it back.
    if card.exists():
        card.write_text(re.sub(r"^(\*\*Listen:\*\*.*)\n(?!\n)", r"\1\n\n", card.read_text(), count=1, flags=re.M))
    print(f"wrote {out_path} ({length}) from {len(turns)} turns via Edge TTS")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
