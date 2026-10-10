# Tasks

← [ROADMAP](../../../docs/ROADMAP.md) · [сводная таблица](../../../docs/TASKS.md)

Задачи по этапам ROADMAP. Подробности, INVEST, оценки и открытые вопросы — в документе задачи по ссылке. Задачи ICPlan этапа 3 детализированы также в [icplan-agent-autopickup](../icplan-agent-autopickup/tasks.md).

## 1. Агент работает сам

- [ ] 1.1 Mock-LLM и LiteLLM: Harness нужно разрабатывать и тестировать без платного провайдера и без случайности ответов. Подробно: [docs/tasks/1.1-mock-llm-litellm.md](../../../docs/tasks/1.1-mock-llm-litellm.md)
- [ ] 1.2 Формат определения агента (YAML): Формат YAML — контракт между ICPlan, Harness и экспортом/импортом. Подробно: [docs/tasks/1.2-agent-definition-yaml.md](../../../docs/tasks/1.2-agent-definition-yaml.md)
- [ ] 1.3 Harness: ядро на LangGraph: Ядро MVP: агентский цикл, собранный из конфига. Подробно: [docs/tasks/1.3-harness-core.md](../../../docs/tasks/1.3-harness-core.md)
- [ ] 1.4 Harness: MCP и тулы: Без тулов агент только отвечает текстом. Подробно: [docs/tasks/1.4-harness-mcp-tools.md](../../../docs/tasks/1.4-harness-mcp-tools.md)
- [ ] 1.5 Harness: hooks и пауза на approve: Approve опасных действий — обязательное требование; механизм паузы и возобновления нужен и для вопросов пользователю. Подробно: [docs/tasks/1.5-harness-hooks-approve.md](../../../docs/tasks/1.5-harness-hooks-approve.md)
- [ ] 1.6 Harness: лимиты, завершение, контекст: Без лимитов агент может зациклиться и тратить токены; без управления контекстом длинные задачи падают на переполнении окна. Подробно: [docs/tasks/1.6-harness-limits-context.md](../../../docs/tasks/1.6-harness-limits-context.md)
- [ ] 1.7 UI для прокликивания агента: Нужно видеть работу агента кликами до интеграции с ICPlan: шаги, вызовы тулов, паузы на approve. Подробно: [docs/tasks/1.7-dev-ui.md](../../../docs/tasks/1.7-dev-ui.md)

## 2. Агент работает из ICPlan

- [ ] 2.1 Agent Runner как внешний раннер ICPlan: Первая связь с ICPlan: задачи из очереди ICPlan выполняет наш Harness, а не CLI на машине оператора. Подробно: [docs/tasks/2.1-runner-external.md](../../../docs/tasks/2.1-runner-external.md)
- [ ] 2.2 Harness в Docker-контейнере на запуск: Изоляция запусков с первого дня интеграции; тёплый пул — оптимизация позже (4. Подробно: [docs/tasks/2.2-sandbox-docker-oneshot.md](../../../docs/tasks/2.2-sandbox-docker-oneshot.md)
- [ ] 2.3 Конфиг агента из ICPlan + YAML: Пользователь настраивает агента в UI ICPlan; Harness должен брать модель, инструкцию и тулы оттуда, а недостающее (лимиты, approve) — из YAML до появления Platform module. Подробно: [docs/tasks/2.3-config-from-icplan.md](../../../docs/tasks/2.3-config-from-icplan.md)
- [ ] 2.4 MCP `itsaplan-core` для агента: Агент должен читать задачу, писать комментарии и менять статус — иначе процесс между этапами не работает. Подробно: [docs/tasks/2.4-mcp-itsaplan-core.md](../../../docs/tasks/2.4-mcp-itsaplan-core.md)
- [ ] 2.5 Память M3 и M2 в контекст: Агент следующего этапа должен продолжать работу, а не начинать с нуля. Подробно: [docs/tasks/2.5-memory-m2-m3.md](../../../docs/tasks/2.5-memory-m2-m3.md)
- [ ] 2.6 E2E: от задачи до итога: Фиксирует, что этап 2 работает целиком и не ломается при следующих доработках. Подробно: [docs/tasks/2.6-e2e-icplan.md](../../../docs/tasks/2.6-e2e-icplan.md)

## 3. ICPlan ведёт процесс

- [ ] 3.1 ICPlan: агент-делегат статуса: Процесс «перевёл в статус → агент взял» — ключевая автоматизация, которой сейчас нет. Подробно: [docs/tasks/3.1-icplan-autodelegate-status.md](../../../docs/tasks/3.1-icplan-autodelegate-status.md)
- [ ] 3.2 ICPlan: передача между агентами: Следующий агент должен получать итог предыдущего, а пользователь — понимать, почему агент начал работу. Подробно: [docs/tasks/3.2-icplan-handoff.md](../../../docs/tasks/3.2-icplan-handoff.md)
- [ ] 3.3 События запуска и таймлайн в задаче: Пользователь хочет видеть все этапы выполнения задачи агентом, а не только итог. Подробно: [docs/tasks/3.3-run-events-timeline.md](../../../docs/tasks/3.3-run-events-timeline.md)
- [ ] 3.4 ICPlan: approve в задаче: Пауза на approve из 1. Подробно: [docs/tasks/3.4-icplan-approve-ui.md](../../../docs/tasks/3.4-icplan-approve-ui.md)
- [ ] 3.5 ICPlan: агент типа, эффект Действия, затраты: Расширение автоматизации (типы задач, произвольные условия) и видимость стоимости задачи. Подробно: [docs/tasks/3.5-icplan-type-actions-cost.md](../../../docs/tasks/3.5-icplan-type-actions-cost.md)

## 4. После MVP

- [ ] 4.1 Тёплый пул sandbox: Убрать задержку старта контейнера, не жертвуя изоляцией. Подробно: [docs/tasks/4.1-sandbox-warm-pool.md](../../../docs/tasks/4.1-sandbox-warm-pool.md)
- [ ] 4.2 Egress-прокси и доступ к репозиториям: Агенту-разработчику нужен код, но без утечки секретов и без доступа куда не положено. Подробно: [docs/tasks/4.2-egress-repo-access.md](../../../docs/tasks/4.2-egress-repo-access.md)
- [ ] 4.3 Guardrails: OPA для G1/G2 и включение точек: Правила безопасности в одном месте, проверяемые и отключаемые конфигом. Подробно: [docs/tasks/4.3-guardrails-opa.md](../../../docs/tasks/4.3-guardrails-opa.md)
- [ ] 4.4 Platform module в ICPlan: Перенести настройки из YAML в ICPlan: бюджеты, профили, данные guardrails, версии — с UI. Подробно: [docs/tasks/4.4-platform-module.md](../../../docs/tasks/4.4-platform-module.md)
- [ ] 4.5 LiteLLM: бюджеты, fallback, G4: Контроль трат и устойчивость к сбоям провайдера; базовая защита содержимого. Подробно: [docs/tasks/4.5-litellm-budgets-fallback-g4.md](../../../docs/tasks/4.5-litellm-budgets-fallback-g4.md)

## Workflow follow-up

- Архивировать change после ревью (`/opsx:archive`).
