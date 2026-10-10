# R&D: Runner и очередь запусков

← [Все R&D](README.md) · компонент: Agent Runner · решения: [design D8, D14](../../openspec/changes/define-agent-platform/design.md)

## 1. Кто исполняет запуск

| Критерий | Внутренние агенты ICPlan | Раннер ICPlan (CLI) | Свой Runner как внешний раннер ICPlan | Свой push-API `start_run` |
|---|---|---|---|---|
| Изоляция запуска | ❌ в процессе ICPlan | ❌ общая папка | ✅ sandbox | ✅ sandbox |
| LLM только через LiteLLM | ⚠️ настройкой | ❌ CLI сам | ✅ | ✅ |
| Guardrails, approve | ❌ | ❌ approve отключён | ✅ | ✅ |
| Доработки ICPlan | — | — | минимальные | вызов нашего API |

**Решение:** свой Runner, подключённый к очереди ICPlan по протоколу внешнего раннера (D8).

## 2. Очередь и планирование

Условия: агентов несколько; часть может работать параллельно, часть нет; агенты делят модели (TPM/RPM провайдера); нужен переключатель «всё последовательно / параллельно»; по одной задаче не должно быть двух запусков одновременно.

| | A. Очередь на агента | B. Планировщик со слотами | C. Очередь с приоритетами и арендой |
|---|---|---|---|
| Суть | FIFO на агента, лимит `concurrency` | Запуск стартует, когда свободны все его слоты: глобальный, агента, модели, задачи | Общая очередь, исполнитель берёт задачу в аренду, продлевает её |
| Аналоги | раннер ICPlan, Sidekiq | квоты Kubernetes, семафоры Celery, лимиты LiteLLM | Temporal task queues, SQS visibility timeout |
| Режим «последовательно / параллельно» | только на агента | глобально и на агента | глобально |
| Общая модель у агентов | ❌ | ✅ слот модели | ⚠️ через LiteLLM |
| Один запуск на задачу | ❌ | ✅ слот задачи | ⚠️ отдельная блокировка |
| Сложность | низкая | средняя | высокая |

**Решение:** вариант B — планировщик внутри Agent Runner на этапе допуска (G1); очередь остаётся в ICPlan (D14).

```yaml
scheduling:
  mode: parallel            # sequential — все агенты строго по одному
  global_max: 4
  per_issue: 1
  order: fifo               # или priority (приоритет задачи ICPlan)
  agents:
    analyst:   { parallel: true,  max: 2 }
    developer: { parallel: false }
  models:
    team-default: { max: 3 }
```

Несколько экземпляров Runner делят слоты через общую блокировку в Postgres (advisory lock / таблица слотов).

## Источники

- Протокол раннера: `D:\АИ агент\itsaplan\docs\runner.md`, `packages/runner/README.md` (concurrency, pollIntervalMs)
- [Kubernetes ResourceQuota](https://kubernetes.io/docs/concepts/policy/resource-quotas/)
- [Celery: rate limits и очереди](https://docs.celeryq.dev/)
- [Temporal: task queues](https://docs.temporal.io/)
- [LiteLLM: лимиты на ключ и модель](https://docs.litellm.ai/)
- Проект AI-агент, предложение 4.4 `max_concurrent_runs` (`decisions-log.md`)
