# R&D: шлюз к моделям

← [Все R&D](README.md) · компонент: LiteLLM gateway · решение: [design D5](../../openspec/changes/define-agent-platform/design.md)

## Варианты

| Критерий | LiteLLM Proxy | Kong AI Gateway | Portkey | Прямые вызовы (как в ICPlan) |
|---|---|---|---|---|
| Self-host | ✅ контейнер + Postgres | ✅ тяжелее | ⚠️ в основном managed | — |
| Virtual keys, бюджеты | ✅ | ⚠️ плагины | ✅ | ❌ |
| Алиасы и fallback | ✅ | ✅ | ✅ | ❌ |
| OpenAI-совместимый API | ✅ | ✅ | ✅ | — |
| Уже развёрнут у нас | ✅ `itsaplan-agents` | — | — | — |

## Mock для разработки

Ключ провайдера на этапе разработки не нужен: mock-LLM (OpenAI-совместимый, скриптовые ответы и tool calls) за тем же алиасом. Смена на реальную модель — одна строка конфига.

## Решение

LiteLLM Proxy; версия закреплена (`v1.77.3-stable` — более новые падали на миграциях, проект AI-агент).

## Источники

- [LiteLLM](https://github.com/BerriAI/litellm) · [документация](https://docs.litellm.ai/)
- Проект AI-агент: решения 1.1, 7.1; `platform/technical/layers-and-mcp.md` §3; `infra/README.md` (версии)
