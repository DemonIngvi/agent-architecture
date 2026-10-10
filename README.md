# Agent Platform — документация

Платформа запуска LLM-агентов для задач из таск-трекера ICPlan (It's a Plan): изоляция каждого запуска, контроль моделей и затрат, guardrails, память.

- HTML-версия — https://demoningvi.github.io/agent-architecture/ ([как собрать](html-view/README.md))
- Впервые здесь — [как читать документацию](docs/HOW-TO-READ.md)
- Схемы C1/C2 — [architecture.md](architecture.md)
- План работ по документации — [docs/PLAN.md](docs/PLAN.md)
- Roadmap MVP с оценками — [docs/ROADMAP.md](docs/ROADMAP.md)
- Сводная таблица задач — [docs/TASKS.md](docs/TASKS.md)
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
| [ICPlan](docs/icplan/README.md) | Таск-трекер: доска, процессы, настройка агентов, очередь запусков, UI для пользователя. Автоподхват задач агентом — [доработка](openspec/changes/icplan-agent-autopickup/tasks.md) | [Agent Runner](docs/agent-runner/README.md), [Platform module](docs/platform-module/README.md), [Observability](docs/observability/README.md) | ⚠️ есть, нужны доработки |
| [Platform module](docs/platform-module/README.md) | Модуль ICPlan (своя схема в БД ICPlan): алиасы LLM, бюджеты, профили sandbox и памяти, данные guardrails | [ICPlan](docs/icplan/README.md), [Agent Runner](docs/agent-runner/README.md), [Guardrails](docs/guardrails/README.md), [LiteLLM gw](docs/llm-gateway/README.md) | ⬜ |
| [Agent Runner](docs/agent-runner/README.md) | Берёт запуск из очереди ICPlan, поднимает Sandbox, следит за лимитами [G1], возвращает результат | [ICPlan](docs/icplan/README.md), [Sandbox](docs/sandbox/README.md), [Platform module](docs/platform-module/README.md) | ⬜ протокол ICPlan есть |
| [Sandbox](docs/sandbox/README.md) | Тёплый пул, одноразовая изолированная среда на запуск [G3] | [Agent Runner](docs/agent-runner/README.md), [Harness](docs/harness/README.md) | ⬜ |
| [Harness](docs/harness/README.md) | Агентский цикл на LangGraph: контекст → LLM → тулы, hooks [G2] | [LiteLLM gw](docs/llm-gateway/README.md), [MCP / Tools](docs/mcp-tools/README.md), [Memory](docs/memory/README.md) | ⬜ |
| [Memory](docs/memory/README.md) | Память агентов M1–M6 (M0 — в Harness) | [Harness](docs/harness/README.md), [Platform module](docs/platform-module/README.md) | ⬜ |
| [MCP / Tools](docs/mcp-tools/README.md) | Внешние действия агента: тулы, MCP-серверы, скиллы | [Harness](docs/harness/README.md), [ICPlan](docs/icplan/README.md) | ⚠️ есть в ICPlan |
| [Guardrails](docs/guardrails/README.md) | Политика и точки G1–G4 (OPA для G1/G2), каждая включается в конфиге деплоя | [Agent Runner](docs/agent-runner/README.md), [Harness](docs/harness/README.md), [Sandbox](docs/sandbox/README.md), [LiteLLM gw](docs/llm-gateway/README.md) | ⬜ |
| [LiteLLM gw](docs/llm-gateway/README.md) | Единственный выход к моделям: алиасы, учёт токенов, лимиты, fallback [G4] | [Harness](docs/harness/README.md), [Observability](docs/observability/README.md) | ⚠️ развёрнут, не подключён |
| [Observability](docs/observability/README.md) | События и таймлайн запуска, затраты, аудит guardrails | [LiteLLM gw](docs/llm-gateway/README.md), [ICPlan](docs/icplan/README.md) | ⚠️ история запусков в ICPlan |

Ссылки на карточки компонентов заработают по мере их создания ([план](docs/PLAN.md)).
