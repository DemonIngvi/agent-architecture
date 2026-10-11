# Агентная архитектура (v0.7)

Модель C4: **C1** — наша система (Agent Platform) и её связь с ICPlan и внешним миром. **C2** — внутренняя структура платформы.

## C1 — System Context

```
┌──────────────┐               ┌───────────────┐
│ Пользователь │               │ Администратор │
│ ICPlan       │               │ платформы     │
└──────┬───────┘               └───────┬───────┘
       │ задачи                        │ агенты, модели, правила
┌──────▼───────┐ задача, approve ┌─────▼───────┐
│   ICPlan     ├────────────────▶│ Agent       │
│              │◀────────────────┤ Platform    │
└──────────────┘ события,        └──┬───────┬──┘
                 результат          │ LLM   │ tools
                             ┌──────▼───┐ ┌─▼────────────┐
                             │ LLM-     │ │ Внешние      │
                             │ провайд. │ │ системы, MCP │
                             └──────────┘ └──────────────┘
```

Интеграция с ICPlan (Integration API: каталог агентов, runs, approvals, events) — уровень C1, детализация в отдельном разделе.

## C2 — Containers (внутренняя структура)

ICPlan назначает агента на задачу. Agent Runner только исполняет.

Верхний блок **ICPlan** — то, что уже есть в It's a Plan и дорабатывается в нём. Всё ниже — наша платформа. Harness не меняется.

```
┌──────────────────── ICPlan (It's a Plan) ────────────────────┐
│ ┌───────────┐ ┌───────────┐ ┌─────────────┐  ┌─────────────┐ │
│ │ Control   │ │ Registry  │ │ Run Queue   │  │ Task UI     │ │
│ │ Plane UI  ├▶│ агенты,   │ │ + runner API│  │ доска, чат, │ │
│ │ настройки │ │ тулы,MCP  │ │ (внешн.)    │  │ approve, QG │ │
│ └───┬───────┘ └─────┬─────┘ └───┬───▲─────┘  └─────────────┘ │
└─────┼───────────────┼───────────┼───┼────────────────────────┘
      │ доп.настройки │ agent def │   │ стрим, результат
      │             ┌─▼───────────▼───┴──┐
      │             │ Agent Runner [G1]  │
      │             │ допуск, лимиты, $  │
      │             └─────────┬──────────┘
      │                       │ up(agent_def) / run / cleanup
┌─────▼─────┐     ┌───────────▼ Sandbox [G3] ──────────────────┐
│ Platform  ├────▶│ ┌─────────────── Harness ────────────────┐ │       ┌────────────┐
│ мод.ICPlan│     │ │ ┌──────────────┐                       │ │       │ Memory Svc │
│ алиасы LLM│     │ │ │ Context Mgr  │◀──────────────────────┼─┼──────▶│ M1 M2 M3   │
│ бюджеты   │     │ │ └──┬───────▲───┘                       │ │  r/w  │ M4 M5 M6   │
│ sandbox   │     │ │    │prompt │ ответ + результат тула    │ │       │ M0: Harness│
│ память    │     │ │ ┌──▼───────┴───┐        ┌───────────┐  │ │       └────────────┘
│ версии    │     │ │ │ LLM client   ├───────▶│ Tool Exec │  │ │       ┌────────────┐
└─────┬─────┘     │ │ └───────┬──────┘        │ MCP client│◀─┼─┼──────▶│ MCP/Tools  │
      │ правила   │ │         │               └───────────┘  │ │  call └────────────┘
┌─────▼─────┐     │ │         │ [G2] hooks: тулы,память,итог │ │
│ Guardrail ├────▶│ │         │ policy: лимиты шагов, права  │ │
│ Policy    │     │ └─────────┼──────────────────────────────┘ │
│ G1 G2 G3  │     └───────────┼────────────────────────────────┘
│ G4        │                 │ prompt ▼ ▲ ответ
└─────┬─────┘       ┌─────────▼─────────┐
      └────────────▶│ LiteLLM gw   [G4] ├──▶ Observability (трейсы, токены, $)
                    └─────────┬─────────┘
                              ▼
                 Anthropic │ OpenAI │ local
```

## Развёртывание (C4 deployment)

```
Пользователи ──HTTPS──▶ Traefik (k3s ingress, TLS) ──▶ itsaplan-core: web ×1–2 · api ×2 · worker · bot
                                                      itsaplan-agents: Runner · LiteLLM ×2 · OPA ×2 · Memory · egress · запуски
                                                      itsaplan-data: PgBouncer ─▶ PostgreSQL 17 + pgvector (CloudNativePG) · RustFS (S3)
                                                      копии ─▶ S3 вне узла
Узел: k3s, 8 vCPU / 32 ГБ / 400 ГБ (один узел для MVP)
```

| Профиль нагрузки (гипотеза) | Значение |
|---|---|
| Пользователи | 50 зарегистрированных, 15 одновременно |
| API ICPlan | ~20 RPS в пике, p95 < 300 мс |
| Запуски агентов | ~400 в день, пик 30 в час, 4 активных + очередь |
| LiteLLM | 0.4–1 RPS, ~55 тыс. токенов/мин |
| Postgres | ~60 клиентских соединений → PgBouncer ≤ 30 серверных |

Подробно: спека [platform-infrastructure](openspec/changes/define-agent-platform/specs/platform-infrastructure/spec.md) и [схема](openspec/changes/define-agent-platform/specs/platform-infrastructure/architecture.md). Технологии — [сводная таблица](docs/TECHNOLOGIES.md). Обоснование: [R&D: профиль нагрузки](docs/rnd/load-profile.md) · [Kubernetes](docs/rnd/kubernetes-runtime.md) · [ingress](docs/rnd/ingress-and-balancing.md) · [СУБД и хранилища](docs/rnd/data-stores.md) · [design D15, D16](openspec/changes/define-agent-platform/design.md).

## Harness (внутри Sandbox)

Рантайм, который крутит агентский цикл и навязывает агенту все правила. LLM только «думает», всё остальное делает харнес. Границы — на общей схеме выше.

| Часть | Задача |
|---|---|
| Context Manager | Сборка промпта, сжатие истории, память (M0 + подгрузка M1–M6) |
| LLM client | Вызов модели только через LiteLLM |
| Tool Executor | Вызов MCP/тулов, проверка прав |
| Hooks | Точки расширения: плагины, guardrails |
| Policy / Stop | Лимиты и критерий завершения |

Основа: **LangGraph** (решено) за своим интерфейсом harness + свои хуки. Обоснование: [R&D: фреймворк цикла](docs/rnd/harness-framework.md) · [design D2](openspec/changes/define-agent-platform/design.md). Причины: `interrupt` для approve, checkpointer для возобновления, стрим шагов для таймлайна.

## Guardrails

Логика правил (Rego) — в git, данные правил (allowlist, лимиты агента) — в БД ICPlan. Мягкие (G1, G2) → жёсткие (G3, G4). Каждая точка включается отдельно.

| ID | Где | Движок | Основные правила |
|---|---|---|---|
| **G1 Admission** | Agent Runner | OPA | • агент разрешён для этой задачи/инициатора<br>• бюджет токенов/$ на запуск<br>• таймаут, max шагов<br>• лимит параллельных запусков<br>• kill switch агента |
| **G2 Action** | Harness hooks | OPA | • allowlist тулов/MCP для агента<br>• валидация аргументов тула (схема, пути, write-операции)<br>• human approval для опасных действий<br>• фильтр результатов тулов на prompt injection<br>• права на память: кто читает/пишет M1–M6<br>• проверка итогового результата (формат, схема) |
| **G3 Isolation** | Sandbox | профиль контейнера, сеть | • egress только по allowlist доменов<br>• ФС: запись только в workspace<br>• лимиты CPU/RAM/disk<br>• секреты не в env — через прокси<br>• без privileged, без доступа к хосту |
| **G4 LLM** | LiteLLM gateway | хуки LiteLLM | • allowlist моделей для агента<br>• rate limit, лимит токенов/$ на ключ<br>• маскирование PII и секретов во входе<br>• детект jailbreak/injection во входе<br>• модерация ответа<br>• полное логирование запросов |

### Включение и выключение (конфиг деплоя)

```yaml
# deploy/values.yaml — фрагмент
guardrails:
  engine: opa                 # opa | none
  opa_url: http://opa:8181
  g1: { enabled: true,  on_engine_error: deny }    # deny = fail-closed
  g2: { enabled: true,  on_engine_error: deny, approval: true }
  g3: { enabled: true }       # сеть, ФС, ресурсы sandbox
  g4: { enabled: false }      # PII, injection, модерация в LiteLLM
```
Выключенная точка не ломает платформу; при старте пишется «Gx disabled». Обоснование: [R&D: движок guardrails](docs/rnd/guardrails-engine.md) · [design D6](openspec/changes/define-agent-platform/design.md). Спека: [guardrails](openspec/changes/define-agent-platform/specs/guardrails/spec.md).

### Защита от зацикливания и перерасхода

| Правило | Точка | Порог по умолчанию | Действие |
|---|---|---|---|
| Повтор одинакового вызова тула | G2 | 3 подряд | стоп `loop_detected` |
| Нет прогресса (состояние задачи не меняется) | G2 | 8 шагов | стоп `loop_detected` |
| Лимит шагов / времени / простоя | G2 | 30 шагов / 30 мин / 5 мин | стоп `limit` |
| Max output tokens на вызов | G4 | 4 000 | обрезка ответа |
| Бюджет запуска (токены, $) | G2, G4 | 200 000 / 1 $ | стоп `limit` |
| Бюджет агента в сутки | G1, G4 | 5 $ | отказ новых запусков |
| Бюджет проекта и команды в месяц | G1 | задаётся | 80% — предупреждение, 100% — отказ |
| Аномальный расход шага | G2 | 5× медианы | пауза на approve |
| Ошибки подряд (circuit breaker) | G2 | 3 | стоп `failed`, повторы с backoff |
| RPM / TPM на модель и агента | G4 | по провайдеру | ожидание или отказ |
| Kill switch агента / платформы | G1 | — | очередь закрыта, активные — `canceled` |

Все проверки детерминированные (кодом, без LLM). Обоснование: [R&D: защита от перерасхода](docs/rnd/runaway-protection.md). Спека: [guardrails](openspec/changes/define-agent-platform/specs/guardrails/spec.md).

## Очередь и планирование запусков

Очередь — в ICPlan. Agent Runner стартует запуск, только когда свободны все его слоты (вариант B):

```yaml
scheduling:
  mode: parallel            # sequential — вся платформа строго по одному
  global_max: 4             # всего запусков одновременно
  per_issue: 1              # один активный запуск на задачу
  order: fifo               # или priority (приоритет задачи ICPlan)
  agents:
    analyst:   { parallel: true,  max: 2 }
    developer: { parallel: false }
  models:
    team-default: { max: 3 }  # общий лимит для всех агентов на модели
```

Обоснование: [R&D: Runner и очередь](docs/rnd/runner-and-scheduling.md) · [design D14](openspec/changes/define-agent-platform/design.md) · спека: [agent-runner](openspec/changes/define-agent-platform/specs/agent-runner/spec.md).

## Исполнение: тёплый пул + одноразовое использование

```
┌──────────────┐ claim  ┌──────────────┐ run  ┌──────────────┐ destroy ┌──────────────┐
│ Тёплый пул   ├───────▶│ Sandbox      ├─────▶│ Harness      ├────────▶│ Пул доливает │
│ N на профиль │        │ (один запуск)│      │ работает     │         │ новый        │
└──────▲───────┘        └──────────────┘      └──────────────┘         └──────┬───────┘
       └──────────────────────────────────────────────────────────────────────┘
```
Обоснование: [R&D: изоляция](docs/rnd/sandbox-isolation.md) · [design D1](openspec/changes/define-agent-platform/design.md).

Старт за доли секунды, изоляция как у «контейнер на запуск». Рабочие данные в контейнере не живут (см. «Рабочие данные и доступы»). Ориентиры: harness 150–300 МБ RAM, агент-разработчик 0.5–2 ГБ, CPU почти не нужен (ожидание LLM). Спека: [agent-sandbox](openspec/changes/define-agent-platform/specs/agent-sandbox/spec.md).

## Память M0–M6

| Уровень | Что | Где | MVP |
|---|---|---|---|
| M0 рабочая | Контекст запуска | Harness (процесс) | ✅ |
| M1 сессионная | Переписка в треде | БД ICPlan | ✅ есть |
| M2 эпизодическая | Запуски, итоги, ошибки | БД ICPlan (`agent_run`) | ✅ есть + подача в промпт |
| M3 задачная | Сделано / дальше / блокеры по задаче | БД ICPlan | ⬜ первым делом |
| M4 семантическая | Факты, поиск по смыслу | pgvector в Postgres ICPlan | ⬜ позже, вместе с RAG |
| M5 процедурная | Инструкция, навыки | БД ICPlan | ✅ есть |
| M6 организационная | Документы проекта, ADR | Документы ICPlan | ✅ есть (`get_document`) |

Область видимости (агент / проект / команда) — атрибут записи, не уровень. Обоснование: [R&D: модель памяти](docs/rnd/memory-model.md) · [design D4](openspec/changes/define-agent-platform/design.md). Спека: [agent-memory](openspec/changes/define-agent-platform/specs/agent-memory/spec.md).

## RAG

Не в MVP. В MVP: документы через `get_document` (M6), по коду — агентный поиск тулами (grep/read). RAG вводится, когда корпус документов перестаёт помещаться в навигацию. Хранилище — pgvector, эмбеддер — локальный контейнер. RAG — механизм чтения M4/M6, новых уровней не добавляет. Обоснование: [R&D: RAG](docs/rnd/rag.md) · [design D13](openspec/changes/define-agent-platform/design.md).

## Хранение конфигурации

| Что | Где |
|---|---|
| Определения агентов, MCP, тулы, навыки | БД ICPlan — источник правды |
| Версии определений агента | БД ICPlan (таблица версий) |
| Ревью и перенос между окружениями | Экспорт / импорт YAML |
| Наши настройки (алиасы, бюджеты, профили sandbox, данные guardrails) | **Platform module** — модуль ICPlan, отдельная схема в БД ICPlan |
| Логика guardrails (Rego) | git (код, тесты `opa test`, ревью) |

Обоснование: [R&D: хранение конфигурации](docs/rnd/config-storage.md) · [design D9](openspec/changes/define-agent-platform/design.md).

## MCP или прямой вызов

| # | Правило | Как |
|---|---|---|
| R1 | Последовательность известна заранее (детерминированно) | Прямой вызов (REST / gRPC / SDK) |
| R2 | Следующий шаг решает модель | Тул агента |
| R3 | Тул нужен нескольким агентам/хостам или держит секрет вне агента | MCP-сервер |
| R4 | Тул один, стабильный, только внутри Harness | Нативный тул Harness |
| R5 | Пакетные и массовые операции | Прямой вызов (MCP медленнее и дороже по токенам) |
| R6 | Админ-функции | Отдельные MCP-серверы по уровню доверия, рабочим агентам недоступны |
| R7 | Внутренности платформы: Runner↔ICPlan, Harness↔LiteLLM, проверки G1–G4, автозапись M1/M2 | Только прямой вызов |

Спека: [tool-integration](openspec/changes/define-agent-platform/specs/tool-integration/spec.md). Обоснование: [R&D: MCP или прямой вызов](docs/rnd/mcp-vs-direct.md) · [design D10](openspec/changes/define-agent-platform/design.md).

## Рабочие данные и доступы

| Данные | Куда |
|---|---|
| Рабочие файлы запуска | `/workspace` в Sandbox, удаляется с контейнером |
| Код | Ветка `agent/<KEY>` + PR в целевой репозиторий; push в защищённые ветки запрещён |
| Документы, артефакты | Документы и вложения задачи ICPlan (RustFS, S3 API) |
| Состояние задачи (M3), лог запуска (M2) | БД ICPlan |

**Доступ к репозиториям:** в определении агента — allowlist `repos: [{repo, access: read|write, branch_prefix}]`. Runner выдаёт короткоживущий токен на запуск, ограниченный этими репозиториями; токен подставляет egress-прокси или credential helper, в env контейнера его нет. Репозитории клонируются в `/workspace` при старте (shallow).

**MCP-серверы**

| MCP-сервер | Для чего | Статус |
|---|---|---|
| `itsaplan-core` | Задачи, комментарии, документы, вложения | ✅ есть в ICPlan |
| git-провайдер (Gitea / GitHub MCP) | PR, ревью, issues репозитория | ⬜ подключить |
| memory | Запись агентом M3 (позже M4) | ⬜ наш |
| web-research | Выход в интернет | [бэклог](docs/BACKLOG.md) |

**Окружение Sandbox**

| Переменная | Значение |
|---|---|
| `RUN_ID`, `AGENT_ID`, `ISSUE_KEY` | Контекст запуска |
| `WORKSPACE` | `/workspace` |
| `LLM_BASE_URL` | LiteLLM (ключ агента подставляет прокси) |
| `ITSAPLAN_MCP_URL`, `MEMORY_URL` | Сервисы платформы |
| `OPA_URL` | Если включён G2 |
| `HTTPS_PROXY` | Egress-прокси с allowlist (G3) |

## Observability

Обоснование: [R&D: наблюдаемость](docs/rnd/observability.md) · [design D12](openspec/changes/define-agent-platform/design.md).

MVP: таблица событий запуска в БД ICPlan → пошаговый таймлайн в задаче. Langfuse — позже (evals, анализ промптов; тяжёлый self-host). Prometheus / Grafana / Loki — компоненты есть, остаются пустыми: [бэклог](docs/BACKLOG.md). Спека: [observability](openspec/changes/define-agent-platform/specs/observability/spec.md).

## Блоки

| Блок | Задача | Нужен? |
|---|---|---|
| Agent Runner | Жизненный цикл запуска: sandbox up → run → лимиты/таймауты/ретраи → результат → cleanup | Да — без него некому поднимать среду |
| Control Plane UI (ICPlan) | UI настройки агентов | Да — уже есть в ICPlan |
| Platform module (модуль ICPlan) | Настройки, которых нет в ICPlan: алиасы, бюджеты, профили sandbox и памяти, данные guardrails | Да |
| Registry (ICPlan) | Агенты, тулы, скиллы, MCP, ключи | Да — уже есть в ICPlan |
| Run Queue + runner API (ICPlan) | Очередь запусков, протокол внешнего раннера | Да — точка входа Agent Runner |
| Task UI (ICPlan) | Доска, чат, approve, quality gate | Да |
| Sandbox | Изоляция каждого запуска | Да — требование |
| Harness | Агентский цикл + хуки | Да — ядро |
| Memory Svc | Память M1–M6 вне sandbox (M0 — в Harness) | Да |
| MCP/Tools | Внешние действия агента | Да |
| Guardrail Policy | Rego (git) + данные (БД ICPlan), раздаёт решения в точки G1–G4 | Да — одно место правды для политик |
| G1–G4 | Точки применения правил (см. раздел Guardrails) | Да — одна точка не покрывает все риски |
| LiteLLM | Единственный выход к моделям, учёт токенов, fallback | Да |
| Observability | Таймлайн запуска и стоимость | Да; MVP — таблица событий в БД, Langfuse позже |

## Расширения

```
новый агент   → ICPlan (UI / импорт YAML) ▶ Agent Runner берёт из очереди
новая модель  → алиас в LiteLLM ──────▶ меняется в agent def
новый тул     → MCP-сервер в Registry ▶ подключается в agent def
новый скилл   → пакет (prompt+tools) ─▶ Registry
своя логика   → plugin ──▶ hooks Harness (before/after LLM|tool)
новая политика→ Rego (git) + данные (БД) ▶ Policy ──▶ точка G1–G4
```

## Плюсы / минусы по модулям

| Модуль | ➕ | ➖ |
|---|---|---|
| Agent Runner | Простой, без логики планирования | Единая точка отказа; нужна очередь/HA |
| Control Plane | Управление без кода | Отдельный продукт (UI) |
| Registry | Версии, переиспользование, сборка из конфига | Нужна валидация связей |
| Sandbox | Безопасность, чистая среда | Холодный старт, ресурсы |
| Harness | Единые правила, хуки | Хуки могут ломать цикл — строгий API |
| Memory Svc | Переживает перезапуск, общие знания | Права, консистентность, очистка |
| MCP/Tools | Стандарт, подключение без кода | Ненадёжные внешние серверы, нужны таймауты/права |
| Guardrail Policy | Правила в одном месте, версии | Сложно отлаживать, какое правило сработало — нужен аудит |
| G1 Admission | Отсекает до запуска, дёшево | Видит только метаданные |
| G2 Action | Понимает контекст действия | Обходится при сломанном харнесе |
| G3 Isolation | Жёстко на уровне ОС | Грубо, не понимает смысла |
| G4 LLM | Не обойти — весь LLM-трафик | Не видит тулы, добавляет латентность |
| LiteLLM | Одна точка, смена модели, учёт токенов | Лишний хоп, неполная поддержка фич провайдеров |
| Observability | Трейсы и $ по агенту | Объём данных, политика хранения |

## Доработки по модулям

Спеки: `openspec/changes/define-agent-platform/specs/<модуль>/spec.md` (далее `dap/`), интеграция — `openspec/changes/add-icplan-integration/specs/icplan-integration/spec.md` (далее `ici/`).

### ICPlan → Control Plane UI
- **Есть:** настройка агента (имя, модель, инструкция, проекты), ключи, тулы, навыки, MCP.
- **Доработать:** экраны для настроек Platform module (бюджеты, guardrails, sandbox, память, версии).
- **Спека:** [dap/control-plane](openspec/changes/define-agent-platform/specs/control-plane/spec.md)

### ICPlan → Registry
- **Есть:** агенты, тулы, навыки, MCP, ключи провайдеров.
- **Доработать:** версии определения агента; экспорт/импорт YAML; ссылка агента на профили Platform module; allowlist репозиториев агента.
- **Спека:** [dap/agent-registry](openspec/changes/define-agent-platform/specs/agent-registry/spec.md)

### ICPlan → Run Queue + runner API
- **Есть:** очередь запусков внешнего агента, опрос по ключу, стрим ответа и тулов.
- **Доработать:** передача в запуске quality gate и лимитов; события approve/вопрос; затраты запуска.
- **Спека:** [ici/icplan-integration](openspec/changes/add-icplan-integration/specs/icplan-integration/spec.md) — обновлено: pull через очередь раннера ICPlan.

### ICPlan → Task UI
- **Есть:** доска, статусы с автоназначением исполнителя (без запуска агента), комментарии, чат агента, история запусков (итог).
- **Доработать:** автоподхват задачи агентом по статусу/типу/действию — [change icplan-agent-autopickup](openspec/changes/icplan-agent-autopickup/tasks.md), спека: [icplan-agent-autopickup](openspec/changes/icplan-agent-autopickup/specs/icplan-agent-autopickup/spec.md); approve действия агента; результат quality gate; пошаговый лог; затраты задачи.
- **Спека:** [ici/icplan-integration](openspec/changes/add-icplan-integration/specs/icplan-integration/spec.md)

### Platform module (модуль ICPlan)
- **Есть:** —
- **Доработать:** модуль в форке ICPlan, своя схема БД: алиасы LLM, бюджеты, профили sandbox и памяти, данные guardrails.
- **Спека:** [dap/control-plane](openspec/changes/define-agent-platform/specs/control-plane/spec.md) — обновлено: модуль ICPlan.

### Agent Runner
- **Есть:** протокол раннера ICPlan (как основа).
- **Доработать:** работать как внешний раннер ICPlan; на каждый запуск поднимать Sandbox; G1 (допуск, лимиты, $); cleanup.
- **Спека:** [dap/agent-runner](openspec/changes/define-agent-platform/specs/agent-runner/spec.md) — обновлено: запуск из очереди ICPlan, планировщик слотов.

### Sandbox [G3]
- **Есть:** —
- **Доработать:** тёплый пул по профилям, одноразовое использование, egress-прокси, токены репозиториев на запуск.
- **Спека:** [dap/agent-sandbox](openspec/changes/define-agent-platform/specs/agent-sandbox/spec.md)

### Harness [G2]
- **Есть:** —
- **Доработать:** целиком на LangGraph, без изменений плана.
- **Спека:** [dap/agent-harness](openspec/changes/define-agent-platform/specs/agent-harness/spec.md)

### Memory Svc
- **Есть:** M1, M2, M5, M6 в ICPlan.
- **Доработать:** M3 (первым), M2 в промпт; M4 вместе с RAG позже.
- **Спека:** [dap/agent-memory](openspec/changes/define-agent-platform/specs/agent-memory/spec.md)

### MCP / Tools
- **Есть:** MCP-серверы и тулы в ICPlan; MCP-сервер самого ICPlan.
- **Доработать:** передача списка тулов/MCP из ICPlan в Harness; MCP git-провайдера; правила R1–R7.
- **Спека:** [dap/tool-integration](openspec/changes/define-agent-platform/specs/tool-integration/spec.md)

### Guardrail Policy [G1–G4]
- **Есть:** —
- **Доработать:** OPA для G1/G2 (Rego в git, данные в БД ICPlan); включение/выключение точек в конфиге деплоя.
- **Спека:** [dap/guardrails](openspec/changes/define-agent-platform/specs/guardrails/spec.md)

### LiteLLM gw [G4]
- **Есть:** стек `itsaplan-agents` (LiteLLM запущен, ICPlan его не вызывает).
- **Доработать:** virtual key на агента, алиасы, G4-хуки.
- **Спека:** [dap/llm-gateway](openspec/changes/define-agent-platform/specs/llm-gateway/spec.md)

### Observability
- **Есть:** история запусков ICPlan; Grafana/Loki/Prometheus в `itsaplan-platform`.
- **Доработать:** таблица событий запуска → таймлайн в Task UI; затраты. Langfuse и метрики — [бэклог](docs/BACKLOG.md).
- **Спека:** [dap/observability](openspec/changes/define-agent-platform/specs/observability/spec.md)
