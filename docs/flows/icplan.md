# Потоки: ICPlan

← [Все потоки](README.md)

## Потоки

| # | Поток | От → к | Данные |
|---|---|---|---|
| 1 | Пользователь двигает задачу по доске | Пользователь → Task UI | смена статуса задачи |
| 2 | Автоподхват: статус / тип / действие → агент-делегат | ICPlan → ICPlan | `delegateUserId` задачи |
| 3 | Постановка запуска в очередь | ICPlan → БД | `Run` (pending) |
| 4 | Runner забирает запуск | Agent Runner → ICPlan | `Run` |
| 5 | Шаги работы агента в задачу | Agent Runner → ICPlan | `RunEvent` → таймлайн |
| 6 | Подтверждение действия | Пользователь → Task UI → Runner | `ApprovalDecision` |
| 7 | Итог в задачу | Agent Runner → ICPlan | `RunResult` → комментарий, вложения |
| 8 | Агент сам переводит задачу на следующий этап | Агент (MCP) → ICPlan | `update_issue` |
| 9 | Администратор настраивает агента | Админ → Control Plane UI → Registry | `AgentDefinition` |

## Данные

`Run` — запуск в очереди (черновик, уточняется по протоколу `@itsaplan/runner` в задаче [2.1](../tasks/2.1-runner-external.md)):

```json
{
  "run_id": "run_01J9Z4K",
  "agent_id": "ag_42",
  "source": "delegation",
  "issue": { "key": "MKT-42", "title": "Описать требования к экспорту", "url": "http://localhost:3001/team/MKT/issue/42" },
  "prompt": "Work item MKT-42 has been delegated to you. Review it and take the appropriate next step.",
  "rule": { "type": "column", "column": "Анализ" },
  "created_at": "2026-10-10T12:00:00Z"
}
```

Правило автоподхвата (поле статуса, доработка [3.1](../tasks/3.1-icplan-autodelegate-status.md)):

```json
{ "column_id": 17, "name": "Анализ", "auto_delegate_user_id": "agent:analyst" }
```

`ApprovalDecision` — ответ пользователя на паузу агента:

```json
{ "run_id": "run_01J9Z4K", "seq": 12, "decision": "approve", "by": "user_7", "comment": "Можно" }
```
