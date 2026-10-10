# R&D: хранение конфигурации

← [Все R&D](README.md) · компонент: Platform module · решение: [design D9](../../openspec/changes/define-agent-platform/design.md)

## Варианты

| | Git (Config Repo, проект AI-агент) | БД ICPlan + экспорт YAML | Отдельный Platform API со своей БД |
|---|---|---|---|
| Правка из UI | ❌ нужна синхронизация | ✅ сразу | ✅ |
| Ревью изменений | ✅ PR | ⚠️ через экспорт YAML | ⚠️ |
| История и откат | ✅ | ✅ таблица версий | писать |
| Источник правды | два (git и UI) | один | два (ICPlan и наш) |
| Перенос dev → prod | ✅ merge | ✅ экспорт / импорт | писать |
| Слияние с upstream ICPlan | не влияет | ⚠️ модуль в форке | не влияет |

Индустрия: гибрид — БД и UI как источник правды, экспорт/импорт для ревью и переноса.

## Разделение для guardrails

Логика правил (Rego) — код: git, тесты, ревью. Данные правил (allowlist, лимиты агента) — БД: меняются часто и из UI. Стандартное для OPA разделение policy / data.

## Решение

БД ICPlan; Platform module — модуль форка со своей схемой; версии и YAML экспорт/импорт.

## Источники

- [OPA: policy и data](https://www.openpolicyagent.org)
- Проект AI-агент: решения 1.6, 1.7; `agents/technical/pools-and-binding.md`
