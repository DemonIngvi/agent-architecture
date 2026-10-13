# Tasks

← [proposal](proposal.md) · [ROADMAP](../../../docs/ROADMAP.md) · [сводная таблица](../../../docs/TASKS.md)

Задачи по этапам ROADMAP; файл собирается из ROADMAP (`html-view/tasksmd.py`). Подробности, INVEST, оценки и приёмка — в документе задачи. Задачи процесса ICPlan детализированы также в [icplan-agent-autopickup](../icplan-agent-autopickup/tasks.md).

## 1. Агент работает сам

- [ ] 1.1 Mock-LLM и LiteLLM: Harness нужно разрабатывать и тестировать без платного провайдера и без случайности ответов. Требования: R-LLM-01, R-LLM-02, R-LLM-04, R-LLM-07, R-LLM-08, R-LLM-09 и др.. Подробно: [docs/tasks/1.1-mock-llm-litellm.md](../../../docs/tasks/1.1-mock-llm-litellm.md)
- [ ] 1.2 Формат определения агента (YAML): Формат YAML — контракт между ICPlan, Harness и экспортом/импортом. Требования: R-HRN-10, R-REG-01, R-REG-02, R-REG-05. Подробно: [docs/tasks/1.2-agent-definition-yaml.md](../../../docs/tasks/1.2-agent-definition-yaml.md)
- [ ] 1.3 Harness: ядро на LangGraph: Ядро MVP: агентский цикл, собранный из конфига. Требования: R-HRN-01, R-HRN-02, R-HRN-03, R-HRN-06, R-HRN-18, R-HRN-10 и др.. Подробно: [docs/tasks/1.3-harness-core.md](../../../docs/tasks/1.3-harness-core.md)
- [ ] 1.4 Harness: MCP и тулы: Без тулов агент только отвечает текстом. Требования: R-HRN-17, R-HRN-12, R-HRN-13, R-MCP-01, R-MCP-02, R-MCP-03 и др.. Подробно: [docs/tasks/1.4-harness-mcp-tools.md](../../../docs/tasks/1.4-harness-mcp-tools.md)
- [ ] 1.5 Harness: hooks и пауза на approve: Approve опасных действий — обязательное требование; механизм паузы и возобновления нужен и для вопросов пользователю. Требования: R-HRN-04, R-HRN-05, R-HRN-11, R-GRD-03. Подробно: [docs/tasks/1.5-harness-hooks-approve.md](../../../docs/tasks/1.5-harness-hooks-approve.md)
- [ ] 1.6 Harness: лимиты, завершение, контекст: Без лимитов агент может зациклиться и тратить токены; без управления контекстом длинные задачи падают на переполнении окна. Требования: R-HRN-07, R-HRN-08, R-HRN-09, R-HRN-13, R-GRD-09, R-GRD-10 и др.. Подробно: [docs/tasks/1.6-harness-limits-context.md](../../../docs/tasks/1.6-harness-limits-context.md)
- [x] 1.7 ~~закрыта~~ — закрыта. Подробно: [docs/tasks/1.7-dev-ui.md](../../../docs/tasks/1.7-dev-ui.md)

## 2. Агент работает из ICPlan

- [ ] 2.1 Agent Runner как внешний раннер ICPlan: Первая связь с ICPlan: задачи из очереди ICPlan выполняет наш Harness, а не CLI на машине оператора. Требования: R-ICP-01, R-ICP-02, R-ICP-03, R-ICP-04, R-ICP-07, R-ICP-09 и др.. Подробно: [docs/tasks/2.1-runner-external.md](../../../docs/tasks/2.1-runner-external.md)
- [ ] 2.2 Harness в Docker-контейнере на запуск: Изоляция запусков с первого дня интеграции; тёплый пул — оптимизация позже (4.1). Требования: R-RUN-10, R-SBX-01, R-SBX-03, R-SBX-05, R-SBX-14, R-SBX-08 и др.. Подробно: [docs/tasks/2.2-sandbox-docker-oneshot.md](../../../docs/tasks/2.2-sandbox-docker-oneshot.md)
- [ ] 2.3 Конфиг агента из ICPlan + YAML: Пользователь настраивает агента в UI ICPlan; Harness должен брать модель, инструкцию и тулы оттуда, а недостающее (лимиты, approve) — из YAML до появления Platform module. Требования: R-ICP-08, R-REG-02, R-REG-06, R-REG-07, R-REG-08, R-REG-09 и др.. Подробно: [docs/tasks/2.3-config-from-icplan.md](../../../docs/tasks/2.3-config-from-icplan.md)
- [ ] 2.4 MCP `itsaplan-core` для агента: Агент должен читать задачу, писать комментарии и менять статус — иначе процесс между этапами не работает. Требования: R-MCP-04, R-MCP-13, R-MCP-09. Подробно: [docs/tasks/2.4-mcp-itsaplan-core.md](../../../docs/tasks/2.4-mcp-itsaplan-core.md)
- [ ] 2.5 Память M1–M3: контекст, управление: Агент следующего этапа должен продолжать работу, а не начинать с нуля. Требования: R-MEM-01, R-MEM-02, R-MEM-04, R-MEM-05, R-MEM-07, R-MEM-08 и др.. Подробно: [docs/tasks/2.5-memory-m2-m3.md](../../../docs/tasks/2.5-memory-m2-m3.md)
- [ ] 2.6 E2E: от задачи до итога: Фиксирует, что этап 2 работает целиком и не ломается при следующих доработках. Требования: R-ICP-13, R-RUN-08, R-RUN-14. Подробно: [docs/tasks/2.6-e2e-icplan.md](../../../docs/tasks/2.6-e2e-icplan.md)
- [ ] 2.7 Планировщик запусков (слоты, режимы): Агентов несколько, они делят модели и могут работать параллельно или только по одному. Требования: R-ICP-03, R-RUN-02, R-RUN-03, R-RUN-04, R-RUN-05, R-RUN-06 и др.. Подробно: [docs/tasks/2.7-runner-scheduler.md](../../../docs/tasks/2.7-runner-scheduler.md)
- [ ] 2.8 Общий резолвер конфигурации L0–L3: Пять модулей получают параметры запуска через `RunBundle` от Runner. Требования: R-HRN-10, R-MEM-09, R-RUN-11, R-SBX-08, R-MCP-07. Подробно: [docs/tasks/2.8-config-storage-interfaces-fmea.md](../../../docs/tasks/2.8-config-storage-interfaces-fmea.md)

## 3. ICPlan ведёт процесс

- [ ] 3.1 ICPlan: процесс типа задачи и агент шага: Тип задачи задаёт процесс, шаг процесса — колонку и агента. Требования: R-AP-01, R-AP-02, R-AP-04, R-AP-05, R-AP-08, R-AP-15 и др.. Подробно: [docs/tasks/3.1-icplan-process-step-agent.md](../../../docs/tasks/3.1-icplan-process-step-agent.md)
- [ ] 3.2 ICPlan: передача между агентами: Следующий агент должен получать итог предыдущего, а пользователь — понимать, почему агент начал работу. Требования: R-AP-06, R-AP-07, R-HRN-08. Подробно: [docs/tasks/3.2-icplan-handoff.md](../../../docs/tasks/3.2-icplan-handoff.md)
- [ ] 3.3 События запуска и чат запуска в задаче: Пользователь хочет видеть в задаче, что делает агент и почему: реплики, рассуждения, действия, вопросы и итог — чат запуска (D21, R&D, поток). Требования: R-ICP-04, R-GRD-16, R-OBS-01, R-OBS-02, R-OBS-03, R-OBS-04 и др.. Подробно: [docs/tasks/3.3-run-events-timeline.md](../../../docs/tasks/3.3-run-events-timeline.md)
- [ ] 3.4 ICPlan: approve в задаче: Пауза на approve из 1.5 должна управляться из задачи ICPlan, иначе опасные действия блокируют работу. Требования: R-ICP-05, R-ICP-06, R-GRD-08. Подробно: [docs/tasks/3.4-icplan-approve-ui.md](../../../docs/tasks/3.4-icplan-approve-ui.md)
- [ ] 3.5 ICPlan: эффект Действия, затраты: Расширение автоматизации (произвольные условия Действий) и видимость стоимости задачи. Требования: R-LLM-02, R-OBS-05, R-AP-03. Подробно: [docs/tasks/3.5-icplan-type-actions-cost.md](../../../docs/tasks/3.5-icplan-type-actions-cost.md)
- [ ] 3.6 ICPlan: переходы по итогу запуска и очередь агента: Задача сама проходит процесс: переход делает ICPlan по итогу запуска, а не агент по своему усмотрению. Требования: R-AP-16, R-AP-17. Подробно: [docs/tasks/3.6-icplan-process-engine.md](../../../docs/tasks/3.6-icplan-process-engine.md)
- [ ] 3.7 ICPlan: управление ходом задачи: Пользователь управляет ходом задачи: проверяет результат перед переходом, возвращает с заметкой, останавливает и возобновляет процесс, повторяет шаг. Требования: R-AP-18, R-AP-19, R-AP-20, R-AP-21, R-AP-22. Подробно: [docs/tasks/3.7-icplan-task-control.md](../../../docs/tasks/3.7-icplan-task-control.md)
- [ ] 3.8 Чат с агентом, указания во время работы, выключение агента: Пользователь поправляет агента без перезапуска, администратор проверяет агента в чате до подключения к процессу и временно выключает агента. Требования: R-ICP-16, R-ICP-17, R-ICP-18, R-HRN-16. Подробно: [docs/tasks/3.8-agent-chat-control.md](../../../docs/tasks/3.8-agent-chat-control.md)
- [ ] 3.9 Сводка задач с агентами и статистика агентов: Пользователь видит, что выполняется, сколько это идёт и стоит; администратор и владелец продукта — какой агент полезен. Требования: R-OBS-13. Подробно: [docs/tasks/3.9-agent-summary-stats.md](../../../docs/tasks/3.9-agent-summary-stats.md)

## 4. После MVP

- [ ] 4.1 Тёплый пул sandbox: Убрать задержку старта контейнера, не жертвуя изоляцией. Требования: R-SBX-02, R-SBX-11. Подробно: [docs/tasks/4.1-sandbox-warm-pool.md](../../../docs/tasks/4.1-sandbox-warm-pool.md)
- [ ] 4.2 Egress-прокси и доступ к репозиториям: Агенту-разработчику нужен код, но без утечки секретов и без доступа куда не положено. Требования: R-SBX-03, R-SBX-04, R-SBX-06, R-SBX-07, R-SBX-14, R-SBX-10 и др.. Подробно: [docs/tasks/4.2-egress-repo-access.md](../../../docs/tasks/4.2-egress-repo-access.md)
- [ ] 4.3 Guardrails: OPA для G1/G2 и включение точек: Правила безопасности в одном месте, проверяемые и отключаемые конфигом. Требования: R-GRD-01, R-GRD-02, R-GRD-03, R-GRD-06, R-GRD-07, R-GRD-08 и др.. Подробно: [docs/tasks/4.3-guardrails-opa.md](../../../docs/tasks/4.3-guardrails-opa.md)
- [ ] 4.4 Platform module в ICPlan: Перенести настройки из YAML в ICPlan: бюджеты, профили, данные guardrails, версии — с UI. Требования: R-REG-03, R-REG-04, R-REG-08, R-CP-01, R-CP-02, R-CP-03 и др.. Подробно: [docs/tasks/4.4-platform-module.md](../../../docs/tasks/4.4-platform-module.md)
- [ ] 4.5 LiteLLM: бюджеты, fallback, G4: Контроль трат и устойчивость к сбоям провайдера; базовая защита содержимого. Требования: R-GRD-05, R-GRD-11, R-GRD-14, R-LLM-03, R-LLM-05, R-LLM-06 и др.. Подробно: [docs/tasks/4.5-litellm-budgets-fallback-g4.md](../../../docs/tasks/4.5-litellm-budgets-fallback-g4.md)
- [ ] 4.6 Kubernetes: k3s, Helm, namespaces, Traefik, сетевые политики: Платформа должна разворачиваться воспроизводимо на сервере: кластер, чарты, вход по HTTPS, изоляция namespaces, секреты вне git. Требования: R-ICP-15, R-HRN-15, R-MEM-14, R-REG-12, R-RUN-16, R-SBX-13 и др.. Подробно: [docs/tasks/4.6-k8s-helm-ingress.md](../../../docs/tasks/4.6-k8s-helm-ingress.md)
- [ ] 4.7 Postgres (CloudNativePG), PgBouncer, RustFS, бэкап вне узла: Одна СУБД обслуживает ICPlan, платформу и LiteLLM — нужны пул соединений, бэкапы вне узла и проверка восстановления (риск X5 ревью). Требования: R-INF-06, R-INF-07, R-INF-08, R-INF-14, R-INF-16, R-ICP-19. Подробно: [docs/tasks/4.7-postgres-storage-backup.md](../../../docs/tasks/4.7-postgres-storage-backup.md)
- [ ] 4.8 Нагрузочный тест и подтверждение профиля: Профиль нагрузки — гипотеза; без замера нельзя выпускать в продуктив и настраивать лимиты. Требования: R-ICP-14, R-HRN-14, R-MEM-13, R-REG-11, R-RUN-15, R-SBX-12 и др.. Подробно: [docs/tasks/4.8-load-test.md](../../../docs/tasks/4.8-load-test.md)

## Архивация

Change архивируется (`openspec archive`) после реализации и приёмки его задач — тогда спеки становятся действующими в `openspec/specs/` ([правило](../../../docs/rules/change-process.md#archive)).
