# API: MCP / Tools

← [Каталог API](README.md) · [компонент](../../components/mcp-tools/index.md) · [техспека](../techspec/mcp-tools.md)

<div class="api-head">
<div><span class="about-label">Базовый адрес</span> MCP-серверы по протоколу MCP (streamable HTTP)</div>
<div><span class="about-label">Аутентификация</span> ключ агента / секрет сервера</div>
</div>

## Протокол MCP

| Метод | Путь | Статус | Что делает | Кто вызывает | Истории | Требования | I |
|---|---|---|---|---|---|---|---|
| <span class="m m-post">POST</span> | `tools/list` | <span class="st st-ok">✅ есть</span> | тулы сервера (фильтр по allowlist агента) | Harness · ключ | [US-MCP-02](../stories/mcp-tools.md#us-mcp-02) | [R-MCP-02](../../openspec/changes/define-agent-platform/specs/tool-integration/spec.md#r-mcp-02) | I9 |
| <span class="m m-post">POST</span> | `tools/call` | <span class="st st-ok">✅ есть</span> | вызов тула | Harness · ключ | [US-MCP-02](../stories/mcp-tools.md#us-mcp-02), [US-HAR-01](../stories/harness.md#us-har-01) | [R-MCP-03](../../openspec/changes/define-agent-platform/specs/tool-integration/spec.md#r-mcp-03), [R-MCP-13](../../openspec/changes/define-agent-platform/specs/tool-integration/spec.md#r-mcp-13) | I9 |
