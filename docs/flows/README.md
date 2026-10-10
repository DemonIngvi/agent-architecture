# Потоки данных: от задачи до итога

← [README](../../README.md) · [architecture.md](../../architecture.md) · [ROADMAP](../ROADMAP.md)

Сквозной поток MVP: пользователь двигает задачу — агент выполняет — итог возвращается в задачу. Форматы данных ниже — **черновик контрактов**, уточняются в задачах [1.2](../tasks/1.2-agent-definition-yaml.md) и [2.1](../tasks/2.1-runner-external.md).

```
Пользователь   ICPlan            Agent Runner      Sandbox+Harness      LiteLLM   MCP / Memory
    │ статус →     │                   │                   │                │           │
    ├─────────────▶│ ① автоподхват     │                   │                │           │
    │              │ ② run в очередь   │                   │                │           │
    │              │◀──────────────────┤ ③ опрос очереди   │                │           │
    │              │                   │ ④ G1 допуск       │                │           │
    │              │                   ├──────────────────▶│ ⑤ claim + bundle               │
    │              │                   │                   ├───────────────▶│ ⑥ LLM     │
    │              │                   │                   ├───────────────────────────▶│ ⑦ тулы, память
    │              │◀──────────────────┤◀──────────────────┤ ⑧ события      │           │
    │ approve  ───▶│──────────────────▶│──────────────────▶│ ⑨ пауза/ответ  │           │
    │              │◀──────────────────┤◀──────────────────┤ ⑩ итог         │           │
    │              │                   ├──────────────────▶│ ⑪ destroy      │           │
    │              │ ⑫ агент сменил статус → следующий агент (снова ①)       │           │
```

| # | Шаг | От → к | Данные | Канал |
|---|---|---|---|---|
| ① | Задача вошла в статус с агентом-делегатом | ICPlan → ICPlan | событие `issue.state_changed` | внутри ICPlan |
| ② | Запуск в очередь | ICPlan → БД | `Run` (pending) | БД ICPlan |
| ③ | Runner забирает запуск | Runner → ICPlan | `Run` | HTTP, ключ агента |
| ④ | Допуск и бюджет | Runner → OPA | `PolicyInput` G1 → `PolicyDecision` | HTTP |
| ⑤ | Выдача sandbox и задания | Runner → Harness | `RunBundle` | HTTP / stdin |
| ⑥ | Вызов модели | Harness → LiteLLM | `chat.completions` + `metadata.run_id` | OpenAI API |
| ⑦ | Действия и память | Harness → MCP / Memory | `tools/call`, `M3Record` | MCP, HTTP |
| ⑧ | Шаги работы | Harness → Runner → ICPlan | `RunEvent` | поток событий |
| ⑨ | Подтверждение | ICPlan → Runner → Harness | `ApprovalDecision` | HTTP |
| ⑩ | Итог | Harness → Runner → ICPlan | `RunResult` | HTTP |
| ⑪ | Уничтожение среды | Runner → Sandbox | `sandbox_id` | Docker API |
| ⑫ | Передача следующему этапу | агент → ICPlan | `update_issue` (статус) | MCP |

## Основные типы данных

| Тип | Кто создаёт | Кто читает | Подробно |
|---|---|---|---|
| `AgentDefinition` | ICPlan + Platform module | Runner, Harness | [ICPlan](icplan.md), [Platform module](platform-module.md) |
| `Run` | ICPlan | Runner | [Agent Runner](agent-runner.md) |
| `RunBundle` | Runner | Harness | [Agent Runner](agent-runner.md) |
| `RunEvent` | Harness | Runner, ICPlan, Observability | [Harness](harness.md), [Observability](observability.md) |
| `RunResult` | Harness | Runner, ICPlan | [Harness](harness.md) |
| `PolicyInput` / `PolicyDecision` | Runner, Harness / OPA | — | [Guardrails](guardrails.md) |
| `M3Record` | агент (тул) | Harness следующего запуска | [Memory](memory.md) |
| `RepoGrant` | Runner | Sandbox | [Sandbox](sandbox.md) |

## Потоки компонентов

[ICPlan](icplan.md) · [Platform module](platform-module.md) · [Agent Runner](agent-runner.md) · [Sandbox](sandbox.md) · [Harness](harness.md) · [Memory](memory.md) · [MCP / Tools](mcp-tools.md) · [Guardrails](guardrails.md) · [LiteLLM gateway](llm-gateway.md) · [Observability](observability.md)
