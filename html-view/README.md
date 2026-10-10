# HTML-view

HTML-сайт документации на MkDocs Material. Источник — Markdown репозитория (README, architecture.md, `docs/`, `openspec/changes/`), отдельной копии нет.

- Сайт: https://demoningvi.github.io/agent-architecture/
- Публикуется автоматически при push в `main` ([workflow](../.github/workflows/pages.yml)).

Локально:

```bash
pip install -r html-view/requirements.txt
python html-view/build.py serve   # http://127.0.0.1:8000
python html-view/build.py         # статический сайт в html-view/site
```

Меню строится автоматически: новые задачи в `docs/tasks/` и новые changes в `openspec/changes/` появляются на сайте сами.
