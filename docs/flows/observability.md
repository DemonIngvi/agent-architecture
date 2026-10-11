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

Таблица событий `run_event` — поля, связи, индексы и срок в [Модели данных](../../data-model.md#s3); формат события — [`RunEvent`](../../data-model.md#model-runevent) (AG-UI, D21). Описание здесь не дублируется ([правило](../rules/change-process.md#single-source)).

Агрегат затрат:

Поля — [`CostAggregate`](../../data-model.md#model-costaggregate); пример — [каталог API](../api/README.md#costaggregate). Здесь копия не ведётся: модели и примеры живут в одном источнике ([правило](../rules/change-process.md#single-source)).
