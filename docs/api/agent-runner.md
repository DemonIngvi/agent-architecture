# API: Agent Runner ↔ Harness

← [Каталог API](README.md) · [компонент](../../components/agent-runner/index.md) · [техспека](../techspec/agent-runner.md)

<div class="api-head">
<div><span class="about-label">Базовый адрес</span> Harness: `http://<sandbox>:8090`; Runner: `http://agent-runner:8080`</div>
<div><span class="about-label">Аутентификация</span> одноразовый токен запуска `RUN_TOKEN`</div>
</div>

## Harness (вызывает Runner)

| Метод | Путь | Статус | Что делает | Кто вызывает | Истории | Требования | I |
|---|---|---|---|---|---|---|---|
| <span class="m m-post">POST</span> | `/run` | <span class="st st-new">🆕 новое</span> | передать `RunBundle` и начать цикл | Agent Runner · токен запуска | [US-RUN-01](../stories/agent-runner.md#us-run-01) | [R-HRN-01](../../openspec/changes/define-agent-platform/specs/agent-harness/spec.md#r-hrn-01), [R-HRN-17](../../openspec/changes/define-agent-platform/specs/agent-harness/spec.md#r-hrn-17), [R-RUN-01](../../openspec/changes/define-agent-platform/specs/agent-runner/spec.md#r-run-01) | I7 |
| <span class="m m-get">GET</span> | `/run/events` | <span class="st st-new">🆕 новое</span> | поток `RunEvent` (NDJSON), переподключение с `seq` | Agent Runner · токен запуска | [US-ICP-02](../stories/icplan.md#us-icp-02) | [R-HRN-06](../../openspec/changes/define-agent-platform/specs/agent-harness/spec.md#r-hrn-06) | I7 |
| <span class="m m-post">POST</span> | `/run/approval` | <span class="st st-new">🆕 новое</span> | решение пользователя (`ApprovalDecision`) | Agent Runner · токен запуска | [US-HAR-02](../stories/harness.md#us-har-02) | [R-HRN-05](../../openspec/changes/define-agent-platform/specs/agent-harness/spec.md#r-hrn-05) | I7 |
| <span class="m m-post">POST</span> | `/run/message` | <span class="st st-new">🆕 новое</span> | указание пользователя во время работы | Agent Runner · токен запуска | [US-HAR-06](../stories/harness.md#us-har-06) | [R-HRN-16](../../openspec/changes/define-agent-platform/specs/agent-harness/spec.md#r-hrn-16) | I7 |
| <span class="m m-post">POST</span> | `/run/cancel` | <span class="st st-new">🆕 новое</span> | отмена | Agent Runner · токен запуска | [US-ICP-04](../stories/icplan.md#us-icp-04) | [R-RUN-09](../../openspec/changes/define-agent-platform/specs/agent-runner/spec.md#r-run-09) | I7 |
| <span class="m m-get">GET</span> | `/ready` | <span class="st st-new">🆕 новое</span> | готовность среды | Agent Runner · — | [US-SBX-01](../stories/sandbox.md#us-sbx-01) | [R-SBX-02](../../openspec/changes/define-agent-platform/specs/agent-sandbox/spec.md#r-sbx-02) | I7 |

## Runner (вызывает Harness)

| Метод | Путь | Статус | Что делает | Кто вызывает | Истории | Требования | I |
|---|---|---|---|---|---|---|---|
| <span class="m m-put">PUT</span> | `/runs/:runId/checkpoint` | <span class="st st-new">🆕 новое</span> | сохранить состояние цикла | Harness · токен запуска | [US-HAR-05](../stories/harness.md#us-har-05) | [R-HRN-05](../../openspec/changes/define-agent-platform/specs/agent-harness/spec.md#r-hrn-05) | I12 |
| <span class="m m-get">GET</span> | `/runs/:runId/checkpoint` | <span class="st st-new">🆕 новое</span> | восстановить состояние | Harness · токен запуска | [US-HAR-05](../stories/harness.md#us-har-05) | [R-HRN-05](../../openspec/changes/define-agent-platform/specs/agent-harness/spec.md#r-hrn-05) | I12 |
| <span class="m m-get">GET</span> | `/healthz · /readyz` | <span class="st st-new">🆕 новое</span> | здоровье Runner | Kubernetes · — | [US-RUN-05](../stories/agent-runner.md#us-run-05) | [R-RUN-16](../../openspec/changes/define-agent-platform/specs/agent-runner/spec.md#r-run-16) | — |
