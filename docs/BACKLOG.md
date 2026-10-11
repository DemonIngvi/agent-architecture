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
| «Умное» подтверждение | Вспомогательная модель оценивает риск действия; безопасное проходит, спорное — к человеку (как `approvals.mode: smart` в Hermes) | Нужна оценка ложных пропусков; сейчас подтверждение по списку `approval.tools` | [R&D фреймворка, Э6](rnd/harness-framework.md#e6) |
| Справедливая доля проектов | Порядок ждущих запусков с учётом истории потребления проекта (как admission fair sharing в Kueue) | Один проект и `aging_s` достаточно для MVP | [R&D Runner, Э6](rnd/runner-and-scheduling.md#e6) |
| M4: факты агентов | Движок M4 — Mem0 или LangMem поверх pgvector, выбор прототипом; функции: разрешение противоречий (Mem0), срок действия факта (Graphiti), маскирование при записи | MVP закрыт M3 + M2; факты нужны позже | [R&D памяти, Э6](rnd/memory-model.md#e6) |
| A/B-варианты моделей и промптов | Доля трафика агента на вариант модели или промпта, сравнение по evals и вердиктам (как в TensorZero) | Нужны evals и достаточный поток запусков | [R&D шлюза, Э6](rnd/llm-gateway.md#e6) |
