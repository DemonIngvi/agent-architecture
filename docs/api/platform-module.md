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

## Проект

| Метод | Путь | Статус | Что делает | Кто вызывает | Истории | Требования | I |
|---|---|---|---|---|---|---|---|
| <span class="m m-put">PUT</span> | `/platform/projects/:projectKey/guidance` | <span class="st st-new">🆕 новое</span> | руководство проекта для агентов | Администратор · сессия | [US-PM-08](../stories/platform-module.md#us-pm-08) | [R-CP-14](../../openspec/changes/define-agent-platform/specs/control-plane/spec.md#r-cp-14) | I20 |
| <span class="m m-put">PUT</span> | `/platform/projects/:projectKey/budget` | <span class="st st-new">🆕 новое</span> | бюджет проекта | Администратор · сессия | [US-PM-06](../stories/platform-module.md#us-pm-06) | [R-GRD-11](../../openspec/changes/define-agent-platform/specs/guardrails/spec.md#r-grd-11) | I20 |
| <span class="m m-get">GET</span> | `/platform/projects/:projectKey/access` | <span class="st st-new">🆕 новое</span> | политика доступа агент × ресурс × право | Администратор, безопасность · сессия | [US-SBX-06](../stories/sandbox.md#us-sbx-06) | [R-RUN-17](../../openspec/changes/define-agent-platform/specs/agent-runner/spec.md#r-run-17) | I20 |
| <span class="m m-put">PUT</span> | `/platform/projects/:projectKey/access` | <span class="st st-new">🆕 новое</span> | изменить политику доступа | Администратор · сессия | [US-SBX-06](../stories/sandbox.md#us-sbx-06) | [R-RUN-17](../../openspec/changes/define-agent-platform/specs/agent-runner/spec.md#r-run-17) | I20 |

## Для Runner и журнал

| Метод | Путь | Статус | Что делает | Кто вызывает | Истории | Требования | I |
|---|---|---|---|---|---|---|---|
| <span class="m m-get">GET</span> | `/platform/runs/:runId/manifest` | <span class="st st-new">🆕 новое</span> | манифест рабочего пространства запуска | Agent Runner · сервисный токен | [US-SBX-05](../stories/sandbox.md#us-sbx-05) | [R-RUN-17](../../openspec/changes/define-agent-platform/specs/agent-runner/spec.md#r-run-17) | I4 |
| <span class="m m-get">GET</span> | `/platform/audit` | <span class="st st-new">🆕 новое</span> | журнал изменений настроек и политик | Безопасность · сессия | [US-PM-07](../stories/platform-module.md#us-pm-07) | [R-CP-07](../../openspec/changes/define-agent-platform/specs/control-plane/spec.md#r-cp-07) | I20 |
