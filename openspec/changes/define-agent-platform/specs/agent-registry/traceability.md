# agent-registry — трассировка требований (RTM)

← [spec.md](spec.md) · [интерфейсы и отказы](interfaces.md) · [правила](../../../../../docs/rules/spec-criteria.md)

Вверх — к исследованию и решению, вниз — к задаче реализации (ISO/IEC/IEEE 29148).

| Требование | User Story (вверх) | Обоснование (вверх) | Задача (вниз) | Сценариев |
|---|---|---|---|---|
| [R-REG-01](spec.md#r-reg-01) Каталог ресурсов | [US-ICP-20](../../../../../docs/stories/icplan.md#us-icp-20) | [R&D: хранение конфигурации](../../../../../docs/rnd/config-storage.md) · [design D9](../../../../../openspec/changes/define-agent-platform/design.md) | [1.2](../../../../../docs/tasks/1.2-agent-definition-yaml.md) | 3 |
| [R-REG-02](spec.md#r-reg-02) Определение агента | [US-ICP-20](../../../../../docs/stories/icplan.md#us-icp-20) | [R&D: хранение конфигурации](../../../../../docs/rnd/config-storage.md) · [design D9](../../../../../openspec/changes/define-agent-platform/design.md) | [1.2](../../../../../docs/tasks/1.2-agent-definition-yaml.md), [2.3](../../../../../docs/tasks/2.3-config-from-icplan.md) | 3 |
| [R-REG-03](spec.md#r-reg-03) Версионирование | [US-ICP-21](../../../../../docs/stories/icplan.md#us-icp-21) | [R&D: хранение конфигурации](../../../../../docs/rnd/config-storage.md) · [design D9](../../../../../openspec/changes/define-agent-platform/design.md) | [4.4](../../../../../docs/tasks/4.4-platform-module.md) | 3 |
| [R-REG-04](spec.md#r-reg-04) Источник правды и экспорт | [US-PM-03](../../../../../docs/stories/platform-module.md#us-pm-03) | [R&D: хранение конфигурации](../../../../../docs/rnd/config-storage.md) · [design D9](../../../../../openspec/changes/define-agent-platform/design.md) | [4.4](../../../../../docs/tasks/4.4-platform-module.md) | 3 |
| [R-REG-05](spec.md#r-reg-05) Валидация связей | [US-ICP-20](../../../../../docs/stories/icplan.md#us-icp-20) | [R&D: хранение конфигурации](../../../../../docs/rnd/config-storage.md) · [design D9](../../../../../openspec/changes/define-agent-platform/design.md) | [1.2](../../../../../docs/tasks/1.2-agent-definition-yaml.md) | 3 |
| [R-REG-06](spec.md#r-reg-06) Смена модели агента | [US-LLM-01](../../../../../docs/stories/llm-gateway.md#us-llm-01) | [R&D: хранение конфигурации](../../../../../docs/rnd/config-storage.md) · [design D9](../../../../../openspec/changes/define-agent-platform/design.md) | [2.3](../../../../../docs/tasks/2.3-config-from-icplan.md) | 3 |
| [R-REG-07](spec.md#r-reg-07) Конфигурация модуля | техническое | [параметры с обоснованием](interfaces.md) · [виды спек](../../../../../docs/rules/spec-kinds.md) | [2.3](../../../../../docs/tasks/2.3-config-from-icplan.md) | 3 |
| [R-REG-08](spec.md#r-reg-08) Хранилища данных | техническое | [R&D: СУБД](../../../../../docs/rnd/data-stores.md) · [D15](../../../../../openspec/changes/define-agent-platform/design.md) | [2.3](../../../../../docs/tasks/2.3-config-from-icplan.md), [4.4](../../../../../docs/tasks/4.4-platform-module.md) | 3 |
| [R-REG-09](spec.md#r-reg-09) Интерфейсы обмена | техническое | [интерфейсы](interfaces.md) · [типы данных](../../../../../docs/data-types.md) | [2.3](../../../../../docs/tasks/2.3-config-from-icplan.md) | 3 |
| [R-REG-10](spec.md#r-reg-10) Поведение при отказах зависимостей | техническое | [FMEA](interfaces.md) · [R&D: защита от сбоев](../../../../../docs/rnd/runaway-protection.md) | [2.3](../../../../../docs/tasks/2.3-config-from-icplan.md) | 3 |
| [R-REG-11](spec.md#r-reg-11) Нагрузка и производительность | техническое | [R&D: профиль нагрузки](../../../../../docs/rnd/load-profile.md) · [D16](../../../../../openspec/changes/define-agent-platform/design.md) | [4.8](../../../../../docs/tasks/4.8-load-test.md) | 3 |
| [R-REG-12](spec.md#r-reg-12) Развёртывание | техническое | [R&D: Kubernetes](../../../../../docs/rnd/kubernetes-runtime.md) · [D15](../../../../../openspec/changes/define-agent-platform/design.md) | [4.6](../../../../../docs/tasks/4.6-k8s-helm-ingress.md) | 3 |
