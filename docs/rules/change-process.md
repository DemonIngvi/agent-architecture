# Процесс изменения документации

← [Правила документации](README.md)

## Шаги

1. **Определить тип** каждого затрагиваемого документа ([типы](doc-types.md)).
2. **Определить роль** для шага ([роли](roles.md)) и взять её промпт ([промпты](prompts.md)).
3. **Внести изменение** по правилам типа.
4. **Синхронизировать связанные документы** по матрице ниже.
5. **Проверить:**
   - `openspec validate <change> --strict` для затронутых changes;
   - для спек — [критерии полноты](spec-criteria.md);
   - `python html-view/build.py` — сайт собирается, ссылки ведут на существующие страницы.
6. **Отчитаться** пользователю: список изменённых файлов и что в каждом.
7. **Коммит** с описанием; публикация — push в `main`.

## Матрица синхронизации

Изменили слева → проверить справа.

| Изменение | Проверить и при необходимости обновить |
|---|---|
| Новое решение / смена технологии | R&D → design (D-номер) → architecture.md («Обоснование») → спека (Purpose) → rationale.py (RATIONALE, REFS) → subcomponents.py |
| Новое требование в спеке | задача (Приёмка, ссылка на требование) → flows (данные) → конфигурация компонента |
| Новая задача | docs/tasks → ROADMAP (строка и итоги) → TASKS → tasks.md change → components.py (tids) |
| Новый параметр конфигурации | rationale.py (config) → subcomponents.py (params) → спека (сценарий S9) → architecture.md при необходимости |
| Новый блок на схеме компонента | components.py (BLOCKS) → subcomponents.py (SUB) |
| Новый тип данных | flows → спека (сценарии) → IO в components.py |
| Новый компонент | README → architecture.md → components.py (COMPONENTS, BLOCKS, ABOUT, IO) → rationale.py → flows → спека → R&D |
| Новый тип документа | docs/rules/doc-types.md → html-view/build.py (навигация) |
