# Подтверждения документов

← [Методология подтверждений](rules/approval-methodology.md) · [сводная таблица](approvals-summary.md)

Реестр ведёт сборка и `./tools/doc approve`; руками не правится. ⏳ — ждёт роли; ✅ — подтверждено; ❌ — отказ (причина в комментарии); решение сбрасывается в ⏳, если текст документа изменился (столбец «Версия»).

| Документ | Роль | Кто | 👤 / 🤖 | Дата | Решение | Версия | Комментарий |
|---|---|---|---|---|---|---|---|
| `components/agent-runner/admission/index.md` | А | Claude, роль Архитектор | 🤖 | 2026-10-13 | ✅ | fa70872d | Связи и владельцы данных определены |
| `components/agent-runner/admission/index.md` | Р | Claude, роль Разработчик | 🤖 | 2026-10-13 | ✅ | fa70872d | Операция, параметры, входы и выходы есть |
| `components/agent-runner/admission/index.md` | Т | Claude, роль Тестировщик | 🤖 | 2026-10-13 | ✅ | fa70872d | Сценарии и сбои проверяемы |
| `components/agent-runner/event-relay/index.md` | А | Claude, роль Архитектор | 🤖 | 2026-10-13 | ✅ | 82ab334c | Границы с ICPlan заданы |
| `components/agent-runner/event-relay/index.md` | Р | Claude, роль Разработчик | 🤖 | 2026-10-13 | ✅ | 82ab334c | Операции и потоки описаны |
| `components/agent-runner/event-relay/index.md` | Т | Claude, роль Тестировщик | 🤖 | 2026-10-13 | ✅ | 82ab334c | Поведение при сбое задано |
| `components/agent-runner/finalizer/index.md` | А | — | — | — | ⏳ | f9b1050b | текст изменён после решения «✅» от Claude, роль Архитектор |
| `components/agent-runner/finalizer/index.md` | Р | — | — | — | ⏳ | f9b1050b | текст изменён после решения «✅» от Claude, роль Разработчик |
| `components/agent-runner/finalizer/index.md` | Т | — | — | — | ⏳ | f9b1050b | текст изменён после решения «✅» от Claude, роль Тестировщик |
| `components/agent-runner/index.md` | А | Claude, роль Архитектор | 🤖 | 2026-10-13 | ✅ | 7222f959 | C1/sequence, I-коды, D23/D19, таблица статусов R-HRN-09→R-RUN-07→agent_run, +/- есть; границы с ICPlan/Platform/Sandbox определены |
| `components/agent-runner/index.md` | Р | Claude, роль Разработчик | 🤖 | 2026-10-13 | ✅ | 7222f959 | порядок работы с I-кодами и моделями, статусы и переходы, ссылки на Deploy/интеграции — реализуемо |
| `components/agent-runner/mcp-proksi/index.md` | А | Claude, роль Архитектор | 🤖 | 2026-10-13 | ✅ | 5e8f8a4b | Граница с OPA и MCP ясна |
| `components/agent-runner/mcp-proksi/index.md` | Р | Claude, роль Разработчик | 🤖 | 2026-10-13 | ✅ | 5e8f8a4b | Операции и параметры есть |
| `components/agent-runner/mcp-proksi/index.md` | Т | Claude, роль Тестировщик | 🤖 | 2026-10-13 | ✅ | 5e8f8a4b | Отказы проверяемы |
| `components/agent-runner/poller/index.md` | А | — | — | — | ⏳ | 48ce759f | текст изменён после решения «✅» от Claude, роль Архитектор |
| `components/agent-runner/poller/index.md` | Р | — | — | — | ⏳ | 48ce759f | текст изменён после решения «✅» от Claude, роль Разработчик |
| `components/agent-runner/poller/index.md` | Т | — | — | — | ⏳ | 48ce759f | текст изменён после решения «✅» от Claude, роль Тестировщик |
| `components/agent-runner/run-supervisor/index.md` | А | — | — | — | ⏳ | 74c7e38f | текст изменён после решения «✅» от Claude, роль Архитектор |
| `components/agent-runner/run-supervisor/index.md` | Р | — | — | — | ⏳ | 74c7e38f | текст изменён после решения «✅» от Claude, роль Разработчик |
| `components/agent-runner/run-supervisor/index.md` | Т | — | — | — | ⏳ | 74c7e38f | текст изменён после решения «✅» от Claude, роль Тестировщик |
| `components/agent-runner/sandbox-claim/index.md` | А | — | — | — | ⏳ | 7eb3e7ca | текст изменён после решения «✅» от Claude, роль Архитектор |
| `components/agent-runner/sandbox-claim/index.md` | Р | — | — | — | ⏳ | 7eb3e7ca | текст изменён после решения «✅» от Claude, роль Разработчик |
| `components/agent-runner/sandbox-claim/index.md` | Т | — | — | — | ⏳ | 7eb3e7ca | текст изменён после решения «✅» от Claude, роль Тестировщик |
| `components/agent-runner/scheduler/index.md` | А | Claude, роль Архитектор | 🤖 | 2026-10-13 | ✅ | 0404b95c | Данные слотов определены |
| `components/agent-runner/scheduler/index.md` | Р | Claude, роль Разработчик | 🤖 | 2026-10-13 | ✅ | 0404b95c | Операции и параметры есть |
| `components/agent-runner/scheduler/index.md` | Т | Claude, роль Тестировщик | 🤖 | 2026-10-13 | ✅ | 0404b95c | Fail-closed и сценарии проверяемы |
| `components/agent-runner/shag-podgotovki/index.md` | А | Claude, роль Архитектор | 🤖 | 2026-10-13 | ✅ | e387d8ad | Связи и данные определены |
| `components/agent-runner/shag-podgotovki/index.md` | Р | Claude, роль Разработчик | 🤖 | 2026-10-13 | ✅ | e387d8ad | Параметры и операции есть |
| `components/agent-runner/shag-podgotovki/index.md` | Т | Claude, роль Тестировщик | 🤖 | 2026-10-13 | ✅ | e387d8ad | Сбои заданы |
| `components/agent-runner/tokeny-repozitoriev/index.md` | А | Claude, роль Архитектор | 🤖 | 2026-10-13 | ✅ | e79a06a0 | Границы с git-провайдером и Sandbox ясны |
| `components/agent-runner/tokeny-repozitoriev/index.md` | Р | Claude, роль Разработчик | 🤖 | 2026-10-13 | ✅ | e79a06a0 | Операции и входы есть |
| `components/agent-runner/tokeny-repozitoriev/index.md` | Т | Claude, роль Тестировщик | 🤖 | 2026-10-13 | ✅ | e79a06a0 | Отказ и повторы проверяемы |
| `components/guardrails/index.md` | А | — | — | — | ⏳ | 1efcfc82 | Архитектура компонента |
| `components/guardrails/index.md` | Р | — | — | — | ⏳ | 1efcfc82 | Архитектура компонента |
| `components/guardrails/konfig-deploya/index.md` | А | — | — | — | ⏳ | 72e577c9 | Блок |
| `components/guardrails/konfig-deploya/index.md` | Р | — | — | — | ⏳ | 72e577c9 | Блок |
| `components/guardrails/konfig-deploya/index.md` | Т | — | — | — | ⏳ | 72e577c9 | Блок |
| `components/guardrails/opa/index.md` | А | — | — | — | ⏳ | e5f645b6 | Блок |
| `components/guardrails/opa/index.md` | Р | — | — | — | ⏳ | e5f645b6 | Блок |
| `components/guardrails/opa/index.md` | Т | — | — | — | ⏳ | e5f645b6 | Блок |
| `components/guardrails/rego-v-git/index.md` | А | — | — | — | ⏳ | 5cbd7f44 | Блок |
| `components/guardrails/rego-v-git/index.md` | Р | — | — | — | ⏳ | 5cbd7f44 | Блок |
| `components/guardrails/rego-v-git/index.md` | Т | — | — | — | ⏳ | 5cbd7f44 | Блок |
| `components/harness/bootstrap/index.md` | А | Claude, роль Архитектор | 🤖 | 2026-10-13 | ✅ | db458c49 | достаточно |
| `components/harness/bootstrap/index.md` | Р | Claude, роль Разработчик | 🤖 | 2026-10-13 | ✅ | db458c49 | достаточно |
| `components/harness/bootstrap/index.md` | Т | Claude, роль Тестировщик | 🤖 | 2026-10-13 | ✅ | db458c49 | достаточно |
| `components/harness/context-manager/index.md` | А | Claude, роль Архитектор | 🤖 | 2026-10-13 | ✅ | 8886c5a9 | достаточно |
| `components/harness/context-manager/index.md` | Р | Claude, роль Разработчик | 🤖 | 2026-10-13 | ✅ | 8886c5a9 | достаточно |
| `components/harness/context-manager/index.md` | Т | Claude, роль Тестировщик | 🤖 | 2026-10-13 | ✅ | 8886c5a9 | достаточно |
| `components/harness/event-stream/index.md` | А | Claude, роль Архитектор | 🤖 | 2026-10-13 | ✅ | 24a69b87 | достаточно |
| `components/harness/event-stream/index.md` | Р | Claude, роль Разработчик | 🤖 | 2026-10-13 | ✅ | 24a69b87 | достаточно |
| `components/harness/event-stream/index.md` | Т | Claude, роль Тестировщик | 🤖 | 2026-10-13 | ✅ | 24a69b87 | достаточно |
| `components/harness/hooks/index.md` | А | Claude, роль Архитектор | 🤖 | 2026-10-13 | ✅ | aec753f4 | достаточно |
| `components/harness/hooks/index.md` | Р | Claude, роль Разработчик | 🤖 | 2026-10-13 | ✅ | aec753f4 | достаточно |
| `components/harness/hooks/index.md` | Т | Claude, роль Тестировщик | 🤖 | 2026-10-13 | ✅ | aec753f4 | достаточно |
| `components/harness/index.md` | А | Claude, роль Архитектор | 🤖 | 2026-10-13 | ✅ | 2947fad1 | достаточно |
| `components/harness/index.md` | Р | Claude, роль Разработчик | 🤖 | 2026-10-13 | ✅ | 2947fad1 | достаточно |
| `components/harness/llm-client/index.md` | А | Claude, роль Архитектор | 🤖 | 2026-10-13 | ✅ | ec484e18 | достаточно |
| `components/harness/llm-client/index.md` | Р | Claude, роль Разработчик | 🤖 | 2026-10-13 | ✅ | ec484e18 | достаточно |
| `components/harness/llm-client/index.md` | Т | Claude, роль Тестировщик | 🤖 | 2026-10-13 | ✅ | ec484e18 | достаточно |
| `components/harness/pause-resume/index.md` | А | Claude, роль Архитектор | 🤖 | 2026-10-13 | ✅ | f29c2ce5 | достаточно |
| `components/harness/pause-resume/index.md` | Р | Claude, роль Разработчик | 🤖 | 2026-10-13 | ✅ | f29c2ce5 | достаточно |
| `components/harness/pause-resume/index.md` | Т | Claude, роль Тестировщик | 🤖 | 2026-10-13 | ✅ | f29c2ce5 | достаточно |
| `components/harness/policy-stop/index.md` | А | Claude, роль Архитектор | 🤖 | 2026-10-13 | ✅ | 34d6420f | достаточно |
| `components/harness/policy-stop/index.md` | Р | Claude, роль Разработчик | 🤖 | 2026-10-13 | ✅ | 34d6420f | достаточно |
| `components/harness/policy-stop/index.md` | Т | Claude, роль Тестировщик | 🤖 | 2026-10-13 | ✅ | 34d6420f | достаточно |
| `components/harness/tool-executor/index.md` | А | Claude, роль Архитектор | 🤖 | 2026-10-13 | ✅ | 30278eea | достаточно |
| `components/harness/tool-executor/index.md` | Р | Claude, роль Разработчик | 🤖 | 2026-10-13 | ✅ | 30278eea | достаточно |
| `components/harness/tool-executor/index.md` | Т | Claude, роль Тестировщик | 🤖 | 2026-10-13 | ✅ | 30278eea | достаточно |
| `components/icplan/avtopodhvat/index.md` | А | — | — | — | ⏳ | bb9d016b | текст изменён после решения «✅» от Claude, роль Архитектор |
| `components/icplan/avtopodhvat/index.md` | Р | — | — | — | ⏳ | bb9d016b | текст изменён после решения «✅» от Claude, роль Разработчик |
| `components/icplan/avtopodhvat/index.md` | Т | — | — | — | ⏳ | bb9d016b | текст изменён после решения «✅» от Claude, роль Тестировщик |
| `components/icplan/control-plane-ui/index.md` | А | — | — | — | ⏳ | 785ddf1e | текст изменён после решения «✅» от Claude, роль Архитектор |
| `components/icplan/control-plane-ui/index.md` | Р | — | — | — | ⏳ | 785ddf1e | текст изменён после решения «✅» от Claude, роль Разработчик |
| `components/icplan/control-plane-ui/index.md` | Т | — | — | — | ⏳ | 785ddf1e | текст изменён после решения «✅» от Claude, роль Тестировщик |
| `components/icplan/index.md` | А | Claude, роль Архитектор | 🤖 | 2026-10-13 | ✅ | dc437139 | Повтор: Z-ICP-34/63 закрыты (встроенные в зоне, I4 и decisions в С1), порядок работы с данными и I-кодами |
| `components/icplan/index.md` | Р | Claude, роль Разработчик | 🤖 | 2026-10-13 | ✅ | dc437139 | Повтор: Z-ICP-1/71 закрыты (С1 с I4, decisions); потоки, данные, I-коды определены |
| `components/icplan/registry/index.md` | А | Claude, роль Архитектор | 🤖 | 2026-10-13 | ✅ | bf904abc | Повтор: Z-ICP-66/76 закрыты (apikey, integration_credential в Данных; версии по D26) |
| `components/icplan/registry/index.md` | Р | Claude, роль Разработчик | 🤖 | 2026-10-13 | ✅ | bf904abc | Повтор: Z-ICP-66/76 закрыты (apikey, integration_credential в Данных; версии по D26) |
| `components/icplan/registry/index.md` | Т | Claude, роль Тестировщик | 🤖 | 2026-10-13 | ✅ | bf904abc | Повтор: сценарии R-REG-01..06 проверяемы; Z-ICP-86 ждёт владельца, не блокирует |
| `components/icplan/run-queue-runner-api/index.md` | А | — | — | — | ⏳ | ea645811 | текст изменён после решения «✅» от Claude, роль Архитектор |
| `components/icplan/run-queue-runner-api/index.md` | Р | — | — | — | ⏳ | ea645811 | текст изменён после решения «✅» от Claude, роль Разработчик |
| `components/icplan/run-queue-runner-api/index.md` | Т | — | — | — | ⏳ | ea645811 | текст изменён после решения «✅» от Claude, роль Тестировщик |
| `components/icplan/task-ui/index.md` | А | Claude, роль Архитектор | 🤖 | 2026-10-12 | ✅ | 681818b3 | повторная проверка: вердикт в issue_process_state, затраты — LiteLLM_SpendLogs ролью litellm_read, эндпоинты I20 |
| `components/icplan/task-ui/index.md` | Р | Claude, роль Разработчик | 🤖 | 2026-10-12 | ✅ | 681818b3 | повторная проверка: 9 экранов с эндпоинтами, источники вердикта и затрат, сбои |
| `components/icplan/task-ui/index.md` | Т | Claude, роль Тестировщик | 🤖 | 2026-10-12 | ✅ | 681818b3 | повторная проверка: экраны с эндпоинтами и ошибками; SSE, цена неизвестна; Z-ICP-31/32 закрыты |
| `components/infrastructure/index.md` | А | — | — | — | ⏳ | d8325b1e | Архитектура компонента |
| `components/infrastructure/index.md` | Р | — | — | — | ⏳ | d8325b1e | Архитектура компонента |
| `components/infrastructure/pgbouncer/index.md` | А | — | — | — | ⏳ | 5482c064 | Блок |
| `components/infrastructure/pgbouncer/index.md` | Р | — | — | — | ⏳ | 5482c064 | Блок |
| `components/infrastructure/pgbouncer/index.md` | Т | — | — | — | ⏳ | 5482c064 | Блок |
| `components/infrastructure/postgresql-17-pgvector/index.md` | А | — | — | — | ⏳ | 29c961ff | Блок |
| `components/infrastructure/postgresql-17-pgvector/index.md` | Р | — | — | — | ⏳ | 29c961ff | Блок |
| `components/infrastructure/postgresql-17-pgvector/index.md` | Т | — | — | — | ⏳ | 29c961ff | Блок |
| `components/infrastructure/rezervnoe-hranilische-s3-vne-uzla/index.md` | А | — | — | — | ⏳ | f25c950f | Блок |
| `components/infrastructure/rezervnoe-hranilische-s3-vne-uzla/index.md` | Р | — | — | — | ⏳ | f25c950f | Блок |
| `components/infrastructure/rezervnoe-hranilische-s3-vne-uzla/index.md` | Т | — | — | — | ⏳ | f25c950f | Блок |
| `components/infrastructure/rustfs/index.md` | А | — | — | — | ⏳ | b6ba2ea7 | Блок |
| `components/infrastructure/rustfs/index.md` | Р | — | — | — | ⏳ | b6ba2ea7 | Блок |
| `components/infrastructure/rustfs/index.md` | Т | — | — | — | ⏳ | b6ba2ea7 | Блок |
| `components/infrastructure/traefik/index.md` | А | — | — | — | ⏳ | 00304355 | Блок |
| `components/infrastructure/traefik/index.md` | Р | — | — | — | ⏳ | 00304355 | Блок |
| `components/infrastructure/traefik/index.md` | Т | — | — | — | ⏳ | 00304355 | Блок |
| `components/llm-gateway/aliasy/index.md` | А | — | — | — | ⏳ | 907e35f5 | Блок |
| `components/llm-gateway/aliasy/index.md` | Р | — | — | — | ⏳ | 907e35f5 | Блок |
| `components/llm-gateway/aliasy/index.md` | Т | — | — | — | ⏳ | 907e35f5 | Блок |
| `components/llm-gateway/byudzhety-rate-limit/index.md` | А | — | — | — | ⏳ | 51b4735a | Блок |
| `components/llm-gateway/byudzhety-rate-limit/index.md` | Р | — | — | — | ⏳ | 51b4735a | Блок |
| `components/llm-gateway/byudzhety-rate-limit/index.md` | Т | — | — | — | ⏳ | 51b4735a | Блок |
| `components/llm-gateway/fallback/index.md` | А | — | — | — | ⏳ | 249852db | Блок |
| `components/llm-gateway/fallback/index.md` | Р | — | — | — | ⏳ | 249852db | Блок |
| `components/llm-gateway/fallback/index.md` | Т | — | — | — | ⏳ | 249852db | Блок |
| `components/llm-gateway/g4-huki/index.md` | А | — | — | — | ⏳ | 17a9b9e0 | Блок |
| `components/llm-gateway/g4-huki/index.md` | Р | — | — | — | ⏳ | 17a9b9e0 | Блок |
| `components/llm-gateway/g4-huki/index.md` | Т | — | — | — | ⏳ | 17a9b9e0 | Блок |
| `components/llm-gateway/index.md` | А | — | — | — | ⏳ | a0eea543 | Архитектура компонента |
| `components/llm-gateway/index.md` | Р | — | — | — | ⏳ | a0eea543 | Архитектура компонента |
| `components/llm-gateway/mock-llm/index.md` | А | — | — | — | ⏳ | d8909a26 | Блок |
| `components/llm-gateway/mock-llm/index.md` | Р | — | — | — | ⏳ | d8909a26 | Блок |
| `components/llm-gateway/mock-llm/index.md` | Т | — | — | — | ⏳ | d8909a26 | Блок |
| `components/llm-gateway/spend-log/index.md` | А | — | — | — | ⏳ | 2fbff707 | Блок |
| `components/llm-gateway/spend-log/index.md` | Р | — | — | — | ⏳ | 2fbff707 | Блок |
| `components/llm-gateway/spend-log/index.md` | Т | — | — | — | ⏳ | 2fbff707 | Блок |
| `components/llm-gateway/virtual-keys/index.md` | А | — | — | — | ⏳ | cc42b7e6 | Блок |
| `components/llm-gateway/virtual-keys/index.md` | Р | — | — | — | ⏳ | cc42b7e6 | Блок |
| `components/llm-gateway/virtual-keys/index.md` | Т | — | — | — | ⏳ | cc42b7e6 | Блок |
| `components/mcp-tools/git-provayder/index.md` | А | — | — | — | ⏳ | 486bf14f | текст изменён после решения «❌» от Claude, роль Архитектор |
| `components/mcp-tools/git-provayder/index.md` | Р | — | — | — | ⏳ | 486bf14f | текст изменён после решения «❌» от Claude, роль Разработчик |
| `components/mcp-tools/git-provayder/index.md` | Т | — | — | — | ⏳ | 486bf14f | текст изменён после решения «❌» от Claude, роль Тестировщик |
| `components/mcp-tools/index.md` | А | Claude, роль Архитектор | 🤖 | 2026-10-13 | ✅ | 25460dc5 | достаточно |
| `components/mcp-tools/index.md` | Р | Claude, роль Разработчик | 🤖 | 2026-10-13 | ✅ | 25460dc5 | достаточно |
| `components/mcp-tools/itsaplan-core/index.md` | А | — | — | — | ⏳ | 00daaf6f | текст изменён после решения «✅» от Claude, роль Архитектор |
| `components/mcp-tools/itsaplan-core/index.md` | Р | — | — | — | ⏳ | 00daaf6f | текст изменён после решения «✅» от Claude, роль Разработчик |
| `components/mcp-tools/itsaplan-core/index.md` | Т | — | — | — | ⏳ | 00daaf6f | текст изменён после решения «✅» от Claude, роль Тестировщик |
| `components/mcp-tools/memory/index.md` | А | — | — | — | ⏳ | 2d12dfda | текст изменён после решения «❌» от Claude, роль Архитектор |
| `components/mcp-tools/memory/index.md` | Р | — | — | — | ⏳ | 2d12dfda | текст изменён после решения «❌» от Claude, роль Разработчик |
| `components/mcp-tools/memory/index.md` | Т | — | — | — | ⏳ | 2d12dfda | текст изменён после решения «❌» от Claude, роль Тестировщик |
| `components/mcp-tools/pravila-r1-r7/index.md` | А | — | — | — | ⏳ | 0fbe3bba | текст изменён после решения «✅» от Claude, роль Архитектор |
| `components/mcp-tools/pravila-r1-r7/index.md` | Р | — | — | — | ⏳ | 0fbe3bba | текст изменён после решения «❌» от Claude, роль Разработчик |
| `components/mcp-tools/pravila-r1-r7/index.md` | Т | — | — | — | ⏳ | 0fbe3bba | текст изменён после решения «❌» от Claude, роль Тестировщик |
| `components/memory/index.md` | А | — | — | — | ⏳ | b386ace5 | Архитектура компонента |
| `components/memory/index.md` | Р | — | — | — | ⏳ | b386ace5 | Архитектура компонента |
| `components/memory/m3-zadachnaya/index.md` | А | — | — | — | ⏳ | 42ddac48 | Блок |
| `components/memory/m3-zadachnaya/index.md` | Р | — | — | — | ⏳ | 42ddac48 | Блок |
| `components/memory/m3-zadachnaya/index.md` | Т | — | — | — | ⏳ | 42ddac48 | Блок |
| `components/memory/memory-api/index.md` | А | — | — | — | ⏳ | 547b7925 | Блок |
| `components/memory/memory-api/index.md` | Р | — | — | — | ⏳ | 547b7925 | Блок |
| `components/memory/memory-api/index.md` | Т | — | — | — | ⏳ | 547b7925 | Блок |
| `components/observability/agregaty-zatrat/index.md` | А | — | — | — | ⏳ | a2d56823 | Блок |
| `components/observability/agregaty-zatrat/index.md` | Р | — | — | — | ⏳ | a2d56823 | Блок |
| `components/observability/agregaty-zatrat/index.md` | Т | — | — | — | ⏳ | a2d56823 | Блок |
| `components/observability/index.md` | А | — | — | — | ⏳ | b6af9b9e | Архитектура компонента |
| `components/observability/index.md` | Р | — | — | — | ⏳ | b6af9b9e | Архитектура компонента |
| `components/observability/sobytiya-zapuska/index.md` | А | — | — | — | ⏳ | 0c9d5600 | Блок |
| `components/observability/sobytiya-zapuska/index.md` | Р | — | — | — | ⏳ | 0c9d5600 | Блок |
| `components/observability/sobytiya-zapuska/index.md` | Т | — | — | — | ⏳ | 0c9d5600 | Блок |
| `components/platform-module/aliasy-llm/index.md` | А | — | — | — | ⏳ | 1b1a64ad | Блок |
| `components/platform-module/aliasy-llm/index.md` | Р | — | — | — | ⏳ | 1b1a64ad | Блок |
| `components/platform-module/aliasy-llm/index.md` | Т | — | — | — | ⏳ | 1b1a64ad | Блок |
| `components/platform-module/api-modulya/index.md` | А | — | — | — | ⏳ | a7343581 | Блок |
| `components/platform-module/api-modulya/index.md` | Р | — | — | — | ⏳ | a7343581 | Блок |
| `components/platform-module/api-modulya/index.md` | Т | — | — | — | ⏳ | a7343581 | Блок |
| `components/platform-module/byudzhety/index.md` | А | — | — | — | ⏳ | 2f06d223 | Блок |
| `components/platform-module/byudzhety/index.md` | Р | — | — | — | ⏳ | 2f06d223 | Блок |
| `components/platform-module/byudzhety/index.md` | Т | — | — | — | ⏳ | 2f06d223 | Блок |
| `components/platform-module/dannye-guardrails/index.md` | А | — | — | — | ⏳ | 625d9141 | Блок |
| `components/platform-module/dannye-guardrails/index.md` | Р | — | — | — | ⏳ | 625d9141 | Блок |
| `components/platform-module/dannye-guardrails/index.md` | Т | — | — | — | ⏳ | 625d9141 | Блок |
| `components/platform-module/index.md` | А | — | — | — | ⏳ | 66b5db86 | Архитектура компонента |
| `components/platform-module/index.md` | Р | — | — | — | ⏳ | 66b5db86 | Архитектура компонента |
| `components/platform-module/profili-pamyati/index.md` | А | — | — | — | ⏳ | 263e575e | Блок |
| `components/platform-module/profili-pamyati/index.md` | Р | — | — | — | ⏳ | 263e575e | Блок |
| `components/platform-module/profili-pamyati/index.md` | Т | — | — | — | ⏳ | 263e575e | Блок |
| `components/platform-module/profili-sandbox/index.md` | А | — | — | — | ⏳ | 984ffd34 | Блок |
| `components/platform-module/profili-sandbox/index.md` | Р | — | — | — | ⏳ | 984ffd34 | Блок |
| `components/platform-module/profili-sandbox/index.md` | Т | — | — | — | ⏳ | 984ffd34 | Блок |
| `components/platform-module/versii-agentov/index.md` | А | — | — | — | ⏳ | 11f2a85d | Блок |
| `components/platform-module/versii-agentov/index.md` | Р | — | — | — | ⏳ | 11f2a85d | Блок |
| `components/platform-module/versii-agentov/index.md` | Т | — | — | — | ⏳ | 11f2a85d | Блок |
| `components/sandbox/credential-helper/index.md` | А | Claude, роль Архитектор | 🤖 | 2026-10-13 | ✅ | e1b6f46d | достаточно |
| `components/sandbox/credential-helper/index.md` | Р | Claude, роль Разработчик | 🤖 | 2026-10-13 | ✅ | e1b6f46d | достаточно |
| `components/sandbox/credential-helper/index.md` | Т | Claude, роль Тестировщик | 🤖 | 2026-10-13 | ✅ | e1b6f46d | достаточно |
| `components/sandbox/egress-proksi/index.md` | А | Claude, роль Архитектор | 🤖 | 2026-10-13 | ✅ | 07885620 | достаточно |
| `components/sandbox/egress-proksi/index.md` | Р | Claude, роль Разработчик | 🤖 | 2026-10-13 | ✅ | 07885620 | достаточно |
| `components/sandbox/egress-proksi/index.md` | Т | Claude, роль Тестировщик | 🤖 | 2026-10-13 | ✅ | 07885620 | достаточно |
| `components/sandbox/index.md` | А | Claude, роль Архитектор | 🤖 | 2026-10-13 | ✅ | a6c9f995 | достаточно |
| `components/sandbox/index.md` | Р | Claude, роль Разработчик | 🤖 | 2026-10-13 | ✅ | a6c9f995 | достаточно |
| `components/sandbox/profil/index.md` | А | Claude, роль Архитектор | 🤖 | 2026-10-13 | ✅ | 4f79208c | достаточно |
| `components/sandbox/profil/index.md` | Р | Claude, роль Разработчик | 🤖 | 2026-10-13 | ✅ | 4f79208c | достаточно |
| `components/sandbox/profil/index.md` | Т | Claude, роль Тестировщик | 🤖 | 2026-10-13 | ✅ | 4f79208c | достаточно |
| `components/sandbox/sandboxprovider/index.md` | А | Claude, роль Архитектор | 🤖 | 2026-10-13 | ✅ | 37701f0b | достаточно |
| `components/sandbox/sandboxprovider/index.md` | Р | Claude, роль Разработчик | 🤖 | 2026-10-13 | ✅ | 37701f0b | достаточно |
| `components/sandbox/sandboxprovider/index.md` | Т | Claude, роль Тестировщик | 🤖 | 2026-10-13 | ✅ | 37701f0b | достаточно |
| `components/sandbox/teplyy-pul/index.md` | А | Claude, роль Архитектор | 🤖 | 2026-10-13 | ✅ | 17690ccb | достаточно |
| `components/sandbox/teplyy-pul/index.md` | Р | Claude, роль Разработчик | 🤖 | 2026-10-13 | ✅ | 17690ccb | достаточно |
| `components/sandbox/teplyy-pul/index.md` | Т | Claude, роль Тестировщик | 🤖 | 2026-10-13 | ✅ | 17690ccb | достаточно |
| `data-by-component/agent-runner/index.md` | А | Claude, роль Архитектор | 🤖 | 2026-10-13 | ✅ | 23678591 | Схемы runner/harness_ckpt/platform с владельцем и ролью; связи ER с agent_run/issue/project; срок и очистка у всех таблиц |
| `data-by-component/agent-runner/index.md` | Р | Claude, роль Разработчик | 🤖 | 2026-10-13 | ✅ | 23678591 | Колонки, типы, ключи, индексы, TTL и очистка достаточны для миграций; параметры названы |
| `data-by-component/agent-runner/index.md` | Д | Claude, роль DevOps-инженер | 🤖 | 2026-10-13 | ✅ | 23678591 | База/роль/схемы названы и совпадают с Deploy (DATABASE_URL); очистка по expires_at, миграции при старте |
| `data-by-component/guardrails/index.md` | А | — | — | — | ⏳ | da428d85 | Данные |
| `data-by-component/guardrails/index.md` | Р | — | — | — | ⏳ | da428d85 | Данные |
| `data-by-component/guardrails/index.md` | Д | — | — | — | ⏳ | da428d85 | Данные |
| `data-by-component/harness/index.md` | А | Claude, роль Архитектор | 🤖 | 2026-10-13 | ✅ | 69b3bd65 | достаточно |
| `data-by-component/harness/index.md` | Р | Claude, роль Разработчик | 🤖 | 2026-10-13 | ✅ | 69b3bd65 | достаточно |
| `data-by-component/harness/index.md` | Д | Claude, роль DevOps-инженер | 🤖 | 2026-10-13 | ✅ | 69b3bd65 | достаточно |
| `data-by-component/icplan/index.md` | А | Claude, роль Архитектор | 🤖 | 2026-10-13 | ✅ | 2b0e1e7d | повторно: хранилища S1/S7, база и роль, срок и очистка agent_run/agent_chat_thread по D25/R-ICP-19, process_version, связи в ER согласованы |
| `data-by-component/icplan/index.md` | Р | Claude, роль Разработчик | 🤖 | 2026-10-13 | ✅ | 2b0e1e7d | повторно: таблицы, колонки, индексы, миграции и сроки определены; Z-ICP-67/78 закрыты в тексте |
| `data-by-component/icplan/index.md` | Д | Claude, роль DevOps-инженер | 🤖 | 2026-10-13 | ✅ | 2b0e1e7d | повторно: STORES S1+S7, бэкапы backups/postgres, база itsaplan и роль указаны, срок и очистка заданы; Z-ICP-97 закрыт |
| `data-by-component/infrastructure/index.md` | А | — | — | — | ⏳ | f1f26a81 | Данные |
| `data-by-component/infrastructure/index.md` | Р | — | — | — | ⏳ | f1f26a81 | Данные |
| `data-by-component/infrastructure/index.md` | Д | — | — | — | ⏳ | f1f26a81 | Данные |
| `data-by-component/llm-gateway/index.md` | А | — | — | — | ⏳ | f2b3467e | Данные |
| `data-by-component/llm-gateway/index.md` | Р | — | — | — | ⏳ | f2b3467e | Данные |
| `data-by-component/llm-gateway/index.md` | Д | — | — | — | ⏳ | f2b3467e | Данные |
| `data-by-component/mcp-tools/index.md` | А | Claude, роль Архитектор | 🤖 | 2026-10-13 | ✅ | 49fecc37 | достаточно |
| `data-by-component/mcp-tools/index.md` | Р | Claude, роль Разработчик | 🤖 | 2026-10-13 | ✅ | 49fecc37 | достаточно |
| `data-by-component/mcp-tools/index.md` | Д | Claude, роль DevOps-инженер | 🤖 | 2026-10-13 | ✅ | 49fecc37 | достаточно |
| `data-by-component/memory/index.md` | А | — | — | — | ⏳ | 13d74d7a | Данные |
| `data-by-component/memory/index.md` | Р | — | — | — | ⏳ | 13d74d7a | Данные |
| `data-by-component/memory/index.md` | Д | — | — | — | ⏳ | 13d74d7a | Данные |
| `data-by-component/observability/index.md` | А | — | — | — | ⏳ | cba2079f | Данные |
| `data-by-component/observability/index.md` | Р | — | — | — | ⏳ | cba2079f | Данные |
| `data-by-component/observability/index.md` | Д | — | — | — | ⏳ | cba2079f | Данные |
| `data-by-component/platform-module/index.md` | А | — | — | — | ⏳ | 7b86fc6a | Данные |
| `data-by-component/platform-module/index.md` | Р | — | — | — | ⏳ | 7b86fc6a | Данные |
| `data-by-component/platform-module/index.md` | Д | — | — | — | ⏳ | 7b86fc6a | Данные |
| `data-by-component/sandbox/index.md` | А | Claude, роль Архитектор | 🤖 | 2026-10-13 | ✅ | dbcbfc2f | достаточно |
| `data-by-component/sandbox/index.md` | Р | Claude, роль Разработчик | 🤖 | 2026-10-13 | ✅ | dbcbfc2f | достаточно |
| `data-by-component/sandbox/index.md` | Д | Claude, роль DevOps-инженер | 🤖 | 2026-10-13 | ✅ | dbcbfc2f | достаточно |
| `docs/api/agent-runner.md` | А | Claude, роль Архитектор | 🤖 | 2026-10-13 | ✅ | 3a4c361a | Блоки, хранилища и задачи указаны |
| `docs/api/agent-runner.md` | Р | Claude, роль Разработчик | 🤖 | 2026-10-13 | ✅ | 3a4c361a | Эндпоинты с кодами и ошибками есть |
| `docs/api/agent-runner.md` | Т | Claude, роль Тестировщик | 🤖 | 2026-10-13 | ✅ | 3a4c361a | Коды ответов проверяемы |
| `docs/api/guardrails.md` | А | — | — | — | ⏳ | 3c56d741 | Интеграции |
| `docs/api/guardrails.md` | Р | — | — | — | ⏳ | 3c56d741 | Интеграции |
| `docs/api/guardrails.md` | Т | — | — | — | ⏳ | 3c56d741 | Интеграции |
| `docs/api/harness.md` | А | Claude, роль Архитектор | 🤖 | 2026-10-13 | ✅ | 7f2621b0 | достаточно |
| `docs/api/harness.md` | Р | Claude, роль Разработчик | 🤖 | 2026-10-13 | ✅ | 7f2621b0 | достаточно |
| `docs/api/harness.md` | Т | Claude, роль Тестировщик | 🤖 | 2026-10-13 | ✅ | 7f2621b0 | достаточно |
| `docs/api/icplan.md` | А | Claude, роль Архитектор | 🤖 | 2026-10-13 | ✅ | a4f06bb6 | повторно: источник правды ai_agent.enabled, I4/I20 на C1, версии и граница с Platform module определены; Z-ICP-68 закрыт |
| `docs/api/icplan.md` | Р | Claude, роль Разработчик | 🤖 | 2026-10-13 | ✅ | a4f06bb6 | повторно: пути помечены 🆕/🛠, тела и ошибки заданы (decisions, messages, cancel, costs, PATCH ai-agents); Z-ICP-79..81 закрыты |
| `docs/api/icplan.md` | Т | Claude, роль Тестировщик | 🤖 | 2026-10-13 | ✅ | a4f06bb6 | повторно: у изменяющих эндпоинтов 403/409/404, /costs при недоступном журнале 200 с null, повтор итога 404; Z-ICP-87..89 закрыты, Z-ICP-86 ждёт владельца |
| `docs/api/infrastructure.md` | А | — | — | — | ⏳ | e5b694e2 | Интеграции |
| `docs/api/infrastructure.md` | Р | — | — | — | ⏳ | e5b694e2 | Интеграции |
| `docs/api/infrastructure.md` | Т | — | — | — | ⏳ | e5b694e2 | Интеграции |
| `docs/api/llm-gateway.md` | А | — | — | — | ⏳ | 7016fea2 | Интеграции |
| `docs/api/llm-gateway.md` | Р | — | — | — | ⏳ | 7016fea2 | Интеграции |
| `docs/api/llm-gateway.md` | Т | — | — | — | ⏳ | 7016fea2 | Интеграции |
| `docs/api/mcp-tools.md` | А | Claude, роль Архитектор | 🤖 | 2026-10-13 | ✅ | e2d6cd24 | достаточно |
| `docs/api/mcp-tools.md` | Р | Claude, роль Разработчик | 🤖 | 2026-10-13 | ✅ | e2d6cd24 | достаточно |
| `docs/api/mcp-tools.md` | Т | Claude, роль Тестировщик | 🤖 | 2026-10-13 | ✅ | e2d6cd24 | достаточно |
| `docs/api/memory.md` | А | — | — | — | ⏳ | 6c52c422 | Интеграции |
| `docs/api/memory.md` | Р | — | — | — | ⏳ | 6c52c422 | Интеграции |
| `docs/api/memory.md` | Т | — | — | — | ⏳ | 6c52c422 | Интеграции |
| `docs/api/observability.md` | А | — | — | — | ⏳ | ea7cc7f8 | Интеграции |
| `docs/api/observability.md` | Р | — | — | — | ⏳ | ea7cc7f8 | Интеграции |
| `docs/api/observability.md` | Т | — | — | — | ⏳ | ea7cc7f8 | Интеграции |
| `docs/api/platform-module.md` | А | — | — | — | ⏳ | d6e9912f | Интеграции |
| `docs/api/platform-module.md` | Р | — | — | — | ⏳ | d6e9912f | Интеграции |
| `docs/api/platform-module.md` | Т | — | — | — | ⏳ | d6e9912f | Интеграции |
| `docs/api/sandbox.md` | А | Claude, роль Архитектор | 🤖 | 2026-10-13 | ✅ | 5a07f788 | достаточно |
| `docs/api/sandbox.md` | Р | Claude, роль Разработчик | 🤖 | 2026-10-13 | ✅ | 5a07f788 | достаточно |
| `docs/api/sandbox.md` | Т | Claude, роль Тестировщик | 🤖 | 2026-10-13 | ✅ | 5a07f788 | достаточно |
| `docs/rnd/agent-workspace.md` | В | — | — | — | ⏳ | 30a7763d | R&D |
| `docs/rnd/agent-workspace.md` | А | — | — | — | ⏳ | 30a7763d | R&D |
| `docs/rnd/autopickup-rules.md` | В | Claude, роль Владелец продукта | 🤖 | 2026-10-13 | ✅ | e0349a00 | цена 7.5-12 дн (3.1+3.6), выбор D17 с опровержением, бэклог зависимостей |
| `docs/rnd/autopickup-rules.md` | А | Claude, роль Архитектор | 🤖 | 2026-10-13 | ✅ | e0349a00 | стыки I1/I2/I20, переход делает ICPlan, Runner/Harness не меняются, порядок ICPlan vs слоты Runner разведён; ОВ-2 не блокирует |
| `docs/rnd/config-storage.md` | В | — | — | — | ⏳ | b220b4b1 | R&D |
| `docs/rnd/config-storage.md` | А | — | — | — | ⏳ | b220b4b1 | R&D |
| `docs/rnd/data-stores.md` | В | — | — | — | ⏳ | 09b858d0 | R&D |
| `docs/rnd/data-stores.md` | А | — | — | — | ⏳ | 09b858d0 | R&D |
| `docs/rnd/db-roles-schemas.md` | В | — | — | — | ⏳ | b08f9299 | R&D |
| `docs/rnd/db-roles-schemas.md` | А | — | — | — | ⏳ | b08f9299 | R&D |
| `docs/rnd/doc-automation.md` | В | — | — | — | ⏳ | 75904ffa | R&D |
| `docs/rnd/doc-automation.md` | А | — | — | — | ⏳ | 75904ffa | R&D |
| `docs/rnd/fork-run-retention.md` | В | Claude, роль Владелец продукта | 🤖 | 2026-10-13 | ✅ | 865e8bf3 | цена 7 ч (4.7.7 + 2.5.9), срок хранения и история/статистика сохранены, риск по ПДн с условием пересмотра |
| `docs/rnd/fork-run-retention.md` | А | Claude, роль Архитектор | 🤖 | 2026-10-13 | ✅ | 865e8bf3 | удаляет владелец таблицы (D22), Memory только SELECT и фильтр, M3 через retention/run, границы сроков и FK к run_event учтены |
| `docs/rnd/guardrails-engine.md` | В | — | — | — | ⏳ | bfd39326 | R&D |
| `docs/rnd/guardrails-engine.md` | А | — | — | — | ⏳ | bfd39326 | R&D |
| `docs/rnd/harness-framework.md` | В | Claude, роль Владелец продукта | 🤖 | 2026-10-13 | ✅ | 49b20541 | достаточно |
| `docs/rnd/harness-framework.md` | А | Claude, роль Архитектор | 🤖 | 2026-10-13 | ✅ | 49b20541 | достаточно |
| `docs/rnd/ingress-and-balancing.md` | В | — | — | — | ⏳ | 702e49f3 | R&D |
| `docs/rnd/ingress-and-balancing.md` | А | — | — | — | ⏳ | 702e49f3 | R&D |
| `docs/rnd/kubernetes-runtime.md` | В | — | — | — | ⏳ | 2028b6f2 | R&D |
| `docs/rnd/kubernetes-runtime.md` | А | — | — | — | ⏳ | 2028b6f2 | R&D |
| `docs/rnd/llm-gateway.md` | В | — | — | — | ⏳ | a9ed06b0 | R&D |
| `docs/rnd/llm-gateway.md` | А | — | — | — | ⏳ | a9ed06b0 | R&D |
| `docs/rnd/load-profile.md` | В | — | — | — | ⏳ | 521689a5 | R&D |
| `docs/rnd/load-profile.md` | А | — | — | — | ⏳ | 521689a5 | R&D |
| `docs/rnd/mcp-vs-direct.md` | В | — | — | — | ⏳ | b9c3200f | текст изменён после решения «✅» от Claude, роль Владелец продукта |
| `docs/rnd/mcp-vs-direct.md` | А | — | — | — | ⏳ | b9c3200f | текст изменён после решения «✅» от Claude, роль Архитектор |
| `docs/rnd/memory-model.md` | В | — | — | — | ⏳ | 14716bb7 | R&D |
| `docs/rnd/memory-model.md` | А | — | — | — | ⏳ | 14716bb7 | R&D |
| `docs/rnd/observability.md` | В | — | — | — | ⏳ | a3760256 | R&D |
| `docs/rnd/observability.md` | А | — | — | — | ⏳ | a3760256 | R&D |
| `docs/rnd/platform-module-screens.md` | В | Claude, роль Владелец продукта | 🤖 | 2026-10-13 | ✅ | 16d43b38 | 30 ч подзадач 4.4, раскладка по уровням, риск God mode и условия пересмотра названы |
| `docs/rnd/platform-module-screens.md` | А | Claude, роль Архитектор | 🤖 | 2026-10-13 | ✅ | 16d43b38 | таблицы и эндпоинты по уровням, права ai_agents, @/cloud без правок, правки двух файлов форка и PR в upstream; ОВ-agent-registry-2 не блокирует |
| `docs/rnd/rag.md` | В | — | — | — | ⏳ | 1d9772fa | R&D |
| `docs/rnd/rag.md` | А | — | — | — | ⏳ | 1d9772fa | R&D |
| `docs/rnd/rnd-methodology-choice.md` | В | — | — | — | ⏳ | 1ad6d93e | R&D |
| `docs/rnd/rnd-methodology-choice.md` | А | — | — | — | ⏳ | 1ad6d93e | R&D |
| `docs/rnd/run-view.md` | В | — | — | — | ⏳ | b4da9c90 | R&D |
| `docs/rnd/run-view.md` | А | — | — | — | ⏳ | b4da9c90 | R&D |
| `docs/rnd/runaway-protection.md` | В | — | — | — | ⏳ | 43cde392 | R&D |
| `docs/rnd/runaway-protection.md` | А | — | — | — | ⏳ | 43cde392 | R&D |
| `docs/rnd/runner-agent-definition.md` | В | Claude, роль Владелец продукта | 🤖 | 2026-10-13 | ✅ | ee5ca14e | объём 6 ч (2.3.7), перенос Platform module в этап 2 как риск назван, выбор и пересмотр есть |
| `docs/rnd/runner-agent-definition.md` | А | Claude, роль Архитектор | 🤖 | 2026-10-13 | ✅ | ee5ca14e | I4 GET /platform/runs/:runId/agent, версия закрепляется в agent_run.agent_version, claim не меняется, доступ только через API, 404/409 определены |
| `docs/rnd/runner-and-scheduling.md` | В | Claude, роль Владелец продукта | 🤖 | 2026-10-13 | ✅ | 1c28186c | Выбор и последствия показаны |
| `docs/rnd/runner-and-scheduling.md` | А | Claude, роль Архитектор | 🤖 | 2026-10-13 | ✅ | 1c28186c | Стыки I1-I3 разобраны |
| `docs/rnd/sandbox-isolation.md` | В | Claude, роль Владелец продукта | 🤖 | 2026-10-13 | ✅ | 740292bf | достаточно |
| `docs/rnd/sandbox-isolation.md` | А | Claude, роль Архитектор | 🤖 | 2026-10-13 | ✅ | 740292bf | достаточно |
| `docs/rnd/step-contract.md` | В | — | — | — | ⏳ | 140bc29a | R&D |
| `docs/rnd/step-contract.md` | А | — | — | — | ⏳ | 140bc29a | R&D |
| `docs/rnd/tracker-choice.md` | В | Claude, роль Владелец продукта | 🤖 | 2026-10-12 | ✅ | ed65e738 | повторная проверка: Z-ICP-52 закрыт; AGPL ждёт владельца |
| `docs/rnd/tracker-choice.md` | А | Claude, роль Архитектор | 🤖 | 2026-10-12 | ✅ | ed65e738 | повторная проверка: Z-ICP-52 закрыт; AGPL — решение владельца |
| `docs/rnd/us-analogs-agent-tracker.md` | В | Claude, роль Владелец продукта | 🤖 | 2026-10-12 | ✅ | f6b5a75d | повторная проверка: Z-ICP-53 закрыт |
| `docs/rnd/us-analogs-agent-tracker.md` | А | Claude, роль Архитектор | 🤖 | 2026-10-12 | ✅ | f6b5a75d | повторная проверка: Z-ICP-53 закрыт |
| `docs/rules/api-methodology.md` | В | — | — | — | ⏳ | d2ea729f | Методология |
| `docs/rules/api-methodology.md` | А | — | — | — | ⏳ | d2ea729f | Методология |
| `docs/rules/approval-methodology.md` | В | — | — | — | ⏳ | f971b37c | Методология |
| `docs/rules/approval-methodology.md` | А | — | — | — | ⏳ | f971b37c | Методология |
| `docs/rules/architecture-methodology.md` | В | — | — | — | ⏳ | 03347175 | Методология |
| `docs/rules/architecture-methodology.md` | А | — | — | — | ⏳ | 03347175 | Методология |
| `docs/rules/block-methodology.md` | В | — | — | — | ⏳ | c89c4621 | Методология |
| `docs/rules/block-methodology.md` | А | — | — | — | ⏳ | c89c4621 | Методология |
| `docs/rules/data-methodology.md` | В | — | — | — | ⏳ | 9b7a95d2 | Методология |
| `docs/rules/data-methodology.md` | А | — | — | — | ⏳ | 9b7a95d2 | Методология |
| `docs/rules/decision-methodology.md` | В | — | — | — | ⏳ | 0af1d5d9 | Методология |
| `docs/rules/decision-methodology.md` | А | — | — | — | ⏳ | 0af1d5d9 | Методология |
| `docs/rules/review-methodology.md` | В | — | — | — | ⏳ | 00fb603f | Методология |
| `docs/rules/review-methodology.md` | А | — | — | — | ⏳ | 00fb603f | Методология |
| `docs/rules/rnd-methodology.md` | В | — | — | — | ⏳ | d2ff1c00 | Методология |
| `docs/rules/rnd-methodology.md` | А | — | — | — | ⏳ | d2ff1c00 | Методология |
| `docs/rules/sdd-methodology.md` | В | — | — | — | ⏳ | 56577938 | Методология |
| `docs/rules/sdd-methodology.md` | А | — | — | — | ⏳ | 56577938 | Методология |
| `docs/rules/structure-methodology.md` | В | — | — | — | ⏳ | 3236614f | Методология |
| `docs/rules/structure-methodology.md` | А | — | — | — | ⏳ | 3236614f | Методология |
| `docs/rules/support-docs-methodology.md` | В | — | — | — | ⏳ | ebbf9293 | Методология |
| `docs/rules/support-docs-methodology.md` | А | — | — | — | ⏳ | ebbf9293 | Методология |
| `docs/rules/task-methodology.md` | В | — | — | — | ⏳ | 54fbc54b | Методология |
| `docs/rules/task-methodology.md` | А | — | — | — | ⏳ | 54fbc54b | Методология |
| `docs/rules/tech-spec.md` | В | — | — | — | ⏳ | ca2d288e | Методология |
| `docs/rules/tech-spec.md` | А | — | — | — | ⏳ | ca2d288e | Методология |
| `docs/rules/us-methodology.md` | В | — | — | — | ⏳ | 2ab78054 | Методология |
| `docs/rules/us-methodology.md` | А | — | — | — | ⏳ | 2ab78054 | Методология |
| `docs/stories/agent-runner.md` | В | Claude, роль Владелец продукта | 🤖 | 2026-10-13 | ✅ | 59c7108a | Ценность историй ясна |
| `docs/stories/agent-runner.md` | И | Claude, роль Аналитик историй | 🤖 | 2026-10-13 | ✅ | 59c7108a | Действия и сбои описаны |
| `docs/stories/agent-runner.md` | П | Claude, роль Пользователь | 🤖 | 2026-10-13 | ✅ | 59c7108a | Задача пользователя решается |
| `docs/stories/guardrails.md` | В | — | — | — | ⏳ | 3ba76b1f | User Stories |
| `docs/stories/guardrails.md` | И | — | — | — | ⏳ | 3ba76b1f | User Stories |
| `docs/stories/guardrails.md` | П | — | — | — | ⏳ | 3ba76b1f | User Stories |
| `docs/stories/harness.md` | В | Claude, роль Владелец продукта | 🤖 | 2026-10-13 | ✅ | d62dc5a0 | достаточно |
| `docs/stories/harness.md` | И | Claude, роль Аналитик историй | 🤖 | 2026-10-13 | ✅ | d62dc5a0 | достаточно |
| `docs/stories/harness.md` | П | Claude, роль Пользователь | 🤖 | 2026-10-13 | ✅ | d62dc5a0 | достаточно |
| `docs/stories/icplan.md` | В | Claude, роль Владелец продукта | 🤖 | 2026-10-13 | ✅ | d854644a | Истории и требования покрывают ценность: создание, видимость, отмена, проверка результата; открытый вопрос Z-ICP-106 не блокирует. |
| `docs/stories/icplan.md` | И | Claude, роль Аналитик историй | 🤖 | 2026-10-13 | ✅ | d854644a | Роли и отказы разобраны: дубли, не участник проекта, пауза hook G2, отмена запуска. |
| `docs/stories/icplan.md` | П | Claude, роль Пользователь | 🤖 | 2026-10-13 | ✅ | d854644a | Пользователь может создать задачу, видеть работу агента, ответить, принять или вернуть результат. |
| `docs/stories/infrastructure.md` | В | — | — | — | ⏳ | 26336d62 | User Stories |
| `docs/stories/infrastructure.md` | И | — | — | — | ⏳ | 26336d62 | User Stories |
| `docs/stories/infrastructure.md` | П | — | — | — | ⏳ | 26336d62 | User Stories |
| `docs/stories/llm-gateway.md` | В | — | — | — | ⏳ | 752ac795 | User Stories |
| `docs/stories/llm-gateway.md` | И | — | — | — | ⏳ | 752ac795 | User Stories |
| `docs/stories/llm-gateway.md` | П | — | — | — | ⏳ | 752ac795 | User Stories |
| `docs/stories/mcp-tools.md` | В | Claude, роль Владелец продукта | 🤖 | 2026-10-13 | ✅ | 5bc875c3 | достаточно |
| `docs/stories/mcp-tools.md` | И | Claude, роль Аналитик историй | 🤖 | 2026-10-13 | ✅ | 5bc875c3 | достаточно |
| `docs/stories/mcp-tools.md` | П | Claude, роль Пользователь | 🤖 | 2026-10-13 | ✅ | 5bc875c3 | достаточно |
| `docs/stories/memory.md` | В | — | — | — | ⏳ | 58bbaf3c | User Stories |
| `docs/stories/memory.md` | И | — | — | — | ⏳ | 58bbaf3c | User Stories |
| `docs/stories/memory.md` | П | — | — | — | ⏳ | 58bbaf3c | User Stories |
| `docs/stories/observability.md` | В | — | — | — | ⏳ | 654a3dd3 | User Stories |
| `docs/stories/observability.md` | И | — | — | — | ⏳ | 654a3dd3 | User Stories |
| `docs/stories/observability.md` | П | — | — | — | ⏳ | 654a3dd3 | User Stories |
| `docs/stories/platform-module.md` | В | — | — | — | ⏳ | cde57b9f | User Stories |
| `docs/stories/platform-module.md` | И | — | — | — | ⏳ | cde57b9f | User Stories |
| `docs/stories/platform-module.md` | П | — | — | — | ⏳ | cde57b9f | User Stories |
| `docs/stories/sandbox.md` | В | Claude, роль Владелец продукта | 🤖 | 2026-10-13 | ✅ | 3ec8d662 | достаточно |
| `docs/stories/sandbox.md` | И | Claude, роль Аналитик историй | 🤖 | 2026-10-13 | ✅ | 3ec8d662 | достаточно |
| `docs/stories/sandbox.md` | П | Claude, роль Пользователь | 🤖 | 2026-10-13 | ✅ | 3ec8d662 | достаточно |
| `docs/tasks/1.1-mock-llm-litellm.md` | В | — | — | — | ⏳ | ef73dd9b | Задача |
| `docs/tasks/1.1-mock-llm-litellm.md` | Р | — | — | — | ⏳ | ef73dd9b | Задача |
| `docs/tasks/1.1-mock-llm-litellm.md` | Т | — | — | — | ⏳ | ef73dd9b | Задача |
| `docs/tasks/1.2-agent-definition-yaml.md` | В | Claude, роль Владелец продукта | 🤖 | 2026-10-13 | ✅ | d6f47d29 | повторная проверка: закрытие прежних замечаний на месте, приёмка/требования/декомпозиция согласованы |
| `docs/tasks/1.2-agent-definition-yaml.md` | Р | Claude, роль Разработчик | 🤖 | 2026-10-13 | ✅ | d6f47d29 | повторная проверка: закрытие прежних замечаний на месте, приёмка/требования/декомпозиция согласованы |
| `docs/tasks/1.2-agent-definition-yaml.md` | Т | Claude, роль Тестировщик | 🤖 | 2026-10-13 | ✅ | d6f47d29 | повторная проверка: закрытие прежних замечаний на месте, приёмка/требования/декомпозиция согласованы |
| `docs/tasks/1.3-harness-core.md` | В | — | — | — | ⏳ | 79ab90dd | текст изменён после решения «✅» от Claude, роль Владелец продукта |
| `docs/tasks/1.3-harness-core.md` | Р | — | — | — | ⏳ | 79ab90dd | текст изменён после решения «✅» от Claude, роль Разработчик |
| `docs/tasks/1.3-harness-core.md` | Т | — | — | — | ⏳ | 79ab90dd | текст изменён после решения «✅» от Claude, роль Тестировщик |
| `docs/tasks/1.4-harness-mcp-tools.md` | В | — | — | — | ⏳ | 754c6d5c | текст изменён после решения «✅» от Claude, роль Владелец продукта |
| `docs/tasks/1.4-harness-mcp-tools.md` | Р | — | — | — | ⏳ | 754c6d5c | текст изменён после решения «✅» от Claude, роль Разработчик |
| `docs/tasks/1.4-harness-mcp-tools.md` | Т | — | — | — | ⏳ | 754c6d5c | текст изменён после решения «✅» от Claude, роль Тестировщик |
| `docs/tasks/1.5-harness-hooks-approve.md` | В | — | — | — | ⏳ | 32b8ac79 | текст изменён после решения «✅» от Claude, роль Владелец продукта |
| `docs/tasks/1.5-harness-hooks-approve.md` | Р | — | — | — | ⏳ | 32b8ac79 | текст изменён после решения «✅» от Claude, роль Разработчик |
| `docs/tasks/1.5-harness-hooks-approve.md` | Т | — | — | — | ⏳ | 32b8ac79 | текст изменён после решения «✅» от Claude, роль Тестировщик |
| `docs/tasks/1.6-harness-limits-context.md` | В | — | — | — | ⏳ | 2525b206 | текст изменён после решения «✅» от Claude, роль Владелец продукта |
| `docs/tasks/1.6-harness-limits-context.md` | Р | — | — | — | ⏳ | 2525b206 | текст изменён после решения «✅» от Claude, роль Разработчик |
| `docs/tasks/1.6-harness-limits-context.md` | Т | — | — | — | ⏳ | 2525b206 | текст изменён после решения «✅» от Claude, роль Тестировщик |
| `docs/tasks/1.7-dev-ui.md` | В | Claude, роль Владелец продукта | 🤖 | 2026-10-13 | ✅ | 2d8becba | достаточно |
| `docs/tasks/1.7-dev-ui.md` | Р | Claude, роль Разработчик | 🤖 | 2026-10-13 | ✅ | 2d8becba | достаточно |
| `docs/tasks/1.7-dev-ui.md` | Т | Claude, роль Тестировщик | 🤖 | 2026-10-13 | ✅ | 2d8becba | достаточно |
| `docs/tasks/2.1-runner-external.md` | В | — | — | — | ⏳ | 3b865677 | текст изменён после решения «✅» от Claude, роль Владелец продукта |
| `docs/tasks/2.1-runner-external.md` | Р | — | — | — | ⏳ | 3b865677 | текст изменён после решения «✅» от Claude, роль Разработчик |
| `docs/tasks/2.1-runner-external.md` | Т | — | — | — | ⏳ | 3b865677 | текст изменён после решения «✅» от Claude, роль Тестировщик |
| `docs/tasks/2.2-sandbox-docker-oneshot.md` | В | — | — | — | ⏳ | 53d77597 | текст изменён после решения «✅» от Claude, роль Владелец продукта |
| `docs/tasks/2.2-sandbox-docker-oneshot.md` | Р | — | — | — | ⏳ | 53d77597 | текст изменён после решения «✅» от Claude, роль Разработчик |
| `docs/tasks/2.2-sandbox-docker-oneshot.md` | Т | — | — | — | ⏳ | 53d77597 | текст изменён после решения «✅» от Claude, роль Тестировщик |
| `docs/tasks/2.3-config-from-icplan.md` | В | Claude, роль Владелец продукта | 🤖 | 2026-10-13 | ✅ | 9a602cc4 | повторная проверка: закрытие прежних замечаний на месте, приёмка/требования/декомпозиция согласованы |
| `docs/tasks/2.3-config-from-icplan.md` | Р | Claude, роль Разработчик | 🤖 | 2026-10-13 | ✅ | 9a602cc4 | повторная проверка: закрытие прежних замечаний на месте, приёмка/требования/декомпозиция согласованы |
| `docs/tasks/2.3-config-from-icplan.md` | Т | Claude, роль Тестировщик | 🤖 | 2026-10-13 | ✅ | 9a602cc4 | повторная проверка: закрытие прежних замечаний на месте, приёмка/требования/декомпозиция согласованы |
| `docs/tasks/2.4-mcp-itsaplan-core.md` | В | — | — | — | ⏳ | 6bd4fdd1 | текст изменён после решения «✅» от Claude, роль Владелец продукта |
| `docs/tasks/2.4-mcp-itsaplan-core.md` | Р | — | — | — | ⏳ | 6bd4fdd1 | текст изменён после решения «✅» от Claude, роль Разработчик |
| `docs/tasks/2.4-mcp-itsaplan-core.md` | Т | — | — | — | ⏳ | 6bd4fdd1 | текст изменён после решения «✅» от Claude, роль Тестировщик |
| `docs/tasks/2.5-memory-m2-m3.md` | В | — | — | — | ⏳ | 4c3692bc | Задача |
| `docs/tasks/2.5-memory-m2-m3.md` | Р | — | — | — | ⏳ | 4c3692bc | Задача |
| `docs/tasks/2.5-memory-m2-m3.md` | Т | — | — | — | ⏳ | 4c3692bc | Задача |
| `docs/tasks/2.6-e2e-icplan.md` | В | Claude, роль Владелец продукта | 🤖 | 2026-10-13 | ✅ | d3f3b496 | Z-ICP-122 закрыто: приёмка по сценариям, 2.6.6-2.6.7, оценка 28 ч в 3-4 дн |
| `docs/tasks/2.6-e2e-icplan.md` | Р | Claude, роль Разработчик | 🤖 | 2026-10-13 | ✅ | d3f3b496 | сценарии отказов разложены по подзадачам 2.6.6-2.6.7 с готовностью |
| `docs/tasks/2.6-e2e-icplan.md` | Т | Claude, роль Тестировщик | 🤖 | 2026-10-13 | ✅ | d3f3b496 | приёмка: сценарий -> результат по R-ICP-13, R-RUN-08, R-RUN-14 |
| `docs/tasks/2.7-runner-scheduler.md` | В | — | — | — | ⏳ | f28fd7ec | текст изменён после решения «✅» от Claude, роль Владелец продукта |
| `docs/tasks/2.7-runner-scheduler.md` | Р | — | — | — | ⏳ | f28fd7ec | текст изменён после решения «✅» от Claude, роль Разработчик |
| `docs/tasks/2.7-runner-scheduler.md` | Т | — | — | — | ⏳ | f28fd7ec | текст изменён после решения «✅» от Claude, роль Тестировщик |
| `docs/tasks/2.8-config-storage-interfaces-fmea.md` | В | — | — | — | ⏳ | 5a41f0e0 | Задача |
| `docs/tasks/2.8-config-storage-interfaces-fmea.md` | Р | — | — | — | ⏳ | 5a41f0e0 | Задача |
| `docs/tasks/2.8-config-storage-interfaces-fmea.md` | Т | — | — | — | ⏳ | 5a41f0e0 | Задача |
| `docs/tasks/3.1-icplan-process-step-agent.md` | В | — | — | — | ⏳ | 99a7a101 | текст изменён после решения «✅» от Claude, роль Владелец продукта |
| `docs/tasks/3.1-icplan-process-step-agent.md` | Р | — | — | — | ⏳ | 99a7a101 | текст изменён после решения «✅» от Claude, роль Разработчик |
| `docs/tasks/3.1-icplan-process-step-agent.md` | Т | — | — | — | ⏳ | 99a7a101 | текст изменён после решения «✅» от Claude, роль Тестировщик |
| `docs/tasks/3.2-icplan-handoff.md` | В | Claude, роль Владелец продукта | 🤖 | 2026-10-13 | ✅ | 353ac49e | повторная проверка: закрытие прежних замечаний на месте, приёмка/требования/декомпозиция согласованы |
| `docs/tasks/3.2-icplan-handoff.md` | Р | Claude, роль Разработчик | 🤖 | 2026-10-13 | ✅ | 353ac49e | повторная проверка: закрытие прежних замечаний на месте, приёмка/требования/декомпозиция согласованы |
| `docs/tasks/3.2-icplan-handoff.md` | Т | Claude, роль Тестировщик | 🤖 | 2026-10-13 | ✅ | 353ac49e | повторная проверка: закрытие прежних замечаний на месте, приёмка/требования/декомпозиция согласованы |
| `docs/tasks/3.3-run-events-timeline.md` | В | — | — | — | ⏳ | 0d953076 | Задача |
| `docs/tasks/3.3-run-events-timeline.md` | Р | — | — | — | ⏳ | 0d953076 | Задача |
| `docs/tasks/3.3-run-events-timeline.md` | Т | — | — | — | ⏳ | 0d953076 | Задача |
| `docs/tasks/3.4-icplan-approve-ui.md` | В | Claude, роль Владелец продукта | 🤖 | 2026-10-13 | ✅ | 7e4acf6b | повторная проверка: закрытие прежних замечаний на месте, приёмка/требования/декомпозиция согласованы |
| `docs/tasks/3.4-icplan-approve-ui.md` | Р | Claude, роль Разработчик | 🤖 | 2026-10-13 | ✅ | 7e4acf6b | повторная проверка: закрытие прежних замечаний на месте, приёмка/требования/декомпозиция согласованы |
| `docs/tasks/3.4-icplan-approve-ui.md` | Т | Claude, роль Тестировщик | 🤖 | 2026-10-13 | ✅ | 7e4acf6b | повторная проверка: закрытие прежних замечаний на месте, приёмка/требования/декомпозиция согласованы |
| `docs/tasks/3.5-icplan-type-actions-cost.md` | В | Claude, роль Владелец продукта | 🤖 | 2026-10-13 | ✅ | e47aae72 | повторно: замечания Z-ICP-5/60/83/96 закрыты в тексте (3.5.1–3.5.5, приёмка по сценариям R-AP-03/R-LLM-02/R-OBS-05) |
| `docs/tasks/3.5-icplan-type-actions-cost.md` | Р | Claude, роль Разработчик | 🤖 | 2026-10-13 | ✅ | e47aae72 | повторно: замечания Z-ICP-5/60/83/96 закрыты в тексте (3.5.1–3.5.5, приёмка по сценариям R-AP-03/R-LLM-02/R-OBS-05) |
| `docs/tasks/3.5-icplan-type-actions-cost.md` | Т | Claude, роль Тестировщик | 🤖 | 2026-10-13 | ✅ | e47aae72 | повторно: замечания Z-ICP-5/60/83/96 закрыты в тексте (3.5.1–3.5.5, приёмка по сценариям R-AP-03/R-LLM-02/R-OBS-05) |
| `docs/tasks/3.6-icplan-process-engine.md` | В | Claude, роль Владелец продукта | 🤖 | 2026-10-13 | ✅ | 8a659c27 | Z-ICP-123 закрыто; оценка 31 ч сходится |
| `docs/tasks/3.6-icplan-process-engine.md` | Р | Claude, роль Разработчик | 🤖 | 2026-10-13 | ✅ | 8a659c27 | 3.6.5 покрывает порядок, второй запуск, истечение аренды |
| `docs/tasks/3.6-icplan-process-engine.md` | Т | Claude, роль Тестировщик | 🤖 | 2026-10-13 | ✅ | 8a659c27 | приёмка: активный запуск и истёкшая аренда проверяемы, R-AP-17 |
| `docs/tasks/3.7-icplan-task-control.md` | В | — | — | — | ⏳ | 226b1955 | текст изменён после решения «✅» от Claude, роль Владелец продукта |
| `docs/tasks/3.7-icplan-task-control.md` | Р | — | — | — | ⏳ | 226b1955 | текст изменён после решения «✅» от Claude, роль Разработчик |
| `docs/tasks/3.7-icplan-task-control.md` | Т | — | — | — | ⏳ | 226b1955 | текст изменён после решения «✅» от Claude, роль Тестировщик |
| `docs/tasks/3.8-agent-chat-control.md` | В | — | — | — | ⏳ | 38748459 | текст изменён после решения «✅» от Claude, роль Владелец продукта |
| `docs/tasks/3.8-agent-chat-control.md` | Р | — | — | — | ⏳ | 38748459 | текст изменён после решения «✅» от Claude, роль Разработчик |
| `docs/tasks/3.8-agent-chat-control.md` | Т | — | — | — | ⏳ | 38748459 | текст изменён после решения «✅» от Claude, роль Тестировщик |
| `docs/tasks/3.9-agent-summary-stats.md` | В | Claude, роль Владелец продукта | 🤖 | 2026-10-13 | ✅ | a39f3839 | R-OBS-13: подзадачи 3.9.1–3.9.5, приёмка с отказом LiteLLM |
| `docs/tasks/3.9-agent-summary-stats.md` | Р | Claude, роль Разработчик | 🤖 | 2026-10-13 | ✅ | a39f3839 | R-OBS-13: подзадачи 3.9.1–3.9.5, приёмка с отказом LiteLLM |
| `docs/tasks/3.9-agent-summary-stats.md` | Т | Claude, роль Тестировщик | 🤖 | 2026-10-13 | ✅ | a39f3839 | повторная проверка: приёмка по сценариям (восстановлено после гонки записи реестра) |
| `docs/tasks/4.1-sandbox-warm-pool.md` | В | — | — | — | ⏳ | 9395a03b | текст изменён после решения «✅» от Claude, роль Владелец продукта |
| `docs/tasks/4.1-sandbox-warm-pool.md` | Р | — | — | — | ⏳ | 9395a03b | текст изменён после решения «✅» от Claude, роль Разработчик |
| `docs/tasks/4.1-sandbox-warm-pool.md` | Т | — | — | — | ⏳ | 9395a03b | текст изменён после решения «✅» от Claude, роль Тестировщик |
| `docs/tasks/4.2-egress-repo-access.md` | В | — | — | — | ⏳ | ce72d242 | Задача |
| `docs/tasks/4.2-egress-repo-access.md` | Р | — | — | — | ⏳ | ce72d242 | Задача |
| `docs/tasks/4.2-egress-repo-access.md` | Т | — | — | — | ⏳ | ce72d242 | Задача |
| `docs/tasks/4.3-guardrails-opa.md` | В | — | — | — | ⏳ | 57d3fe2e | Задача |
| `docs/tasks/4.3-guardrails-opa.md` | Р | — | — | — | ⏳ | 57d3fe2e | Задача |
| `docs/tasks/4.3-guardrails-opa.md` | Т | — | — | — | ⏳ | 57d3fe2e | Задача |
| `docs/tasks/4.4-platform-module.md` | В | — | — | — | ⏳ | 6b825d8e | Задача |
| `docs/tasks/4.4-platform-module.md` | Р | — | — | — | ⏳ | 6b825d8e | Задача |
| `docs/tasks/4.4-platform-module.md` | Т | — | — | — | ⏳ | 6b825d8e | Задача |
| `docs/tasks/4.5-litellm-budgets-fallback-g4.md` | В | — | — | — | ⏳ | 68726eda | Задача |
| `docs/tasks/4.5-litellm-budgets-fallback-g4.md` | Р | — | — | — | ⏳ | 68726eda | Задача |
| `docs/tasks/4.5-litellm-budgets-fallback-g4.md` | Т | — | — | — | ⏳ | 68726eda | Задача |
| `docs/tasks/4.6-k8s-helm-ingress.md` | В | — | — | — | ⏳ | 7beb2faa | Задача |
| `docs/tasks/4.6-k8s-helm-ingress.md` | Р | — | — | — | ⏳ | 7beb2faa | Задача |
| `docs/tasks/4.6-k8s-helm-ingress.md` | Т | — | — | — | ⏳ | 7beb2faa | Задача |
| `docs/tasks/4.7-postgres-storage-backup.md` | В | — | — | — | ⏳ | 9dfefec2 | Задача |
| `docs/tasks/4.7-postgres-storage-backup.md` | Р | — | — | — | ⏳ | 9dfefec2 | Задача |
| `docs/tasks/4.7-postgres-storage-backup.md` | Т | — | — | — | ⏳ | 9dfefec2 | Задача |
| `docs/tasks/4.8-load-test.md` | В | — | — | — | ⏳ | 4a97957b | Задача |
| `docs/tasks/4.8-load-test.md` | Р | — | — | — | ⏳ | 4a97957b | Задача |
| `docs/tasks/4.8-load-test.md` | Т | — | — | — | ⏳ | 4a97957b | Задача |
| `docs/techspec/agent-runner.md` | Д | — | — | — | ⏳ | b98a1154 | текст изменён после решения «✅» от Claude, роль DevOps-инженер |
| `docs/techspec/agent-runner.md` | Б | — | — | — | ⏳ | b98a1154 | текст изменён после решения «✅» от Claude, роль Безопасность |
| `docs/techspec/agent-runner.md` | С | — | — | — | ⏳ | b98a1154 | текст изменён после решения «✅» от Claude, роль Инженер сборки и поставки |
| `docs/techspec/guardrails.md` | Д | — | — | — | ⏳ | 07b0bc0d | Deploy |
| `docs/techspec/guardrails.md` | Б | — | — | — | ⏳ | 07b0bc0d | Deploy |
| `docs/techspec/guardrails.md` | С | — | — | — | ⏳ | 07b0bc0d | Deploy |
| `docs/techspec/harness.md` | Д | — | — | — | ⏳ | 107eb106 | Deploy |
| `docs/techspec/harness.md` | Б | — | — | — | ⏳ | 107eb106 | Deploy |
| `docs/techspec/harness.md` | С | — | — | — | ⏳ | 107eb106 | Deploy |
| `docs/techspec/icplan.md` | Д | Claude, роль DevOps-инженер | 🤖 | 2026-10-13 | ✅ | c8b90db6 | повторно: emptyDir /tmp, MIGRATION_DATABASE_URL, переменные AGENT_RUN_*/RUNNER_OFFLINE_AFTER_S/REVIEW_REMINDER_HOURS/retention, откат через PITR в отдельный кластер; Z-ICP-98..100 закрыты |
| `docs/techspec/icplan.md` | Б | Claude, роль Безопасность | 🤖 | 2026-10-13 | ✅ | c8b90db6 | повторно: secrets.existingSecret, шифротекст с APP_ENCRYPTION_KEY вне БД, non-root, readOnlyRootFilesystem; Z-ICP-102/103 закрыты |
| `docs/techspec/icplan.md` | С | Claude, роль Инженер сборки и поставки | 🤖 | 2026-10-13 | ✅ | c8b90db6 | повторно: сборка web с CLOUD_UI_ENTRY (4.6.10), теги X.Y.Z-sha, SBOM/trivy, проверка после развёртывания; Z-ICP-101 закрыт |
| `docs/techspec/infrastructure.md` | Д | — | — | — | ⏳ | 7659af2f | Deploy |
| `docs/techspec/infrastructure.md` | Б | — | — | — | ⏳ | 7659af2f | Deploy |
| `docs/techspec/infrastructure.md` | С | — | — | — | ⏳ | 7659af2f | Deploy |
| `docs/techspec/llm-gateway.md` | Д | — | — | — | ⏳ | d6da2a0b | Deploy |
| `docs/techspec/llm-gateway.md` | Б | — | — | — | ⏳ | d6da2a0b | Deploy |
| `docs/techspec/llm-gateway.md` | С | — | — | — | ⏳ | d6da2a0b | Deploy |
| `docs/techspec/mcp-tools.md` | Д | — | — | — | ⏳ | da409342 | Deploy |
| `docs/techspec/mcp-tools.md` | Б | — | — | — | ⏳ | da409342 | Deploy |
| `docs/techspec/mcp-tools.md` | С | — | — | — | ⏳ | da409342 | Deploy |
| `docs/techspec/memory.md` | Д | — | — | — | ⏳ | e40678d0 | Deploy |
| `docs/techspec/memory.md` | Б | — | — | — | ⏳ | e40678d0 | Deploy |
| `docs/techspec/memory.md` | С | — | — | — | ⏳ | e40678d0 | Deploy |
| `docs/techspec/observability.md` | Д | — | — | — | ⏳ | 155a22e5 | Deploy |
| `docs/techspec/observability.md` | Б | — | — | — | ⏳ | 155a22e5 | Deploy |
| `docs/techspec/observability.md` | С | — | — | — | ⏳ | 155a22e5 | Deploy |
| `docs/techspec/platform-module.md` | Д | — | — | — | ⏳ | a4a5dd02 | Deploy |
| `docs/techspec/platform-module.md` | Б | — | — | — | ⏳ | a4a5dd02 | Deploy |
| `docs/techspec/platform-module.md` | С | — | — | — | ⏳ | a4a5dd02 | Deploy |
| `docs/techspec/sandbox.md` | Д | — | — | — | ⏳ | 4e939442 | Deploy |
| `docs/techspec/sandbox.md` | Б | — | — | — | ⏳ | 4e939442 | Deploy |
| `docs/techspec/sandbox.md` | С | — | — | — | ⏳ | 4e939442 | Deploy |
| `index.md` | В | — | — | — | ⏳ | 42b2b191 | Главная |
| `index.md` | А | — | — | — | ⏳ | 42b2b191 | Главная |
| `openspec/changes/define-agent-platform/design.md` | В | — | — | — | ⏳ | f1c09b02 | Решения (design) |
| `openspec/changes/define-agent-platform/design.md` | А | — | — | — | ⏳ | f1c09b02 | Решения (design) |
