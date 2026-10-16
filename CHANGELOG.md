# Changelog

- 2026-10-15 — Public release: bot, builder, 80 original SAP-C03 new-topic questions (two banks), architecture diagram.
- 2026-10-15 — `build_csv.py` also parses local `sources/*.docx` sample-question files (private, not shipped).
- 2026-10-15 — Study cards: `build_notes.py` turns a slide-deck PDF into `data/study_notes.csv` (private); the bot posts a random slide topic every `STUDY_EVERY_MIN` minutes (Claude note + redrawn diagram + "Quiz me on this" button to the closest bank question); `/study` command.
- 2026-10-16 — online sources parsed from sources/online/ (open-exam-prep 100, certsafari 35, PatrickWiloak 40, certland 8, blogs): bank 449 → 653.
