# Proposal

## Why

ICPlan назначает агентов на задачи и должен работать с платформой через стабильный контракт уровня C1, не завися от её внутренней структуры (C2).

## What Changes

- Вводится Integration API — единый вход ICPlan в платформу (REST + MCP-сервер).
- Модули API: Агенты (каталог), Runs (запуски), Approvals (подтверждения и ответы), Events (push-события).
- Сквозные свойства: аутентификация, квоты, идемпотентность, версионирование API.

## Capabilities

### New Capabilities
- `icplan-integration`: контракт взаимодействия ICPlan с Agent Platform (C1)

### Modified Capabilities
<!-- нет -->

## Impact

- Новый внешний API платформы; внутри опирается на Registry, Agent Runner, Harness (G2), Observability из change `define-agent-platform`.
