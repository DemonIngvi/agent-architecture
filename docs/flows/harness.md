# Потоки: Harness

← [Все потоки](README.md)

## Цикл

```
RunBundle ─▶ Bootstrap ─▶ Context Manager ─▶ LLM client ──▶ ответ модели
                               ▲                              │
                               │                    tool_calls?│ нет ─▶ RunResult
                               │                              ▼ да
                               │                   hook before_tool (G2)
                               │                     │allow   │confirm ─▶ пауза (interrupt) ─▶ ApprovalDecision
                               │                     ▼        │deny ──▶ отказ в контекст
                               └──── результат ◀── Tool Executor (MCP)
```

## Потоки

| # | Поток | От → к | Данные |
|---|---|---|---|
| 1 | Задание | Runner → Harness | `RunBundle` |
| 2 | Сборка контекста: инструкция, навыки, M3, M2 | Harness → Memory | `M3Record`, итоги запусков |
| 3 | Вызов модели | Harness → LiteLLM | `chat.completions` |
| 4 | Проверка действия (G2) | Harness → OPA | `PolicyInput` G2 |
| 5 | Вызов тула | Harness → MCP | `tools/call` |
| 6 | Пауза на подтверждение | Harness → Runner → ICPlan | `RunEvent` `needs_approval` |
| 7 | Сохранение шага | Harness → checkpointer | состояние графа |
| 8 | Шаги работы | Harness → Runner | `RunEvent` |
| 9 | Итог | Harness → Runner | `RunResult` |

## Данные

`RunEvent` — один шаг:

```json
{ "run_id": "run_01J9Z4K", "seq": 7, "ts": "2026-10-10T12:01:13Z", "type": "tool_call",
  "data": { "tool": "add_comment", "args": { "issue": "MKT-42", "body": "Черновик требований готов" } } }
```

Типы событий: `run_started`, `llm_call`, `tool_call`, `tool_result`, `needs_approval`, `question`, `memory_write`, `guardrail_decision`, `run_finished`.

`RunResult`:

```json
{ "run_id": "run_01J9Z4K", "status": "succeeded",
  "output": "## Требования\n…",
  "artifacts": [{ "name": "requirements.md", "url": "minio://attachments/MKT-42/requirements.md" }],
  "usage": { "prompt_tokens": 18450, "completion_tokens": 2210, "cost_usd": 0.12, "steps": 9 } }
```

Статусы: `succeeded`, `failed`, `limit`, `cancelled`.
