# HTML-view

HTML-сайт документации на MkDocs Material. Источник — Markdown репозитория (README, architecture.md, `docs/`, `openspec/changes/`), отдельной копии нет.

- Сайт: https://demoningvi.github.io/agent-architecture/
- Публикуется автоматически при push в `main` ([workflow](../.github/workflows/pages.yml)).

Локально (Windows) — двойной клик по [serve.cmd](serve.cmd): при первом запуске создаёт `html-view/.venv` и ставит MkDocs, затем открывает http://127.0.0.1:8000. Правки в `.md` появляются на странице сами. Остановить — Ctrl+C в окне.

Вручную:

```bash
python -m venv html-view/.venv
html-view/.venv/Scripts/python -m pip install -r html-view/requirements.txt
html-view/.venv/Scripts/python html-view/build.py serve   # http://127.0.0.1:8000
html-view/.venv/Scripts/python html-view/build.py         # статический сайт в html-view/site
```

Сайт разделён на вкладки по типу документации: **Архитектура** (карта и блочная схема каждого компонента), **Спеки**, **Задачи**, **Справка**. Внизу страницы компонента — панель перехода к его спекам и задачам.

Меню строится автоматически: новые задачи в `docs/tasks/` и новые changes в `openspec/changes/` появляются на сайте сами. Данные сайта (компоненты, блоки, модели, таблицы, эндпоинты, интеграции, истории) — YAML по единице в [`data/`](../data/), модули `*.py` только загружают их ([yamldata.py](yamldata.py); правило — [data-methodology](../docs/rules/data-methodology.md#yaml)). Проверка — `./tools/doc yaml-check`, карточка единицы — `./tools/doc unit <ID>`.
