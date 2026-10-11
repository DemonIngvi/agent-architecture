# R&D: обоснование решений

← [README](../../README.md) · [architecture.md](../../architecture.md) · [design.md (решения D1–D14)](../../openspec/changes/define-agent-platform/design.md)

Исследования, на которых основаны решения. Проводятся по [методологии R&D](../rules/rnd-methodology.md): путь исследования, обязательные условия до баллов, карточки данных, критерии из сценариев со шкалами, сравнение по фактам. Колонка «Методология»: **v2** — оформлено полностью; **v1 + альтернативы** — есть альтернативы и сравнение по фактам, нужно довести до v2 (обязательные условия, шкалы с якорями, чувствительность).

| R&D | Компонент | Решение | Design | Методология |
|---|---|---|---|---|
| [Выбор таск-трекера](tracker-choice.md) | ICPlan | Форк It's a Plan (после отсева Linear, Jira, Hermes Agent; 85 против 64 у Plane CE) | — | v2 |
| [Автоподхват задач агентом](autopickup-rules.md) | ICPlan | Процесс типа задачи (шаг = колонка + агент + переходы) + эффект Действия | — | v1 + альтернативы |
| [Потоки аналогов «трекер + ИИ-агенты»](us-analogs-agent-tracker.md) | ICPlan (истории всех компонентов) | потоки Linear, Copilot, Jira + Rovo, Devin → истории | — | потоки (матрица аналогов) |
| [Runner и очередь запусков](runner-and-scheduling.md) | Agent Runner | Свой Runner как внешний раннер ICPlan; планировщик со слотами (вариант B) | D8, D14 | v1 + альтернативы |
| [Изоляция запусков](sandbox-isolation.md) | Sandbox | Тёплый пул + одноразовые контейнеры | D1 | v1 + альтернативы |
| [Фреймворк агентского цикла](harness-framework.md) | Harness | LangGraph | D2 | v1 + альтернативы |
| [Модель памяти](memory-model.md) | Memory | M0–M6 | D4 | v1 + альтернативы |
| [RAG](rag.md) | Memory | Не в MVP; pgvector позже | D13 | v1 + альтернативы |
| [MCP или прямой вызов](mcp-vs-direct.md) | MCP / Tools | Гибрид R1–R7 | D10 | v1 + альтернативы |
| [Движок guardrails](guardrails-engine.md) | Guardrails | OPA для G1/G2 | D6 | v1 + альтернативы |
| [Защита от зацикливания и перерасхода](runaway-protection.md) | Guardrails | Детерминированные лимиты и бюджеты | D6 | v1 + альтернативы |
| [Хранение конфигурации](config-storage.md) | Platform module | БД ICPlan + YAML экспорт | D9 | v1 + альтернативы |
| [Шлюз к моделям](llm-gateway.md) | LiteLLM gateway | LiteLLM Proxy | D5 | v1 + альтернативы |
| [Профиль нагрузки и ёмкость](load-profile.md) | Инфраструктура | Один узел k3s для MVP, гипотезы нагрузки | D16 | v1 + альтернативы |
| [Ingress и балансировка](ingress-and-balancing.md) | Инфраструктура | Traefik, Service, PgBouncer | D15 | v1 + альтернативы |
| [Kubernetes и развёртывание](kubernetes-runtime.md) | Инфраструктура | k3s + Helm, k3d локально | D15 | v1 + альтернативы |
| [СУБД и хранилища](data-stores.md) | Инфраструктура | PostgreSQL 17 + CloudNativePG, RustFS | D4, D15 | v1 + альтернативы |
| [Рабочее пространство агентов и доступы](agent-workspace.md) | Sandbox, MCP, Platform module | 📌 открыт; рекомендация — каталог проекта + workspace задачи + политика | — | v1 + альтернативы |
| [Наблюдаемость](observability.md) | Observability | Таблица событий в MVP, Langfuse позже | D12 | v1 + альтернативы |

Источники — по состоянию на октябрь 2026; часть ссылок на внутренние документы проекта AI-агент (`D:\АИ агент\Архитектура`).
