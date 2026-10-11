# API: Memory API

← [Каталог API](README.md) · [компонент](../../components/memory/index.md) · [техспека](../techspec/memory.md)

<div class="api-head">
<div><span class="about-label">Базовый адрес</span> `http://memory-api:8085`</div>
<div><span class="about-label">Аутентификация</span> токен запуска (Harness), сервисный токен (администрирование)</div>
</div>

## Память

| Метод | Путь | Статус | Что делает | Кто вызывает | Истории | Требования | I |
|---|---|---|---|---|---|---|---|
| <span class="m m-get">GET</span> | `/context?issueId=&agentId=` | <span class="st st-new">🆕 новое</span> | контекст запуска: M1, M2, M3 по профилю | Harness · токен запуска | [US-MEM-01](../stories/memory.md#us-mem-01), [US-MEM-02](../stories/memory.md#us-mem-02), [US-MEM-06](../stories/memory.md#us-mem-06) | [R-MEM-05](../../openspec/changes/define-agent-platform/specs/agent-memory/spec.md#r-mem-05), [R-MEM-04](../../openspec/changes/define-agent-platform/specs/agent-memory/spec.md#r-mem-04) | I11 |
| <span class="m m-put">PUT</span> | `/m3/:issueId` | <span class="st st-new">🆕 новое</span> | записать состояние задачи (проверки до записи) | Harness (тул памяти) · токен запуска | [US-MEM-01](../stories/memory.md#us-mem-01) | [R-MEM-04](../../openspec/changes/define-agent-platform/specs/agent-memory/spec.md#r-mem-04), [R-MEM-15](../../openspec/changes/define-agent-platform/specs/agent-memory/spec.md#r-mem-15) | I11 |
| <span class="m m-del">DELETE</span> | `/records/:level/:id` | <span class="st st-new">🆕 новое</span> | удалить запись | Администратор · сервисный токен | [US-MEM-03](../stories/memory.md#us-mem-03) | [R-MEM-07](../../openspec/changes/define-agent-platform/specs/agent-memory/spec.md#r-mem-07) | I11 |
| <span class="m m-post">POST</span> | `/retention/run` | <span class="st st-new">🆕 новое</span> | очистка по срокам (CronJob) | Kubernetes CronJob · сервисный токен | [US-MEM-10](../stories/memory.md#us-mem-10) | [R-MEM-08](../../openspec/changes/define-agent-platform/specs/agent-memory/spec.md#r-mem-08) | — |
