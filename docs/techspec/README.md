# Техническая спецификация

← [Справка](../rules/README.md) · [правило и роль](../rules/tech-spec.md)

Как собираются, откуда берутся и как запускаются образы и сервисы каждого компонента. Заполняет **инженер сборки и поставки** по [правилу](../rules/tech-spec.md); значения параметров — в `interfaces.md` спек, здесь — техника поставки.

| Компонент | Что разворачивается |
|---|---|
| [ICPlan (форк)](icplan.md) | web, api, worker, bot форка ICPlan с доработками платформы (модуль Platform, автоподхват, протокол раннера) |
| [Platform module](platform-module.md) | модуль внутри api форка ICPlan: настройки агентов, бюджеты, профили, политики |
| [Agent Runner](agent-runner.md) | Go-сервис: забирает запуски из ICPlan, планирует слоты, поднимает sandbox, связывает с Harness |
| [Sandbox](sandbox.md) | одноразовый контейнер запуска на образе Harness; тёплый пул; сеть только через egress-прокси |
| [Harness](harness.md) | Python-процесс агентского цикла (LangGraph) внутри sandbox |
| [Memory](memory.md) | Memory API: чтение M1–M3, запись M3 с проверками, очистка по срокам |
| [MCP / Tools](mcp-tools.md) | MCP-серверы: `itsaplan-core` в api ICPlan; внешние — отдельные образы; клиент MCP — в Harness |
| [Guardrails](guardrails.md) | OPA рядом с Runner и Harness; правила Rego из git; данные из Platform module |
| [LiteLLM gateway](llm-gateway.md) | LiteLLM Proxy: алиасы, бюджеты, учёт; mock-LLM для разработки |
| [Observability](observability.md) | в MVP — без своего сервиса: события в БД ICPlan, затраты из LiteLLM, сводка в ICPlan |
| [Инфраструктура](infrastructure.md) | k3s на одном узле, Helm-чарты, Traefik, CloudNativePG + PgBouncer, RustFS, бэкапы вне площадки |
