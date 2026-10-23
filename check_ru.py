"""Russian-specific checks on top of claudemy's check_lessons.py.

The plugin checker is tuned for English: its word band (280 to 350) runs 3+
minutes in Russian TTS, and its demand-phrase list is English only. This adds
a 230 to 280 word band, Russian demand phrases, and no Latin letters or long
dashes in scripts (the TTS reads Latin vitamin letters unpredictably, so
scripts spell them out: дэ, бэ двенадцать, цэ).

Usage: python3 check_ru.py <lesson-folder> [...]   Exit 1 on any failure.
"""
import re, sys
from pathlib import Path

DEMAND = re.compile(r"\b((ты|вы) должн\w*|(тебе|вам) (нужно|надо|следует|необходимо)|обязательно|не забудь\w*|непременно)\b", re.I)
failed = 0
for d in map(Path, sys.argv[1:]):
    text = (d / "script.txt").read_text(encoding="utf-8")
    spoken = re.sub(r"^[AB]: ", "", text, flags=re.M)
    words = len(spoken.split())
    problems = [] if 230 <= words <= 280 else [f"{words} words, want 230 to 280"]
    problems += [f"demand phrase {m.group(0)!r}" for m in DEMAND.finditer(spoken)]
    problems += [f"Latin letters {sorted(set(re.findall(r'[A-Za-z]+', spoken)))}"] if re.search(r"[A-Za-z]", spoken) else []
    problems += ["long dash"] if re.search(r"[—–]", spoken) else []
    card = (d / "card.md").read_text(encoding="utf-8")
    problems += [f"card: demand phrase {m.group(0)!r}" for m in DEMAND.finditer(card)]
    print(f"{'FAIL' if problems else 'ok  '} {d.name} ({words} words)")
    for p in problems:
        print(f"     {p}")
    failed += bool(problems)
sys.exit(1 if failed else 0)
