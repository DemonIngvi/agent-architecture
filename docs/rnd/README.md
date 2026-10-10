# R&D: обоснование решений

← [README](../../README.md) · [architecture.md](../../architecture.md) · [design.md (решения D1–D14)](../../openspec/changes/define-agent-platform/design.md)

Небольшие исследования, на которых основаны решения. В каждом: контекст, варианты, сравнение, решение, источники.

| R&D | Компонент | Решение | Design |
|---|---|---|---|
| [Выбор таск-трекера](tracker-choice.md) | ICPlan | Форк It's a Plan | — |
| [Runner и очередь запусков](runner-and-scheduling.md) | Agent Runner | Свой Runner как внешний раннер ICPlan; планировщик со слотами (вариант B) | D8, D14 |
| [Изоляция запусков](sandbox-isolation.md) | Sandbox | Тёплый пул + одноразовые контейнеры | D1 |
| [Фреймворк агентского цикла](harness-framework.md) | Harness | LangGraph | D2 |
| [Модель памяти](memory-model.md) | Memory | M0–M6 | D4 |
| [RAG](rag.md) | Memory | Не в MVP; pgvector позже | D13 |
| [MCP или прямой вызов](mcp-vs-direct.md) | MCP / Tools | Гибрид R1–R7 | D10 |
| [Движок guardrails](guardrails-engine.md) | Guardrails | OPA для G1/G2 | D6 |
| [Защита от зацикливания и перерасхода](runaway-protection.md) | Guardrails | Детерминированные лимиты и бюджеты | D6 |
| [Хранение конфигурации](config-storage.md) | Platform module | БД ICPlan + YAML экспорт | D9 |
| [Шлюз к моделям](llm-gateway.md) | LiteLLM gateway | LiteLLM Proxy | D5 |
| [Наблюдаемость](observability.md) | Observability | Таблица событий в MVP, Langfuse позже | D12 |

Источники — по состоянию на октябрь 2026; часть ссылок на внутренние документы проекта AI-агент (`D:\АИ агент\Архитектура`).
