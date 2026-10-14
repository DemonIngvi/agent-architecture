# Сводка последствий R&D

Сводка последствий исследовательских решений по этапу Э10. Здесь перечислены изменения, которые внесены в архитектуру, спеки, модели данных и задачи после R&D.

| Исследование | Изменение | Статус | Ссылка |
|---|---|---|---|
| [Цепочки агентов](rnd/agent-chain.md) | D27 / D28: граф процесса, причины возврата, лимиты, режимы обучения, снимки и ограничения | ✅ внесено | [D27 / D28](../openspec/changes/define-agent-platform/design.md) |
| [Разработка, деплой и мониторинг](rnd/dev-deploy-monitoring.md) | D29: три уровня контроля токенов, CI-процесс, среды, версии и kill switch | ✅ внесено | [D29](../openspec/changes/define-agent-platform/design.md) |
| [Модель памяти](rnd/memory-model.md) | память M1–M3, M4 после MVP, источники и TTL | ✅ внесено | [agent-memory](../openspec/changes/define-agent-platform/specs/agent-memory/spec.md) |
| [Хранение конфигурации](rnd/config-storage.md) | версии настроек, экспорт/импорт, роли и профили | ✅ внесено | [agent-registry](../openspec/changes/define-agent-platform/specs/agent-registry/spec.md) |
| [Движок guardrails](rnd/guardrails-engine.md) | единый движок OPA, уровни и ограничения | ✅ внесено | [guardrails](../openspec/changes/define-agent-platform/specs/guardrails/spec.md) |
| [Наблюдаемость](rnd/observability.md) | события запуска, стоимость на принятую задачу и статистика | ✅ внесено | [observability](../openspec/changes/define-agent-platform/specs/observability/spec.md) |

## Проверка

Каждая строка Э10 должна иметь ссылку на существующий документ и статус: «внесено» или «предложено». При изменениях архитектуры и требовании к интеграциям следует проверять сразу связанные спецификации и таблицы задач.

## Статус по текущему состоянию

- D27 и D28 внесены в [design.md](../openspec/changes/define-agent-platform/design.md).
- Изменения отражены в [BACKLOG.md](BACKLOG.md), [ROADMAP.md](ROADMAP.md) и связанных задачах.
- Все ссылки в документах должны вести на реальные разделы и якоря в существующих файлах.
