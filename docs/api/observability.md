# API: Observability

← [Каталог API](README.md) · [компонент](../../components/observability/index.md) · [техспека](../techspec/observability.md)

<div class="api-head">
<div><span class="about-label">Базовый адрес</span> в api ICPlan</div>
<div><span class="about-label">Аутентификация</span> сессия</div>
</div>

## Где описано

| Метод | Путь | Статус | Что делает | Кто вызывает | Истории | Требования | I |
|---|---|---|---|---|---|---|---|
| <span class="m m-get">GET</span> | [ICPlan → Сводка и статистика](icplan.md) | <span class="st st-ok">✅ есть</span> | аналитика агентов, сводка, чат запуска | Пользователь, администратор · сессия | [US-OBS-01](../stories/observability.md#us-obs-01), [US-OBS-05](../stories/observability.md#us-obs-05) | [R-OBS-13](../../openspec/changes/define-agent-platform/specs/observability/spec.md#r-obs-13) | I20 |
