# Tasks

← [proposal](proposal.md) · [спека](specs/icplan-integration/spec.md) · [ROADMAP](../../../docs/ROADMAP.md)

Задачи ROADMAP, закрывающие требования `R-ICP-*`; файл собирается из ROADMAP (`html-view/tasksmd.py`). Общий список — [define-agent-platform](../define-agent-platform/tasks.md).

## 2. Агент работает из ICPlan

- [ ] 2.1 Agent Runner как внешний раннер ICPlan: Первая связь с ICPlan: задачи из очереди ICPlan выполняет наш Harness, а не CLI на машине оператора. Требования: R-ICP-01, R-ICP-02, R-ICP-03, R-ICP-04, R-ICP-07, R-ICP-09 и др.. Подробно: [docs/tasks/2.1-runner-external.md](../../../docs/tasks/2.1-runner-external.md)
- [ ] 2.3 Конфиг агента из ICPlan + YAML: Пользователь настраивает агента в UI ICPlan; Harness должен брать модель, инструкцию и тулы оттуда, а недостающее (лимиты, approve) — из YAML до появления Platform module. Требования: R-ICP-08, R-REG-02, R-REG-06, R-REG-07, R-REG-08, R-REG-09 и др.. Подробно: [docs/tasks/2.3-config-from-icplan.md](../../../docs/tasks/2.3-config-from-icplan.md)
- [ ] 2.6 E2E: от задачи до итога: Фиксирует, что этап 2 работает целиком и не ломается при следующих доработках. Требования: R-ICP-13, R-RUN-08, R-RUN-14. Подробно: [docs/tasks/2.6-e2e-icplan.md](../../../docs/tasks/2.6-e2e-icplan.md)
- [ ] 2.7 Планировщик запусков (слоты, режимы): Агентов несколько, они делят модели и могут работать параллельно или только по одному. Требования: R-ICP-03, R-RUN-02, R-RUN-03, R-RUN-04, R-RUN-05, R-RUN-06 и др.. Подробно: [docs/tasks/2.7-runner-scheduler.md](../../../docs/tasks/2.7-runner-scheduler.md)

## 3. ICPlan ведёт процесс

- [ ] 3.3 События запуска и чат запуска в задаче: Пользователь хочет видеть в задаче, что делает агент и почему: реплики, рассуждения, действия, вопросы и итог — чат запуска ([D21](../../openspec/changes/define-agent-platform/design.md), [R&D](../rnd/run-view.md), [поток](../stories/icplan.md#agent-feed)). Требования: R-ICP-04, R-GRD-16, R-OBS-01, R-OBS-02, R-OBS-03, R-OBS-04 и др.. Подробно: [docs/tasks/3.3-run-events-timeline.md](../../../docs/tasks/3.3-run-events-timeline.md)
- [ ] 3.4 ICPlan: approve в задаче: Пауза на approve из 1.5 должна управляться из задачи ICPlan, иначе опасные действия блокируют работу. Требования: R-ICP-05, R-ICP-06, R-GRD-08. Подробно: [docs/tasks/3.4-icplan-approve-ui.md](../../../docs/tasks/3.4-icplan-approve-ui.md)
- [ ] 3.8 Чат с агентом, указания во время работы, выключение агента: Пользователь поправляет агента без перезапуска, администратор проверяет агента в чате до подключения к процессу и временно выключает агента. Требования: R-ICP-16, R-ICP-17, R-ICP-18, R-HRN-16. Подробно: [docs/tasks/3.8-agent-chat-control.md](../../../docs/tasks/3.8-agent-chat-control.md)

## 4. После MVP

- [ ] 4.6 Kubernetes: k3s, Helm, namespaces, Traefik, сетевые политики: Платформа должна разворачиваться воспроизводимо на сервере: кластер, чарты, вход по HTTPS, изоляция namespaces, секреты вне git. Требования: R-ICP-15, R-HRN-15, R-MEM-14, R-REG-12, R-RUN-16, R-SBX-13 и др.. Подробно: [docs/tasks/4.6-k8s-helm-ingress.md](../../../docs/tasks/4.6-k8s-helm-ingress.md)
- [ ] 4.8 Нагрузочный тест и подтверждение профиля: Профиль нагрузки — гипотеза; без замера нельзя выпускать в продуктив и настраивать лимиты. Требования: R-ICP-14, R-HRN-14, R-MEM-13, R-REG-11, R-RUN-15, R-SBX-12 и др.. Подробно: [docs/tasks/4.8-load-test.md](../../../docs/tasks/4.8-load-test.md)

## Архивация

Change архивируется (`openspec archive`) после реализации и приёмки его задач — тогда спеки становятся действующими в `openspec/specs/` ([правило](../../../docs/rules/change-process.md#archive)).
