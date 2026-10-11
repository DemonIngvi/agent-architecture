"""Подкомпоненты (внутренние блоки схем): технология, ключевые параметры, что делает, почему так.

Ключ — (slug компонента, название блока на схеме). Блок с описанием становится ссылкой.
Поля: tech, params [(параметр, значение)], does [..], why, rnd (файл в docs/rnd или "").
"""

SUB = {
    # ---------- ICPlan ----------
    ("icplan", "Task UI"): dict(
        tech="It's a Plan web (Next.js), доработки в форке",
        params=[("Таймлайн запуска", "из таблицы событий (задача 3.3)"), ("Approve", "кнопки в задаче (3.4)"), ("Затраты задачи", "из LiteLLM (3.5)")],
        does=["Доска, статусы, карточка задачи, комментарии, чат агента", "Показывает ход работы агента и итог", "Даёт человеку подтвердить опасное действие"],
        why="Пользователи остаются в привычном трекере; всё про агента видно в задаче.", rnd="tracker-choice.md"),
    ("icplan", "Control Plane UI"): dict(
        tech="It's a Plan web: Команда → ИИ-агенты, Интеграции, Инструменты, Навыки, MCP",
        params=[("Модель агента", "провайдер + модель / алиас"), ("Инструкция", "текст"), ("Проекты", "где работает агент"), ("Тип", "внутренний / внешний")],
        does=["Создание и настройка агентов", "Ключи провайдеров (переводим на LiteLLM)", "Подключение тулов, навыков, MCP"],
        why="UI уже есть — не пишем свою консоль; наши настройки добавляются экранами Platform module.", rnd="tracker-choice.md"),
    ("icplan", "Автоподхват"): dict(
        tech="Доработка форка (D17): тип задачи задаёт процесс; шаг = колонка + агент + переходы по итогу; эффект Действия",
        params=[("Шаг", "колонка + агент + переход при успехе / при неудаче"), ("max_runs", "3"), ("require_review", "проверка человеком"), ("Контракт шага (D20)", "результат, готовность, criteria_approval"), ("Дубли", "один активный запуск на агента и задачу")],
        does=["Задача вошла в шаг → агент шага становится делегатом, запуск в его очереди", "По итогу запуска ICPlan переводит задачу по правилам шага", "Пишет в историю, по какому правилу агент взял задачу"],
        why="Процесс идёт сам, а переход делает трекер, а не агент — правило однозначно.", rnd="autopickup-rules.md"),
    ("icplan", "Registry"): dict(
        tech="Таблицы ICPlan: агенты, тулы, навыки, MCP, ключи",
        params=[("Версии агента", "доработка"), ("Экспорт / импорт", "YAML `agent/v1`"), ("Allowlist репозиториев", "доработка")],
        does=["Хранит определения агентов и их ресурсы", "Отдаёт определение агента Runner и Harness"],
        why="Источник правды — БД ICPlan; git только для ревью через экспорт.", rnd="config-storage.md"),
    ("icplan", "Run Queue + runner API"): dict(
        tech="Очередь `agent_run` + протокол `@itsaplan/runner` (опрос, стрим)",
        params=[("Опрос", "по API-ключу агента"), ("pollIntervalMs", "3000 (у раннера)"), ("Стрим", "ответ и вызовы тулов")],
        does=["Хранит запуски в статусе pending", "Отдаёт запуск внешнему раннеру (наш Agent Runner)", "Принимает стрим ответа и итог"],
        why="Протокол уже есть — Agent Runner подключается к нему, ICPlan почти не меняем.", rnd="runner-and-scheduling.md"),
    ("icplan", "MCP itsaplan-core"): dict(
        tech="MCP-сервер ICPlan (`/mcp`), весь REST API как тулы",
        params=[("Включение", "на проект, по умолчанию выкл"), ("Ключ", "API-ключ агента"), ("Allowlist", "get_issue, add_comment, update_issue…")],
        does=["Агент читает задачу, пишет комментарий, меняет статус", "Доступ к документам проекта (M6)"],
        why="Стандарт MCP: тот же сервер используют и наши агенты, и внешние CLI.", rnd="mcp-vs-direct.md"),
    # ---------- Platform module ----------
    ("platform-module", "API модуля"): dict(
        tech="Модуль форка ICPlan (TypeScript), схема `platform` в Postgres",
        params=[("Права", "роли ICPlan"), ("Валидация", "ссылки и диапазоны"), ("Версии", "каждое изменение — версия")],
        does=["CRUD наших настроек агента", "Отдаёт настройки Runner, LiteLLM, OPA"],
        why="Одна БД и одна авторизация с ICPlan.", rnd="config-storage.md"),
    ("platform-module", "Алиасы LLM"): dict(
        tech="Алиасы LiteLLM, синхронизация из модуля",
        params=[("model_alias", "team-default"), ("fallback", "резервная модель")],
        does=["Связывает агента с моделью через алиас", "Смена модели — без изменения агента"],
        why="Модель меняется в одном месте.", rnd="llm-gateway.md"),
    ("platform-module", "Бюджеты"): dict(
        tech="Бюджеты virtual key LiteLLM + проверка G1 в Runner",
        params=[("budget.run", "1 $"), ("budget.agent_day", "5 $"), ("budget.project_month", "задаётся"), ("Пороги", "80% / 100%")],
        does=["Задаёт лимиты трат агента, проекта, команды", "Отказ до траты, а не после"],
        why="Иерархия бюджетов — стандарт (LiteLLM, облачные биллинги).", rnd="runaway-protection.md"),
    ("platform-module", "Профили sandbox"): dict(
        tech="Профили Sandbox (образ, ресурсы, сеть, пул)",
        params=[("image", "harness:<версия>"), ("resources", "1 CPU / 1 ГБ / 2 ГБ"), ("egress_allow", "только платформа"), ("pool.size", "2")],
        does=["Определяет, что агент может запускать и куда ходить"],
        why="Разным агентам — разная среда без изменения кода.", rnd="sandbox-isolation.md"),
    ("platform-module", "Профили памяти"): dict(
        tech="Профили Memory",
        params=[("read", "M2, M3, M5, M6"), ("write", "M3"), ("m2_last_runs", "3"), ("retention", "M1 30 д, M2 180 д")],
        does=["Какие уровни памяти агент читает и пишет, сколько хранить"],
        why="Баланс преемственности и токенов на агента.", rnd="memory-model.md"),
    ("platform-module", "Данные guardrails"): dict(
        tech="Данные для OPA (bundle data)",
        params=[("tools_allow", "из определения"), ("approval", "тулы с подтверждением"), ("approval_timeout", "24 ч")],
        does=["Что агенту разрешено и что ждёт человека", "Попадает в OPA без изменения Rego"],
        why="Логика — в git (Rego), данные — в БД: стандартное разделение OPA.", rnd="guardrails-engine.md"),
    ("platform-module", "Версии агентов"): dict(
        tech="Таблица версий + экспорт / импорт YAML",
        params=[("Формат", "`agent/v1`"), ("Пин версии", "в запуске можно указать версию")],
        does=["История изменений агента", "Перенос dev → prod", "Ревью через YAML"],
        why="Воспроизводимость запусков и ревью без Config Repo.", rnd="config-storage.md"),
    # ---------- Agent Runner ----------
    ("agent-runner", "Poller"): dict(
        tech="Go, протокол раннера ICPlan",
        params=[("poll_interval_ms", "3000"), ("agents", "ключи обслуживаемых агентов")],
        does=["Опрашивает очередь ICPlan", "Берёт запуск в работу"],
        why="Pull-модель: ICPlan не нужно знать адрес Runner.", rnd="runner-and-scheduling.md"),
    ("agent-runner", "Scheduler"): dict(
        tech="Go + таблица слотов в Postgres (вариант B)",
        params=[("mode", "parallel / sequential"), ("global_max", "4"), ("per_issue", "1"), ("models.<alias>.max", "3"), ("agents.<id>.parallel", "true / false"), ("order", "fifo / priority")],
        does=["Стартует запуск, только когда свободны все слоты: глобальный, агента, модели, задачи", "Держит запуск в `queued` с причиной ожидания", "Общие слоты для нескольких Runner"],
        why="Учитывает общие модели и агентов, которые нельзя параллелить; режим платформы — одной настройкой.", rnd="runner-and-scheduling.md"),
    ("agent-runner", "Admission"): dict(
        tech="OPA (G1)",
        params=[("g1.enabled", "true"), ("Бюджеты", "из Platform module"), ("kill_switch", "агент / платформа")],
        does=["Допуск агента к задаче", "Проверка бюджета до старта", "Отказ — без создания sandbox"],
        why="Дешевле всего остановить трату до запуска.", rnd="guardrails-engine.md"),
    ("agent-runner", "Sandbox claim"): dict(
        tech="SandboxProvider (Docker → K8s)",
        params=[("profile", "из агента"), ("Пустой пул", "создание на лету")],
        does=["Берёт готовый контейнер из тёплого пула", "Передаёт ему задание"],
        why="Старт < 1 с без потери изоляции.", rnd="sandbox-isolation.md"),
    ("agent-runner", "Токены репозиториев"): dict(
        tech="GitHub App / fine-grained token / Gitea token",
        params=[("ttl", "1 ч"), ("access", "read / write"), ("branch_prefix", "agent/<KEY>")],
        does=["Выдаёт короткоживущий токен только на разрешённые репозитории", "Токен подставляет прокси, не env"],
        why="Минимальные права и короткий срок жизни секрета.", rnd="sandbox-isolation.md"),
    ("agent-runner", "MCP-прокси"): dict(
        tech="Go, официальный MCP Go SDK (D19)",
        params=[("Путь", "/runs/:id/mcp/:server"), ("Проверки", "allowlist манифеста, G2 в OPA"), ("Ключи", "Secret по auth.secret_ref")],
        does=["Отдаёт агенту только разрешённые тулы", "Проверяет каждый вызов вне sandbox", "Подставляет учётные данные MCP-сервера"],
        why="Проверка внутри sandbox обходится кодом агента; Runner уже знает манифест, токен и подтверждения.", rnd="mcp-vs-direct.md"),
    ("agent-runner", "Шаг подготовки"): dict(
        tech="Контейнер подготовки в сети sbx-setup (D19)",
        params=[("setup.script", "из каталога проекта"), ("setup.cache_ttl_h", "168"), ("setup.timeout_s", "600")],
        does=["Ставит зависимости проекта до старта агента", "Кэширует по хешу lock-файлов в /workspace/.deps", "Повторяет установку по тулу install_dependencies"],
        why="Агенту нужны зависимости для тестов, а доступ к реестрам — канал утечки; поэтому реестры только у подготовки.", rnd="agent-workspace.md"),
    ("agent-runner", "Run supervisor"): dict(
        tech="Go",
        params=[("timeout_s", "1800"), ("idle_s", "300"), ("retry", "0")],
        does=["Запускает Harness с `RunBundle`", "Следит за таймаутом, простоем, отменой"],
        why="Зависшие запуски не держат слоты.", rnd="runaway-protection.md"),
    ("agent-runner", "Event relay"): dict(
        tech="Go, поток `RunEvent`",
        params=[("events.level", "всё"), ("Approve", "пробрасывает `ApprovalDecision`")],
        does=["Передаёт шаги Harness в ICPlan и таблицу событий", "Передаёт решение человека обратно"],
        why="Один канал для таймлайна, approve и аудита.", rnd="observability.md"),
    ("agent-runner", "Finalizer"): dict(
        tech="Go",
        params=[("Итог", "комментарий + вложения"), ("M2", "запись итога"), ("Пул", "destroy + долив")],
        does=["Пишет итог в задачу", "Освобождает слоты", "Уничтожает контейнер"],
        why="Каждый запуск заканчивается чисто, без хвостов.", rnd="sandbox-isolation.md"),
    # ---------- Sandbox ----------
    ("sandbox", "Тёплый пул"): dict(
        tech="Docker-контейнеры, заранее запущенные",
        params=[("pool.size", "2 на профиль"), ("Долив", "после каждого destroy")],
        does=["Держит готовые контейнеры", "Отдаёт контейнер запуску за доли секунды"],
        why="Подход E2B, Copilot agent: скорость без потери изоляции.", rnd="sandbox-isolation.md"),
    ("sandbox", "SandboxProvider"): dict(
        tech="Интерфейс create / claim / exec / destroy; Docker сейчас, K8s позже",
        params=[("provider", "docker"), ("Будущее", "k8s, microVM")],
        does=["Скрывает, где исполняется контейнер"],
        why="Смена Docker → K8s → microVM без изменения Runner.", rnd="sandbox-isolation.md"),
    ("sandbox", "Профиль"): dict(
        tech="Ограничения контейнера",
        params=[("cpu", "1"), ("memory_mb", "1024"), ("disk_mb", "2048"), ("privileged", "нет")],
        does=["Ограничивает ресурсы и права (G3)"],
        why="Агент не съест хост и не выйдет за границы.", rnd="sandbox-isolation.md"),
    ("sandbox", "Credential helper"): dict(
        tech="git credential helper / подстановка прокси",
        params=[("Источник", "токен от Runner"), ("env", "секретов нет")],
        does=["Даёт git доступ к репозиторию без секрета в окружении"],
        why="Агент не видит токен — не может его утечь.", rnd="sandbox-isolation.md"),
    ("sandbox", "Egress-прокси"): dict(
        tech="Squid (D18): allowlist доменов по CONNECT, без расшифровки TLS; две подсети — среда агента и шаг подготовки (D19)",
        params=[("egress_allow", "litellm, memory, opa, git-хост"), ("setup.registries", "только шаг подготовки"), ("Секреты", "внешние хосты — прокси; MCP — Runner")],
        does=["Весь исходящий трафик только через прокси", "Блокирует запрещённые хосты, пишет событие"],
        why="Закрывает утечки и доступ к внутренним сервисам (G3).", rnd="sandbox-isolation.md"),
    # ---------- Harness ----------
    ("harness", "Bootstrap"): dict(
        tech="Python, загрузка `AgentDefinition`",
        params=[("Формат", "`agent/v1`"), ("Источник", "ICPlan + YAML дополнений")],
        does=["Собирает агента: промпт, навыки, тулы, лимиты"],
        why="Агент полностью задаётся конфигом.", rnd="harness-framework.md"),
    ("harness", "Context Manager"): dict(
        tech="Python, узел графа LangGraph",
        params=[("compaction.threshold", "80% окна"), ("Память", "M0 + M2/M3/M5/M6 по профилю")],
        does=["Собирает контекст шага", "Сжимает историю при переполнении", "Подгружает память"],
        why="Длинные задачи не падают на окне модели, токены не тратятся на лишнее.", rnd="memory-model.md"),
    ("harness", "LLM client"): dict(
        tech="OpenAI-совместимый клиент → LiteLLM",
        params=[("model", "алиас агента"), ("max_output_tokens", "4000"), ("metadata", "run_id, issue_key, agent")],
        does=["Вызывает модель только через LiteLLM", "Передаёт метаданные для учёта"],
        why="Одна точка выхода к моделям и учёт затрат по задаче.", rnd="llm-gateway.md"),
    ("harness", "Tool Executor"): dict(
        tech="Адаптер MCP → тулы LangGraph",
        params=[("tools", "allowlist агента (проверяет и Runner)"), ("timeout_s", "30"), ("max_result_kb", "64"), ("MCP", "через прокси Runner")],
        does=["Вызывает тулы MCP и нативные", "Ошибки и таймауты возвращает агенту"],
        why="Стандарт MCP; вызовы идут через MCP-прокси Runner, ключи — у Runner (D19).", rnd="mcp-vs-direct.md"),
    ("harness", "Hooks"): dict(
        tech="Узлы графа before/after llm и tool, on_stop",
        params=[("G2", "OPA"), ("loop.repeat_calls", "3"), ("loop.no_progress_steps", "8")],
        does=["Проверяет каждое действие (G2)", "Ловит зацикливание и аномальный расход"],
        why="Правила применяются на каждом шаге детерминированно.", rnd="runaway-protection.md"),
    ("harness", "Pause / resume"): dict(
        tech="LangGraph `interrupt` + свой checkpointer через API Runner (I12, D18)",
        params=[("approval.tools", "из guardrails"), ("checkpoint.ttl", "7 дней"), ("approval_timeout", "24 ч")],
        does=["Останавливается на approve или вопросе", "Продолжает с того же шага", "Восстанавливается после падения"],
        why="Ключевое преимущество LangGraph перед своим циклом.", rnd="harness-framework.md"),
    ("harness", "Policy / stop"): dict(
        tech="Python",
        params=[("max_steps", "30"), ("timeout_s", "1800"), ("max_tokens", "200 000"), ("circuit.max_errors", "3")],
        does=["Соблюдает лимиты запуска", "Завершает с done / limit / gate_failed / error и частичным итогом (статусы — R-RUN-07)"],
        why="Предсказуемые затраты и время.", rnd="runaway-protection.md"),
    ("harness", "Event stream"): dict(
        tech="Поток `RunEvent`",
        params=[("Типы", "AG-UI: RUN_*, TEXT_MESSAGE_*, REASONING_*, TOOL_CALL_*, CUSTOM (D21)")],
        does=["Отдаёт шаги по мере работы"],
        why="Таймлайн в задаче и аудит.", rnd="observability.md"),
    # ---------- Memory ----------
    ("memory", "Memory API"): dict(
        tech="Сервис над БД ICPlan",
        params=[("Профиль", "read / write / retention"), ("Область", "задача, агент, проект, команда")],
        does=["Проверяет права и области", "Отдаёт память в контекст запуска"],
        why="Агенты не ходят в БД напрямую.", rnd="memory-model.md"),
    ("memory", "M3 задачная"): dict(
        tech="Таблица в БД ICPlan + тул записи",
        params=[("Формат", "done / next / blockers + передача: artifacts, questions, criteriaNext (D20)"), ("Срок", "до закрытия задачи")],
        does=["Агент записывает состояние работы по задаче", "Следующий агент получает его в контексте"],
        why="Самый дешёвый способ преемственности этапов.", rnd="memory-model.md"),
    # ---------- MCP / Tools ----------
    ("mcp-tools", "Правила R1–R7"): dict(
        tech="Архитектурное правило",
        params=[("R2", "шаг решает модель → тул"), ("R3", "нескольким агентам / секрет → MCP"), ("R7", "внутренности → прямой вызов")],
        does=["Определяет, как подключать новую интеграцию"],
        why="Экономит токены и задержку, не теряя переиспользование.", rnd="mcp-vs-direct.md"),
    ("mcp-tools", "itsaplan-core"): dict(
        tech="MCP-сервер ICPlan",
        params=[("tools", "get_issue, add_comment, update_issue"), ("auth", "ключ агента")],
        does=["Задачи, комментарии, статусы, документы"],
        why="Уже есть в ICPlan.", rnd="mcp-vs-direct.md"),
    ("mcp-tools", "git-провайдер"): dict(
        tech="MCP Gitea / GitHub",
        params=[("tools", "branch, commit, pr.create"), ("Токен", "короткоживущий от Runner")],
        does=["Ветки, PR, ревью"],
        why="Агент-разработчик отдаёт код через PR, без прямого push.", rnd="mcp-vs-direct.md"),
    ("mcp-tools", "memory"): dict(
        tech="Нативный тул Harness (R4)",
        params=[("Уровень", "M3")],
        does=["Запись состояния задачи"],
        why="Используется только Harness — MCP не нужен.", rnd="mcp-vs-direct.md"),
    # ---------- Guardrails ----------
    ("guardrails", "OPA"): dict(
        tech="Open Policy Agent v1.21.1 (Apache-2.0)",
        params=[("engine", "opa"), ("on_engine_error", "deny"), ("Rego", "git + opa test"), ("Данные", "Platform module")],
        does=["Решения allow / deny / confirm для G1 и G2", "Журнал решений"],
        why="Правила как код, тесты, аудит; CNCF graduated.", rnd="guardrails-engine.md"),
    ("guardrails", "Rego в git"): dict(
        tech="Rego-политики",
        params=[("Тесты", "opa test в CI"), ("Ревью", "через PR")],
        does=["Логика: что разрешено, что требует подтверждения"],
        why="Безопасник ревьюит политику, а не код сервисов.", rnd="guardrails-engine.md"),
    ("guardrails", "Конфиг деплоя"): dict(
        tech="YAML деплоя",
        params=[("g1…g4.enabled", "g1–g3 вкл, g4 выкл"), ("on_engine_error", "deny")],
        does=["Включает и выключает точки независимо"],
        why="Можно начать без guardrails и включать по мере готовности.", rnd="guardrails-engine.md"),
    # ---------- LiteLLM ----------
    ("llm-gateway", "Virtual keys"): dict(
        tech="LiteLLM virtual keys",
        params=[("Ключ", "на агента"), ("metadata", "run_id, issue_key")],
        does=["Отделяет агентов друг от друга по учёту и лимитам"],
        why="Учёт и бюджет на агента без своего биллинга.", rnd="llm-gateway.md"),
    ("llm-gateway", "Бюджеты, rate limit"): dict(
        tech="LiteLLM budgets, RPM / TPM",
        params=[("max_budget", "из Platform module"), ("rpm", "60"), ("tpm", "по провайдеру")],
        does=["Отклоняет вызов до траты при превышении"],
        why="Жёсткий стоп перерасхода на уровне шлюза (G4).", rnd="runaway-protection.md"),
    ("llm-gateway", "G4 хуки"): dict(
        tech="LiteLLM guardrail hooks pre_call / post_call",
        params=[("enabled", "false"), ("Проверки", "PII, injection, модерация")],
        does=["Маскирует секреты и PII во входе", "Модерирует ответ"],
        why="Весь трафик к модели проходит через одну точку.", rnd="guardrails-engine.md"),
    ("llm-gateway", "Алиасы"): dict(
        tech="LiteLLM model_list",
        params=[("team-default", "→ mock (разработка)"), ("Смена", "одна строка конфига")],
        does=["Связывает алиас с моделью провайдера"],
        why="Смена модели без изменения агентов.", rnd="llm-gateway.md"),
    ("llm-gateway", "Fallback"): dict(
        tech="LiteLLM router fallbacks",
        params=[("fallbacks", "team-default → резервная")],
        does=["При сбое основной модели отвечает резервная"],
        why="Агент работает при недоступности провайдера.", rnd="llm-gateway.md"),
    ("llm-gateway", "Spend log"): dict(
        tech="LiteLLM spend logs (Postgres)",
        params=[("Поля", "ключ, модель, токены, $, metadata")],
        does=["Записывает расход каждого вызова"],
        why="Источник затрат по задаче и агенту.", rnd="observability.md"),
    ("llm-gateway", "mock-LLM"): dict(
        tech="OpenAI-совместимый mock со сценариями (задача 1.1)",
        params=[("Сценарии", "YAML: текст, tool_calls, ошибка, задержка")],
        does=["Отвечает вместо модели при разработке и тестах"],
        why="Не нужен ключ провайдера; тесты детерминированные.", rnd="llm-gateway.md"),
    # ---------- Observability ----------
    ("observability", "События запуска"): dict(
        tech="Таблица `run_event` в БД ICPlan",
        params=[("events.level", "всё"), ("retention_days", "90")],
        does=["Хранит шаги запуска", "Источник таймлайна и аудита"],
        why="Самый дешёвый способ дать таймлайн в MVP.", rnd="observability.md"),
    ("observability", "Агрегаты затрат"): dict(
        tech="Агрегаты из spend log LiteLLM",
        params=[("Разрезы", "запуск, задача, агент, модель, период")],
        does=["Считает затраты для задачи и отчётов"],
        why="Один источник правды по деньгам — LiteLLM.", rnd="observability.md"),
}


# --- infrastructure ---
SUB.update({
    ("infrastructure", "Traefik"): dict(tech="Traefik v3.7 (в составе k3s), MIT", params=[("entrypoints", "web → websecure (HTTPS)"), ("TLS", "ACME / свой сертификат"), ("маршруты", "web, api, /mcp")],
        does=["Принимает внешний трафик по HTTPS", "Маршрутизирует на сервисы ICPlan", "Не публикует админки"], why="Встроен в k3s, ingress-nginx архивирован.", rnd="ingress-and-balancing.md"),
    ("infrastructure", "PgBouncer"): dict(tech="PgBouncer 1.26 (пулер CloudNativePG), ISC", params=[("pool_mode", "transaction"), ("default_pool_size", "30"), ("session-клиенты", "по списку")],
        does=["Держит пул серверных соединений", "Защищает Postgres от роста числа клиентов"], why="Агенты, Runner и LiteLLM множат соединения.", rnd="ingress-and-balancing.md"),
    ("infrastructure", "PostgreSQL 17 + pgvector"): dict(tech="PostgreSQL 17 под CloudNativePG v1.30, образ с pgvector", params=[("БД", "itsaplan, litellm"), ("схемы", "public, platform, harness_ckpt"), ("бэкап", "базовые копии + WAL в S3 вне узла")],
        does=["Хранит данные ICPlan, платформы, LiteLLM, checkpoint"], why="Одна СУБД на всё; оператор даёт бэкап и восстановление.", rnd="data-stores.md"),
    ("infrastructure", "RustFS"): dict(tech="RustFS 1.0 (S3 API), Apache-2.0", params=[("бакет", "planner-attachments"), ("доступ", "ключи сервисов из Secret")],
        does=["Хранит вложения, артефакты, копии"], why="Уже в стеке ICPlan; MinIO архивирован.", rnd="data-stores.md"),
    ("infrastructure", "Резервное хранилище S3 вне узла"): dict(tech="S3-совместимое хранилище вне узла (второй сервер или облако)", params=[("частота", "базовая копия ежедневно, WAL непрерывно"), ("проверка", "раз в месяц")],
        does=["Хранит копии вне узла"], why="Копии на том же диске — не бэкап.", rnd="data-stores.md"),
})
