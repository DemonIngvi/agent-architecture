# icplan-integration — трассировка требований (RTM)

← [spec.md](spec.md) · [интерфейсы и отказы](interfaces.md) · [правила](../../../../../docs/rules/spec-criteria.md)

Вверх — к исследованию и решению, вниз — к задаче реализации (ISO/IEC/IEEE 29148).

| Требование | User Story (вверх) | Обоснование (вверх) | Задача (вниз) | Сценариев |
|---|---|---|---|---|
| [R-ICP-10](spec.md#r-icp-10) Конфигурация модуля | техническое | [параметры с обоснованием](interfaces.md) · [виды спек](../../../../../docs/rules/spec-kinds.md) | [2.1](../../../../../docs/tasks/2.1-runner-external.md) | 3 |
| [R-ICP-11](spec.md#r-icp-11) Хранилища данных | техническое | [R&D: СУБД](../../../../../docs/rnd/data-stores.md) · [D15](../../../../../openspec/changes/define-agent-platform/design.md) | [2.1](../../../../../docs/tasks/2.1-runner-external.md) | 3 |
| [R-ICP-12](spec.md#r-icp-12) Интерфейсы обмена | техническое | [интерфейсы](interfaces.md) · [типы данных](../../../../../docs/flows/data-types.md) | [2.1](../../../../../docs/tasks/2.1-runner-external.md) | 3 |
| [R-ICP-13](spec.md#r-icp-13) Поведение при отказах зависимостей | техническое | [FMEA](interfaces.md) · [R&D: защита от сбоев](../../../../../docs/rnd/runaway-protection.md) | [2.1](../../../../../docs/tasks/2.1-runner-external.md), [2.6](../../../../../docs/tasks/2.6-e2e-icplan.md) | 3 |
| [R-ICP-14](spec.md#r-icp-14) Нагрузка и производительность | техническое | [R&D: профиль нагрузки](../../../../../docs/rnd/load-profile.md) · [D16](../../../../../openspec/changes/define-agent-platform/design.md) | [4.8](../../../../../docs/tasks/4.8-load-test.md) | 3 |
| [R-ICP-15](spec.md#r-icp-15) Развёртывание | техническое | [R&D: Kubernetes](../../../../../docs/rnd/kubernetes-runtime.md) · [D15](../../../../../openspec/changes/define-agent-platform/design.md) | [4.6](../../../../../docs/tasks/4.6-k8s-helm-ingress.md) | 3 |
| [R-ICP-16](spec.md#r-icp-16) Указания пользователя во время запуска | [US-ICP-10](../../../../../docs/stories/icplan.md#us-icp-10), [US-HAR-06](../../../../../docs/stories/harness.md#us-har-06) | [D17](../../../../../openspec/changes/define-agent-platform/design.md) · [R&D: потоки аналогов](../../../../../docs/rnd/us-analogs-agent-tracker.md) | [3.8](../../../../../docs/tasks/3.8-agent-chat-control.md) | 3 |
| [R-ICP-17](spec.md#r-icp-17) Выключение агента | [US-ICP-22](../../../../../docs/stories/icplan.md#us-icp-22) | [D17](../../../../../openspec/changes/define-agent-platform/design.md) · [R&D: потоки аналогов](../../../../../docs/rnd/us-analogs-agent-tracker.md) | [3.8](../../../../../docs/tasks/3.8-agent-chat-control.md) | 3 |
| [R-ICP-18](spec.md#r-icp-18) Проверка агента в чате | [US-ICP-24](../../../../../docs/stories/icplan.md#us-icp-24) | [D17](../../../../../openspec/changes/define-agent-platform/design.md) · [R&D: потоки аналогов](../../../../../docs/rnd/us-analogs-agent-tracker.md) | [3.8](../../../../../docs/tasks/3.8-agent-chat-control.md) | 3 |
