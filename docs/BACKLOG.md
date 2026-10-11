# Дальний бэклог и техдолг

← [README](../README.md) · [architecture.md](../architecture.md)

Не в MVP. Компоненты учтены в архитектуре, работа по ним — после MVP.

| Тема | Что | Почему отложено | Основа |
|---|---|---|---|
| Метрики и логи | Prometheus, Grafana, Loki — развёрнуты в `itsaplan-platform`, остаются пустыми | Метриками сейчас не занимаемся, есть другие ресурсы | [architecture.md → Observability](../architecture.md) |
| Langfuse / Phoenix | LLM-трейсы, evals, анализ промптов; события — экспортом OTel GenAI (соответствие в каталоге API) | Тяжёлый self-host (Langfuse: ClickHouse, Redis, S3); в MVP хватает таблицы событий; выбор — прототипом | [design D12](../openspec/changes/define-agent-platform/design.md) |
| RAG | Индексация документов, `search_knowledge`, M4; pgvector в той же Postgres; гибридный поиск (полнотекстовый + векторы), контекст документа во фрагменте, переранжирование ([R&D RAG](rnd/rag.md#e6)); код — поиском по файлам | Корпус пока помещается в навигацию по документам | [design D13](../openspec/changes/define-agent-platform/design.md) |
| A2A | Делегирование между агентами | Нет потребности; процесс ведёт ICPlan | Проект AI-агент: фаза 4 |
| web-research MCP | Выход агентов в интернет | Отдельная зона риска, нужна своя политика | [architecture.md → MCP-серверы](../architecture.md) |
| Админ-MCP | `llmproxy-admin`, `guardrails-admin`, `rag-admin` | Управление пока через UI ICPlan | [tool-integration](../openspec/changes/define-agent-platform/specs/tool-integration/spec.md) |
| CI/CD, SSDLC | Gitea Actions, ArgoCD, SonarQube, ZAP, Trivy, k6 | Сначала решаем, что и как деплоим и проверяем | Проект AI-агент: `platform/technical/deployment/` |
| Функции для людей из Plane | Сравнить циклы, модули, страницы Plane с функциями ICPlan по историям; недостающее — в истории и задачи форка | Не влияет на выбор трекера; ядро — агентная часть (П1–П3) | [R&D трекера, Э8](rnd/tracker-choice.md#e8) |
| «Умное» подтверждение | Вспомогательная модель оценивает риск действия; безопасное проходит, спорное — к человеку (как `approvals.mode: smart` в Hermes) | Нужна оценка ложных пропусков; сейчас подтверждение по списку `approval.tools` | [R&D фреймворка, Э6](rnd/harness-framework.md#e6) |
| Справедливая доля проектов | Порядок ждущих запусков с учётом истории потребления проекта (как admission fair sharing в Kueue) | Один проект и `aging_s` достаточно для MVP | [R&D Runner, Э6](rnd/runner-and-scheduling.md#e6) |
| M4: факты агентов | Движок M4 — Mem0 или LangMem поверх pgvector, выбор прототипом; функции: разрешение противоречий (Mem0), срок действия факта (Graphiti), маскирование при записи | MVP закрыт M3 + M2; факты нужны позже | [R&D памяти, Э6](rnd/memory-model.md#e6) |
| A/B-варианты моделей и промптов | Доля трафика агента на вариант модели или промпта, сравнение по evals и вердиктам (как в TensorZero) | Нужны evals и достаточный поток запусков | [R&D шлюза, Э6](rnd/llm-gateway.md#e6) |
| Детекторы содержания для G4 | PromptGuard 2 (22M) — детектор инъекций в хуке LiteLLM; AlignmentCheck — аудит трассы запуска на подмену цели (LlamaFirewall) | G4 выключен по умолчанию; AlignmentCheck экспериментальный | [R&D guardrails, Э6](rnd/guardrails-engine.md#e6) |
| Исполнение кода поверх MCP | Тулы как код в sandbox, загрузка только нужных определений (до −98,7% токенов, Anthropic) | Вызовы из кода обходят G2 на тул; вернуться после выноса проверки в MCP-шлюз (Q-MCP-01) | [R&D MCP, Э6](rnd/mcp-vs-direct.md#e6) |
| Агент из файла в репозитории | Импорт определения агента из файла Markdown + YAML в репозитории проекта (как `.claude/agents`, `.github/agents`) в новую версию; БД остаётся источником правды; сверка полей с Agent File (Letta) | Агентов создают администраторы в интерфейсе | [R&D конфигурации, Э6](rnd/config-storage.md#e6) |
| Зависимости задач | Шаг процесса задачи стартует, когда закрыты родительские задачи (как parent → child в Hermes Kanban) | Нет историй с порядком между задачами | [R&D автоподхвата, Э6](rnd/autopickup-rules.md#e6) |
| Предупреждение агенту перед остановкой | На пороге повтора N — сообщение агенту «ты повторяешься», остановка на 2N (как пороги 3 и 6 в OpenClaw) | Сначала уточнить правило цикла (R-GRD-09) | [R&D защиты от разгона, Э6](rnd/runaway-protection.md#e6) |
| Ленивая загрузка тулов и скиллов | Поиск тулов вместо полного списка, если описания тулов > 10% окна; краткое описание скилла в промпте, инструкции — по запросу (Agent Skills) | Allowlist агента по умолчанию минимальный — порог на MVP не достигается | [R&D MCP, Э6](rnd/mcp-vs-direct.md#e6) |
