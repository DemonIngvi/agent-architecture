# Потоки: Agent Runner

← [Все потоки](README.md)

## Потоки

| # | Поток | От → к | Данные |
|---|---|---|---|
| 1 | Опрос очереди по ключу агента | Runner → ICPlan | `Run` |
| 2 | Планирование: свободны ли слоты (глобальный, агента, модели, задачи) | Runner → таблица слотов | `queued` → `admitted` |
| 2a | Допуск, бюджет (G1) | Runner → OPA | `PolicyInput` → `PolicyDecision` |
| 3 | Профиль и бюджет агента | Runner → Platform module | `AgentSettings` |
| 4 | Контейнер из тёплого пула | Runner → Sandbox | `profile` → `sandbox_id` |
| 5 | Токен репозиториев на запуск | Runner → git-провайдер | `RepoGrant` |
| 6 | Задание для Harness | Runner → Harness | `RunBundle` |
| 7 | События шагов | Harness → Runner → ICPlan | `RunEvent` |
| 8 | Решение по паузе | ICPlan → Runner → Harness | `ApprovalDecision` |
| 9 | Итог | Harness → Runner → ICPlan | `RunResult` |
| 10 | Таймаут или отмена | Runner → Harness | сигнал остановки |
| 11 | Уничтожение контейнера, долив пула | Runner → Sandbox | `sandbox_id` |

## Состояния запуска

```
pending ─▶ queued ─────────▶ admitted ─▶ running ─▶ succeeded
           (ждёт слот)          │           ├──────▶ waiting_approval ─▶ running
                                │           └──────▶ failed │ limit │ loop_detected │ cancelled
                                └─▶ rejected (G1: бюджет, kill switch)
```

## Данные

`RunBundle` — всё, что нужно Harness для запуска:

```json
{
  "run_id": "run_01J9Z4K",
  "agent": { "$ref": "AgentDefinition analyst v3" },
  "task": { "issue_key": "MKT-42", "prompt": "…", "acceptance": "Требования в формате SDD, разделы: проблема, ограничения, критерии" },
  "context": { "m3": "Сделано: черновик раздела «Проблема». Дальше: ограничения.", "m2": ["run_01J9Y: собраны вводные"] },
  "limits": { "max_steps": 30, "timeout_s": 1800, "max_tokens": 200000 },
  "endpoints": { "llm": "http://litellm:4000/v1", "itsaplan_mcp": "http://api:3000/mcp", "memory": "http://memory:8080" }
}
```

`PolicyInput` для G1:

```json
{ "input": { "point": "G1", "agent": "analyst", "issue": "MKT-42", "spent_today_usd": 3.2, "running_runs": 1 } }
```
