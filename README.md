# Витамины и их влияние на здоровье человека

Короткий аудиокурс для начинающих: 12 уроков по 2–2,5 минуты, два ведущих, к каждому уроку карточка с идеей, небольшим заданием и правилом. Собран плагином [Claudemy](https://github.com/assafkip/claudemy) для Claude Code по 41 открытому источнику (NHS, ВОЗ, USPSTF, Cochrane, Endocrine Society, российские клинические рекомендации по витамину D, Science-Based Medicine и другие).

Курс образовательный и не заменяет врача. Где совет зависит от ситуации (беременность, лекарства, возраст, диета, курение), это сказано в уроке.

## Что где лежит

- `vitamins/class/NN-*/` уроки: `script.txt` (диалог), `card.md` (карточка), `*.mp3` (аудио)
- `vitamins/class/lesson-plan.md` план курса, споры между источниками и пробелы
- `vitamins/class/playbook.md` правила, которые остаются после курса
- `vitamins/research/` карта тем, заметки чтецов со ссылками и карта согласия источников
- `vitamins/sources.json` список прочитанных страниц
- `render_edge.py` озвучка сценария голосами Microsoft Edge TTS (Светлана и Remy Multilingual)
- `check_ru.py` проверки для русских сценариев поверх проверки плагина

Копии исходных статей (`vitamins/raw/`) в репозиторий не входят: они сохранены только для личного изучения.

## Как переозвучить урок

```
uv venv .venv-tts && uv pip install --python .venv-tts/bin/python edge-tts
.venv-tts/bin/python render_edge.py vitamins/class/01-trinadtsat-nezamenimyh/script.txt vitamins/class/01-trinadtsat-nezamenimyh/trinadtsat-nezamenimyh.mp3
```

Нужен `ffmpeg` и установленный плагин Claudemy (рендерер использует его модуль обработки звука).
