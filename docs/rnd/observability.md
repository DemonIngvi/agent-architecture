# R&D: наблюдаемость

← [Все R&D](README.md) · компонент: Observability · решение: [design D12](../../openspec/changes/define-agent-platform/design.md)

## Варианты

| Критерий | Таблица событий в БД ICPlan | Langfuse | Prometheus / Grafana / Loki |
|---|---|---|---|
| Шаги агента в задаче | ✅ | ✅ | ❌ |
| Затраты | ✅ из LiteLLM | ✅ | ⚠️ метрики |
| Evals, анализ промптов | ❌ | ✅ | ❌ |
| Self-host | ничего нового | Postgres + ClickHouse + Redis + S3 | уже развёрнуто |
| Лицензия | — | MIT ядро, часть EE | Apache 2.0 / AGPL |

## Решение

MVP — таблица событий запуска → таймлайн в задаче. Langfuse — после MVP. Prometheus / Grafana / Loki — в бэклоге (пустые).

## Источники

- [Langfuse](https://github.com/langfuse/langfuse)
- Проект AI-агент: решение 3.8; стек `itsaplan-platform`
