# Интеграции: LiteLLM gateway

← [компонент](../../components/llm-gateway/index.md) · [Deploy](../techspec/llm-gateway.md) · [методология](../rules/api-methodology.md)

<div class="api-head">
<div><span class="about-label">Базовый адрес</span> `http://litellm:4000`</div>
<div><span class="about-label">Аутентификация</span> virtual key агента; админ — master key</div>
</div>

## Модели

| Метод | Путь | Статус | Что делает | Кто вызывает | Истории | Требования | I |
|---|---|---|---|---|---|---|---|
| <span class="m m-post">POST</span> | `/v1/chat/completions` | <span class="st st-ok">✅ есть</span> | вызов модели (поля — [сборка запроса](../how/harness.md#llm-request)) | Harness · virtual key | [US-HAR-01](../stories/harness.md#us-har-01), [US-LLM-01](../stories/llm-gateway.md#us-llm-01) | [R-HRN-03](../../openspec/changes/define-agent-platform/specs/agent-harness/spec.md#r-hrn-03), [R-HRN-18](../../openspec/changes/define-agent-platform/specs/agent-harness/spec.md#r-hrn-18), [R-LLM-01](../../openspec/changes/define-agent-platform/specs/llm-gateway/spec.md#r-llm-01) | I8 |
| <span class="m m-post">POST</span> | `/key/generate · /key/update` | <span class="st st-ok">✅ есть</span> | virtual key агента с бюджетом и лимитами | Platform module · master key | [US-PM-04](../stories/platform-module.md#us-pm-04) | [R-CP-06](../../openspec/changes/define-agent-platform/specs/control-plane/spec.md#r-cp-06), [R-LLM-05](../../openspec/changes/define-agent-platform/specs/llm-gateway/spec.md#r-llm-05) | I15 |
| <span class="m m-get">GET</span> | `/spend/logs` | <span class="st st-ok">✅ есть</span> | затраты по `metadata.run_id` | Observability · master key | [US-LLM-03](../stories/llm-gateway.md#us-llm-03), [US-LLM-05](../stories/llm-gateway.md#us-llm-05) | [R-LLM-03](../../openspec/changes/define-agent-platform/specs/llm-gateway/spec.md#r-llm-03) | I14 |

## mock-LLM

| Метод | Путь | Статус | Что делает | Кто вызывает | Истории | Требования | I |
|---|---|---|---|---|---|---|---|
| <span class="m m-post">POST</span> | `/v1/chat/completions` | <span class="st st-new">🆕 новое</span> | скриптовые ответы и вызовы тулов | LiteLLM (алиас `mock`) · — | [US-LLM-02](../stories/llm-gateway.md#us-llm-02) | [R-LLM-04](../../openspec/changes/define-agent-platform/specs/llm-gateway/spec.md#r-llm-04) | I13 |
