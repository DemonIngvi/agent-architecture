# Потоки: Observability

← [Все потоки](README.md)

## Потоки

| # | Поток | От → к | Данные |
|---|---|---|---|
| 1 | Шаги запуска | Harness → Runner → БД ICPlan | `RunEvent` |
| 2 | Решения guardrails | Runner, Harness → БД | `RunEvent` (`CUSTOM` `guardrail_decision`) |
| 3 | Затраты | LiteLLM spend log → агрегаты | токены, $, `run_id` |
| 4 | Чат запуска в задаче | БД и живой поток → панель «Агент» | `RunEvent` (AG-UI), [поток](icplan.md#agent-feed) |
| 5 | Затраты задачи | агрегаты → Task UI | сумма по задаче |
| 6 | Очистка по сроку | БД | события старше срока; агрегаты остаются |

## Данные

<!-- flow-data -->
