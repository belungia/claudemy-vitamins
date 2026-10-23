# Writer notes for this class (approved by the learner on lesson 1)

These override the plugin's writer brief where they differ. Lesson 1 in
`class/01-trinadtsat-nezamenimyh/` is the approved shape: copy it.

- Language: Russian. The hosts speak to the listener as "ты", warm and lively, short turns.
- Hosts: A is Svetlana (female voice), B is Remy (male voice). When a host talks
  about themself in the past tense, A uses feminine forms, B masculine. Avoid
  gendered forms about the listener ("ты ел" no; "что было в тарелке" yes).
- Length: 230 to 280 words of speech (renders at about 2:15 to 2:40). The plugin
  checker's 280 to 350 band is for English; ignore only that one line of its output.
- Scripts have no Latin letters and no long dashes: the TTS reads them badly.
  Spell vitamin letters: а, бэ, бэ шесть, бэ двенадцать, цэ, дэ, е, ка.
  Write numbers and units as words: "четыреста микрограммов", "две тысячи
  международных единиц" (never "МЕ", "мкг", "мг" or digits in a script).
  Prefer short sentences. No audio tags like [laughs].
- No demand words toward the listener: ты должен, тебе нужно/надо/следует,
  обязательно, не забудь. Offer: "попробуй", "можно".
- Cards: headers are bilingual exactly as in lesson 1 (English part first, it is
  what the plugin checker looks for, then " · " and the Russian). Cards may use
  Latin letters (A, D, B12) and digits.
- Cards say "(2 min)" on the Listen line; the render replaces it.
- Health: where advice depends on pregnancy, medications, age, diet or smoking,
  say so; where sources send people to a doctor, say so. Numbers are the
  source's claims.
- Checks (both must pass; the plugin one may only complain about the 280 floor):
  python3 /home/andrew/study/learn/claudemy/check_ru.py <lesson-folder>
  python3 /home/andrew/.claude/plugins/cache/claudemy/claudemy/0.3.2/skills/claudemy/scripts/check_lessons.py /home/andrew/study/learn/claudemy/vitamins <lesson-folder>
