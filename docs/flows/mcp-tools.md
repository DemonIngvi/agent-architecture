# Потоки: MCP / Tools

← [Все потоки](README.md)

## Потоки

| # | Поток | От → к | Данные | Правило |
|---|---|---|---|---|
| 1 | Список тулов агенту | MCP-сервер → MCP-прокси Runner → Harness | `tools/list`, отфильтровано allowlist запуска (D19) | R3 |
| 2 | Вызов тула | Harness → MCP-прокси Runner → MCP-сервер | `tools/call`; Runner проверяет allowlist и подставляет учётные данные | R2 / R3 |
| 3 | Проверка перед вызовом | Harness → OPA; для MCP повторно Runner → OPA | `PolicyInput` G2 | — |
| 4 | Работа с задачей | MCP `itsaplan-core` → ICPlan | задача, комментарий, статус | R3 |
| 5 | Работа с кодом | MCP git → git-провайдер | ветка, PR | R3 |
| 6 | Запись памяти | нативный тул Harness → Memory | `M3Record` | R4 |
| 7 | Внутренние вызовы платформы | сервис → сервис | REST / gRPC, не MCP | R7 |

## Данные

`tools/call` (MCP):

```json
{ "jsonrpc": "2.0", "id": 12, "method": "tools/call",
  "params": { "name": "update_issue", "arguments": { "issue": "MKT-42", "state": "Ревью" } } }
```

Подключение MCP-сервера к агенту:

```yaml
mcp:
  - server: itsaplan-core
    url: http://api:3000/mcp      # агент ходит через http://agent-runner:8080/runs/<id>/mcp/itsaplan-core (D19)
    auth: { secret_ref: agent-key/analyst }   # ключ не попадает в контекст агента
    tools: [get_issue, add_comment, update_issue]
    timeout_s: 30
```
