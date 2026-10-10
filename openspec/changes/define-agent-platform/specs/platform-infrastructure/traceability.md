# platform-infrastructure — трассировка требований (RTM)

← [spec.md](spec.md) · [интерфейсы и отказы](interfaces.md) · [правила](../../../../../docs/rules/spec-criteria.md)

Вверх — к исследованию и решению, вниз — к задаче реализации (ISO/IEC/IEEE 29148).

| Требование | User Story (вверх) | Обоснование (вверх) | Задача (вниз) | Сценариев |
|---|---|---|---|---|
| [R-INF-13](spec.md#r-inf-13) Конфигурация модуля | техническое | [параметры с обоснованием](interfaces.md) · [виды спек](../../../../../docs/rules/spec-kinds.md) | [4.6](../../../../../docs/tasks/4.6-k8s-helm-ingress.md) | 3 |
| [R-INF-14](spec.md#r-inf-14) Хранилища данных | техническое | [R&D: СУБД](../../../../../docs/rnd/data-stores.md) · [D15](../../../../../openspec/changes/define-agent-platform/design.md) | [4.7](../../../../../docs/tasks/4.7-postgres-storage-backup.md) | 3 |
| [R-INF-15](spec.md#r-inf-15) Интерфейсы обмена | техническое | [интерфейсы](interfaces.md) · [типы данных](../../../../../docs/flows/data-types.md) | [4.6](../../../../../docs/tasks/4.6-k8s-helm-ingress.md) | 3 |
| [R-INF-16](spec.md#r-inf-16) Поведение при отказах зависимостей | техническое | [FMEA](interfaces.md) · [R&D: защита от сбоев](../../../../../docs/rnd/runaway-protection.md) | [4.7](../../../../../docs/tasks/4.7-postgres-storage-backup.md) | 4 |
| [R-INF-17](spec.md#r-inf-17) Нагрузка и производительность | техническое | [R&D: профиль нагрузки](../../../../../docs/rnd/load-profile.md) · [D16](../../../../../openspec/changes/define-agent-platform/design.md) | [4.8](../../../../../docs/tasks/4.8-load-test.md) | 3 |
| [R-INF-18](spec.md#r-inf-18) Развёртывание | техническое | [R&D: Kubernetes](../../../../../docs/rnd/kubernetes-runtime.md) · [D15](../../../../../openspec/changes/define-agent-platform/design.md) | [4.6](../../../../../docs/tasks/4.6-k8s-helm-ingress.md) | 3 |
