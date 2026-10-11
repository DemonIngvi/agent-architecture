# R&D: обоснование решений

← [README](../../README.md) · [architecture.md](../../architecture.md) · [design.md (решения D1–D14)](../../openspec/changes/define-agent-platform/design.md)

Исследования, на которых основаны решения. Проводятся по [методологии R&D v3.1](../rules/rnd-methodology.md): цепочка «потребность → ключевые функции → ценность → перенос → встраивание → спор ролей → выбор → последствия», ворота между этапами, первая страница — ответ и микропрезентация на 3 минуты ([почему так](rnd-methodology-choice.md)). Что из исследований меняется в документах — [сводка последствий R&D](../../rnd-consequences.md). Колонка «Методология»: **v3.1** — оформлено полностью; **v1 + альтернативы** — нужно перевести на v3.1.

| R&D | Компонент | Решение | Design | Методология |
|---|---|---|---|---|
| [Выбор таск-трекера](tracker-choice.md) | ICPlan | Форк It's a Plan: агентная часть есть (делегат, очередь с арендой, раннер), процесс — доработкой; функции Linear, Jira, Plane перенесены | D17, D18 | v3.1 (эталон) |
| [Как проводить и подавать исследования](rnd-methodology-choice.md) | Правила документации | Методология v3: этапы с воротами, функции и их ценность, аргумент вывода, ответ первым | — | v3.1 |
| [Автоподхват задач агентом](autopickup-rules.md) | ICPlan | Процесс типа задачи (шаг = колонка + агент + переходы) + эффект Действия | — | v1 + альтернативы |
| [Потоки аналогов «трекер + ИИ-агенты»](us-analogs-agent-tracker.md) | ICPlan (истории всех компонентов) | потоки Linear, Copilot, Jira + Rovo, Devin → истории | — | потоки (матрица аналогов) |
| [Runner и очередь запусков](runner-and-scheduling.md) | Agent Runner | Свой Runner на Go + слоты в Postgres; движки (Hatchet, Temporal, River Pro) — вторая очередь и новый сервис; тест гонок в 2.7 | D8, D14 | v3.1 |
| [Изоляция запусков](sandbox-isolation.md) | Sandbox | Одноразовый контейнер + тёплый пул на rootless Docker; gVisor — проверка в 2.2; microVM — при внешнем коде; Daytona архивирован | D18 | v3.1 |
| [Фреймворк агентского цикла](harness-framework.md) | Harness | LangGraph за своим интерфейсом; Trial до прототипа AG1–AG5 (OpenAI Agents SDK — запасной); Hermes заменил бы 4 компонента | D2 | v3.1 |
| [Модель памяти](memory-model.md) | Memory | M0–M6 по видам знания, область — атрибут, своя Memory API; M4 после MVP на Mem0 или LangMem (противоречия, срок действия) | D4 | v3.1 |
| [RAG](rag.md) | Memory | Не в MVP; pgvector позже | D13 | v1 + альтернативы |
| [MCP или прямой вызов](mcp-vs-direct.md) | MCP / Tools | Гибрид R1–R7 | D10 | v1 + альтернативы |
| [Движок guardrails](guardrails-engine.md) | Guardrails | OPA для G1/G2 | D6 | v1 + альтернативы |
| [Защита от зацикливания и перерасхода](runaway-protection.md) | Guardrails | Детерминированные лимиты и бюджеты | D6 | v1 + альтернативы |
| [Хранение конфигурации](config-storage.md) | Platform module | БД ICPlan + YAML экспорт | D9 | v1 + альтернативы |
| [Шлюз к моделям](llm-gateway.md) | LiteLLM gateway | LiteLLM Proxy v1.104.2: ключи, бюджеты и учёт в открытом ядре; Bifrost — запасной при пороге 4.8.4; TensorZero архивирован | D5, D18 | v3.1 |
| [Профиль нагрузки и ёмкость](load-profile.md) | Инфраструктура | Один узел k3s для MVP, гипотезы нагрузки | D16 | v1 + альтернативы |
| [Ingress и балансировка](ingress-and-balancing.md) | Инфраструктура | Traefik, Service, PgBouncer | D15 | v1 + альтернативы |
| [Kubernetes и развёртывание](kubernetes-runtime.md) | Инфраструктура | k3s + Helm, k3d локально | D15 | v1 + альтернативы |
| [СУБД и хранилища](data-stores.md) | Инфраструктура | PostgreSQL 17 + CloudNativePG, RustFS | D4, D15 | v1 + альтернативы |
| [Рабочее пространство агентов и доступы](agent-workspace.md) | Sandbox, MCP, Platform module | 📌 открыт; рекомендация — каталог проекта + workspace задачи + политика | — | v1 + альтернативы |
| [Наблюдаемость](observability.md) | Observability | Таблица событий в MVP, Langfuse позже | D12 | v1 + альтернативы |

Источники — по состоянию на октябрь 2026; часть ссылок на внутренние документы проекта AI-агент (`D:\АИ агент\Архитектура`).
