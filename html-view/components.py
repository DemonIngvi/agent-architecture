"""Компоненты архитектуры для сайта.

Сайт разделён на типы документации (вкладки): Архитектура, Спеки, Задачи, Справка.
Во вкладке «Архитектура» у каждого компонента — блочная схема внутреннего устройства
(BLOCKS), соседние компоненты на ней ведут на их схемы. Спеки и задачи — отдельные вкладки,
на них ведёт панель «Другая документация» внизу страницы компонента.
"""

DAP = "openspec/changes/define-agent-platform"
ICI = "openspec/changes/add-icplan-integration"
AP = "openspec/changes/icplan-agent-autopickup"

# slug, название, статус (done|part|todo), guardrails, описание, связи, спеки [(подпись, путь)], задачи
COMPONENTS = [
    ("icplan", "ICPlan", "part", "",
     "Таск-трекер It's a Plan: доска, процессы, настройка агентов, очередь запусков, UI задачи. Уже есть, дорабатываем.",
     ["agent-runner", "platform-module", "observability"],
     [("Registry — спека", f"{DAP}/specs/agent-registry/spec.md"),
      ("Интеграция — proposal", f"{ICI}/proposal.md"),
      ("Интеграция — спека", f"{ICI}/specs/icplan-integration/spec.md"),
      ("Интеграция — схема и user flow", f"{ICI}/specs/icplan-integration/architecture.md"),
      ("Автоподхват — proposal", f"{AP}/proposal.md"),
      ("Автоподхват — спека", f"{AP}/specs/icplan-agent-autopickup/spec.md"),
      ("Автоподхват — схема", f"{AP}/specs/icplan-agent-autopickup/architecture.md")],
     ["1.2", "2.3", "3.1", "3.2", "3.4", "3.5"]),
    ("platform-module", "Platform module", "todo", "",
     "Модуль ICPlan (своя схема в БД ICPlan): алиасы LLM, бюджеты, профили sandbox и памяти, данные guardrails, версии агентов.",
     ["icplan", "agent-runner", "guardrails", "llm-gateway"],
     [("Спека (control-plane)", f"{DAP}/specs/control-plane/spec.md")],
     ["4.4"]),
    ("agent-runner", "Agent Runner", "todo", "G1",
     "Берёт запуск из очереди ICPlan, выдаёт sandbox из тёплого пула, следит за лимитами, возвращает итог.",
     ["icplan", "sandbox", "platform-module"],
     [("Спека", f"{DAP}/specs/agent-runner/spec.md")],
     ["2.1", "2.6"]),
    ("sandbox", "Sandbox", "todo", "G3",
     "Одноразовый изолированный контейнер из тёплого пула; эфемерный /workspace, egress-прокси, доступ к репозиториям.",
     ["agent-runner", "harness"],
     [("Спека", f"{DAP}/specs/agent-sandbox/spec.md")],
     ["2.2", "4.1", "4.2"]),
    ("harness", "Harness", "todo", "G2",
     "Агентский цикл на LangGraph: контекст → LLM → тулы, hooks, пауза на approve, возобновление, стрим шагов.",
     ["llm-gateway", "mcp-tools", "memory", "sandbox"],
     [("Спека", f"{DAP}/specs/agent-harness/spec.md")],
     ["1.3", "1.4", "1.5", "1.6", "1.7"]),
    ("memory", "Memory", "part", "",
     "Память M0–M6: M1, M2, M5, M6 уже есть в ICPlan; M3 — первой; M4 — вместе с RAG.",
     ["harness", "platform-module"],
     [("Спека", f"{DAP}/specs/agent-memory/spec.md")],
     ["2.5"]),
    ("mcp-tools", "MCP / Tools", "part", "",
     "Тулы и MCP-серверы агента; правила R1–R7: MCP или прямой вызов.",
     ["harness", "icplan"],
     [("Спека", f"{DAP}/specs/tool-integration/spec.md")],
     ["2.4"]),
    ("guardrails", "Guardrails", "todo", "G1–G4",
     "Единая политика: Rego в git, данные в БД ICPlan, OPA для G1/G2; каждая точка включается в конфиге деплоя.",
     ["agent-runner", "harness", "sandbox", "llm-gateway"],
     [("Спека", f"{DAP}/specs/guardrails/spec.md")],
     ["4.3"]),
    ("llm-gateway", "LiteLLM gateway", "part", "G4",
     "Единственный выход к моделям: алиасы, virtual key на агента, лимиты, fallback. Развёрнут, не подключён.",
     ["harness", "observability"],
     [("Спека", f"{DAP}/specs/llm-gateway/spec.md")],
     ["1.1", "4.5"]),
    ("observability", "Observability", "part", "",
     "События запуска → таймлайн в задаче, затраты. Langfuse и метрики — в бэклоге.",
     ["llm-gateway", "icplan"],
     [("Спека", f"{DAP}/specs/observability/spec.md")],
     ["3.3"]),
]

STATUS = {"done": "✅ есть", "part": "⚠️ частично", "todo": "⬜ не начато"}
BY_SLUG = {c[0]: c for c in COMPONENTS}


def B(title, desc="", kind="", st="", g="", to=""):
    """Блок схемы. kind: core | ext (другой компонент, to=slug) | store | user | back (бэклог)."""
    return dict(title=title, desc=desc, kind=kind, st=st, g=g, to=to)


def Z(title, rows, cls="", g="", note=""):
    """Зона (контейнер) с вложенными рядами."""
    return dict(zone=title, rows=rows, cls=cls, g=g, note=note)


# Внутреннее устройство компонентов: ряды блоков сверху вниз; строка — подпись потока между рядами
BLOCKS = {
    "icplan": [
        [B("Пользователь", "задачи, доска, чат", "user"), B("Администратор", "агенты, процесс", "user")],
        "↓ работает с задачами · настраивает ↓",
        Z("ICPlan", [
            [B("Task UI", "доска, статусы, комментарии, чат агента; нужны таймлайн, approve, затраты", "core", "part"),
             B("Control Plane UI", "настройка агента: модель, инструкция, тулы, навыки, MCP, проекты", "core", "done")],
            "↓ статус / делегат задачи · сохранение настроек ↓",
            [B("Автоподхват", "статус / тип / действие → агент-делегат (доработка)", "core", "todo"),
             B("Registry", "агенты, тулы, навыки, MCP, ключи; нужны версии и YAML", "core", "part")],
            "↓ запуск",
            [B("Run Queue + runner API", "очередь запусков, протокол внешнего раннера, стрим", "core", "part"),
             B("MCP itsaplan-core", "весь REST API ICPlan как тулы агента", "core", "done"),
             B("БД ICPlan (Postgres)", "задачи, агенты, запуски, память M1/M2/M3", "store", "done")],
        ], cls="icplan"),
        "↓ запуск из очереди · стрим и итог ↑",
        [B("Agent Runner", "исполняет запуск", "ext", to="agent-runner"),
         B("Platform module", "наши настройки в БД ICPlan", "ext", to="platform-module"),
         B("Observability", "события → таймлайн", "ext", to="observability")],
    ],
    "platform-module": [
        [B("Control Plane UI", "экраны настроек в ICPlan", "ext", to="icplan")],
        "↓ CRUD",
        Z("Platform module (модуль ICPlan)", [
            [B("API модуля", "проверка прав, валидация, версии", "core", "todo")],
            "↓",
            [B("Алиасы LLM", "алиас → модель", "core", "todo"), B("Бюджеты", "лимиты токенов и $ на агента", "core", "todo"),
             B("Профили sandbox", "образ, CPU/RAM, сеть", "core", "todo")],
            [B("Профили памяти", "уровни, области, сроки", "core", "todo"), B("Данные guardrails", "allowlist, лимиты для OPA", "core", "todo"),
             B("Версии агентов", "история, экспорт/импорт YAML", "core", "todo")],
            "↓",
            [B("Схема platform в БД ICPlan", "отдельная схема — проще слияние с upstream", "store", "todo")],
        ], cls="icplan"),
        "↓ читают настройки",
        [B("Agent Runner", "профили, бюджеты (G1)", "ext", to="agent-runner"), B("LiteLLM gateway", "алиасы, virtual keys", "ext", to="llm-gateway"),
         B("Guardrails", "данные правил", "ext", to="guardrails")],
    ],
    "agent-runner": [
        [B("ICPlan · Run Queue", "очередь запусков", "ext", to="icplan")],
        "↓ опрос по ключу агента · стрим и итог ↑",
        Z("Agent Runner", [
            [B("Poller", "забирает запуск из очереди", "core", "todo"), B("Admission", "допуск, бюджет, параллельность, kill switch", "core", "todo", "G1")],
            "↓",
            [B("Sandbox claim", "берёт контейнер из тёплого пула", "core", "todo"), B("Токены репозиториев", "короткоживущие, на запуск", "core", "todo")],
            "↓",
            [B("Run supervisor", "старт Harness, таймаут, отмена", "core", "todo"), B("Event relay", "события Harness → стрим в ICPlan", "core", "todo")],
            "↓",
            [B("Finalizer", "итог в задачу, destroy sandbox", "core", "todo")],
        ], g="G1"),
        "↓",
        [B("Sandbox", "контейнер запуска", "ext", to="sandbox"), B("Platform module", "профили, бюджеты", "ext", to="platform-module"),
         B("Observability", "события запуска", "ext", to="observability")],
    ],
    "sandbox": [
        [B("Agent Runner", "claim / destroy", "ext", to="agent-runner")],
        "↓",
        [B("Тёплый пул", "N готовых контейнеров на профиль", "core", "todo"), B("SandboxProvider", "Docker сейчас · K8s позже", "core", "todo")],
        "↓ один контейнер = один запуск",
        Z("Контейнер запуска", [
            [B("Harness", "агентский цикл", "ext", to="harness"), B("/workspace", "эфемерный, клон репозиториев", "store", "todo")],
            [B("Профиль", "CPU, RAM, диск, без privileged", "core", "todo"), B("Credential helper", "токены git без env", "core", "todo")],
        ], cls="sandbox", g="G3"),
        "↓ весь исходящий трафик",
        [B("Egress-прокси", "allowlist хостов, подстановка секретов", "core", "todo", "G3")],
        "↓",
        [B("LiteLLM gateway", "", "ext", to="llm-gateway"), B("MCP / Tools", "", "ext", to="mcp-tools"), B("Memory", "", "ext", to="memory")],
    ],
    "harness": [
        [B("Agent Runner", "задание + определение агента", "ext", to="agent-runner")],
        "↓",
        Z("Harness (LangGraph)", [
            [B("Bootstrap", "определение агента (YAML / ICPlan), скиллы, лимиты", "core", "todo")],
            "↓",
            [B("Context Manager", "промпт, сжатие истории, M0 + M2/M3", "core", "todo"),
             B("LLM client", "только через LiteLLM, алиас модели", "core", "todo"),
             B("Tool Executor", "MCP-адаптер, allowlist, таймауты", "core", "todo")],
            "↺ цикл: context → llm → tools → context",
            [B("Hooks", "before/after llm и tool, on_stop", "core", "todo", "G2"),
             B("Pause / resume", "interrupt на approve и вопрос, checkpointer", "core", "todo"),
             B("Policy / stop", "лимиты шагов, времени, токенов", "core", "todo")],
            "↓",
            [B("Event stream", "шаги для таймлайна", "core", "todo")],
        ], cls="sandbox", g="G2"),
        "↓",
        [B("LiteLLM gateway", "модели", "ext", to="llm-gateway"), B("MCP / Tools", "действия", "ext", to="mcp-tools"),
         B("Memory", "M1–M6", "ext", to="memory"), B("Guardrails", "OPA для G2", "ext", to="guardrails")],
    ],
    "memory": [
        [B("Harness", "чтение в контекст, запись через тул", "ext", to="harness")],
        "↓",
        [B("Memory API", "профиль памяти, области видимости, сроки", "core", "todo")],
        "↓",
        Z("Уровни M0–M6", [
            [B("M0 рабочая", "контекст запуска · Harness", "core", "done"), B("M1 сессионная", "тред · БД ICPlan", "core", "done"),
             B("M2 эпизодическая", "запуски · agent_run", "core", "done")],
            [B("M3 задачная", "сделано / дальше · БД ICPlan · первой", "core", "todo"), B("M4 семантическая", "pgvector · с RAG", "back"),
             B("M5 процедурная", "инструкция, навыки", "core", "done")],
            [B("M6 организационная", "документы проекта · get_document", "core", "done")],
        ]),
        "↓",
        [B("БД ICPlan", "M1, M2, M3, M5", "store", "done"), B("Документы ICPlan", "M6", "store", "done"), B("pgvector", "M4, позже", "back")],
    ],
    "mcp-tools": [
        [B("Harness · Tool Executor", "вызывает тулы", "ext", to="harness")],
        "↓ решает модель → тул · детерминированное → прямой вызов",
        [B("Правила R1–R7", "MCP, нативный тул или прямой вызов", "core", "todo")],
        "↓",
        Z("MCP-серверы и тулы", [
            [B("itsaplan-core", "задачи, комментарии, документы", "core", "done"), B("git-провайдер", "PR, ревью (Gitea / GitHub)", "core", "todo"),
             B("memory", "запись M3", "core", "todo")],
            [B("web-research", "интернет", "back"), B("Админ-MCP", "бюджеты, политики — не для рабочих агентов", "back")],
        ]),
        "↓",
        [B("ICPlan", "MCP itsaplan-core", "ext", to="icplan"), B("Sandbox", "egress-прокси", "ext", to="sandbox")],
    ],
    "guardrails": [
        [B("Rego в git", "логика правил, opa test", "store", "todo"), B("Данные правил", "allowlist, лимиты · Platform module", "ext", to="platform-module"),
         B("Конфиг деплоя", "guardrails.gN.enabled, on_engine_error", "store", "todo")],
        "↓",
        [B("OPA", "движок решений G1 / G2", "core", "part")],
        "↓ решения allow / deny / confirm",
        Z("Точки применения", [
            [B("G1 Admission", "Agent Runner: допуск, бюджет", "ext", to="agent-runner", g="G1"),
             B("G2 Action", "Harness hooks: тулы, память, approve", "ext", to="harness", g="G2"),
             B("G3 Isolation", "Sandbox: сеть, ФС, ресурсы", "ext", to="sandbox", g="G3"),
             B("G4 LLM", "LiteLLM: PII, injection, модерация", "ext", to="llm-gateway", g="G4")],
        ], cls="sandbox"),
        "↓",
        [B("Аудит", "каждое срабатывание с run_id", "ext", to="observability")],
    ],
    "llm-gateway": [
        [B("Harness · LLM client", "OpenAI-совместимый API", "ext", to="harness")],
        "↓ virtual key агента",
        Z("LiteLLM", [
            [B("Virtual keys", "ключ на агента", "core", "part"), B("Бюджеты, rate limit", "отказ до траты", "core", "todo"),
             B("G4 хуки", "PII, injection, модерация", "core", "todo", "G4")],
            [B("Алиасы", "team-default → модель", "core", "part"), B("Fallback", "резервная модель", "core", "todo"),
             B("Spend log", "токены и $ по ключу", "core", "part")],
        ], g="G4"),
        "↓",
        [B("mock-LLM", "разработка и тесты", "core", "todo"), B("Anthropic", "", "store"), B("OpenAI", "", "store"), B("Локальные модели", "", "store")],
        "→ spend log",
        [B("Observability", "затраты", "ext", to="observability")],
    ],
    "observability": [
        [B("Harness · Event stream", "шаги", "ext", to="harness"), B("LiteLLM · Spend log", "токены и $", "ext", to="llm-gateway"),
         B("Guardrails · аудит", "срабатывания", "ext", to="guardrails")],
        "↓ через Agent Runner",
        Z("Observability (MVP)", [
            [B("События запуска", "таблица в БД ICPlan, срок хранения", "core", "todo"), B("Агрегаты затрат", "запуск, задача, агент, модель", "core", "todo")],
        ]),
        "↓",
        [B("Таймлайн в задаче", "ICPlan Task UI", "ext", to="icplan"), B("Затраты в задаче", "ICPlan Task UI", "ext", to="icplan")],
        "бэклог",
        [B("Langfuse", "evals, анализ промптов", "back"), B("Prometheus / Grafana / Loki", "метрики и логи", "back")],
    ],
}
