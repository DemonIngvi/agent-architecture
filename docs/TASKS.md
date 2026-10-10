# Сводная таблица задач

← [README](../README.md) · [план документации](PLAN.md) · [бэклог](BACKLOG.md)

По компонентам: сначала выполненное ✅ (и частично ⚠️), затем то, что нужно сделать ⬜. Детали и критерии приёмки — по ссылке в колонке «Где».

Источники: `ap` — [icplan-agent-autopickup/tasks.md](../openspec/changes/icplan-agent-autopickup/tasks.md), `arch` — [architecture.md → Доработки по модулям](../architecture.md).

Порядок, оценки и документы задач по INVEST — в [ROADMAP](ROADMAP.md).

## ICPlan

| Статус | Задача | Где |
|---|---|---|
| ✅ | Локальный стек ICPlan (web, api, worker, bot, postgres, minio) | `D:\АИ агент\itsaplan` |
| ✅ | CRUD агентов: имя, модель, инструкция, проекты | ICPlan: Команда → ИИ-агенты |
| ✅ | Ключи провайдеров, тулы, навыки, MCP-серверы | ICPlan: Команда → Настройки |
| ✅ | MCP-сервер `itsaplan-core` (весь REST API как тулы) | ICPlan |
| ✅ | Запуск агента по делегату и по упоминанию | [ap 0.1](../openspec/changes/icplan-agent-autopickup/tasks.md) |
| ✅ | Автоназначение исполнителя на статус (без запуска) | [ap 0.2](../openspec/changes/icplan-agent-autopickup/tasks.md) |
| ✅ | Агент сам переводит статус (`update_issue`) | [ap 0.3](../openspec/changes/icplan-agent-autopickup/tasks.md) |
| ✅ | Очередь запусков внешнего раннера, стрим ответа | ICPlan `@itsaplan/runner` |
| ✅ | Ответ агента публикуется комментарием в задаче | Форк `itsaplan-app` (`postRunAnswer`) |
| ⚠️ | История запусков — только итог, без шагов | [arch → Task UI](../architecture.md) |
| ⬜ | Агент-делегат статуса: поле, запуск, UI | [ap 1.1–1.3](../openspec/changes/icplan-agent-autopickup/tasks.md) |
| ⬜ | Агент-делегат типа задачи: поле, запуск, UI | [ap 2.1–2.3](../openspec/changes/icplan-agent-autopickup/tasks.md) |
| ⬜ | Эффект Действия «делегировать агенту» (T-04) | [ap 3.1–3.2](../openspec/changes/icplan-agent-autopickup/tasks.md) |
| ⬜ | Приоритет правил, защита от дублей, очистка при выходе агента | [ap 4.1–4.3](../openspec/changes/icplan-agent-autopickup/tasks.md) |
| ⬜ | Передача итога следующему агенту, запись в истории | [ap 5.1–5.2](../openspec/changes/icplan-agent-autopickup/tasks.md) |
| ⬜ | Approve действия агента в UI | [arch → Task UI](../architecture.md) |
| ⬜ | Результат quality gate в задаче | [arch → Task UI](../architecture.md) |
| ⬜ | Пошаговый таймлайн запуска в задаче | [arch → Task UI](../architecture.md) |
| ⬜ | Затраты по задаче | [arch → Task UI](../architecture.md) |
| ⬜ | Версии определения агента, экспорт/импорт YAML | [задача 1.2](tasks/1.2-agent-definition-yaml.md) |
| ⬜ | Allowlist репозиториев агента | [arch → Registry](../architecture.md) |
| ⬜ | Передача в запуске quality gate, лимитов; события approve/вопрос | [arch → Run Queue](../architecture.md) |

## Platform module (модуль ICPlan)

| Статус | Задача | Где |
|---|---|---|
| ⬜ | Модуль в форке ICPlan, своя схема БД | [arch → Platform module](../architecture.md) |
| ⬜ | Алиасы LLM, бюджеты, профили sandbox и памяти | [задача 4.4](tasks/4.4-platform-module.md) |
| ⬜ | Хранение данных guardrails (allowlist, лимиты) | [задача 4.4](tasks/4.4-platform-module.md) |
| ⬜ | Экраны настроек в UI ICPlan | [arch → Control Plane UI](../architecture.md) |
| ⬜ | Аутентификация и роли для этих настроек | [задача 4.4](tasks/4.4-platform-module.md) |

## Agent Runner

| Статус | Задача | Где |
|---|---|---|
| ✅ | Протокол раннера ICPlan как основа (опрос очереди, стрим) | ICPlan `docs/runner.md` |
| ⬜ | Каркас Runner (Go), контракт Runner↔Harness | [задача 2.1](tasks/2.1-runner-external.md) |
| ⬜ | Работа как внешний раннер ICPlan: опрос, стрим, итог | [задача 2.1](tasks/2.1-runner-external.md) |
| ⬜ | Жизненный цикл: claim из пула → Harness → результат → destroy | [задача 2.2](tasks/2.2-sandbox-docker-oneshot.md) |
| ⬜ | Планировщик: слоты, режим sequential / parallel, один запуск на задачу | [задача 2.7](tasks/2.7-runner-scheduler.md) |
| ⬜ | Таймаут и отмена | [задача 2.1](tasks/2.1-runner-external.md) |
| ⬜ | Короткоживущий токен репозиториев на запуск | [arch → Рабочие данные](../architecture.md) |

## Sandbox [G3]

| Статус | Задача | Где |
|---|---|---|
| ⚠️ | Локальный k3d-кластер работает (основа для K8s-провайдера) | `D:\АИ агент\Архитектура\infra` |
| ⬜ | `SandboxProvider` + Docker-реализация | [задача 2.2](tasks/2.2-sandbox-docker-oneshot.md) |
| ⬜ | Тёплый пул по профилям, одноразовое использование | [arch → Исполнение](../architecture.md) |
| ⬜ | Профили CPU/RAM/disk | [задача 4.1](tasks/4.1-sandbox-warm-pool.md) |
| ⬜ | Изолированная сеть + egress-прокси с allowlist | [задача 4.2](tasks/4.2-egress-repo-access.md) |
| ⬜ | Подстановка секретов и токенов прокси | [задача 4.2](tasks/4.2-egress-repo-access.md) |
| ⬜ | Эфемерный `/workspace`, клон репозиториев, запрет push в защищённые ветки | [arch → Рабочие данные](../architecture.md) |

## Harness [G2]

| Статус | Задача | Где |
|---|---|---|
| ⬜ | Образ Harness, сборка агента из определения | [задача 1.3](tasks/1.3-harness-core.md) |
| ⬜ | Граф LangGraph `context → llm → tools` | [задача 1.3](tasks/1.3-harness-core.md) |
| ⬜ | Hooks before/after llm\|tool, on_stop | [задача 1.5](tasks/1.5-harness-hooks-approve.md) |
| ⬜ | MCP через адаптер, таймауты тулов | [задача 1.4](tasks/1.4-harness-mcp-tools.md) |
| ⬜ | Пауза на approve и возобновление (checkpointer) | [agent-harness spec](../openspec/changes/define-agent-platform/specs/agent-harness/spec.md) |
| ⬜ | Стрим шагов для таймлайна | [agent-harness spec](../openspec/changes/define-agent-platform/specs/agent-harness/spec.md) |
| ⬜ | Управление контекстом и сжатие | [задача 1.6](tasks/1.6-harness-limits-context.md) |
| ⬜ | Завершение done/limit/error, отдача результата | [задача 1.6](tasks/1.6-harness-limits-context.md) |

## Memory (M0–M6)

| Статус | Задача | Где |
|---|---|---|
| ✅ | M0 рабочая — в каждом запуске | [arch → Память](../architecture.md) |
| ✅ | M1 сессионная — тред в БД ICPlan | [arch → Память](../architecture.md) |
| ✅ | M2 эпизодическая — `agent_run` в БД | [arch → Память](../architecture.md) |
| ✅ | M5 процедурная — инструкция и навыки | [arch → Память](../architecture.md) |
| ✅ | M6 организационная — документы, `get_document` | [arch → Память](../architecture.md) |
| ⬜ | M3 задачная: тул записи + подача в контекст (первым) | [agent-memory spec](../openspec/changes/define-agent-platform/specs/agent-memory/spec.md) |
| ⬜ | M2 в контекст: итоги последних N запусков задачи | [agent-memory spec](../openspec/changes/define-agent-platform/specs/agent-memory/spec.md) |
| ⬜ | API памяти с проверкой профиля и области видимости | [задача 2.5](tasks/2.5-memory-m2-m3.md) |
| ⬜ | Сроки хранения и админ-удаление | [задача 2.5](tasks/2.5-memory-m2-m3.md) |

## MCP / Tools

| Статус | Задача | Где |
|---|---|---|
| ✅ | MCP-серверы, тулы и навыки в ICPlan | ICPlan |
| ⬜ | Передача списка тулов/MCP из ICPlan в Harness | [arch → MCP / Tools](../architecture.md) |
| ⬜ | MCP git-провайдера (Gitea / GitHub) | [arch → Рабочие данные](../architecture.md) |
| ⬜ | Тул памяти (запись M3) | [arch → Рабочие данные](../architecture.md) |
| ⬜ | Правила R1–R7: MCP или прямой вызов | [tool-integration spec](../openspec/changes/define-agent-platform/specs/tool-integration/spec.md) |

## Guardrails [G1–G4]

| Статус | Задача | Где |
|---|---|---|
| ⚠️ | Контейнер OPA развёрнут, не подключён | `D:\АИ агент\itsaplan-agents` |
| ⬜ | Конфиг деплоя: включение/выключение G1–G4, режим отказа | [guardrails spec](../openspec/changes/define-agent-platform/specs/guardrails/spec.md) |
| ⬜ | G1 в Runner через OPA | [задача 4.3](tasks/4.3-guardrails-opa.md) |
| ⬜ | G2 в Harness hooks через OPA, human approval | [задача 4.3](tasks/4.3-guardrails-opa.md) |
| ⬜ | G3: профиль контейнера и egress | [задача 4.2](tasks/4.2-egress-repo-access.md) |
| ⬜ | G4: хуки LiteLLM (PII, injection, модерация) | [задача 4.5](tasks/4.5-litellm-budgets-fallback-g4.md) |
| ⬜ | Rego в git с тестами `opa test` | [design D6](../openspec/changes/define-agent-platform/design.md) |
| ⬜ | Аудит срабатываний | [задача 4.3](tasks/4.3-guardrails-opa.md) |

## LiteLLM gw [G4]

| Статус | Задача | Где |
|---|---|---|
| ✅ | LiteLLM развёрнут (`itsaplan-agents`) | `D:\АИ агент\itsaplan-agents` |
| ✅ | Маршрут по алиасу до провайдера проверен | AI-агент, решение 7.1 |
| ⚠️ | ICPlan пока ходит к провайдерам напрямую | AI-агент, решение 7.1 |
| ⬜ | Алиасы, 2+ провайдера, локальная модель | [задача 1.1](tasks/1.1-mock-llm-litellm.md) |
| ⬜ | Virtual key на агента с лимитами и бюджетом | [задача 1.1](tasks/1.1-mock-llm-litellm.md) |
| ⬜ | Fallback-модель | [задача 4.5](tasks/4.5-litellm-budgets-fallback-g4.md) |

## Observability

| Статус | Задача | Где |
|---|---|---|
| ✅ | История запусков в ICPlan (итог) | ICPlan |
| ⬜ | Таблица событий запуска в БД ICPlan | [observability spec](../openspec/changes/define-agent-platform/specs/observability/spec.md) |
| ⬜ | Агрегаты затрат по запуску, задаче, агенту, модели | [задача 3.5](tasks/3.5-icplan-type-actions-cost.md) |
| ⬜ | Срок хранения событий | [задача 3.3](tasks/3.3-run-events-timeline.md) |

## Интеграция (сквозное)

| Статус | Задача | Где |
|---|---|---|
| ⬜ | Конфигурация L0–L3, роли хранилищ, клиенты интерфейсов, поведение при отказах (FMEA) | [задача 2.8](tasks/2.8-config-storage-interfaces-fmea.md) |
| ⬜ | E2E: задача в ICPlan → Runner → агент с MCP и памятью → итог в задаче | [задача 2.6](tasks/2.6-e2e-icplan.md) |
| ⬜ | E2E: смена модели агента без перезапуска | [задача 2.6](tasks/2.6-e2e-icplan.md) |

## Документация

| Статус | Задача | Где |
|---|---|---|
| ✅ | README, гид по чтению, план, бэклог, architecture.md v0.7 | [PLAN этапы 1–2](PLAN.md) |
| ✅ | Спеки: 10 модулей, интеграция, автоподхват | `openspec/changes/` |
| ✅ | Roadmap и документы задач по INVEST с оценками | [ROADMAP](ROADMAP.md) |
| ✅ | `define-agent-platform/tasks.md` обновлён по ROADMAP | [tasks.md](../openspec/changes/define-agent-platform/tasks.md) |
| ⬜ | Переписать спеки `control-plane` и `icplan-integration` | [arch → Доработки](../architecture.md) |
| ⬜ | Карточки компонентов `docs/<компонент>/` | [PLAN этапы 3–4](PLAN.md) |
| ⬜ | Перенос спек в `openspec/specs/`, проверка ссылок | [PLAN этапы 5–7](PLAN.md) |

Отложенное — в [BACKLOG.md](BACKLOG.md).
