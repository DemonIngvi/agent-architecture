# agent-runner — трассировка требований (RTM)

← [spec.md](spec.md) · [интерфейсы и отказы](interfaces.md) · [правила](../../../../../docs/rules/spec-criteria.md)

Вверх — к исследованию и решению, вниз — к задаче реализации (ISO/IEC/IEEE 29148).

| Требование | User Story (вверх) | Обоснование (вверх) | Задача (вниз) | Сценариев |
|---|---|---|---|---|
| [R-RUN-11](spec.md#r-run-11) Конфигурация модуля | техническое | [параметры с обоснованием](interfaces.md) · [виды спек](../../../../../docs/rules/spec-kinds.md) | [2.1](../../../../../docs/tasks/2.1-runner-external.md), [2.7](../../../../../docs/tasks/2.7-runner-scheduler.md), [2.8](../../../../../docs/tasks/2.8-config-storage-interfaces-fmea.md) | 3 |
| [R-RUN-12](spec.md#r-run-12) Хранилища данных | техническое | [R&D: СУБД](../../../../../docs/rnd/data-stores.md) · [D15](../../../../../openspec/changes/define-agent-platform/design.md) | [2.1](../../../../../docs/tasks/2.1-runner-external.md), [2.7](../../../../../docs/tasks/2.7-runner-scheduler.md) | 3 |
| [R-RUN-13](spec.md#r-run-13) Интерфейсы обмена | техническое | [интерфейсы](interfaces.md) · [типы данных](../../../../../docs/flows/data-types.md) | [2.1](../../../../../docs/tasks/2.1-runner-external.md) | 3 |
| [R-RUN-14](spec.md#r-run-14) Поведение при отказах зависимостей | [US-RUN-05](../../../../../docs/stories/agent-runner.md#us-run-05) | [FMEA](interfaces.md) · [R&D: защита от сбоев](../../../../../docs/rnd/runaway-protection.md) | [2.1](../../../../../docs/tasks/2.1-runner-external.md), [2.6](../../../../../docs/tasks/2.6-e2e-icplan.md) | 4 |
| [R-RUN-15](spec.md#r-run-15) Нагрузка и производительность | техническое | [R&D: профиль нагрузки](../../../../../docs/rnd/load-profile.md) · [D16](../../../../../openspec/changes/define-agent-platform/design.md) | [4.8](../../../../../docs/tasks/4.8-load-test.md) | 3 |
| [R-RUN-16](spec.md#r-run-16) Развёртывание | [US-RUN-06](../../../../../docs/stories/agent-runner.md#us-run-06) | [R&D: Kubernetes](../../../../../docs/rnd/kubernetes-runtime.md) · [D15](../../../../../openspec/changes/define-agent-platform/design.md) | [4.6](../../../../../docs/tasks/4.6-k8s-helm-ingress.md) | 3 |
| [R-RUN-17](spec.md#r-run-17) Манифест рабочего пространства | [US-SBX-06](../../../../../docs/stories/sandbox.md#us-sbx-06) | [D18](../../../../../openspec/changes/define-agent-platform/design.md) · [R&D: рабочее пространство](../../../../../docs/rnd/agent-workspace.md) | [2.1](../../../../../docs/tasks/2.1-runner-external.md) | 3 |
