# Интеграции: Guardrails (OPA)

← [компонент](../../components/guardrails/index.md) · [Deploy](../techspec/guardrails.md) · [методология](../rules/api-methodology.md)

<div class="api-head">
<div><span class="about-label">Базовый адрес</span> `http://opa:8181`</div>
<div><span class="about-label">Аутентификация</span> внутренняя сеть (mTLS — этап 4)</div>
</div>

## Решения

| Метод | Путь | Статус | Что делает | Кто вызывает | Истории | Требования | I |
|---|---|---|---|---|---|---|---|
| <span class="m m-post">POST</span> | `/v1/data/agent/g1` | <span class="st st-ok">✅ есть</span> | допуск запуска (`PolicyInput` → `PolicyDecision`) | Agent Runner · сеть | [US-GRD-03](../stories/guardrails.md#us-grd-03) | [R-GRD-02](../../openspec/changes/define-agent-platform/specs/guardrails/spec.md#r-grd-02) | I5 |
| <span class="m m-post">POST</span> | `/v1/data/agent/g2` | <span class="st st-ok">✅ есть</span> | проверка действия агента | Harness · сеть | [US-GRD-06](../stories/guardrails.md#us-grd-06), [US-HAR-02](../stories/harness.md#us-har-02) | [R-GRD-03](../../openspec/changes/define-agent-platform/specs/guardrails/spec.md#r-grd-03) | I10 |
| <span class="m m-get">GET</span> | `/health?bundles` | <span class="st st-ok">✅ есть</span> | готовность и версия бандла | Kubernetes · — | [US-GRD-01](../stories/guardrails.md#us-grd-01) | [R-GRD-07](../../openspec/changes/define-agent-platform/specs/guardrails/spec.md#r-grd-07) | I16 |
