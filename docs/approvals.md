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
| `components/agent-runner/finalizer/index.md` | А | Claude, роль Архитектор | 🤖 | 2026-10-13 | ✅ | 77af23f6 | Данные и связи определены |
| `components/agent-runner/finalizer/index.md` | Р | Claude, роль Разработчик | 🤖 | 2026-10-13 | ✅ | 77af23f6 | Операции и входы-выходы есть |
| `components/agent-runner/finalizer/index.md` | Т | Claude, роль Тестировщик | 🤖 | 2026-10-13 | ✅ | 77af23f6 | Сбои и повторы проверяемы |
| `components/agent-runner/index.md` | А | Claude, роль Архитектор | 🤖 | 2026-10-13 | ✅ | 7222f959 | C1/sequence, I-коды, D23/D19, таблица статусов R-HRN-09→R-RUN-07→agent_run, +/- есть; границы с ICPlan/Platform/Sandbox определены |
| `components/agent-runner/index.md` | Р | Claude, роль Разработчик | 🤖 | 2026-10-13 | ✅ | 7222f959 | порядок работы с I-кодами и моделями, статусы и переходы, ссылки на Deploy/интеграции — реализуемо |
| `components/agent-runner/mcp-proksi/index.md` | А | Claude, роль Архитектор | 🤖 | 2026-10-13 | ✅ | 5e8f8a4b | Граница с OPA и MCP ясна |
| `components/agent-runner/mcp-proksi/index.md` | Р | Claude, роль Разработчик | 🤖 | 2026-10-13 | ✅ | 5e8f8a4b | Операции и параметры есть |
| `components/agent-runner/mcp-proksi/index.md` | Т | Claude, роль Тестировщик | 🤖 | 2026-10-13 | ✅ | 5e8f8a4b | Отказы проверяемы |
| `components/agent-runner/poller/index.md` | А | Claude, роль Архитектор | 🤖 | 2026-10-13 | ✅ | f46606ba | Связь с I1 определена |
| `components/agent-runner/poller/index.md` | Р | Claude, роль Разработчик | 🤖 | 2026-10-13 | ✅ | f46606ba | Операция и параметры есть |
| `components/agent-runner/poller/index.md` | Т | Claude, роль Тестировщик | 🤖 | 2026-10-13 | ✅ | f46606ba | Backoff и сценарии проверяемы |
| `components/agent-runner/run-supervisor/index.md` | А | Claude, роль Архитектор | 🤖 | 2026-10-13 | ✅ | 01f2b436 | Связи определены |
| `components/agent-runner/run-supervisor/index.md` | Р | Claude, роль Разработчик | 🤖 | 2026-10-13 | ✅ | 01f2b436 | Операции и параметры есть |
| `components/agent-runner/run-supervisor/index.md` | Т | Claude, роль Тестировщик | 🤖 | 2026-10-13 | ✅ | 01f2b436 | Сбои заданы |
| `components/agent-runner/sandbox-claim/index.md` | А | Claude, роль Архитектор | 🤖 | 2026-10-13 | ✅ | eda47963 | Граница с Sandbox ясна |
| `components/agent-runner/sandbox-claim/index.md` | Р | Claude, роль Разработчик | 🤖 | 2026-10-13 | ✅ | eda47963 | Операции и параметры есть |
| `components/agent-runner/sandbox-claim/index.md` | Т | Claude, роль Тестировщик | 🤖 | 2026-10-13 | ✅ | eda47963 | Сбои проверяемы |
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
| `components/guardrails/konfig-deploya/index.md` | А | — | — | — | ⏳ | 022750c1 | Блок |
| `components/guardrails/konfig-deploya/index.md` | Р | — | — | — | ⏳ | 022750c1 | Блок |
| `components/guardrails/konfig-deploya/index.md` | Т | — | — | — | ⏳ | 022750c1 | Блок |
| `components/guardrails/opa/index.md` | А | — | — | — | ⏳ | 43cb7b84 | Блок |
| `components/guardrails/opa/index.md` | Р | — | — | — | ⏳ | 43cb7b84 | Блок |
| `components/guardrails/opa/index.md` | Т | — | — | — | ⏳ | 43cb7b84 | Блок |
| `components/guardrails/rego-v-git/index.md` | А | — | — | — | ⏳ | 886adf44 | Блок |
| `components/guardrails/rego-v-git/index.md` | Р | — | — | — | ⏳ | 886adf44 | Блок |
| `components/guardrails/rego-v-git/index.md` | Т | — | — | — | ⏳ | 886adf44 | Блок |
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
| `components/icplan/avtopodhvat/index.md` | А | Claude, роль Архитектор | 🤖 | 2026-10-13 | ✅ | 56a6d389 | Повтор: Z-ICP-64/72/84 закрыты в тексте (process_version в Данных, при сбое: лимит max_runs → on_failure, 5 попыток); операции, данные, сбои определены |
| `components/icplan/avtopodhvat/index.md` | Р | Claude, роль Разработчик | 🤖 | 2026-10-13 | ✅ | 56a6d389 | Повтор: Z-ICP-64/72/84 закрыты в тексте (process_version в Данных, при сбое: лимит max_runs → on_failure, 5 попыток); операции, данные, сбои определены |
| `components/icplan/avtopodhvat/index.md` | Т | Claude, роль Тестировщик | 🤖 | 2026-10-13 | ✅ | 56a6d389 | Повтор: Z-ICP-64/72/84 закрыты в тексте (process_version в Данных, при сбое: лимит max_runs → on_failure, 5 попыток); операции, данные, сбои определены |
| `components/icplan/control-plane-ui/index.md` | А | Claude, роль Архитектор | 🤖 | 2026-10-13 | ✅ | 76bdaaea | Повтор: Z-ICP-65/73/74/75/85 закрыты в тексте (экраны с эндпоинтами, DELETE профилей 409, сбой LiteLLM 503) |
| `components/icplan/control-plane-ui/index.md` | Р | Claude, роль Разработчик | 🤖 | 2026-10-13 | ✅ | 76bdaaea | Повтор: Z-ICP-65/73/74/75/85 закрыты в тексте (экраны с эндпоинтами, DELETE профилей 409, сбой LiteLLM 503) |
| `components/icplan/control-plane-ui/index.md` | Т | Claude, роль Тестировщик | 🤖 | 2026-10-13 | ✅ | 76bdaaea | Повтор: Z-ICP-65/73/74/75/85 закрыты в тексте (экраны с эндпоинтами, DELETE профилей 409, сбой LiteLLM 503) |
| `components/icplan/index.md` | А | Claude, роль Архитектор | 🤖 | 2026-10-13 | ✅ | dc437139 | Повтор: Z-ICP-34/63 закрыты (встроенные в зоне, I4 и decisions в С1), порядок работы с данными и I-кодами |
| `components/icplan/index.md` | Р | Claude, роль Разработчик | 🤖 | 2026-10-13 | ✅ | dc437139 | Повтор: Z-ICP-1/71 закрыты (С1 с I4, decisions); потоки, данные, I-коды определены |
| `components/icplan/registry/index.md` | А | Claude, роль Архитектор | 🤖 | 2026-10-13 | ✅ | bf904abc | Повтор: Z-ICP-66/76 закрыты (apikey, integration_credential в Данных; версии по D26) |
| `components/icplan/registry/index.md` | Р | Claude, роль Разработчик | 🤖 | 2026-10-13 | ✅ | bf904abc | Повтор: Z-ICP-66/76 закрыты (apikey, integration_credential в Данных; версии по D26) |
| `components/icplan/registry/index.md` | Т | Claude, роль Тестировщик | 🤖 | 2026-10-13 | ✅ | bf904abc | Повтор: сценарии R-REG-01..06 проверяемы; Z-ICP-86 ждёт владельца, не блокирует |
| `components/icplan/run-queue-runner-api/index.md` | А | Claude, роль Архитектор | 🤖 | 2026-10-13 | ✅ | cec509f3 | Повтор: Z-ICP-77/87 закрыты (отмена только 404 на heartbeat, MAX_ATTEMPTS=3 → failed); операции, данные, сбои определены |
| `components/icplan/run-queue-runner-api/index.md` | Р | Claude, роль Разработчик | 🤖 | 2026-10-13 | ✅ | cec509f3 | Повтор: Z-ICP-77/87 закрыты (отмена только 404 на heartbeat, MAX_ATTEMPTS=3 → failed); операции, данные, сбои определены |
| `components/icplan/run-queue-runner-api/index.md` | Т | Claude, роль Тестировщик | 🤖 | 2026-10-13 | ✅ | cec509f3 | Повтор: Z-ICP-77/87 закрыты (отмена только 404 на heartbeat, MAX_ATTEMPTS=3 → failed); операции, данные, сбои определены |
| `components/icplan/task-ui/index.md` | А | Claude, роль Архитектор | 🤖 | 2026-10-12 | ✅ | 681818b3 | повторная проверка: вердикт в issue_process_state, затраты — LiteLLM_SpendLogs ролью litellm_read, эндпоинты I20 |
| `components/icplan/task-ui/index.md` | Р | Claude, роль Разработчик | 🤖 | 2026-10-12 | ✅ | 681818b3 | повторная проверка: 9 экранов с эндпоинтами, источники вердикта и затрат, сбои |
| `components/icplan/task-ui/index.md` | Т | Claude, роль Тестировщик | 🤖 | 2026-10-12 | ✅ | 681818b3 | повторная проверка: экраны с эндпоинтами и ошибками; SSE, цена неизвестна; Z-ICP-31/32 закрыты |
| `components/infrastructure/index.md` | А | — | — | — | ⏳ | d8325b1e | Архитектура компонента |
| `components/infrastructure/index.md` | Р | — | — | — | ⏳ | d8325b1e | Архитектура компонента |
| `components/infrastructure/pgbouncer/index.md` | А | — | — | — | ⏳ | 69b9c278 | Блок |
| `components/infrastructure/pgbouncer/index.md` | Р | — | — | — | ⏳ | 69b9c278 | Блок |
| `components/infrastructure/pgbouncer/index.md` | Т | — | — | — | ⏳ | 69b9c278 | Блок |
| `components/infrastructure/postgresql-17-pgvector/index.md` | А | — | — | — | ⏳ | a1652446 | Блок |
| `components/infrastructure/postgresql-17-pgvector/index.md` | Р | — | — | — | ⏳ | a1652446 | Блок |
| `components/infrastructure/postgresql-17-pgvector/index.md` | Т | — | — | — | ⏳ | a1652446 | Блок |
| `components/infrastructure/rezervnoe-hranilische-s3-vne-uzla/index.md` | А | — | — | — | ⏳ | d1dddbdb | Блок |
| `components/infrastructure/rezervnoe-hranilische-s3-vne-uzla/index.md` | Р | — | — | — | ⏳ | d1dddbdb | Блок |
| `components/infrastructure/rezervnoe-hranilische-s3-vne-uzla/index.md` | Т | — | — | — | ⏳ | d1dddbdb | Блок |
| `components/infrastructure/rustfs/index.md` | А | — | — | — | ⏳ | 3b4341a4 | Блок |
| `components/infrastructure/rustfs/index.md` | Р | — | — | — | ⏳ | 3b4341a4 | Блок |
| `components/infrastructure/rustfs/index.md` | Т | — | — | — | ⏳ | 3b4341a4 | Блок |
| `components/infrastructure/traefik/index.md` | А | — | — | — | ⏳ | 38bad3d4 | Блок |
| `components/infrastructure/traefik/index.md` | Р | — | — | — | ⏳ | 38bad3d4 | Блок |
| `components/infrastructure/traefik/index.md` | Т | — | — | — | ⏳ | 38bad3d4 | Блок |
| `components/llm-gateway/aliasy/index.md` | А | — | — | — | ⏳ | e66e32c7 | Блок |
| `components/llm-gateway/aliasy/index.md` | Р | — | — | — | ⏳ | e66e32c7 | Блок |
| `components/llm-gateway/aliasy/index.md` | Т | — | — | — | ⏳ | e66e32c7 | Блок |
| `components/llm-gateway/byudzhety-rate-limit/index.md` | А | — | — | — | ⏳ | 9869c49c | Блок |
| `components/llm-gateway/byudzhety-rate-limit/index.md` | Р | — | — | — | ⏳ | 9869c49c | Блок |
| `components/llm-gateway/byudzhety-rate-limit/index.md` | Т | — | — | — | ⏳ | 9869c49c | Блок |
| `components/llm-gateway/fallback/index.md` | А | — | — | — | ⏳ | 98fba7b9 | Блок |
| `components/llm-gateway/fallback/index.md` | Р | — | — | — | ⏳ | 98fba7b9 | Блок |
| `components/llm-gateway/fallback/index.md` | Т | — | — | — | ⏳ | 98fba7b9 | Блок |
| `components/llm-gateway/g4-huki/index.md` | А | — | — | — | ⏳ | 7c9c5ecb | Блок |
| `components/llm-gateway/g4-huki/index.md` | Р | — | — | — | ⏳ | 7c9c5ecb | Блок |
| `components/llm-gateway/g4-huki/index.md` | Т | — | — | — | ⏳ | 7c9c5ecb | Блок |
| `components/llm-gateway/index.md` | А | — | — | — | ⏳ | a0eea543 | Архитектура компонента |
| `components/llm-gateway/index.md` | Р | — | — | — | ⏳ | a0eea543 | Архитектура компонента |
| `components/llm-gateway/mock-llm/index.md` | А | — | — | — | ⏳ | 603a06de | Блок |
| `components/llm-gateway/mock-llm/index.md` | Р | — | — | — | ⏳ | 603a06de | Блок |
| `components/llm-gateway/mock-llm/index.md` | Т | — | — | — | ⏳ | 603a06de | Блок |
| `components/llm-gateway/spend-log/index.md` | А | — | — | — | ⏳ | 972a387f | Блок |
| `components/llm-gateway/spend-log/index.md` | Р | — | — | — | ⏳ | 972a387f | Блок |
| `components/llm-gateway/spend-log/index.md` | Т | — | — | — | ⏳ | 972a387f | Блок |
| `components/llm-gateway/virtual-keys/index.md` | А | — | — | — | ⏳ | 04c645bc | Блок |
| `components/llm-gateway/virtual-keys/index.md` | Р | — | — | — | ⏳ | 04c645bc | Блок |
| `components/llm-gateway/virtual-keys/index.md` | Т | — | — | — | ⏳ | 04c645bc | Блок |
| `components/mcp-tools/git-provayder/index.md` | А | Claude, роль Архитектор | 🤖 | 2026-10-13 | ❌ | de8fc7cd | нет входов/выходов, данных и связей: только tools и токен |
| `components/mcp-tools/git-provayder/index.md` | Р | Claude, роль Разработчик | 🤖 | 2026-10-13 | ❌ | de8fc7cd | нет операций, требований и задачи — начать реализацию нельзя |
| `components/mcp-tools/git-provayder/index.md` | Т | Claude, роль Тестировщик | 🤖 | 2026-10-13 | ❌ | de8fc7cd | нет сценария, результата и поведения при сбое |
| `components/mcp-tools/index.md` | А | Claude, роль Архитектор | 🤖 | 2026-10-13 | ✅ | 25460dc5 | достаточно |
| `components/mcp-tools/index.md` | Р | Claude, роль Разработчик | 🤖 | 2026-10-13 | ✅ | 25460dc5 | достаточно |
| `components/mcp-tools/itsaplan-core/index.md` | А | Claude, роль Архитектор | 🤖 | 2026-10-13 | ✅ | a67517df | достаточно |
| `components/mcp-tools/itsaplan-core/index.md` | Р | Claude, роль Разработчик | 🤖 | 2026-10-13 | ✅ | a67517df | достаточно |
| `components/mcp-tools/itsaplan-core/index.md` | Т | Claude, роль Тестировщик | 🤖 | 2026-10-13 | ✅ | a67517df | достаточно |
| `components/mcp-tools/memory/index.md` | А | Claude, роль Архитектор | 🤖 | 2026-10-13 | ❌ | 741dc38d | нет io и данных: с какой памятью и API связь не определена |
| `components/mcp-tools/memory/index.md` | Р | Claude, роль Разработчик | 🤖 | 2026-10-13 | ❌ | 741dc38d | нет операций, требований и задачи; только «запись состояния задачи» |
| `components/mcp-tools/memory/index.md` | Т | Claude, роль Тестировщик | 🤖 | 2026-10-13 | ❌ | 741dc38d | нет сценария, результата и поведения при сбое |
| `components/mcp-tools/pravila-r1-r7/index.md` | А | Claude, роль Архитектор | 🤖 | 2026-10-13 | ✅ | d0c9f81d | достаточно |
| `components/mcp-tools/pravila-r1-r7/index.md` | Р | Claude, роль Разработчик | 🤖 | 2026-10-13 | ❌ | d0c9f81d | нет требований и задачи; правила R1, R4–R6 не перечислены |
| `components/mcp-tools/pravila-r1-r7/index.md` | Т | Claude, роль Тестировщик | 🤖 | 2026-10-13 | ❌ | d0c9f81d | нет проверяемых сценариев применения правил |
| `components/memory/index.md` | А | — | — | — | ⏳ | b386ace5 | Архитектура компонента |
| `components/memory/index.md` | Р | — | — | — | ⏳ | b386ace5 | Архитектура компонента |
| `components/memory/m3-zadachnaya/index.md` | А | — | — | — | ⏳ | daea9279 | Блок |
| `components/memory/m3-zadachnaya/index.md` | Р | — | — | — | ⏳ | daea9279 | Блок |
| `components/memory/m3-zadachnaya/index.md` | Т | — | — | — | ⏳ | daea9279 | Блок |
| `components/memory/memory-api/index.md` | А | — | — | — | ⏳ | b4d0664d | Блок |
| `components/memory/memory-api/index.md` | Р | — | — | — | ⏳ | b4d0664d | Блок |
| `components/memory/memory-api/index.md` | Т | — | — | — | ⏳ | b4d0664d | Блок |
| `components/observability/agregaty-zatrat/index.md` | А | — | — | — | ⏳ | fa7d9697 | Блок |
| `components/observability/agregaty-zatrat/index.md` | Р | — | — | — | ⏳ | fa7d9697 | Блок |
| `components/observability/agregaty-zatrat/index.md` | Т | — | — | — | ⏳ | fa7d9697 | Блок |
| `components/observability/index.md` | А | — | — | — | ⏳ | b6af9b9e | Архитектура компонента |
| `components/observability/index.md` | Р | — | — | — | ⏳ | b6af9b9e | Архитектура компонента |
| `components/observability/sobytiya-zapuska/index.md` | А | — | — | — | ⏳ | 47bd4dca | Блок |
| `components/observability/sobytiya-zapuska/index.md` | Р | — | — | — | ⏳ | 47bd4dca | Блок |
| `components/observability/sobytiya-zapuska/index.md` | Т | — | — | — | ⏳ | 47bd4dca | Блок |
| `components/platform-module/aliasy-llm/index.md` | А | — | — | — | ⏳ | f21b192e | Блок |
| `components/platform-module/aliasy-llm/index.md` | Р | — | — | — | ⏳ | f21b192e | Блок |
| `components/platform-module/aliasy-llm/index.md` | Т | — | — | — | ⏳ | f21b192e | Блок |
| `components/platform-module/api-modulya/index.md` | А | — | — | — | ⏳ | 6bc7ebe4 | Блок |
| `components/platform-module/api-modulya/index.md` | Р | — | — | — | ⏳ | 6bc7ebe4 | Блок |
| `components/platform-module/api-modulya/index.md` | Т | — | — | — | ⏳ | 6bc7ebe4 | Блок |
| `components/platform-module/byudzhety/index.md` | А | — | — | — | ⏳ | b3375a79 | Блок |
| `components/platform-module/byudzhety/index.md` | Р | — | — | — | ⏳ | b3375a79 | Блок |
| `components/platform-module/byudzhety/index.md` | Т | — | — | — | ⏳ | b3375a79 | Блок |
| `components/platform-module/dannye-guardrails/index.md` | А | — | — | — | ⏳ | 442a4023 | Блок |
| `components/platform-module/dannye-guardrails/index.md` | Р | — | — | — | ⏳ | 442a4023 | Блок |
| `components/platform-module/dannye-guardrails/index.md` | Т | — | — | — | ⏳ | 442a4023 | Блок |
| `components/platform-module/index.md` | А | — | — | — | ⏳ | 66b5db86 | Архитектура компонента |
| `components/platform-module/index.md` | Р | — | — | — | ⏳ | 66b5db86 | Архитектура компонента |
| `components/platform-module/profili-pamyati/index.md` | А | — | — | — | ⏳ | bfe29d85 | Блок |
| `components/platform-module/profili-pamyati/index.md` | Р | — | — | — | ⏳ | bfe29d85 | Блок |
| `components/platform-module/profili-pamyati/index.md` | Т | — | — | — | ⏳ | bfe29d85 | Блок |
| `components/platform-module/profili-sandbox/index.md` | А | — | — | — | ⏳ | 05448dfa | Блок |
| `components/platform-module/profili-sandbox/index.md` | Р | — | — | — | ⏳ | 05448dfa | Блок |
| `components/platform-module/profili-sandbox/index.md` | Т | — | — | — | ⏳ | 05448dfa | Блок |
| `components/platform-module/versii-agentov/index.md` | А | — | — | — | ⏳ | be36d77b | Блок |
| `components/platform-module/versii-agentov/index.md` | Р | — | — | — | ⏳ | be36d77b | Блок |
| `components/platform-module/versii-agentov/index.md` | Т | — | — | — | ⏳ | be36d77b | Блок |
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
| `docs/api/llm-gateway.md` | А | — | — | — | ⏳ | 5432fee4 | Интеграции |
| `docs/api/llm-gateway.md` | Р | — | — | — | ⏳ | 5432fee4 | Интеграции |
| `docs/api/llm-gateway.md` | Т | — | — | — | ⏳ | 5432fee4 | Интеграции |
| `docs/api/mcp-tools.md` | А | Claude, роль Архитектор | 🤖 | 2026-10-13 | ✅ | e2d6cd24 | достаточно |
| `docs/api/mcp-tools.md` | Р | Claude, роль Разработчик | 🤖 | 2026-10-13 | ✅ | e2d6cd24 | достаточно |
| `docs/api/mcp-tools.md` | Т | Claude, роль Тестировщик | 🤖 | 2026-10-13 | ✅ | e2d6cd24 | достаточно |
| `docs/api/memory.md` | А | — | — | — | ⏳ | 591106ae | Интеграции |
| `docs/api/memory.md` | Р | — | — | — | ⏳ | 591106ae | Интеграции |
| `docs/api/memory.md` | Т | — | — | — | ⏳ | 591106ae | Интеграции |
| `docs/api/observability.md` | А | — | — | — | ⏳ | ea7cc7f8 | Интеграции |
| `docs/api/observability.md` | Р | — | — | — | ⏳ | ea7cc7f8 | Интеграции |
| `docs/api/observability.md` | Т | — | — | — | ⏳ | ea7cc7f8 | Интеграции |
| `docs/api/platform-module.md` | А | — | — | — | ⏳ | 7de78827 | Интеграции |
| `docs/api/platform-module.md` | Р | — | — | — | ⏳ | 7de78827 | Интеграции |
| `docs/api/platform-module.md` | Т | — | — | — | ⏳ | 7de78827 | Интеграции |
| `docs/api/sandbox.md` | А | Claude, роль Архитектор | 🤖 | 2026-10-13 | ✅ | 5a07f788 | достаточно |
| `docs/api/sandbox.md` | Р | Claude, роль Разработчик | 🤖 | 2026-10-13 | ✅ | 5a07f788 | достаточно |
| `docs/api/sandbox.md` | Т | Claude, роль Тестировщик | 🤖 | 2026-10-13 | ✅ | 5a07f788 | достаточно |
| `docs/rnd/agent-workspace.md` | В | — | — | — | ⏳ | 30a7763d | R&D |
| `docs/rnd/agent-workspace.md` | А | — | — | — | ⏳ | 30a7763d | R&D |
| `docs/rnd/autopickup-rules.md` | В | Claude, роль Владелец продукта | 🤖 | 2026-10-13 | ✅ | e0349a00 | цена 7.5-12 дн (3.1+3.6), выбор D17 с опровержением, бэклог зависимостей |
| `docs/rnd/autopickup-rules.md` | А | Claude, роль Архитектор | 🤖 | 2026-10-13 | ✅ | e0349a00 | стыки I1/I2/I20, переход делает ICPlan, Runner/Harness не меняются, порядок ICPlan vs слоты Runner разведён; ОВ-2 не блокирует |
| `docs/rnd/config-storage.md` | В | — | — | — | ⏳ | 141a8126 | R&D |
| `docs/rnd/config-storage.md` | А | — | — | — | ⏳ | 141a8126 | R&D |
| `docs/rnd/data-stores.md` | В | — | — | — | ⏳ | 7d75af89 | R&D |
| `docs/rnd/data-stores.md` | А | — | — | — | ⏳ | 7d75af89 | R&D |
| `docs/rnd/db-roles-schemas.md` | В | — | — | — | ⏳ | b08f9299 | R&D |
| `docs/rnd/db-roles-schemas.md` | А | — | — | — | ⏳ | b08f9299 | R&D |
| `docs/rnd/doc-automation.md` | В | — | — | — | ⏳ | 75904ffa | R&D |
| `docs/rnd/doc-automation.md` | А | — | — | — | ⏳ | 75904ffa | R&D |
| `docs/rnd/fork-run-retention.md` | В | Claude, роль Владелец продукта | 🤖 | 2026-10-13 | ✅ | 865e8bf3 | цена 7 ч (4.7.7 + 2.5.9), срок хранения и история/статистика сохранены, риск по ПДн с условием пересмотра |
| `docs/rnd/fork-run-retention.md` | А | Claude, роль Архитектор | 🤖 | 2026-10-13 | ✅ | 865e8bf3 | удаляет владелец таблицы (D22), Memory только SELECT и фильтр, M3 через retention/run, границы сроков и FK к run_event учтены |
| `docs/rnd/guardrails-engine.md` | В | — | — | — | ⏳ | 5a6c297f | R&D |
| `docs/rnd/guardrails-engine.md` | А | — | — | — | ⏳ | 5a6c297f | R&D |
| `docs/rnd/harness-framework.md` | В | Claude, роль Владелец продукта | 🤖 | 2026-10-13 | ✅ | 49b20541 | достаточно |
| `docs/rnd/harness-framework.md` | А | Claude, роль Архитектор | 🤖 | 2026-10-13 | ✅ | 49b20541 | достаточно |
| `docs/rnd/ingress-and-balancing.md` | В | — | — | — | ⏳ | e013681f | R&D |
| `docs/rnd/ingress-and-balancing.md` | А | — | — | — | ⏳ | e013681f | R&D |
| `docs/rnd/kubernetes-runtime.md` | В | — | — | — | ⏳ | 8cc2ba19 | R&D |
| `docs/rnd/kubernetes-runtime.md` | А | — | — | — | ⏳ | 8cc2ba19 | R&D |
| `docs/rnd/llm-gateway.md` | В | — | — | — | ⏳ | d0ba8c0b | R&D |
| `docs/rnd/llm-gateway.md` | А | — | — | — | ⏳ | d0ba8c0b | R&D |
| `docs/rnd/load-profile.md` | В | — | — | — | ⏳ | feb406ea | R&D |
| `docs/rnd/load-profile.md` | А | — | — | — | ⏳ | feb406ea | R&D |
| `docs/rnd/mcp-vs-direct.md` | В | Claude, роль Владелец продукта | 🤖 | 2026-10-13 | ✅ | 90bb0541 | достаточно |
| `docs/rnd/mcp-vs-direct.md` | А | Claude, роль Архитектор | 🤖 | 2026-10-13 | ✅ | 90bb0541 | достаточно |
| `docs/rnd/memory-model.md` | В | — | — | — | ⏳ | 3faf1e51 | R&D |
| `docs/rnd/memory-model.md` | А | — | — | — | ⏳ | 3faf1e51 | R&D |
| `docs/rnd/observability.md` | В | — | — | — | ⏳ | 0bafd2b1 | R&D |
| `docs/rnd/observability.md` | А | — | — | — | ⏳ | 0bafd2b1 | R&D |
| `docs/rnd/platform-module-screens.md` | В | Claude, роль Владелец продукта | 🤖 | 2026-10-13 | ✅ | 16d43b38 | 30 ч подзадач 4.4, раскладка по уровням, риск God mode и условия пересмотра названы |
| `docs/rnd/platform-module-screens.md` | А | Claude, роль Архитектор | 🤖 | 2026-10-13 | ✅ | 16d43b38 | таблицы и эндпоинты по уровням, права ai_agents, @/cloud без правок, правки двух файлов форка и PR в upstream; ОВ-agent-registry-2 не блокирует |
| `docs/rnd/rag.md` | В | — | — | — | ⏳ | f226775c | R&D |
| `docs/rnd/rag.md` | А | — | — | — | ⏳ | f226775c | R&D |
| `docs/rnd/rnd-methodology-choice.md` | В | — | — | — | ⏳ | 1ad6d93e | R&D |
| `docs/rnd/rnd-methodology-choice.md` | А | — | — | — | ⏳ | 1ad6d93e | R&D |
| `docs/rnd/run-view.md` | В | — | — | — | ⏳ | b4da9c90 | R&D |
| `docs/rnd/run-view.md` | А | — | — | — | ⏳ | b4da9c90 | R&D |
| `docs/rnd/runaway-protection.md` | В | — | — | — | ⏳ | ef1e1487 | R&D |
| `docs/rnd/runaway-protection.md` | А | — | — | — | ⏳ | ef1e1487 | R&D |
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
| `docs/rules/approval-methodology.md` | В | — | — | — | ⏳ | 49669113 | Методология |
| `docs/rules/approval-methodology.md` | А | — | — | — | ⏳ | 49669113 | Методология |
| `docs/rules/architecture-methodology.md` | В | — | — | — | ⏳ | 03347175 | Методология |
| `docs/rules/architecture-methodology.md` | А | — | — | — | ⏳ | 03347175 | Методология |
| `docs/rules/block-methodology.md` | В | — | — | — | ⏳ | 09b05810 | Методология |
| `docs/rules/block-methodology.md` | А | — | — | — | ⏳ | 09b05810 | Методология |
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
| `docs/stories/guardrails.md` | В | — | — | — | ⏳ | 15468243 | User Stories |
| `docs/stories/guardrails.md` | И | — | — | — | ⏳ | 15468243 | User Stories |
| `docs/stories/guardrails.md` | П | — | — | — | ⏳ | 15468243 | User Stories |
| `docs/stories/harness.md` | В | Claude, роль Владелец продукта | 🤖 | 2026-10-13 | ✅ | d62dc5a0 | достаточно |
| `docs/stories/harness.md` | И | Claude, роль Аналитик историй | 🤖 | 2026-10-13 | ✅ | d62dc5a0 | достаточно |
| `docs/stories/harness.md` | П | Claude, роль Пользователь | 🤖 | 2026-10-13 | ✅ | d62dc5a0 | достаточно |
| `docs/stories/icplan.md` | В | Claude, роль Владелец продукта | 🤖 | 2026-10-13 | ✅ | d854644a | Истории и требования покрывают ценность: создание, видимость, отмена, проверка результата; открытый вопрос Z-ICP-106 не блокирует. |
| `docs/stories/icplan.md` | И | Claude, роль Аналитик историй | 🤖 | 2026-10-13 | ✅ | d854644a | Роли и отказы разобраны: дубли, не участник проекта, пауза hook G2, отмена запуска. |
| `docs/stories/icplan.md` | П | Claude, роль Пользователь | 🤖 | 2026-10-13 | ✅ | d854644a | Пользователь может создать задачу, видеть работу агента, ответить, принять или вернуть результат. |
| `docs/stories/infrastructure.md` | В | — | — | — | ⏳ | 5d4c8aee | User Stories |
| `docs/stories/infrastructure.md` | И | — | — | — | ⏳ | 5d4c8aee | User Stories |
| `docs/stories/infrastructure.md` | П | — | — | — | ⏳ | 5d4c8aee | User Stories |
| `docs/stories/llm-gateway.md` | В | — | — | — | ⏳ | c68ad1fa | User Stories |
| `docs/stories/llm-gateway.md` | И | — | — | — | ⏳ | c68ad1fa | User Stories |
| `docs/stories/llm-gateway.md` | П | — | — | — | ⏳ | c68ad1fa | User Stories |
| `docs/stories/mcp-tools.md` | В | Claude, роль Владелец продукта | 🤖 | 2026-10-13 | ✅ | 5bc875c3 | достаточно |
| `docs/stories/mcp-tools.md` | И | Claude, роль Аналитик историй | 🤖 | 2026-10-13 | ✅ | 5bc875c3 | достаточно |
| `docs/stories/mcp-tools.md` | П | Claude, роль Пользователь | 🤖 | 2026-10-13 | ✅ | 5bc875c3 | достаточно |
| `docs/stories/memory.md` | В | — | — | — | ⏳ | 0f40fd7c | User Stories |
| `docs/stories/memory.md` | И | — | — | — | ⏳ | 0f40fd7c | User Stories |
| `docs/stories/memory.md` | П | — | — | — | ⏳ | 0f40fd7c | User Stories |
| `docs/stories/observability.md` | В | — | — | — | ⏳ | 0f715453 | User Stories |
| `docs/stories/observability.md` | И | — | — | — | ⏳ | 0f715453 | User Stories |
| `docs/stories/observability.md` | П | — | — | — | ⏳ | 0f715453 | User Stories |
| `docs/stories/platform-module.md` | В | — | — | — | ⏳ | cde57b9f | User Stories |
| `docs/stories/platform-module.md` | И | — | — | — | ⏳ | cde57b9f | User Stories |
| `docs/stories/platform-module.md` | П | — | — | — | ⏳ | cde57b9f | User Stories |
| `docs/stories/sandbox.md` | В | Claude, роль Владелец продукта | 🤖 | 2026-10-13 | ✅ | 3ec8d662 | достаточно |
| `docs/stories/sandbox.md` | И | Claude, роль Аналитик историй | 🤖 | 2026-10-13 | ✅ | 3ec8d662 | достаточно |
| `docs/stories/sandbox.md` | П | Claude, роль Пользователь | 🤖 | 2026-10-13 | ✅ | 3ec8d662 | достаточно |
| `docs/tasks/1.1-mock-llm-litellm.md` | В | — | — | — | ⏳ | 024accb2 | Задача |
| `docs/tasks/1.1-mock-llm-litellm.md` | Р | — | — | — | ⏳ | 024accb2 | Задача |
| `docs/tasks/1.1-mock-llm-litellm.md` | Т | — | — | — | ⏳ | 024accb2 | Задача |
| `docs/tasks/1.2-agent-definition-yaml.md` | В | Claude, роль Владелец продукта | 🤖 | 2026-10-13 | ✅ | d6f47d29 | повторная проверка: закрытие прежних замечаний на месте, приёмка/требования/декомпозиция согласованы |
| `docs/tasks/1.2-agent-definition-yaml.md` | Р | Claude, роль Разработчик | 🤖 | 2026-10-13 | ✅ | d6f47d29 | повторная проверка: закрытие прежних замечаний на месте, приёмка/требования/декомпозиция согласованы |
| `docs/tasks/1.2-agent-definition-yaml.md` | Т | Claude, роль Тестировщик | 🤖 | 2026-10-13 | ✅ | d6f47d29 | повторная проверка: закрытие прежних замечаний на месте, приёмка/требования/декомпозиция согласованы |
| `docs/tasks/1.3-harness-core.md` | В | Claude, роль Владелец продукта | 🤖 | 2026-10-13 | ✅ | 5f2db77f | достаточно |
| `docs/tasks/1.3-harness-core.md` | Р | Claude, роль Разработчик | 🤖 | 2026-10-13 | ✅ | 5f2db77f | достаточно |
| `docs/tasks/1.3-harness-core.md` | Т | Claude, роль Тестировщик | 🤖 | 2026-10-13 | ✅ | 5f2db77f | достаточно |
| `docs/tasks/1.4-harness-mcp-tools.md` | В | Claude, роль Владелец продукта | 🤖 | 2026-10-13 | ✅ | 6e759f08 | достаточно |
| `docs/tasks/1.4-harness-mcp-tools.md` | Р | Claude, роль Разработчик | 🤖 | 2026-10-13 | ✅ | 6e759f08 | достаточно |
| `docs/tasks/1.4-harness-mcp-tools.md` | Т | Claude, роль Тестировщик | 🤖 | 2026-10-13 | ✅ | 6e759f08 | достаточно |
| `docs/tasks/1.5-harness-hooks-approve.md` | В | Claude, роль Владелец продукта | 🤖 | 2026-10-13 | ✅ | d2dde3a7 | достаточно |
| `docs/tasks/1.5-harness-hooks-approve.md` | Р | Claude, роль Разработчик | 🤖 | 2026-10-13 | ✅ | d2dde3a7 | достаточно |
| `docs/tasks/1.5-harness-hooks-approve.md` | Т | Claude, роль Тестировщик | 🤖 | 2026-10-13 | ✅ | d2dde3a7 | достаточно |
| `docs/tasks/1.6-harness-limits-context.md` | В | Claude, роль Владелец продукта | 🤖 | 2026-10-13 | ✅ | 89c954d9 | достаточно |
| `docs/tasks/1.6-harness-limits-context.md` | Р | Claude, роль Разработчик | 🤖 | 2026-10-13 | ✅ | 89c954d9 | достаточно |
| `docs/tasks/1.6-harness-limits-context.md` | Т | Claude, роль Тестировщик | 🤖 | 2026-10-13 | ✅ | 89c954d9 | достаточно |
| `docs/tasks/1.7-dev-ui.md` | В | Claude, роль Владелец продукта | 🤖 | 2026-10-13 | ✅ | 2d8becba | достаточно |
| `docs/tasks/1.7-dev-ui.md` | Р | Claude, роль Разработчик | 🤖 | 2026-10-13 | ✅ | 2d8becba | достаточно |
| `docs/tasks/1.7-dev-ui.md` | Т | Claude, роль Тестировщик | 🤖 | 2026-10-13 | ✅ | 2d8becba | достаточно |
| `docs/tasks/2.1-runner-external.md` | В | Claude, роль Владелец продукта | 🤖 | 2026-10-13 | ✅ | 39ea0dca | Оценка и приёмка есть |
| `docs/tasks/2.1-runner-external.md` | Р | Claude, роль Разработчик | 🤖 | 2026-10-13 | ✅ | 39ea0dca | Подзадачи и зависимости есть |
| `docs/tasks/2.1-runner-external.md` | Т | Claude, роль Тестировщик | 🤖 | 2026-10-13 | ✅ | 39ea0dca | Приёмка проверяема |
| `docs/tasks/2.2-sandbox-docker-oneshot.md` | В | Claude, роль Владелец продукта | 🤖 | 2026-10-13 | ✅ | 3d18761c | достаточно |
| `docs/tasks/2.2-sandbox-docker-oneshot.md` | Р | Claude, роль Разработчик | 🤖 | 2026-10-13 | ✅ | 3d18761c | достаточно |
| `docs/tasks/2.2-sandbox-docker-oneshot.md` | Т | Claude, роль Тестировщик | 🤖 | 2026-10-13 | ✅ | 3d18761c | достаточно |
| `docs/tasks/2.3-config-from-icplan.md` | В | Claude, роль Владелец продукта | 🤖 | 2026-10-13 | ✅ | 9a602cc4 | повторная проверка: закрытие прежних замечаний на месте, приёмка/требования/декомпозиция согласованы |
| `docs/tasks/2.3-config-from-icplan.md` | Р | Claude, роль Разработчик | 🤖 | 2026-10-13 | ✅ | 9a602cc4 | повторная проверка: закрытие прежних замечаний на месте, приёмка/требования/декомпозиция согласованы |
| `docs/tasks/2.3-config-from-icplan.md` | Т | Claude, роль Тестировщик | 🤖 | 2026-10-13 | ✅ | 9a602cc4 | повторная проверка: закрытие прежних замечаний на месте, приёмка/требования/декомпозиция согласованы |
| `docs/tasks/2.4-mcp-itsaplan-core.md` | В | Claude, роль Владелец продукта | 🤖 | 2026-10-13 | ✅ | ef77b663 | достаточно |
| `docs/tasks/2.4-mcp-itsaplan-core.md` | Р | Claude, роль Разработчик | 🤖 | 2026-10-13 | ✅ | ef77b663 | достаточно |
| `docs/tasks/2.4-mcp-itsaplan-core.md` | Т | Claude, роль Тестировщик | 🤖 | 2026-10-13 | ✅ | ef77b663 | достаточно |
| `docs/tasks/2.5-memory-m2-m3.md` | В | — | — | — | ⏳ | 2d41cd01 | Задача |
| `docs/tasks/2.5-memory-m2-m3.md` | Р | — | — | — | ⏳ | 2d41cd01 | Задача |
| `docs/tasks/2.5-memory-m2-m3.md` | Т | — | — | — | ⏳ | 2d41cd01 | Задача |
| `docs/tasks/2.6-e2e-icplan.md` | В | Claude, роль Владелец продукта | 🤖 | 2026-10-13 | ✅ | d3f3b496 | Z-ICP-122 закрыто: приёмка по сценариям, 2.6.6-2.6.7, оценка 28 ч в 3-4 дн |
| `docs/tasks/2.6-e2e-icplan.md` | Р | Claude, роль Разработчик | 🤖 | 2026-10-13 | ✅ | d3f3b496 | сценарии отказов разложены по подзадачам 2.6.6-2.6.7 с готовностью |
| `docs/tasks/2.6-e2e-icplan.md` | Т | Claude, роль Тестировщик | 🤖 | 2026-10-13 | ✅ | d3f3b496 | приёмка: сценарий -> результат по R-ICP-13, R-RUN-08, R-RUN-14 |
| `docs/tasks/2.7-runner-scheduler.md` | В | Claude, роль Владелец продукта | 🤖 | 2026-10-13 | ✅ | 23b9b06e | Оценка и приёмка есть |
| `docs/tasks/2.7-runner-scheduler.md` | Р | Claude, роль Разработчик | 🤖 | 2026-10-13 | ✅ | 23b9b06e | Подзадачи есть |
| `docs/tasks/2.7-runner-scheduler.md` | Т | Claude, роль Тестировщик | 🤖 | 2026-10-13 | ✅ | 23b9b06e | Конкурентный тест задан |
| `docs/tasks/2.8-config-storage-interfaces-fmea.md` | В | — | — | — | ⏳ | 5a41f0e0 | Задача |
| `docs/tasks/2.8-config-storage-interfaces-fmea.md` | Р | — | — | — | ⏳ | 5a41f0e0 | Задача |
| `docs/tasks/2.8-config-storage-interfaces-fmea.md` | Т | — | — | — | ⏳ | 5a41f0e0 | Задача |
| `docs/tasks/3.1-icplan-process-step-agent.md` | В | Claude, роль Владелец продукта | 🤖 | 2026-10-13 | ✅ | 396f3149 | повторная проверка: закрытие прежних замечаний на месте, приёмка/требования/декомпозиция согласованы |
| `docs/tasks/3.1-icplan-process-step-agent.md` | Р | Claude, роль Разработчик | 🤖 | 2026-10-13 | ✅ | 396f3149 | повторная проверка: закрытие прежних замечаний на месте, приёмка/требования/декомпозиция согласованы |
| `docs/tasks/3.1-icplan-process-step-agent.md` | Т | Claude, роль Тестировщик | 🤖 | 2026-10-13 | ✅ | 396f3149 | повторная проверка: закрытие прежних замечаний на месте, приёмка/требования/декомпозиция согласованы |
| `docs/tasks/3.2-icplan-handoff.md` | В | Claude, роль Владелец продукта | 🤖 | 2026-10-13 | ✅ | 353ac49e | повторная проверка: закрытие прежних замечаний на месте, приёмка/требования/декомпозиция согласованы |
| `docs/tasks/3.2-icplan-handoff.md` | Р | Claude, роль Разработчик | 🤖 | 2026-10-13 | ✅ | 353ac49e | повторная проверка: закрытие прежних замечаний на месте, приёмка/требования/декомпозиция согласованы |
| `docs/tasks/3.2-icplan-handoff.md` | Т | Claude, роль Тестировщик | 🤖 | 2026-10-13 | ✅ | 353ac49e | повторная проверка: закрытие прежних замечаний на месте, приёмка/требования/декомпозиция согласованы |
| `docs/tasks/3.3-run-events-timeline.md` | В | — | — | — | ⏳ | b3748f47 | Задача |
| `docs/tasks/3.3-run-events-timeline.md` | Р | — | — | — | ⏳ | b3748f47 | Задача |
| `docs/tasks/3.3-run-events-timeline.md` | Т | — | — | — | ⏳ | b3748f47 | Задача |
| `docs/tasks/3.4-icplan-approve-ui.md` | В | Claude, роль Владелец продукта | 🤖 | 2026-10-13 | ✅ | 7e4acf6b | повторная проверка: закрытие прежних замечаний на месте, приёмка/требования/декомпозиция согласованы |
| `docs/tasks/3.4-icplan-approve-ui.md` | Р | Claude, роль Разработчик | 🤖 | 2026-10-13 | ✅ | 7e4acf6b | повторная проверка: закрытие прежних замечаний на месте, приёмка/требования/декомпозиция согласованы |
| `docs/tasks/3.4-icplan-approve-ui.md` | Т | Claude, роль Тестировщик | 🤖 | 2026-10-13 | ✅ | 7e4acf6b | повторная проверка: закрытие прежних замечаний на месте, приёмка/требования/декомпозиция согласованы |
| `docs/tasks/3.5-icplan-type-actions-cost.md` | В | Claude, роль Владелец продукта | 🤖 | 2026-10-13 | ✅ | e47aae72 | повторно: замечания Z-ICP-5/60/83/96 закрыты в тексте (3.5.1–3.5.5, приёмка по сценариям R-AP-03/R-LLM-02/R-OBS-05) |
| `docs/tasks/3.5-icplan-type-actions-cost.md` | Р | Claude, роль Разработчик | 🤖 | 2026-10-13 | ✅ | e47aae72 | повторно: замечания Z-ICP-5/60/83/96 закрыты в тексте (3.5.1–3.5.5, приёмка по сценариям R-AP-03/R-LLM-02/R-OBS-05) |
| `docs/tasks/3.5-icplan-type-actions-cost.md` | Т | Claude, роль Тестировщик | 🤖 | 2026-10-13 | ✅ | e47aae72 | повторно: замечания Z-ICP-5/60/83/96 закрыты в тексте (3.5.1–3.5.5, приёмка по сценариям R-AP-03/R-LLM-02/R-OBS-05) |
| `docs/tasks/3.6-icplan-process-engine.md` | В | Claude, роль Владелец продукта | 🤖 | 2026-10-13 | ✅ | 8a659c27 | Z-ICP-123 закрыто; оценка 31 ч сходится |
| `docs/tasks/3.6-icplan-process-engine.md` | Р | Claude, роль Разработчик | 🤖 | 2026-10-13 | ✅ | 8a659c27 | 3.6.5 покрывает порядок, второй запуск, истечение аренды |
| `docs/tasks/3.6-icplan-process-engine.md` | Т | Claude, роль Тестировщик | 🤖 | 2026-10-13 | ✅ | 8a659c27 | приёмка: активный запуск и истёкшая аренда проверяемы, R-AP-17 |
| `docs/tasks/3.7-icplan-task-control.md` | В | Claude, роль Владелец продукта | 🤖 | 2026-10-13 | ✅ | 9e659fe2 | требования R-AP-18..22 покрыты подзадачами 3.7.1–3.7.8 и приёмкой |
| `docs/tasks/3.7-icplan-task-control.md` | Р | Claude, роль Разработчик | 🤖 | 2026-10-13 | ✅ | 9e659fe2 | требования R-AP-18..22 покрыты подзадачами 3.7.1–3.7.8 и приёмкой |
| `docs/tasks/3.7-icplan-task-control.md` | Т | Claude, роль Тестировщик | 🤖 | 2026-10-13 | ✅ | 9e659fe2 | требования R-AP-18..22 покрыты подзадачами 3.7.1–3.7.8 и приёмкой |
| `docs/tasks/3.8-agent-chat-control.md` | В | Claude, роль Владелец продукта | 🤖 | 2026-10-13 | ✅ | 2af148f7 | повторная проверка: приёмка по сценариям, D25 и enabled — один источник (восстановлено после гонки записи реестра) |
| `docs/tasks/3.8-agent-chat-control.md` | Р | Claude, роль Разработчик | 🤖 | 2026-10-13 | ✅ | 2af148f7 | R-ICP-16..18, R-HRN-16 покрыты подзадачами 3.8.1–3.8.5 и приёмкой |
| `docs/tasks/3.8-agent-chat-control.md` | Т | Claude, роль Тестировщик | 🤖 | 2026-10-13 | ✅ | 2af148f7 | R-ICP-16..18, R-HRN-16 покрыты подзадачами 3.8.1–3.8.5 и приёмкой |
| `docs/tasks/3.9-agent-summary-stats.md` | В | Claude, роль Владелец продукта | 🤖 | 2026-10-13 | ✅ | a39f3839 | R-OBS-13: подзадачи 3.9.1–3.9.5, приёмка с отказом LiteLLM |
| `docs/tasks/3.9-agent-summary-stats.md` | Р | Claude, роль Разработчик | 🤖 | 2026-10-13 | ✅ | a39f3839 | R-OBS-13: подзадачи 3.9.1–3.9.5, приёмка с отказом LiteLLM |
| `docs/tasks/3.9-agent-summary-stats.md` | Т | Claude, роль Тестировщик | 🤖 | 2026-10-13 | ✅ | a39f3839 | повторная проверка: приёмка по сценариям (восстановлено после гонки записи реестра) |
| `docs/tasks/4.1-sandbox-warm-pool.md` | В | Claude, роль Владелец продукта | 🤖 | 2026-10-13 | ✅ | 661b9211 | достаточно |
| `docs/tasks/4.1-sandbox-warm-pool.md` | Р | Claude, роль Разработчик | 🤖 | 2026-10-13 | ✅ | 661b9211 | достаточно |
| `docs/tasks/4.1-sandbox-warm-pool.md` | Т | Claude, роль Тестировщик | 🤖 | 2026-10-13 | ✅ | 661b9211 | достаточно |
| `docs/tasks/4.2-egress-repo-access.md` | В | — | — | — | ⏳ | a7b56f71 | Задача |
| `docs/tasks/4.2-egress-repo-access.md` | Р | — | — | — | ⏳ | a7b56f71 | Задача |
| `docs/tasks/4.2-egress-repo-access.md` | Т | — | — | — | ⏳ | a7b56f71 | Задача |
| `docs/tasks/4.3-guardrails-opa.md` | В | — | — | — | ⏳ | 01ed4d7b | Задача |
| `docs/tasks/4.3-guardrails-opa.md` | Р | — | — | — | ⏳ | 01ed4d7b | Задача |
| `docs/tasks/4.3-guardrails-opa.md` | Т | — | — | — | ⏳ | 01ed4d7b | Задача |
| `docs/tasks/4.4-platform-module.md` | В | — | — | — | ⏳ | 386437b6 | Задача |
| `docs/tasks/4.4-platform-module.md` | Р | — | — | — | ⏳ | 386437b6 | Задача |
| `docs/tasks/4.4-platform-module.md` | Т | — | — | — | ⏳ | 386437b6 | Задача |
| `docs/tasks/4.5-litellm-budgets-fallback-g4.md` | В | — | — | — | ⏳ | c642d3e7 | Задача |
| `docs/tasks/4.5-litellm-budgets-fallback-g4.md` | Р | — | — | — | ⏳ | c642d3e7 | Задача |
| `docs/tasks/4.5-litellm-budgets-fallback-g4.md` | Т | — | — | — | ⏳ | c642d3e7 | Задача |
| `docs/tasks/4.6-k8s-helm-ingress.md` | В | — | — | — | ⏳ | 8f93d147 | Задача |
| `docs/tasks/4.6-k8s-helm-ingress.md` | Р | — | — | — | ⏳ | 8f93d147 | Задача |
| `docs/tasks/4.6-k8s-helm-ingress.md` | Т | — | — | — | ⏳ | 8f93d147 | Задача |
| `docs/tasks/4.7-postgres-storage-backup.md` | В | — | — | — | ⏳ | aad37be0 | Задача |
| `docs/tasks/4.7-postgres-storage-backup.md` | Р | — | — | — | ⏳ | aad37be0 | Задача |
| `docs/tasks/4.7-postgres-storage-backup.md` | Т | — | — | — | ⏳ | aad37be0 | Задача |
| `docs/tasks/4.8-load-test.md` | В | — | — | — | ⏳ | 15f1b712 | Задача |
| `docs/tasks/4.8-load-test.md` | Р | — | — | — | ⏳ | 15f1b712 | Задача |
| `docs/tasks/4.8-load-test.md` | Т | — | — | — | ⏳ | 15f1b712 | Задача |
| `docs/techspec/agent-runner.md` | Д | Claude, роль DevOps-инженер | 🤖 | 2026-10-13 | ✅ | f97844be | Развёртывание, обновление и откат описаны |
| `docs/techspec/agent-runner.md` | Б | Claude, роль Безопасность | 🤖 | 2026-10-13 | ✅ | f97844be | Nonroot, секреты в Secret, digest-пины |
| `docs/techspec/agent-runner.md` | С | Claude, роль Инженер сборки и поставки | 🤖 | 2026-10-13 | ✅ | f97844be | Сборка и источник образа указаны |
| `docs/techspec/guardrails.md` | Д | — | — | — | ⏳ | fed08892 | Deploy |
| `docs/techspec/guardrails.md` | Б | — | — | — | ⏳ | fed08892 | Deploy |
| `docs/techspec/guardrails.md` | С | — | — | — | ⏳ | fed08892 | Deploy |
| `docs/techspec/harness.md` | Д | — | — | — | ⏳ | cbb45e75 | Deploy |
| `docs/techspec/harness.md` | Б | — | — | — | ⏳ | cbb45e75 | Deploy |
| `docs/techspec/harness.md` | С | — | — | — | ⏳ | cbb45e75 | Deploy |
| `docs/techspec/icplan.md` | Д | Claude, роль DevOps-инженер | 🤖 | 2026-10-13 | ✅ | c8b90db6 | повторно: emptyDir /tmp, MIGRATION_DATABASE_URL, переменные AGENT_RUN_*/RUNNER_OFFLINE_AFTER_S/REVIEW_REMINDER_HOURS/retention, откат через PITR в отдельный кластер; Z-ICP-98..100 закрыты |
| `docs/techspec/icplan.md` | Б | Claude, роль Безопасность | 🤖 | 2026-10-13 | ✅ | c8b90db6 | повторно: secrets.existingSecret, шифротекст с APP_ENCRYPTION_KEY вне БД, non-root, readOnlyRootFilesystem; Z-ICP-102/103 закрыты |
| `docs/techspec/icplan.md` | С | Claude, роль Инженер сборки и поставки | 🤖 | 2026-10-13 | ✅ | c8b90db6 | повторно: сборка web с CLOUD_UI_ENTRY (4.6.10), теги X.Y.Z-sha, SBOM/trivy, проверка после развёртывания; Z-ICP-101 закрыт |
| `docs/techspec/infrastructure.md` | Д | — | — | — | ⏳ | 0b43fe33 | Deploy |
| `docs/techspec/infrastructure.md` | Б | — | — | — | ⏳ | 0b43fe33 | Deploy |
| `docs/techspec/infrastructure.md` | С | — | — | — | ⏳ | 0b43fe33 | Deploy |
| `docs/techspec/llm-gateway.md` | Д | — | — | — | ⏳ | 5b9ab6b5 | Deploy |
| `docs/techspec/llm-gateway.md` | Б | — | — | — | ⏳ | 5b9ab6b5 | Deploy |
| `docs/techspec/llm-gateway.md` | С | — | — | — | ⏳ | 5b9ab6b5 | Deploy |
| `docs/techspec/mcp-tools.md` | Д | — | — | — | ⏳ | 66b1940c | Deploy |
| `docs/techspec/mcp-tools.md` | Б | — | — | — | ⏳ | 66b1940c | Deploy |
| `docs/techspec/mcp-tools.md` | С | — | — | — | ⏳ | 66b1940c | Deploy |
| `docs/techspec/memory.md` | Д | — | — | — | ⏳ | 90f60c8c | Deploy |
| `docs/techspec/memory.md` | Б | — | — | — | ⏳ | 90f60c8c | Deploy |
| `docs/techspec/memory.md` | С | — | — | — | ⏳ | 90f60c8c | Deploy |
| `docs/techspec/observability.md` | Д | — | — | — | ⏳ | dd4f744b | Deploy |
| `docs/techspec/observability.md` | Б | — | — | — | ⏳ | dd4f744b | Deploy |
| `docs/techspec/observability.md` | С | — | — | — | ⏳ | dd4f744b | Deploy |
| `docs/techspec/platform-module.md` | Д | — | — | — | ⏳ | bb1b3417 | Deploy |
| `docs/techspec/platform-module.md` | Б | — | — | — | ⏳ | bb1b3417 | Deploy |
| `docs/techspec/platform-module.md` | С | — | — | — | ⏳ | bb1b3417 | Deploy |
| `docs/techspec/sandbox.md` | Д | — | — | — | ⏳ | 4e939442 | Deploy |
| `docs/techspec/sandbox.md` | Б | — | — | — | ⏳ | 4e939442 | Deploy |
| `docs/techspec/sandbox.md` | С | — | — | — | ⏳ | 4e939442 | Deploy |
| `index.md` | В | — | — | — | ⏳ | 42b2b191 | Главная |
| `index.md` | А | — | — | — | ⏳ | 42b2b191 | Главная |
| `openspec/changes/define-agent-platform/design.md` | В | — | — | — | ⏳ | f1c09b02 | Решения (design) |
| `openspec/changes/define-agent-platform/design.md` | А | — | — | — | ⏳ | f1c09b02 | Решения (design) |
