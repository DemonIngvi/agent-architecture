"""Компоненты архитектуры для сайта: страницы-карточки и навигация по иерархии.

Иерархия на сайте: Главная → Компонент → его спеки, схемы, задачи.
Задача попадает к компоненту по номеру; новые задачи и спеки без привязки
попадают в раздел «Прочее» автоматически.
"""

DAP = "openspec/changes/define-agent-platform"
ICI = "openspec/changes/add-icplan-integration"
AP = "openspec/changes/icplan-agent-autopickup"

# slug, название, статус (done|part|todo), guardrails, описание, связи, документы [(подпись, путь)], задачи
COMPONENTS = [
    ("icplan", "ICPlan", "part", "",
     "Таск-трекер It's a Plan: доска, процессы, настройка агентов (Control Plane UI), Registry, очередь запусков, UI задачи. Уже есть, дорабатываем.",
     ["agent-runner", "platform-module", "observability"],
     [("Registry — спека", f"{DAP}/specs/agent-registry/spec.md"),
      ("Интеграция: proposal", f"{ICI}/proposal.md"),
      ("Интеграция: спека", f"{ICI}/specs/icplan-integration/spec.md"),
      ("Интеграция: схема и user flow", f"{ICI}/specs/icplan-integration/architecture.md"),
      ("Автоподхват: proposal", f"{AP}/proposal.md"),
      ("Автоподхват: спека", f"{AP}/specs/icplan-agent-autopickup/spec.md"),
      ("Автоподхват: схема", f"{AP}/specs/icplan-agent-autopickup/architecture.md"),
      ("Автоподхват: задачи ICPlan", f"{AP}/tasks.md")],
     ["1.2", "2.3", "3.1", "3.2", "3.4", "3.5"]),
    ("platform-module", "Platform module", "todo", "",
     "Модуль ICPlan (своя схема в БД ICPlan): алиасы LLM, бюджеты, профили sandbox и памяти, данные guardrails.",
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
