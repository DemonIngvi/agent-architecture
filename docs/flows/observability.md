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

Таблица событий `run_event` (ключ `run_id` + `seq`, `run_id` → `agent_run.id`, тип, время, `data` jsonb, ключ задачи) — поля и связи в [Модели данных](../../data-model.md#s3) (источник `html-view/datamodel.py`; SQL здесь не дублируется — правило О-43).

Агрегат затрат:

```json
{ "issue_key": "MKT-42", "agent": "analyst", "runs": 3, "prompt_tokens": 51200, "completion_tokens": 6400, "cost_usd": 0.34 }
```
