# Agent Platform — документация

Платформа запуска LLM-агентов для задач из таск-трекера ICPlan (It's a Plan): изоляция каждого запуска, контроль моделей и затрат, guardrails, память.

- HTML-версия — https://demoningvi.github.io/agent-architecture/ ([как собрать](https://github.com/DemonIngvi/agent-architecture/blob/main/html-view/README.md))
- Впервые здесь — [как читать документацию](docs/HOW-TO-READ.md)
- Схемы C1/C2 — [architecture.md](architecture.md)
- User Stories и процессы BPMN — [docs/stories/](docs/stories/README.md)
- Потоки данных и форматы — [docs/flows/](architecture.md#interaction)
- R&D: обоснование решений — [docs/rnd/](docs/rnd/README.md)
- План работ по документации — [docs/PLAN.md](docs/PLAN.md)
- Roadmap MVP с оценками — [docs/ROADMAP.md](docs/ROADMAP.md)
- Сводная таблица задач — [docs/TASKS.md](docs/TASKS.md)
- Сводная таблица технологий (ПО, лицензии, откуда качать) — [docs/TECHNOLOGIES.md](docs/TECHNOLOGIES.md)
- Дальний бэклог и техдолг — [docs/BACKLOG.md](docs/BACKLOG.md)

## Как это работает

```
Пользователь ─▶ ICPlan: задача в статусе ─▶ автоназначение агента ─▶ очередь запусков
                                                                       │
     ┌─────────────────────────────────────────────────────────────────┘
     ▼
Agent Runner ─▶ Sandbox ─▶ Harness ─▶ LiteLLM ─▶ модель
     │                       ├─▶ MCP / Tools
     │                       └─▶ Memory
     └─▶ стрим и результат обратно в задачу ICPlan
```

## Компоненты

✅ сделано · ⚠️ частично · ⬜ не начато

| Компонент | Задача | Интеграции | Готовность |
|---|---|---|---|
| [ICPlan](https://demoningvi.github.io/agent-architecture/components/icplan/) | Таск-трекер: доска, процессы, настройка агентов, очередь запусков, UI для пользователя. Автоподхват задач агентом — [доработка](openspec/changes/icplan-agent-autopickup/tasks.md) | [Agent Runner](https://demoningvi.github.io/agent-architecture/components/agent-runner/), [Platform module](https://demoningvi.github.io/agent-architecture/components/platform-module/), [Observability](https://demoningvi.github.io/agent-architecture/components/observability/) | ⚠️ есть, нужны доработки |
| [Platform module](https://demoningvi.github.io/agent-architecture/components/platform-module/) | Модуль ICPlan (своя схема в БД ICPlan): алиасы LLM, бюджеты, профили sandbox и памяти, данные guardrails | [ICPlan](https://demoningvi.github.io/agent-architecture/components/icplan/), [Agent Runner](https://demoningvi.github.io/agent-architecture/components/agent-runner/), [Guardrails](https://demoningvi.github.io/agent-architecture/components/guardrails/), [LiteLLM gw](https://demoningvi.github.io/agent-architecture/components/llm-gateway/) | ⬜ |
| [Agent Runner](https://demoningvi.github.io/agent-architecture/components/agent-runner/) | Берёт запуск из очереди ICPlan, поднимает Sandbox, следит за лимитами [G1], возвращает результат | [ICPlan](https://demoningvi.github.io/agent-architecture/components/icplan/), [Sandbox](https://demoningvi.github.io/agent-architecture/components/sandbox/), [Platform module](https://demoningvi.github.io/agent-architecture/components/platform-module/) | ⬜ протокол ICPlan есть |
| [Sandbox](https://demoningvi.github.io/agent-architecture/components/sandbox/) | Тёплый пул, одноразовая изолированная среда на запуск [G3] | [Agent Runner](https://demoningvi.github.io/agent-architecture/components/agent-runner/), [Harness](https://demoningvi.github.io/agent-architecture/components/harness/) | ⬜ |
| [Harness](https://demoningvi.github.io/agent-architecture/components/harness/) | Агентский цикл на LangGraph: контекст → LLM → тулы, hooks [G2] | [LiteLLM gw](https://demoningvi.github.io/agent-architecture/components/llm-gateway/), [MCP / Tools](https://demoningvi.github.io/agent-architecture/components/mcp-tools/), [Memory](https://demoningvi.github.io/agent-architecture/components/memory/) | ⬜ |
| [Memory](https://demoningvi.github.io/agent-architecture/components/memory/) | Память агентов M1–M6 (M0 — в Harness) | [Harness](https://demoningvi.github.io/agent-architecture/components/harness/), [Platform module](https://demoningvi.github.io/agent-architecture/components/platform-module/) | ⬜ |
| [MCP / Tools](https://demoningvi.github.io/agent-architecture/components/mcp-tools/) | Внешние действия агента: тулы, MCP-серверы, скиллы | [Harness](https://demoningvi.github.io/agent-architecture/components/harness/), [ICPlan](https://demoningvi.github.io/agent-architecture/components/icplan/) | ⚠️ есть в ICPlan |
| [Guardrails](https://demoningvi.github.io/agent-architecture/components/guardrails/) | Политика и точки G1–G4 (OPA для G1/G2), каждая включается в конфиге деплоя | [Agent Runner](https://demoningvi.github.io/agent-architecture/components/agent-runner/), [Harness](https://demoningvi.github.io/agent-architecture/components/harness/), [Sandbox](https://demoningvi.github.io/agent-architecture/components/sandbox/), [LiteLLM gw](https://demoningvi.github.io/agent-architecture/components/llm-gateway/) | ⬜ |
| [LiteLLM gw](https://demoningvi.github.io/agent-architecture/components/llm-gateway/) | Единственный выход к моделям: алиасы, учёт токенов, лимиты, fallback [G4] | [Harness](https://demoningvi.github.io/agent-architecture/components/harness/), [Observability](https://demoningvi.github.io/agent-architecture/components/observability/) | ⚠️ развёрнут, не подключён |
| [Observability](https://demoningvi.github.io/agent-architecture/components/observability/) | События и чат запуска, затраты, аудит guardrails | [LiteLLM gw](https://demoningvi.github.io/agent-architecture/components/llm-gateway/), [ICPlan](https://demoningvi.github.io/agent-architecture/components/icplan/) | ⚠️ история запусков в ICPlan |

Ссылки на компоненты ведут на их страницы на сайте: схема устройства, описание, параметры, спеки, задачи, R&D.
