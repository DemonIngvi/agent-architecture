# Сводная таблица задач

← [README](../README.md) · [план документации](PLAN.md) · [бэклог](BACKLOG.md)

По компонентам: сначала выполненное ✅ (и частично ⚠️), затем то, что нужно сделать ⬜. Детали и критерии приёмки — по ссылке в колонке «Где».

Источники: `ap` — [icplan-agent-autopickup/tasks.md](../openspec/changes/icplan-agent-autopickup/tasks.md), `arch` — [architecture.md → Доработки по модулям](../architecture.md).

Порядок, оценки и документы задач по INVEST — в [ROADMAP](ROADMAP.md).

## ICPlan

| Статус | Задача | Где | Требования |
|---|---|---|---|
| ✅ | Локальный стек ICPlan (web, api, worker, bot, postgres + pgvector, rustfs) | `D:\АИ агент\itsaplan` | [R-INF-12](../openspec/changes/define-agent-platform/specs/platform-infrastructure/spec.md#r-inf-12) |
| ✅ | CRUD агентов: имя, модель, инструкция, проекты | ICPlan: Команда → ИИ-агенты | [R-REG-02](../openspec/changes/define-agent-platform/specs/agent-registry/spec.md#r-reg-02), [R-ICP-08](../openspec/changes/add-icplan-integration/specs/icplan-integration/spec.md#r-icp-08) |
| ✅ | Ключи провайдеров, тулы, навыки, MCP-серверы | ICPlan: Команда → Настройки | [R-LLM-07](../openspec/changes/define-agent-platform/specs/llm-gateway/spec.md#r-llm-07), [R-MCP-01](../openspec/changes/define-agent-platform/specs/tool-integration/spec.md#r-mcp-01), [R-MCP-06](../openspec/changes/define-agent-platform/specs/tool-integration/spec.md#r-mcp-06) |
| ✅ | MCP-сервер `itsaplan-core` (весь REST API как тулы) | ICPlan | [R-MCP-13](../openspec/changes/define-agent-platform/specs/tool-integration/spec.md#r-mcp-13) |
| ✅ | Запуск агента по делегату и по упоминанию | [ap 0.1](../openspec/changes/icplan-agent-autopickup/tasks.md) | [R-AP-23](../openspec/changes/icplan-agent-autopickup/specs/icplan-agent-autopickup/spec.md#r-ap-23) |
| ✅ | Автоназначение исполнителя на статус (без запуска) | [ap 0.2](../openspec/changes/icplan-agent-autopickup/tasks.md) | [R-AP-23](../openspec/changes/icplan-agent-autopickup/specs/icplan-agent-autopickup/spec.md#r-ap-23) |
| ✅ | Агент меняет поля задачи через `update_issue` (колонку задачи в процессе меняет ICPlan) | [ap 0.3](../openspec/changes/icplan-agent-autopickup/tasks.md) | [R-MCP-13](../openspec/changes/define-agent-platform/specs/tool-integration/spec.md#r-mcp-13), [R-AP-16](../openspec/changes/icplan-agent-autopickup/specs/icplan-agent-autopickup/spec.md#r-ap-16) |
| ✅ | Очередь запусков внешнего раннера, стрим ответа | ICPlan `@itsaplan/runner` | [R-ICP-02](../openspec/changes/add-icplan-integration/specs/icplan-integration/spec.md#r-icp-02), [R-ICP-04](../openspec/changes/add-icplan-integration/specs/icplan-integration/spec.md#r-icp-04) |
| ✅ | Ответ агента публикуется комментарием в задаче | Форк `itsaplan-app` (`postRunAnswer`) | [R-ICP-04](../openspec/changes/add-icplan-integration/specs/icplan-integration/spec.md#r-icp-04) |
| ⚠️ | История запусков — только итог, без шагов | [задача 3.3](tasks/3.3-run-events-timeline.md) | [R-ICP-04](../openspec/changes/add-icplan-integration/specs/icplan-integration/spec.md#r-icp-04), [R-OBS-02](../openspec/changes/define-agent-platform/specs/observability/spec.md#r-obs-02) |
| ⬜ | Агент шага процесса: колонка → делегат → запуск | [ap 1.1–1.3](../openspec/changes/icplan-agent-autopickup/tasks.md) | [R-AP-01](../openspec/changes/icplan-agent-autopickup/specs/icplan-agent-autopickup/spec.md#r-ap-01), [R-AP-15](../openspec/changes/icplan-agent-autopickup/specs/icplan-agent-autopickup/spec.md#r-ap-15) |
| ⬜ | Тип задачи задаёт процесс: первый шаг при создании и смене типа | [ap 2.1–2.3](../openspec/changes/icplan-agent-autopickup/tasks.md) | [R-AP-02](../openspec/changes/icplan-agent-autopickup/specs/icplan-agent-autopickup/spec.md#r-ap-02) |
| ⬜ | Эффект Действия «делегировать агенту» (T-04) | [ap 3.1–3.2](../openspec/changes/icplan-agent-autopickup/tasks.md) | [R-AP-03](../openspec/changes/icplan-agent-autopickup/specs/icplan-agent-autopickup/spec.md#r-ap-03) |
| ⬜ | Приоритет правил, защита от дублей, очистка при выходе агента | [ap 4.1–4.3](../openspec/changes/icplan-agent-autopickup/tasks.md) | [R-AP-04](../openspec/changes/icplan-agent-autopickup/specs/icplan-agent-autopickup/spec.md#r-ap-04), [R-AP-05](../openspec/changes/icplan-agent-autopickup/specs/icplan-agent-autopickup/spec.md#r-ap-05), [R-AP-08](../openspec/changes/icplan-agent-autopickup/specs/icplan-agent-autopickup/spec.md#r-ap-08) |
| ⬜ | Передача итога следующему агенту, запись в истории | [ap 5.1–5.2](../openspec/changes/icplan-agent-autopickup/tasks.md) | [R-AP-06](../openspec/changes/icplan-agent-autopickup/specs/icplan-agent-autopickup/spec.md#r-ap-06), [R-AP-07](../openspec/changes/icplan-agent-autopickup/specs/icplan-agent-autopickup/spec.md#r-ap-07) |
| ⬜ | Процесс: переходы по итогу запуска, лимит шага, очередь агента | [задача 3.6](tasks/3.6-icplan-process-engine.md) | [R-AP-16](../openspec/changes/icplan-agent-autopickup/specs/icplan-agent-autopickup/spec.md#r-ap-16), [R-AP-17](../openspec/changes/icplan-agent-autopickup/specs/icplan-agent-autopickup/spec.md#r-ap-17) |
| ⬜ | Управление ходом задачи: проверка, вердикт, остановка, повтор шага, версии процесса | [задача 3.7](tasks/3.7-icplan-task-control.md) | [R-AP-18](../openspec/changes/icplan-agent-autopickup/specs/icplan-agent-autopickup/spec.md#r-ap-18), [R-AP-19](../openspec/changes/icplan-agent-autopickup/specs/icplan-agent-autopickup/spec.md#r-ap-19), [R-AP-20](../openspec/changes/icplan-agent-autopickup/specs/icplan-agent-autopickup/spec.md#r-ap-20), [R-AP-21](../openspec/changes/icplan-agent-autopickup/specs/icplan-agent-autopickup/spec.md#r-ap-21), [R-AP-22](../openspec/changes/icplan-agent-autopickup/specs/icplan-agent-autopickup/spec.md#r-ap-22) |
| ⬜ | Чат с агентом, указания во время работы, выключение агента | [задача 3.8](tasks/3.8-agent-chat-control.md) | [R-ICP-16](../openspec/changes/add-icplan-integration/specs/icplan-integration/spec.md#r-icp-16), [R-ICP-17](../openspec/changes/add-icplan-integration/specs/icplan-integration/spec.md#r-icp-17), [R-ICP-18](../openspec/changes/add-icplan-integration/specs/icplan-integration/spec.md#r-icp-18), [R-HRN-16](../openspec/changes/define-agent-platform/specs/agent-harness/spec.md#r-hrn-16) |
| ⬜ | Сводка задач с агентами и статистика агентов | [задача 3.9](tasks/3.9-agent-summary-stats.md) | [R-OBS-13](../openspec/changes/define-agent-platform/specs/observability/spec.md#r-obs-13) |
| ⬜ | Approve действия агента в UI | [задача 3.4](tasks/3.4-icplan-approve-ui.md), [задача 1.5](tasks/1.5-harness-hooks-approve.md) | [R-ICP-05](../openspec/changes/add-icplan-integration/specs/icplan-integration/spec.md#r-icp-05), [R-ICP-06](../openspec/changes/add-icplan-integration/specs/icplan-integration/spec.md#r-icp-06), [R-HRN-05](../openspec/changes/define-agent-platform/specs/agent-harness/spec.md#r-hrn-05) |
| ⬜ | Результат quality gate в задаче | [задача 1.6](tasks/1.6-harness-limits-context.md), [задача 3.3](tasks/3.3-run-events-timeline.md) | [R-HRN-08](../openspec/changes/define-agent-platform/specs/agent-harness/spec.md#r-hrn-08), [R-ICP-04](../openspec/changes/add-icplan-integration/specs/icplan-integration/spec.md#r-icp-04) |
| ⬜ | Пошаговый таймлайн запуска в задаче | [задача 3.3](tasks/3.3-run-events-timeline.md) | [R-OBS-02](../openspec/changes/define-agent-platform/specs/observability/spec.md#r-obs-02), [R-ICP-04](../openspec/changes/add-icplan-integration/specs/icplan-integration/spec.md#r-icp-04) |
| ⬜ | Затраты по задаче | [задача 3.5](tasks/3.5-icplan-type-actions-cost.md) | [R-OBS-05](../openspec/changes/define-agent-platform/specs/observability/spec.md#r-obs-05), [R-LLM-03](../openspec/changes/define-agent-platform/specs/llm-gateway/spec.md#r-llm-03) |
| ⬜ | Версии определения агента, экспорт/импорт YAML | [задача 1.2](tasks/1.2-agent-definition-yaml.md) | [R-CP-04](../openspec/changes/define-agent-platform/specs/control-plane/spec.md#r-cp-04), [R-CP-05](../openspec/changes/define-agent-platform/specs/control-plane/spec.md#r-cp-05), [R-REG-03](../openspec/changes/define-agent-platform/specs/agent-registry/spec.md#r-reg-03), [R-REG-04](../openspec/changes/define-agent-platform/specs/agent-registry/spec.md#r-reg-04) |
| ⬜ | Allowlist репозиториев агента | [задача 4.4](tasks/4.4-platform-module.md), [задача 4.2](tasks/4.2-egress-repo-access.md) | [R-CP-01](../openspec/changes/define-agent-platform/specs/control-plane/spec.md#r-cp-01), [R-SBX-04](../openspec/changes/define-agent-platform/specs/agent-sandbox/spec.md#r-sbx-04) |
| ⬜ | Передача в запуске quality gate, лимитов; события approve/вопрос | [задача 2.3](tasks/2.3-config-from-icplan.md), [задача 2.8](tasks/2.8-config-storage-interfaces-fmea.md), [задача 3.4](tasks/3.4-icplan-approve-ui.md) | [R-ICP-02](../openspec/changes/add-icplan-integration/specs/icplan-integration/spec.md#r-icp-02), [R-ICP-05](../openspec/changes/add-icplan-integration/specs/icplan-integration/spec.md#r-icp-05), [R-HRN-08](../openspec/changes/define-agent-platform/specs/agent-harness/spec.md#r-hrn-08) |

## Platform module (модуль ICPlan)

| Статус | Задача | Где | Требования |
|---|---|---|---|
| ⬜ | Модуль в форке ICPlan, своя схема БД | [задача 4.4](tasks/4.4-platform-module.md) | [R-CP-02](../openspec/changes/define-agent-platform/specs/control-plane/spec.md#r-cp-02), [R-CP-09](../openspec/changes/define-agent-platform/specs/control-plane/spec.md#r-cp-09) |
| ⬜ | Алиасы LLM, бюджеты, профили sandbox и памяти | [задача 4.4](tasks/4.4-platform-module.md) | [R-CP-01](../openspec/changes/define-agent-platform/specs/control-plane/spec.md#r-cp-01), [R-LLM-01](../openspec/changes/define-agent-platform/specs/llm-gateway/spec.md#r-llm-01), [R-GRD-11](../openspec/changes/define-agent-platform/specs/guardrails/spec.md#r-grd-11), [R-SBX-05](../openspec/changes/define-agent-platform/specs/agent-sandbox/spec.md#r-sbx-05) |
| ⬜ | Хранение данных guardrails (allowlist, лимиты) | [задача 4.4](tasks/4.4-platform-module.md) | [R-CP-01](../openspec/changes/define-agent-platform/specs/control-plane/spec.md#r-cp-01), [R-GRD-01](../openspec/changes/define-agent-platform/specs/guardrails/spec.md#r-grd-01) |
| ⬜ | Экраны настроек в UI ICPlan | [задача 4.4](tasks/4.4-platform-module.md) | [R-CP-01](../openspec/changes/define-agent-platform/specs/control-plane/spec.md#r-cp-01) |
| ⬜ | Аутентификация и роли для этих настроек | [задача 4.4](tasks/4.4-platform-module.md) | [R-CP-07](../openspec/changes/define-agent-platform/specs/control-plane/spec.md#r-cp-07) |

## Agent Runner

| Статус | Задача | Где | Требования |
|---|---|---|---|
| ✅ | Протокол раннера ICPlan как основа (опрос очереди, стрим) | ICPlan `docs/runner.md` | [R-ICP-02](../openspec/changes/add-icplan-integration/specs/icplan-integration/spec.md#r-icp-02), [R-RUN-01](../openspec/changes/define-agent-platform/specs/agent-runner/spec.md#r-run-01) |
| ⬜ | Каркас Runner (Go), контракт Runner↔Harness | [задача 2.1](tasks/2.1-runner-external.md) | [R-RUN-01](../openspec/changes/define-agent-platform/specs/agent-runner/spec.md#r-run-01), [R-RUN-13](../openspec/changes/define-agent-platform/specs/agent-runner/spec.md#r-run-13) |
| ⬜ | Работа как внешний раннер ICPlan: опрос, стрим, итог | [задача 2.1](tasks/2.1-runner-external.md) | [R-ICP-01](../openspec/changes/add-icplan-integration/specs/icplan-integration/spec.md#r-icp-01), [R-ICP-02](../openspec/changes/add-icplan-integration/specs/icplan-integration/spec.md#r-icp-02), [R-ICP-04](../openspec/changes/add-icplan-integration/specs/icplan-integration/spec.md#r-icp-04), [R-RUN-08](../openspec/changes/define-agent-platform/specs/agent-runner/spec.md#r-run-08) |
| ⬜ | Жизненный цикл: claim из пула → Harness → результат → destroy | [задача 2.2](tasks/2.2-sandbox-docker-oneshot.md) | [R-SBX-01](../openspec/changes/define-agent-platform/specs/agent-sandbox/spec.md#r-sbx-01), [R-SBX-02](../openspec/changes/define-agent-platform/specs/agent-sandbox/spec.md#r-sbx-02), [R-RUN-10](../openspec/changes/define-agent-platform/specs/agent-runner/spec.md#r-run-10) |
| ⬜ | Планировщик: слоты, режим sequential / parallel, один запуск на задачу | [задача 2.7](tasks/2.7-runner-scheduler.md) | [R-RUN-02](../openspec/changes/define-agent-platform/specs/agent-runner/spec.md#r-run-02), [R-RUN-03](../openspec/changes/define-agent-platform/specs/agent-runner/spec.md#r-run-03), [R-RUN-04](../openspec/changes/define-agent-platform/specs/agent-runner/spec.md#r-run-04), [R-RUN-05](../openspec/changes/define-agent-platform/specs/agent-runner/spec.md#r-run-05), [R-RUN-06](../openspec/changes/define-agent-platform/specs/agent-runner/spec.md#r-run-06) |
| ⬜ | Таймаут и отмена | [задача 2.1](tasks/2.1-runner-external.md) | [R-RUN-09](../openspec/changes/define-agent-platform/specs/agent-runner/spec.md#r-run-09), [R-ICP-07](../openspec/changes/add-icplan-integration/specs/icplan-integration/spec.md#r-icp-07), [R-GRD-10](../openspec/changes/define-agent-platform/specs/guardrails/spec.md#r-grd-10) |
| ⬜ | Короткоживущий токен репозиториев на запуск | [задача 4.2](tasks/4.2-egress-repo-access.md) | [R-SBX-04](../openspec/changes/define-agent-platform/specs/agent-sandbox/spec.md#r-sbx-04), [R-SBX-07](../openspec/changes/define-agent-platform/specs/agent-sandbox/spec.md#r-sbx-07) |

## Sandbox [G3]

| Статус | Задача | Где | Требования |
|---|---|---|---|
| ⚠️ | Локальный k3d-кластер работает (основа для K8s-провайдера) | [задача 4.6](tasks/4.6-k8s-helm-ingress.md) | [R-INF-12](../openspec/changes/define-agent-platform/specs/platform-infrastructure/spec.md#r-inf-12) |
| ⬜ | `SandboxProvider` + Docker-реализация | [задача 2.2](tasks/2.2-sandbox-docker-oneshot.md) | [R-SBX-01](../openspec/changes/define-agent-platform/specs/agent-sandbox/spec.md#r-sbx-01) |
| ⬜ | Тёплый пул по профилям, одноразовое использование | [задача 4.1](tasks/4.1-sandbox-warm-pool.md) | [R-SBX-02](../openspec/changes/define-agent-platform/specs/agent-sandbox/spec.md#r-sbx-02) |
| ⬜ | Профили CPU/RAM/disk | [задача 4.1](tasks/4.1-sandbox-warm-pool.md) | [R-SBX-05](../openspec/changes/define-agent-platform/specs/agent-sandbox/spec.md#r-sbx-05) |
| ⬜ | Изолированная сеть + egress-прокси с allowlist | [задача 4.2](tasks/4.2-egress-repo-access.md) | [R-SBX-06](../openspec/changes/define-agent-platform/specs/agent-sandbox/spec.md#r-sbx-06), [R-GRD-04](../openspec/changes/define-agent-platform/specs/guardrails/spec.md#r-grd-04) |
| ⬜ | Подстановка секретов и токенов прокси | [задача 4.2](tasks/4.2-egress-repo-access.md) | [R-SBX-07](../openspec/changes/define-agent-platform/specs/agent-sandbox/spec.md#r-sbx-07) |
| ⬜ | Эфемерный `/workspace`, клон репозиториев, запрет push в защищённые ветки | [задача 2.2](tasks/2.2-sandbox-docker-oneshot.md), [задача 4.2](tasks/4.2-egress-repo-access.md) | [R-SBX-03](../openspec/changes/define-agent-platform/specs/agent-sandbox/spec.md#r-sbx-03), [R-SBX-04](../openspec/changes/define-agent-platform/specs/agent-sandbox/spec.md#r-sbx-04) |

## Harness [G2]

| Статус | Задача | Где | Требования |
|---|---|---|---|
| ⬜ | Образ Harness, сборка агента из определения | [задача 1.3](tasks/1.3-harness-core.md) | [R-HRN-01](../openspec/changes/define-agent-platform/specs/agent-harness/spec.md#r-hrn-01) |
| ⬜ | Граф LangGraph `context → llm → tools` | [задача 1.3](tasks/1.3-harness-core.md) | [R-HRN-02](../openspec/changes/define-agent-platform/specs/agent-harness/spec.md#r-hrn-02), [R-HRN-03](../openspec/changes/define-agent-platform/specs/agent-harness/spec.md#r-hrn-03) |
| ⬜ | Hooks before/after llm\|tool, on_stop | [задача 1.5](tasks/1.5-harness-hooks-approve.md) | [R-HRN-04](../openspec/changes/define-agent-platform/specs/agent-harness/spec.md#r-hrn-04) |
| ⬜ | MCP через адаптер, таймауты тулов | [задача 1.4](tasks/1.4-harness-mcp-tools.md) | [R-MCP-03](../openspec/changes/define-agent-platform/specs/tool-integration/spec.md#r-mcp-03) |
| ⬜ | Пауза на approve и возобновление (checkpointer) | [задача 1.5](tasks/1.5-harness-hooks-approve.md) | [R-HRN-05](../openspec/changes/define-agent-platform/specs/agent-harness/spec.md#r-hrn-05) |
| ⬜ | Стрим шагов для таймлайна | [задача 1.3](tasks/1.3-harness-core.md) | [R-HRN-06](../openspec/changes/define-agent-platform/specs/agent-harness/spec.md#r-hrn-06) |
| ⬜ | Управление контекстом и сжатие | [задача 1.6](tasks/1.6-harness-limits-context.md) | [R-HRN-07](../openspec/changes/define-agent-platform/specs/agent-harness/spec.md#r-hrn-07) |
| ⬜ | Завершение done/limit/error, отдача результата | [задача 1.6](tasks/1.6-harness-limits-context.md) | [R-HRN-09](../openspec/changes/define-agent-platform/specs/agent-harness/spec.md#r-hrn-09) |

## Memory (M0–M6)

| Статус | Задача | Где | Требования |
|---|---|---|---|
| ✅ | M0 рабочая — в каждом запуске | [arch → Память](../architecture.md) | [R-MEM-01](../openspec/changes/define-agent-platform/specs/agent-memory/spec.md#r-mem-01) |
| ✅ | M1 сессионная — тред в БД ICPlan | [arch → Память](../architecture.md) | [R-MEM-01](../openspec/changes/define-agent-platform/specs/agent-memory/spec.md#r-mem-01), [R-MEM-03](../openspec/changes/define-agent-platform/specs/agent-memory/spec.md#r-mem-03) |
| ✅ | M2 эпизодическая — `agent_run` в БД | [arch → Память](../architecture.md) | [R-MEM-01](../openspec/changes/define-agent-platform/specs/agent-memory/spec.md#r-mem-01), [R-MEM-03](../openspec/changes/define-agent-platform/specs/agent-memory/spec.md#r-mem-03) |
| ✅ | M5 процедурная — инструкция и навыки | [arch → Память](../architecture.md) | [R-MEM-01](../openspec/changes/define-agent-platform/specs/agent-memory/spec.md#r-mem-01) |
| ✅ | M6 организационная — документы, `get_document` | [arch → Память](../architecture.md) | [R-MEM-01](../openspec/changes/define-agent-platform/specs/agent-memory/spec.md#r-mem-01) |
| ⬜ | M3 задачная: тул записи + подача в контекст (первым) | [задача 2.5](tasks/2.5-memory-m2-m3.md) | [R-MEM-04](../openspec/changes/define-agent-platform/specs/agent-memory/spec.md#r-mem-04) |
| ⬜ | M2 в контекст: итоги последних N запусков задачи | [задача 2.5](tasks/2.5-memory-m2-m3.md) | [R-MEM-05](../openspec/changes/define-agent-platform/specs/agent-memory/spec.md#r-mem-05) |
| ⬜ | API памяти с проверкой профиля и области видимости | [задача 2.5](tasks/2.5-memory-m2-m3.md) | [R-MEM-02](../openspec/changes/define-agent-platform/specs/agent-memory/spec.md#r-mem-02), [R-MEM-07](../openspec/changes/define-agent-platform/specs/agent-memory/spec.md#r-mem-07) |
| ⬜ | Сроки хранения и админ-удаление | [задача 2.5](tasks/2.5-memory-m2-m3.md) | [R-MEM-07](../openspec/changes/define-agent-platform/specs/agent-memory/spec.md#r-mem-07), [R-MEM-08](../openspec/changes/define-agent-platform/specs/agent-memory/spec.md#r-mem-08) |

## MCP / Tools

| Статус | Задача | Где | Требования |
|---|---|---|---|
| ✅ | MCP-серверы, тулы и навыки в ICPlan | ICPlan | [R-MCP-01](../openspec/changes/define-agent-platform/specs/tool-integration/spec.md#r-mcp-01), [R-MCP-06](../openspec/changes/define-agent-platform/specs/tool-integration/spec.md#r-mcp-06) |
| ⬜ | Передача списка тулов/MCP из ICPlan в Harness | [задача 2.3](tasks/2.3-config-from-icplan.md), [задача 1.4](tasks/1.4-harness-mcp-tools.md) | [R-MCP-02](../openspec/changes/define-agent-platform/specs/tool-integration/spec.md#r-mcp-02) |
| ⬜ | MCP git-провайдера (Gitea / GitHub) | [задача 4.2](tasks/4.2-egress-repo-access.md) | [R-MCP-01](../openspec/changes/define-agent-platform/specs/tool-integration/spec.md#r-mcp-01), [R-SBX-04](../openspec/changes/define-agent-platform/specs/agent-sandbox/spec.md#r-sbx-04) |
| ⬜ | Тул памяти (запись M3) | [задача 2.5](tasks/2.5-memory-m2-m3.md) | [R-MEM-04](../openspec/changes/define-agent-platform/specs/agent-memory/spec.md#r-mem-04) |
| ⬜ | Правила R1–R7: MCP или прямой вызов | [задача 1.4](tasks/1.4-harness-mcp-tools.md) | [R-MCP-04](../openspec/changes/define-agent-platform/specs/tool-integration/spec.md#r-mcp-04) |

## Guardrails [G1–G4]

| Статус | Задача | Где | Требования |
|---|---|---|---|
| ⚠️ | Контейнер OPA развёрнут, не подключён | [задача 4.3](tasks/4.3-guardrails-opa.md) | [R-GRD-07](../openspec/changes/define-agent-platform/specs/guardrails/spec.md#r-grd-07) |
| ⬜ | Конфиг деплоя: включение/выключение G1–G4, режим отказа | [задача 4.3](tasks/4.3-guardrails-opa.md) | [R-GRD-06](../openspec/changes/define-agent-platform/specs/guardrails/spec.md#r-grd-06), [R-GRD-17](../openspec/changes/define-agent-platform/specs/guardrails/spec.md#r-grd-17) |
| ⬜ | G1 в Runner через OPA | [задача 4.3](tasks/4.3-guardrails-opa.md) | [R-GRD-02](../openspec/changes/define-agent-platform/specs/guardrails/spec.md#r-grd-02), [R-GRD-07](../openspec/changes/define-agent-platform/specs/guardrails/spec.md#r-grd-07) |
| ⬜ | G2 в Harness hooks через OPA, human approval | [задача 4.3](tasks/4.3-guardrails-opa.md) | [R-GRD-03](../openspec/changes/define-agent-platform/specs/guardrails/spec.md#r-grd-03), [R-GRD-07](../openspec/changes/define-agent-platform/specs/guardrails/spec.md#r-grd-07), [R-GRD-08](../openspec/changes/define-agent-platform/specs/guardrails/spec.md#r-grd-08) |
| ⬜ | G3: профиль контейнера и egress | [задача 4.2](tasks/4.2-egress-repo-access.md) | [R-GRD-04](../openspec/changes/define-agent-platform/specs/guardrails/spec.md#r-grd-04), [R-SBX-06](../openspec/changes/define-agent-platform/specs/agent-sandbox/spec.md#r-sbx-06) |
| ⬜ | G4: хуки LiteLLM (PII, injection, модерация) | [задача 4.5](tasks/4.5-litellm-budgets-fallback-g4.md) | [R-GRD-05](../openspec/changes/define-agent-platform/specs/guardrails/spec.md#r-grd-05) |
| ⬜ | Rego в git с тестами `opa test` | [задача 4.3](tasks/4.3-guardrails-opa.md) | [R-GRD-01](../openspec/changes/define-agent-platform/specs/guardrails/spec.md#r-grd-01) |
| ⬜ | Аудит срабатываний | [задача 4.3](tasks/4.3-guardrails-opa.md) | [R-GRD-16](../openspec/changes/define-agent-platform/specs/guardrails/spec.md#r-grd-16) |

## LiteLLM gw [G4]

| Статус | Задача | Где | Требования |
|---|---|---|---|
| ✅ | LiteLLM развёрнут (`itsaplan-agents`) | `D:\АИ агент\itsaplan-agents` | [R-LLM-13](../openspec/changes/define-agent-platform/specs/llm-gateway/spec.md#r-llm-13) |
| ✅ | Маршрут по алиасу до провайдера проверен | AI-агент, решение 7.1 | [R-LLM-01](../openspec/changes/define-agent-platform/specs/llm-gateway/spec.md#r-llm-01) |
| ⚠️ | ICPlan пока ходит к провайдерам напрямую | [задача 2.3](tasks/2.3-config-from-icplan.md) | [R-HRN-03](../openspec/changes/define-agent-platform/specs/agent-harness/spec.md#r-hrn-03), [R-LLM-07](../openspec/changes/define-agent-platform/specs/llm-gateway/spec.md#r-llm-07) |
| ⬜ | Алиасы, 2+ провайдера, локальная модель | [задача 1.1](tasks/1.1-mock-llm-litellm.md) | [R-LLM-01](../openspec/changes/define-agent-platform/specs/llm-gateway/spec.md#r-llm-01), [R-LLM-07](../openspec/changes/define-agent-platform/specs/llm-gateway/spec.md#r-llm-07) |
| ⬜ | Virtual key на агента с лимитами и бюджетом | [задача 1.1](tasks/1.1-mock-llm-litellm.md) | [R-LLM-02](../openspec/changes/define-agent-platform/specs/llm-gateway/spec.md#r-llm-02), [R-LLM-03](../openspec/changes/define-agent-platform/specs/llm-gateway/spec.md#r-llm-03), [R-LLM-05](../openspec/changes/define-agent-platform/specs/llm-gateway/spec.md#r-llm-05), [R-GRD-11](../openspec/changes/define-agent-platform/specs/guardrails/spec.md#r-grd-11) |
| ⬜ | Fallback-модель | [задача 4.5](tasks/4.5-litellm-budgets-fallback-g4.md) | [R-LLM-06](../openspec/changes/define-agent-platform/specs/llm-gateway/spec.md#r-llm-06) |

## Observability

| Статус | Задача | Где | Требования |
|---|---|---|---|
| ✅ | История запусков в ICPlan (итог) | ICPlan | [R-OBS-01](../openspec/changes/define-agent-platform/specs/observability/spec.md#r-obs-01) |
| ⬜ | Таблица событий запуска в БД ICPlan | [задача 3.3](tasks/3.3-run-events-timeline.md) | [R-OBS-01](../openspec/changes/define-agent-platform/specs/observability/spec.md#r-obs-01), [R-OBS-08](../openspec/changes/define-agent-platform/specs/observability/spec.md#r-obs-08) |
| ⬜ | Агрегаты затрат по запуску, задаче, агенту, модели | [задача 3.5](tasks/3.5-icplan-type-actions-cost.md) | [R-OBS-05](../openspec/changes/define-agent-platform/specs/observability/spec.md#r-obs-05), [R-LLM-03](../openspec/changes/define-agent-platform/specs/llm-gateway/spec.md#r-llm-03) |
| ⬜ | Срок хранения событий | [задача 3.3](tasks/3.3-run-events-timeline.md) | [R-OBS-06](../openspec/changes/define-agent-platform/specs/observability/spec.md#r-obs-06) |

## Инфраструктура

| Статус | Задача | Где | Требования |
|---|---|---|---|
| ⚠️ | Локальный k3d-кластер, чарты `itsaplan`, `litellm`, `platform-infra`, Traefik с клиентским сертификатом (проект AI-агент 7.11–7.14) | [задача 4.6](tasks/4.6-k8s-helm-ingress.md) | [R-INF-12](../openspec/changes/define-agent-platform/specs/platform-infrastructure/spec.md#r-inf-12), [R-INF-03](../openspec/changes/define-agent-platform/specs/platform-infrastructure/spec.md#r-inf-03) |
| ⚠️ | Postgres 17 + pgvector и RustFS в compose ICPlan | [задача 4.7](tasks/4.7-postgres-storage-backup.md) | [R-INF-06](../openspec/changes/define-agent-platform/specs/platform-infrastructure/spec.md#r-inf-06), [R-INF-07](../openspec/changes/define-agent-platform/specs/platform-infrastructure/spec.md#r-inf-07) |
| ⬜ | k3s, Helm, namespaces, Traefik, сетевые политики | [задача 4.6](tasks/4.6-k8s-helm-ingress.md) | [R-INF-02](../openspec/changes/define-agent-platform/specs/platform-infrastructure/spec.md#r-inf-02), [R-INF-03](../openspec/changes/define-agent-platform/specs/platform-infrastructure/spec.md#r-inf-03), [R-INF-04](../openspec/changes/define-agent-platform/specs/platform-infrastructure/spec.md#r-inf-04), [R-INF-10](../openspec/changes/define-agent-platform/specs/platform-infrastructure/spec.md#r-inf-10) |
| ⬜ | CloudNativePG, PgBouncer, RustFS, бэкап вне узла | [задача 4.7](tasks/4.7-postgres-storage-backup.md) | [R-INF-06](../openspec/changes/define-agent-platform/specs/platform-infrastructure/spec.md#r-inf-06), [R-INF-07](../openspec/changes/define-agent-platform/specs/platform-infrastructure/spec.md#r-inf-07), [R-INF-08](../openspec/changes/define-agent-platform/specs/platform-infrastructure/spec.md#r-inf-08) |
| ⬜ | Нагрузочный тест и подтверждение профиля | [задача 4.8](tasks/4.8-load-test.md) | [R-INF-01](../openspec/changes/define-agent-platform/specs/platform-infrastructure/spec.md#r-inf-01), [R-INF-17](../openspec/changes/define-agent-platform/specs/platform-infrastructure/spec.md#r-inf-17) |

## Интеграция (сквозное)

| Статус | Задача | Где | Требования |
|---|---|---|---|
| ⬜ | Общий резолвер конфигурации L0–L3 (своя конфигурация, хранилища, интерфейсы, отказы — в задачах компонентов) | [задача 2.8](tasks/2.8-config-storage-interfaces-fmea.md) | [R-HRN-10](../openspec/changes/define-agent-platform/specs/agent-harness/spec.md#r-hrn-10), [R-MEM-09](../openspec/changes/define-agent-platform/specs/agent-memory/spec.md#r-mem-09), [R-RUN-11](../openspec/changes/define-agent-platform/specs/agent-runner/spec.md#r-run-11), [R-SBX-08](../openspec/changes/define-agent-platform/specs/agent-sandbox/spec.md#r-sbx-08), [R-MCP-07](../openspec/changes/define-agent-platform/specs/tool-integration/spec.md#r-mcp-07) |
| ⬜ | E2E: задача в ICPlan → Runner → агент с MCP и памятью → итог в задаче | [задача 2.6](tasks/2.6-e2e-icplan.md) | [R-ICP-01](../openspec/changes/add-icplan-integration/specs/icplan-integration/spec.md#r-icp-01), [R-ICP-04](../openspec/changes/add-icplan-integration/specs/icplan-integration/spec.md#r-icp-04), [R-RUN-08](../openspec/changes/define-agent-platform/specs/agent-runner/spec.md#r-run-08), [R-MEM-05](../openspec/changes/define-agent-platform/specs/agent-memory/spec.md#r-mem-05) |
| ⬜ | E2E: смена модели агента без перезапуска | [задача 2.6](tasks/2.6-e2e-icplan.md) | [R-REG-06](../openspec/changes/define-agent-platform/specs/agent-registry/spec.md#r-reg-06), [R-CP-03](../openspec/changes/define-agent-platform/specs/control-plane/spec.md#r-cp-03) |

## Документация

| Статус | Задача | Где | Требования |
|---|---|---|---|
| ⬜ | Довести 17 R&D до методологии v2: обязательные условия и отсев, сценарии, шкалы с якорями, чувствительность | [методология R&D](rules/rnd-methodology.md) | — (документация) |
| ✅ | README, гид по чтению, план, бэклог, architecture.md v0.7 | [PLAN этапы 1–2](PLAN.md) | — (документация) |
| ✅ | Спеки: 10 модулей, интеграция, автоподхват | `openspec/changes/` | — (документация) |
| ✅ | Roadmap и документы задач по INVEST с оценками | [ROADMAP](ROADMAP.md) | — (документация) |
| ✅ | `define-agent-platform/tasks.md` обновлён по ROADMAP | [tasks.md](../openspec/changes/define-agent-platform/tasks.md) | — (документация) |
| ✅ | Переписать спеки `control-plane` и `icplan-integration` | [control-plane](../openspec/changes/define-agent-platform/specs/control-plane/spec.md), [icplan-integration](../openspec/changes/add-icplan-integration/specs/icplan-integration/spec.md) | — (документация) |
| ⬜ | Карточки компонентов `docs/<компонент>/` | [PLAN этапы 3–4](PLAN.md) | — (документация) |
| ⬜ | Перенос спек в `openspec/specs/`, проверка ссылок | [PLAN этапы 5–7](PLAN.md) | — (документация) |

Отложенное — в [BACKLOG.md](BACKLOG.md).
