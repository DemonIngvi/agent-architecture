---
name: doc-data
description: Изменение интеграций, моделей данных (контрактов JSON), таблиц БД, хранилищ, эндпоинтов API, блоков, компонентов, историй и процессов в репозитории «агент архитектура». Всё это — YAML по единице в data/ — навык говорит, какой файл править и чем проверить.
---

# Изменение данных и интеграций

Источник — YAML по единице в `data/` (файл 1–3 КБ, раскладка — `docs/rules/data-methodology.md#yaml`); `html-view/*.py` только загружают его, страницы генерируются. Сгенерированное и Python-модули данных руками не правим.

| Что меняется | Файл |
|---|---|
| Интерфейс (I-код) | `data/integrations.yaml`: from → to (стрелка = кто вызывает), `data_in_response`, `types`, `also`; строка с I-кодом в `interfaces.md` **всех** спек-участников |
| Модель (контракт JSON) | `data/models/<Имя>.yaml`: `fields` {name, type, required, desc}, `source` {kind, refs, why} (✅ / 📘 / 🧩 и «почему так»), `planned` / `field_src`; пример — `docs/api/README.md` |
| Таблица БД | `data/tables/<имя>.yaml`: `columns`, `policy` (индексы, срок, очистка, миграции); таблицы форка — `python html-view/schema_import.py` |
| Эндпоинт | строка в `docs/api/<компонент>.md`; структура — OpenAPI форка или `data/endpoints/<компонент>.yaml` |
| Блок, компонент, история, процесс | `data/blocks/<компонент>/<slug>.yaml`, `data/components/<slug>.yaml`, `data/stories/<компонент>/<US-ID>.yaml`, `data/processes/<компонент>.yaml` |

Как заполнять (`docs/rules/data-methodology.md#yaml-units`): строка таблицы — словарь в одну строку с именованными полями, ID — в своих полях, не в тексте:

```yaml
io:
- {dir: ←, with: Harness · Context Manager, model: [M3Record], what: запись состояния, via: [I11]}
data:                                         # или строка «нет: <почему>»
- {table: memory_m3, access: read-write, why: состояние задачи}
params:                                       # имя и тип значения — из interfaces.md своей спеки
- {name: m3_max_kb, value: '16'}
failures:
- {when: БД недоступна, then: запись повторяется, fmea: agent-memory, reqs: [R-MEM-12]}
ops:
- {op: контекст запуска, endpoint: GET /context, who: Harness · Context Manager, via: [I11]}
```

Значения ссылок — из каталогов (участники, таблицы, модели, I/R/D-коды, US, задачи, эндпоинты, параметры спеки): не из списка — `yaml-check` назовёт ближайшие. Редактор с расширением YAML подсказывает поля и значения по `data/_schema` (`doctool yaml-schema`). Участника нет в каталоге — `label: <текст>` вместо `with` / `who`.

Шаги (`docs/rules/change-process.md#yaml-path`):

1. `python html-view/doctool.py unit <ID>` — карточка единицы (`I20`, `Run`, `agent_run`, `icplan/task-ui`, `US-ICP-01`, `"GET /context"`) вместо страницы и целого файла.
2. Правка YAML единицы; новый файл → `doctool yaml-fmt <папка>` (внесёт в `_order.yaml`).
3. `doctool yaml-check <файл>` → `doctool lint <компонент>`.
4. После **каждого** файла — `doctool next <файл>`: что перегенерируется и следующий документ; по одному.
5. В конце пути — один раз: `python html-view/build.py` → `doctool check` → коммит.

Правило имён — `naming` в `data/datamodel.yaml` (JSON camelCase как в ICPlan; внешние протоколы и конфигурация — в своём стиле). Решения в сносках — только со ссылкой на существующие D-номер или R-требование: проверь `grep` по design и спекам, не выдумывай параметры. Модели и имена — навык `doc-dual-read`.
