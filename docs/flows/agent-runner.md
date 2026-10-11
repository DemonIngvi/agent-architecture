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

Единый список статусов запуска — требование R-RUN-07; остальные документы ссылаются на него.

```
queued ─▶ starting ─▶ running ─▶ succeeded
  │  (ждёт слот)          ├──────▶ waiting_approval ─▶ running
  │                       ├──────▶ gate_failed
  │                       ├──────▶ limit_exceeded   (шаги, время, простой, бюджет, зацикливание)
  │                       ├──────▶ failed
  │                       └──────▶ canceled
  └─▶ limit_exceeded / failed   (G1 до старта: бюджет / kill switch, агент недоступен)
```

| Причина завершения Harness (R-HRN-09) | Статус запуска (R-RUN-07) | Статус в ICPlan (`agent_run`) |
|---|---|---|
| `done` | `succeeded` | `success` |
| `gate_failed` | `gate_failed` | `failed` с пометкой «не прошёл проверку» |
| `limit` (шаги, время, простой, `loop_detected`) | `limit_exceeded` | `failed` с причиной |
| `error` | `failed` | `failed` |
| остановка пользователем | `canceled` | `canceled` |

## Данные

`RunBundle` — всё, что нужно Harness для запуска:

Поля — [`RunBundle`](../../data-model.md#model-runbundle); пример — [каталог API](../api/README.md#runbundle). Здесь копия не ведётся: модели и примеры живут в одном источнике ([правило](../rules/change-process.md#single-source)).

`PolicyInput` для G1:

Поля — [`PolicyInput`](../../data-model.md#model-policyinput) · [`PolicyDecision`](../../data-model.md#model-policydecision); пример — [каталог API](../api/README.md#policyinput-policydecision). Здесь копия не ведётся: модели и примеры живут в одном источнике ([правило](../rules/change-process.md#single-source)).
