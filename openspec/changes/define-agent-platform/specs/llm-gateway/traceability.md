# llm-gateway — трассировка требований (RTM)

← [spec.md](spec.md) · [интерфейсы и отказы](interfaces.md) · [правила](../../../../../docs/rules/spec-criteria.md)

Вверх — к исследованию и решению, вниз — к задаче реализации (ISO/IEC/IEEE 29148).

| Требование | User Story (вверх) | Обоснование (вверх) | Задача (вниз) | Сценариев |
|---|---|---|---|---|
| Алиасы моделей | [US-LLM-01](../../../../../docs/stories/llm-gateway.md) | [R&D: шлюз к моделям](../../../../../docs/rnd/llm-gateway.md) · [design D5](../../../../../openspec/changes/define-agent-platform/design.md) | [1.1](../../../../../docs/tasks/1.1-mock-llm-litellm.md) | 3 |
| Учёт токенов | [US-LLM-03](../../../../../docs/stories/llm-gateway.md) | [R&D: шлюз к моделям](../../../../../docs/rnd/llm-gateway.md) · [design D5](../../../../../openspec/changes/define-agent-platform/design.md) | [1.1](../../../../../docs/tasks/1.1-mock-llm-litellm.md), [3.5](../../../../../docs/tasks/3.5-icplan-type-actions-cost.md) | 3 |
| Атрибуция затрат | [US-LLM-03](../../../../../docs/stories/llm-gateway.md) | [R&D: шлюз к моделям](../../../../../docs/rnd/llm-gateway.md) · [design D5](../../../../../openspec/changes/define-agent-platform/design.md) | [3.5](../../../../../docs/tasks/3.5-icplan-type-actions-cost.md) | 3 |
| Mock-модель для разработки | [US-LLM-02](../../../../../docs/stories/llm-gateway.md) | [R&D: шлюз к моделям](../../../../../docs/rnd/llm-gateway.md) · [design D5](../../../../../openspec/changes/define-agent-platform/design.md) | [1.1](../../../../../docs/tasks/1.1-mock-llm-litellm.md) | 3 |
| Лимиты | техническое | [R&D: шлюз к моделям](../../../../../docs/rnd/llm-gateway.md) · [design D5](../../../../../openspec/changes/define-agent-platform/design.md) | [4.5](../../../../../docs/tasks/4.5-litellm-budgets-fallback-g4.md) | 3 |
| Fallback | [US-LLM-04](../../../../../docs/stories/llm-gateway.md) | [R&D: шлюз к моделям](../../../../../docs/rnd/llm-gateway.md) · [design D5](../../../../../openspec/changes/define-agent-platform/design.md) | [4.5](../../../../../docs/tasks/4.5-litellm-budgets-fallback-g4.md) | 3 |
| Несколько провайдеров | техническое | [R&D: шлюз к моделям](../../../../../docs/rnd/llm-gateway.md) · [design D5](../../../../../openspec/changes/define-agent-platform/design.md) | [1.1](../../../../../docs/tasks/1.1-mock-llm-litellm.md) | 3 |
| Конфигурация модуля | техническое | [R&D: шлюз к моделям](../../../../../docs/rnd/llm-gateway.md) · [design D5](../../../../../openspec/changes/define-agent-platform/design.md) | [2.8](../../../../../docs/tasks/2.8-config-storage-interfaces-fmea.md), [1.1](../../../../../docs/tasks/1.1-mock-llm-litellm.md) | 3 |
| Хранилища данных | техническое | [R&D: шлюз к моделям](../../../../../docs/rnd/llm-gateway.md) · [design D5](../../../../../openspec/changes/define-agent-platform/design.md) | [2.8](../../../../../docs/tasks/2.8-config-storage-interfaces-fmea.md), [1.1](../../../../../docs/tasks/1.1-mock-llm-litellm.md) | 3 |
| Интерфейсы обмена | техническое | [R&D: шлюз к моделям](../../../../../docs/rnd/llm-gateway.md) · [design D5](../../../../../openspec/changes/define-agent-platform/design.md) | [2.8](../../../../../docs/tasks/2.8-config-storage-interfaces-fmea.md), [1.1](../../../../../docs/tasks/1.1-mock-llm-litellm.md) | 3 |
| Поведение при отказах зависимостей | техническое | [R&D: шлюз к моделям](../../../../../docs/rnd/llm-gateway.md) · [design D5](../../../../../openspec/changes/define-agent-platform/design.md) | [2.8](../../../../../docs/tasks/2.8-config-storage-interfaces-fmea.md), [4.5](../../../../../docs/tasks/4.5-litellm-budgets-fallback-g4.md) | 4 |
| Нагрузка и производительность | техническое | [R&D: шлюз к моделям](../../../../../docs/rnd/llm-gateway.md) · [design D5](../../../../../openspec/changes/define-agent-platform/design.md) | [4.8](../../../../../docs/tasks/4.8-load-test.md) | 3 |
| Развёртывание | техническое | [R&D: шлюз к моделям](../../../../../docs/rnd/llm-gateway.md) · [design D5](../../../../../openspec/changes/define-agent-platform/design.md) | [4.6](../../../../../docs/tasks/4.6-k8s-helm-ingress.md) | 3 |
