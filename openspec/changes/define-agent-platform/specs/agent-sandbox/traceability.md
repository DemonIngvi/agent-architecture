# agent-sandbox — трассировка требований (RTM)

← [spec.md](spec.md) · [интерфейсы и отказы](interfaces.md) · [правила](../../../../../docs/rules/spec-criteria.md)

Вверх — к исследованию и решению, вниз — к задаче реализации (ISO/IEC/IEEE 29148).

| Требование | User Story (вверх) | Обоснование (вверх) | Задача (вниз) | Сценариев |
|---|---|---|---|---|
| [R-SBX-08](spec.md#r-sbx-08) Конфигурация модуля | техническое | [параметры с обоснованием](interfaces.md) · [виды спек](../../../../../docs/rules/spec-kinds.md) | [2.2](../../../../../docs/tasks/2.2-sandbox-docker-oneshot.md), [2.8](../../../../../docs/tasks/2.8-config-storage-interfaces-fmea.md) | 3 |
| [R-SBX-09](spec.md#r-sbx-09) Хранилища данных | техническое | [R&D: СУБД](../../../../../docs/rnd/data-stores.md) · [D15](../../../../../openspec/changes/define-agent-platform/design.md) | [2.2](../../../../../docs/tasks/2.2-sandbox-docker-oneshot.md) | 3 |
| [R-SBX-10](spec.md#r-sbx-10) Интерфейсы обмена | техническое | [интерфейсы](interfaces.md) · [типы данных](../../../../../docs/flows/data-types.md) | [2.2](../../../../../docs/tasks/2.2-sandbox-docker-oneshot.md), [4.2](../../../../../docs/tasks/4.2-egress-repo-access.md) | 3 |
| [R-SBX-11](spec.md#r-sbx-11) Поведение при отказах зависимостей | техническое | [FMEA](interfaces.md) · [R&D: защита от сбоев](../../../../../docs/rnd/runaway-protection.md) | [2.2](../../../../../docs/tasks/2.2-sandbox-docker-oneshot.md), [4.1](../../../../../docs/tasks/4.1-sandbox-warm-pool.md) | 4 |
| [R-SBX-12](spec.md#r-sbx-12) Нагрузка и производительность | техническое | [R&D: профиль нагрузки](../../../../../docs/rnd/load-profile.md) · [D16](../../../../../openspec/changes/define-agent-platform/design.md) | [4.8](../../../../../docs/tasks/4.8-load-test.md) | 3 |
| [R-SBX-13](spec.md#r-sbx-13) Развёртывание | техническое | [R&D: Kubernetes](../../../../../docs/rnd/kubernetes-runtime.md) · [D15](../../../../../openspec/changes/define-agent-platform/design.md) | [4.6](../../../../../docs/tasks/4.6-k8s-helm-ingress.md) | 3 |
| [R-SBX-14](spec.md#r-sbx-14) Подключение рабочего пространства по манифесту | [US-SBX-05](../../../../../docs/stories/sandbox.md#us-sbx-05), [US-SBX-07](../../../../../docs/stories/sandbox.md#us-sbx-07) | [D18](../../../../../openspec/changes/define-agent-platform/design.md) · [R&D: рабочее пространство](../../../../../docs/rnd/agent-workspace.md) | [2.2](../../../../../docs/tasks/2.2-sandbox-docker-oneshot.md), [4.2](../../../../../docs/tasks/4.2-egress-repo-access.md) | 3 |
