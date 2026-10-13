# Интеграции: Observability

← [компонент](../../components/observability/index.md) · [Deploy](../techspec/observability.md) · [методология](../rules/api-methodology.md)

<div class="api-head">
<div><span class="about-label">Базовый адрес</span> в api ICPlan</div>
<div><span class="about-label">Аутентификация</span> сессия</div>
</div>

## Где описано

Своего API у Observability нет: затраты задачи (`GET /issues/:issueId/costs`, `CostAggregate`), сводку (`GET /me/agent-summary`) и статистику запусков (`GET /projects/:projectKey/analytics/agent-run-stats`) отдаёт API ICPlan (I20), считая их из журнала LiteLLM, `agent_run` и `run_event`; события запуска Agent Runner передаёт в API ICPlan (I2), собственного приёма у Observability нет. Операции, входы и ошибки — на странице ICPlan.

| Метод | Путь | Статус | Что делает | Кто вызывает | Истории | Требования | I |
|---|---|---|---|---|---|---|---|
| <span class="m m-get">GET</span> | [ICPlan → Сводка и статистика](icplan.md) | <span class="st st-ok">✅ есть</span> | аналитика агентов, сводка, чат запуска | Пользователь, администратор · сессия | [US-OBS-01](../stories/observability.md#us-obs-01), [US-OBS-05](../stories/observability.md#us-obs-05) | [R-OBS-13](../../openspec/changes/define-agent-platform/specs/observability/spec.md#r-obs-13) | I20 |
