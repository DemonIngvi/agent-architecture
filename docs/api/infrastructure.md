# Интеграции: Инфраструктура

← [компонент](../../components/infrastructure/index.md) · [Deploy](../techspec/infrastructure.md) · [методология](../rules/api-methodology.md)

<div class="api-head">
<div><span class="about-label">Базовый адрес</span> ingress Traefik</div>
<div><span class="about-label">Аутентификация</span> TLS</div>
</div>

## Входные точки

| Метод | Путь | Статус | Что делает | Кто вызывает | Истории | Требования | I |
|---|---|---|---|---|---|---|---|
| <span class="m m-get">GET</span> | `https://<домен>/` | <span class="st st-ok">✅ есть</span> | web ICPlan | Пользователи · сессия | [US-INF-02](../stories/infrastructure.md#us-inf-02) | [R-INF-04](../../openspec/changes/define-agent-platform/specs/platform-infrastructure/spec.md#r-inf-04) | I21 |
| <span class="m m-get">GET</span> | `https://<домен>/api/*` · `/mcp` | <span class="st st-ok">✅ есть</span> | api и MCP ICPlan | Пользователи, внешние агенты · сессия / ключ | [US-INF-02](../stories/infrastructure.md#us-inf-02) | [R-INF-04](../../openspec/changes/define-agent-platform/specs/platform-infrastructure/spec.md#r-inf-04) | I21 |
