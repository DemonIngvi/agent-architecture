# Потоки: Observability

← [Все потоки](README.md)

## Потоки

| # | Поток | От → к | Данные |
|---|---|---|---|
| 1 | Шаги запуска | Harness → Runner → БД ICPlan | `RunEvent` |
| 2 | Решения guardrails | Runner, Harness → БД | `RunEvent` `guardrail_decision` |
| 3 | Затраты | LiteLLM spend log → агрегаты | токены, $, `run_id` |
| 4 | Таймлайн задачи | БД → Task UI | список `RunEvent` |
| 5 | Затраты задачи | агрегаты → Task UI | сумма по задаче |
| 6 | Очистка по сроку | БД | события старше срока; агрегаты остаются |

## Данные

Таблица событий (черновик):

```sql
create table run_event (
  run_id    text        not null,
  seq       int         not null,
  ts        timestamptz not null,
  type      text        not null,   -- tool_call, llm_call, needs_approval, ...
  data      jsonb       not null,
  issue_key text        not null,
  primary key (run_id, seq)
);
```

Агрегат затрат:

```json
{ "issue_key": "MKT-42", "agent": "analyst", "runs": 3, "prompt_tokens": 51200, "completion_tokens": 6400, "cost_usd": 0.34 }
```
