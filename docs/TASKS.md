# Сводная таблица задач

← [README](../README.md) · [план документации](PLAN.md) · [бэклог](BACKLOG.md)

По компонентам: сначала выполненное ✅ (и частично ⚠️), затем то, что нужно сделать ⬜. Детали и критерии приёмки — по ссылке в колонке «Где».

Источники: `dap` — [define-agent-platform/tasks.md](../openspec/changes/define-agent-platform/tasks.md), `ap` — [icplan-agent-autopickup/tasks.md](../openspec/changes/icplan-agent-autopickup/tasks.md), `arch` — [architecture.md → Доработки по модулям](../architecture.md).

> ⚠️ `dap/tasks.md` написан до решений v0.7 (Qdrant, Langfuse, Control Plane на Go, push-API Runner). Здесь задачи даны уже по актуальным решениям; сам `tasks.md` нужно обновить.

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
| ⬜ | Версии определения агента, экспорт/импорт YAML | [dap 2.1–2.4](../openspec/changes/define-agent-platform/tasks.md) |
| ⬜ | Allowlist репозиториев агента | [arch → Registry](../architecture.md) |
| ⬜ | Передача в запуске quality gate, лимитов; события approve/вопрос | [arch → Run Queue](../architecture.md) |

## Platform module (модуль ICPlan)

| Статус | Задача | Где |
|---|---|---|
| ⬜ | Модуль в форке ICPlan, своя схема БД | [arch → Platform module](../architecture.md) |
| ⬜ | Алиасы LLM, бюджеты, профили sandbox и памяти | [dap 2.x](../openspec/changes/define-agent-platform/tasks.md) |
| ⬜ | Хранение данных guardrails (allowlist, лимиты) | [dap 8.1](../openspec/changes/define-agent-platform/tasks.md) |
| ⬜ | Экраны настроек в UI ICPlan | [arch → Control Plane UI](../architecture.md) |
| ⬜ | Аутентификация и роли для этих настроек | [dap 2.5](../openspec/changes/define-agent-platform/tasks.md) |

## Agent Runner

| Статус | Задача | Где |
|---|---|---|
| ✅ | Протокол раннера ICPlan как основа (опрос очереди, стрим) | ICPlan `docs/runner.md` |
| ⬜ | Каркас Runner (Go), контракт Runner↔Harness | [dap 1.1, 1.3](../openspec/changes/define-agent-platform/tasks.md) |
| ⬜ | Работа как внешний раннер ICPlan: опрос, стрим, итог | [dap 7.1, 7.3](../openspec/changes/define-agent-platform/tasks.md) |
| ⬜ | Жизненный цикл: claim из пула → Harness → результат → destroy | [dap 7.2](../openspec/changes/define-agent-platform/tasks.md) |
| ⬜ | Таймаут и отмена | [dap 7.4](../openspec/changes/define-agent-platform/tasks.md) |
| ⬜ | Короткоживущий токен репозиториев на запуск | [arch → Рабочие данные](../architecture.md) |

## Sandbox [G3]

| Статус | Задача | Где |
|---|---|---|
| ⚠️ | Локальный k3d-кластер работает (основа для K8s-провайдера) | `D:\АИ агент\Архитектура\infra` |
| ⬜ | `SandboxProvider` + Docker-реализация | [dap 4.1](../openspec/changes/define-agent-platform/tasks.md) |
| ⬜ | Тёплый пул по профилям, одноразовое использование | [arch → Исполнение](../architecture.md) |
| ⬜ | Профили CPU/RAM/disk | [dap 4.2](../openspec/changes/define-agent-platform/tasks.md) |
| ⬜ | Изолированная сеть + egress-прокси с allowlist | [dap 4.3](../openspec/changes/define-agent-platform/tasks.md) |
| ⬜ | Подстановка секретов и токенов прокси | [dap 4.4](../openspec/changes/define-agent-platform/tasks.md) |
| ⬜ | Эфемерный `/workspace`, клон репозиториев, запрет push в защищённые ветки | [arch → Рабочие данные](../architecture.md) |

## Harness [G2]

| Статус | Задача | Где |
|---|---|---|
| ⬜ | Образ Harness, сборка агента из определения | [dap 5.1](../openspec/changes/define-agent-platform/tasks.md) |
| ⬜ | Граф LangGraph `context → llm → tools` | [dap 5.2](../openspec/changes/define-agent-platform/tasks.md) |
| ⬜ | Hooks before/after llm\|tool, on_stop | [dap 5.3](../openspec/changes/define-agent-platform/tasks.md) |
| ⬜ | MCP через адаптер, таймауты тулов | [dap 5.4](../openspec/changes/define-agent-platform/tasks.md) |
| ⬜ | Пауза на approve и возобновление (checkpointer) | [agent-harness spec](../openspec/changes/define-agent-platform/specs/agent-harness/spec.md) |
| ⬜ | Стрим шагов для таймлайна | [agent-harness spec](../openspec/changes/define-agent-platform/specs/agent-harness/spec.md) |
| ⬜ | Управление контекстом и сжатие | [dap 5.5](../openspec/changes/define-agent-platform/tasks.md) |
| ⬜ | Завершение done/limit/error, отдача результата | [dap 5.6](../openspec/changes/define-agent-platform/tasks.md) |

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
| ⬜ | API памяти с проверкой профиля и области видимости | [dap 6.1](../openspec/changes/define-agent-platform/tasks.md) |
| ⬜ | Сроки хранения и админ-удаление | [dap 6.4](../openspec/changes/define-agent-platform/tasks.md) |

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
| ⬜ | G1 в Runner через OPA | [dap 8.2](../openspec/changes/define-agent-platform/tasks.md) |
| ⬜ | G2 в Harness hooks через OPA, human approval | [dap 8.3](../openspec/changes/define-agent-platform/tasks.md) |
| ⬜ | G3: профиль контейнера и egress | [dap 8.4](../openspec/changes/define-agent-platform/tasks.md) |
| ⬜ | G4: хуки LiteLLM (PII, injection, модерация) | [dap 8.5](../openspec/changes/define-agent-platform/tasks.md) |
| ⬜ | Rego в git с тестами `opa test` | [design D6](../openspec/changes/define-agent-platform/design.md) |
| ⬜ | Аудит срабатываний | [dap 8.6](../openspec/changes/define-agent-platform/tasks.md) |

## LiteLLM gw [G4]

| Статус | Задача | Где |
|---|---|---|
| ✅ | LiteLLM развёрнут (`itsaplan-agents`) | `D:\АИ агент\itsaplan-agents` |
| ✅ | Маршрут по алиасу до провайдера проверен | AI-агент, решение 7.1 |
| ⚠️ | ICPlan пока ходит к провайдерам напрямую | AI-агент, решение 7.1 |
| ⬜ | Алиасы, 2+ провайдера, локальная модель | [dap 3.1](../openspec/changes/define-agent-platform/tasks.md) |
| ⬜ | Virtual key на агента с лимитами и бюджетом | [dap 3.2](../openspec/changes/define-agent-platform/tasks.md) |
| ⬜ | Fallback-модель | [dap 3.3](../openspec/changes/define-agent-platform/tasks.md) |

## Observability

| Статус | Задача | Где |
|---|---|---|
| ✅ | История запусков в ICPlan (итог) | ICPlan |
| ⬜ | Таблица событий запуска в БД ICPlan | [observability spec](../openspec/changes/define-agent-platform/specs/observability/spec.md) |
| ⬜ | Агрегаты затрат по запуску, задаче, агенту, модели | [dap 9.2](../openspec/changes/define-agent-platform/tasks.md) |
| ⬜ | Срок хранения событий | [dap 9.3](../openspec/changes/define-agent-platform/tasks.md) |

## Интеграция (сквозное)

| Статус | Задача | Где |
|---|---|---|
| ⬜ | E2E: задача в ICPlan → Runner → агент с MCP и памятью → итог в задаче | [dap 10.1](../openspec/changes/define-agent-platform/tasks.md) |
| ⬜ | E2E: смена модели агента без перезапуска | [dap 10.2](../openspec/changes/define-agent-platform/tasks.md) |

## Документация

| Статус | Задача | Где |
|---|---|---|
| ✅ | README, гид по чтению, план, бэклог, architecture.md v0.7 | [PLAN этапы 1–2](PLAN.md) |
| ✅ | Спеки: 10 модулей, интеграция, автоподхват | `openspec/changes/` |
| ⬜ | Обновить `dap/tasks.md` под решения v0.7 | [dap/tasks.md](../openspec/changes/define-agent-platform/tasks.md) |
| ⬜ | Переписать спеки `control-plane` и `icplan-integration` | [arch → Доработки](../architecture.md) |
| ⬜ | Карточки компонентов `docs/<компонент>/` | [PLAN этапы 3–4](PLAN.md) |
| ⬜ | Перенос спек в `openspec/specs/`, проверка ссылок | [PLAN этапы 5–7](PLAN.md) |

Отложенное — в [BACKLOG.md](BACKLOG.md).
