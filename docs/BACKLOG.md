# Дальний бэклог и техдолг

← [README](../README.md) · [architecture.md](../architecture.md)

Не в MVP. Компоненты учтены в архитектуре, работа по ним — после MVP.

| Тема | Что | Почему отложено | Основа |
|---|---|---|---|
| Метрики и логи | Prometheus, Grafana, Loki — развёрнуты в `itsaplan-platform`, остаются пустыми | Метриками сейчас не занимаемся, есть другие ресурсы | [architecture.md → Observability](../architecture.md) |
| Langfuse | LLM-трейсы, evals, анализ промптов | Тяжёлый self-host; в MVP хватает таблицы событий запуска | [design D12](../openspec/changes/define-agent-platform/design.md) |
| RAG | Индексация документов и кода, `search_knowledge`, M4 | Корпус пока помещается в навигацию по документам | [design D13](../openspec/changes/define-agent-platform/design.md) |
| A2A | Делегирование между агентами | Нет потребности; процесс ведёт ICPlan | Проект AI-агент: фаза 4 |
| web-research MCP | Выход агентов в интернет | Отдельная зона риска, нужна своя политика | [architecture.md → MCP-серверы](../architecture.md) |
| Админ-MCP | `llmproxy-admin`, `guardrails-admin`, `rag-admin` | Управление пока через UI ICPlan | [tool-integration](../openspec/changes/define-agent-platform/specs/tool-integration/spec.md) |
| CI/CD, SSDLC | Gitea Actions, ArgoCD, SonarQube, ZAP, Trivy, k6 | Сначала решаем, что и как деплоим и проверяем | Проект AI-агент: `platform/technical/deployment/` |
| Функции для людей из Plane | Сравнить циклы, модули, страницы Plane с функциями ICPlan по историям; недостающее — в истории и задачи форка | Не влияет на выбор трекера; ядро — агентная часть (П1–П3) | [R&D трекера, Э8](rnd/tracker-choice.md#e8) |
