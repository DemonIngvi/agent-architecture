# Proposal

## Why

ICPlan назначает агентов на задачи и должен работать с платформой через стабильный контракт уровня C1, не завися от её внутренней структуры (C2).

## What Changes

- Agent Runner работает как внешний раннер ICPlan (pull, D8): забирает запуски из очереди агента (`claim`), продлевает аренду (`heartbeat`), передаёт события (AG-UI, D21) и итог (`result`).
- Обратный канал без входящих соединений: отмена, решения пользователя и указания — в ответе heartbeat (доработка форка, D17).
- В задаче — чат запуска: ход работы агента, вопросы и подтверждения, карточка итога (D21); переходы по шагам процесса делает ICPlan (D17).
- Агент действует в ICPlan через MCP-сервер `itsaplan-core` (через MCP-прокси Runner, D19).

## Capabilities

### New Capabilities
- `icplan-integration`: контракт взаимодействия ICPlan с Agent Platform (C1)

### Modified Capabilities
<!-- нет -->

## Impact

- Доработки форка ICPlan: протокол раннера (тело heartbeat, события), чат запуска, процесс задачи, вердикт; опирается на Agent Runner, Harness, Observability из change `define-agent-platform`.
