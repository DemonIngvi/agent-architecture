# Интеграции: Platform module

← [компонент](../../components/platform-module/index.md) · [Deploy](../techspec/platform-module.md) · [методология](../rules/api-methodology.md)

<div class="api-head">
<div><span class="about-label">Базовый адрес</span> `/api/platform` (в api форка ICPlan)</div>
<div><span class="about-label">Аутентификация</span> UI — сессия администратора; Runner — сервисный токен</div>
</div>

## Настройки агента

| Метод | Путь | Статус | Что делает | Кто вызывает | Истории | Требования | I |
|---|---|---|---|---|---|---|---|
| <span class="m m-get">GET</span> | `/platform/agents/:agentId/settings` | <span class="st st-new">🆕 новое</span> | бюджеты, профили, автономия, данные guardrails | Администратор, Runner (I4) · сессия / сервисный токен | [US-PM-01](../stories/platform-module.md#us-pm-01) | [R-CP-01](../../openspec/changes/define-agent-platform/specs/control-plane/spec.md#r-cp-01), [R-CP-06](../../openspec/changes/define-agent-platform/specs/control-plane/spec.md#r-cp-06) | I4 |
| <span class="m m-patch">PATCH</span> | `/platform/agents/:agentId/settings` | <span class="st st-new">🆕 новое</span> | изменить настройки (со следующего запуска) | Администратор · сессия | [US-PM-01](../stories/platform-module.md#us-pm-01), [US-PM-02](../stories/platform-module.md#us-pm-02), [US-PM-05](../stories/platform-module.md#us-pm-05) | [R-CP-01](../../openspec/changes/define-agent-platform/specs/control-plane/spec.md#r-cp-01), [R-CP-03](../../openspec/changes/define-agent-platform/specs/control-plane/spec.md#r-cp-03), [R-GRD-08](../../openspec/changes/define-agent-platform/specs/guardrails/spec.md#r-grd-08) | I20 |
| <span class="m m-get">GET</span> | `/platform/agents/:agentId/export` | <span class="st st-new">🆕 новое</span> | экспорт определения в YAML | Администратор · сессия | [US-PM-03](../stories/platform-module.md#us-pm-03) | [R-CP-05](../../openspec/changes/define-agent-platform/specs/control-plane/spec.md#r-cp-05) | I20 |
| <span class="m m-post">POST</span> | `/platform/agents/import` | <span class="st st-new">🆕 новое</span> | импорт YAML (новая версия) | Администратор · сессия | [US-PM-03](../stories/platform-module.md#us-pm-03) | [R-CP-05](../../openspec/changes/define-agent-platform/specs/control-plane/spec.md#r-cp-05) | I20 |
| <span class="m m-get">GET</span> | `/platform/agents/:agentId/settings/versions` | <span class="st st-new">🆕 новое</span> | история настроек: версия, кто, когда | Администратор · сессия (карточка агента → «Платформа», D24) | [US-PM-02](../stories/platform-module.md#us-pm-02) | [R-CP-04](../../openspec/changes/define-agent-platform/specs/control-plane/spec.md#r-cp-04) | I20 |
| <span class="m m-post">POST</span> | `/platform/agents/:agentId/settings/rollback` | <span class="st st-new">🆕 новое</span> | откат к версии: новая версия с её содержимым, со следующего запуска | Администратор · сессия, право `ai_agents` | [US-PM-02](../stories/platform-module.md#us-pm-02) | [R-CP-04](../../openspec/changes/define-agent-platform/specs/control-plane/spec.md#r-cp-04), [R-CP-07](../../openspec/changes/define-agent-platform/specs/control-plane/spec.md#r-cp-07) | I20 |

## Экземпляр: профили и kill switch

| Метод | Путь | Статус | Что делает | Кто вызывает | Истории | Требования | I |
|---|---|---|---|---|---|---|---|
| <span class="m m-get">GET</span> | `/platform/sandbox-profiles` | <span class="st st-new">🆕 новое</span> | профили среды (`sandbox_profile`) | Администратор · сессия | [US-PM-01](../stories/platform-module.md#us-pm-01) | [R-SBX-05](../../openspec/changes/define-agent-platform/specs/agent-sandbox/spec.md#r-sbx-05) | I20 |
| <span class="m m-put">PUT</span> | `/platform/sandbox-profiles/:name` | <span class="st st-new">🆕 новое</span> | создать или изменить профиль среды | Владелец экземпляра · сессия (God mode → «Платформа», D24) | [US-PM-01](../stories/platform-module.md#us-pm-01) | [R-SBX-05](../../openspec/changes/define-agent-platform/specs/agent-sandbox/spec.md#r-sbx-05) | I20 |
| <span class="m m-get">GET</span> | `/platform/memory-profiles` | <span class="st st-new">🆕 новое</span> | профили памяти (`memory_profile`) | Администратор · сессия | [US-MEM-04](../stories/memory.md#us-mem-04) | [R-MEM-09](../../openspec/changes/define-agent-platform/specs/agent-memory/spec.md#r-mem-09) | I20 |
| <span class="m m-put">PUT</span> | `/platform/memory-profiles/:name` | <span class="st st-new">🆕 новое</span> | создать или изменить профиль памяти | Владелец экземпляра · сессия (God mode → «Платформа», D24) | [US-MEM-04](../stories/memory.md#us-mem-04) | [R-MEM-09](../../openspec/changes/define-agent-platform/specs/agent-memory/spec.md#r-mem-09) | I20 |
| <span class="m m-get">GET</span> | `/platform/kill-switch` | <span class="st st-new">🆕 новое</span> | состояние аварийной остановки: `platform`, `agent:<id>` | Администратор, эксплуатация · сессия / сервисный токен | [US-GRD-04](../stories/guardrails.md#us-grd-04) | [R-GRD-15](../../openspec/changes/define-agent-platform/specs/guardrails/spec.md#r-grd-15) | I20 |
| <span class="m m-put">PUT</span> | `/platform/kill-switch/:scope` | <span class="st st-new">🆕 новое</span> | включить или выключить kill switch агента или платформы, сразу | `agent:<id>` — администратор (право `ai_agents`), `platform` — владелец экземпляра; эксплуатация · сервисный токен (D24) | [US-GRD-04](../stories/guardrails.md#us-grd-04) | [R-GRD-15](../../openspec/changes/define-agent-platform/specs/guardrails/spec.md#r-grd-15), [R-CP-03](../../openspec/changes/define-agent-platform/specs/control-plane/spec.md#r-cp-03) | I20 |

## Проект

| Метод | Путь | Статус | Что делает | Кто вызывает | Истории | Требования | I |
|---|---|---|---|---|---|---|---|
| <span class="m m-put">PUT</span> | `/platform/projects/:projectKey/guidance` | <span class="st st-new">🆕 новое</span> | руководство проекта для агентов | Администратор · сессия | [US-PM-08](../stories/platform-module.md#us-pm-08) | [R-CP-14](../../openspec/changes/define-agent-platform/specs/control-plane/spec.md#r-cp-14) | I20 |
| <span class="m m-put">PUT</span> | `/platform/projects/:projectKey/budget` | <span class="st st-new">🆕 новое</span> | бюджет проекта | Администратор · сессия | [US-PM-06](../stories/platform-module.md#us-pm-06) | [R-GRD-11](../../openspec/changes/define-agent-platform/specs/guardrails/spec.md#r-grd-11) | I20 |
| <span class="m m-get">GET</span> | `/platform/projects/:projectKey/access` | <span class="st st-new">🆕 новое</span> | политика доступа агент × ресурс × право | Администратор, безопасность · сессия | [US-SBX-06](../stories/sandbox.md#us-sbx-06) | [R-RUN-17](../../openspec/changes/define-agent-platform/specs/agent-runner/spec.md#r-run-17) | I20 |
| <span class="m m-put">PUT</span> | `/platform/projects/:projectKey/access` | <span class="st st-new">🆕 новое</span> | изменить политику доступа | Администратор · сессия | [US-SBX-06](../stories/sandbox.md#us-sbx-06) | [R-RUN-17](../../openspec/changes/define-agent-platform/specs/agent-runner/spec.md#r-run-17) | I20 |
| <span class="m m-get">GET</span> | `/platform/projects/:projectKey/resources` | <span class="st st-new">🆕 новое</span> | ресурсы проекта: git, папки, документы, MCP (`project_resource`) | Администратор · сессия | [US-SBX-06](../stories/sandbox.md#us-sbx-06) | [R-RUN-17](../../openspec/changes/define-agent-platform/specs/agent-runner/spec.md#r-run-17) | I20 |
| <span class="m m-put">PUT</span> | `/platform/projects/:projectKey/resources` | <span class="st st-new">🆕 новое</span> | изменить ресурсы проекта | Администратор · сессия, право `ai_agents` (Проект → ИИ-команда → «Платформа», D24) | [US-SBX-06](../stories/sandbox.md#us-sbx-06) | [R-RUN-17](../../openspec/changes/define-agent-platform/specs/agent-runner/spec.md#r-run-17) | I20 |
| <span class="m m-put">PUT</span> | `/platform/projects/:projectKey/setup` | <span class="st st-new">🆕 новое</span> | шаг подготовки проекта: скрипт и lock-файлы (D19) | Администратор · сессия, право `ai_agents` | [US-SBX-06](../stories/sandbox.md#us-sbx-06) | [R-SBX-14](../../openspec/changes/define-agent-platform/specs/agent-sandbox/spec.md#r-sbx-14) | I20 |

## Для Runner и журнал

| Метод | Путь | Статус | Что делает | Кто вызывает | Истории | Требования | I |
|---|---|---|---|---|---|---|---|
| <span class="m m-get">GET</span> | `/platform/runs/:runId/manifest` | <span class="st st-new">🆕 новое</span> | манифест рабочего пространства запуска | Agent Runner · сервисный токен | [US-SBX-05](../stories/sandbox.md#us-sbx-05) | [R-RUN-17](../../openspec/changes/define-agent-platform/specs/agent-runner/spec.md#r-run-17) | I4 |
| <span class="m m-get">GET</span> | `/platform/runs/:runId/agent` | <span class="st st-new">🆕 новое</span> | определение и настройки версии запуска одним ответом: `{version, definition, settings}`; версия закрепляется в `agent_run.agent_version` при первом вызове; 404 — запуск не `pending` или агент не `external`, 409 — версии нет (D23) | Agent Runner · сервисный токен | [US-MEM-07](../stories/memory.md#us-mem-07) | [R-REG-02](../../openspec/changes/define-agent-platform/specs/agent-registry/spec.md#r-reg-02), [R-REG-03](../../openspec/changes/define-agent-platform/specs/agent-registry/spec.md#r-reg-03), [R-CP-03](../../openspec/changes/define-agent-platform/specs/control-plane/spec.md#r-cp-03) | I4 |
| <span class="m m-get">GET</span> | `/platform/audit` | <span class="st st-new">🆕 новое</span> | журнал изменений настроек и политик | Безопасность (право чтения), владелец экземпляра (God mode → «Платформа», D24) · сессия | [US-PM-07](../stories/platform-module.md#us-pm-07) | [R-CP-07](../../openspec/changes/define-agent-platform/specs/control-plane/spec.md#r-cp-07) | I20 |
