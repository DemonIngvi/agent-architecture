"""Граф связности документов: изменение в документе слева требует проверки документов справа.

Источник для docs/rules/doc-graph.md (схема и таблица генерируются при сборке), для change-process.md
и для `doctool next <файл>` — какой документ править следующим (по одному, каждый по своей методологии).
"""

LAYERS = [
    ("Правила", ["Методология (docs/rules)", "Инструменты (doctool, навыки, хуки)"]),
    ("Запрос", ["Запрос / ревью", "User Stories"]),
    ("Решение", ["R&D", "design.md"]),
    ("Архитектура", ["architecture.md", "Данные сайта (components.py)"]),
    ("Спека", ["spec.md", "interfaces.md", "traceability.md", "Схема capability"]),
    ("Вкладки", ["Интеграции и Данные (datamodel.py)", "Как работает (docs/how)", "Deploy (docs/techspec)"]),
    ("Работа", ["Задачи (docs/tasks)", "tasks.md change"]),
    ("Сводки", ["ROADMAP", "TASKS", "BACKLOG"]),
]

# узел → пути файлов (шаблоны от корня репозитория); по ним doctool находит узел документа
PATHS = {
    "Методология (docs/rules)": ["docs/rules/*.md", "FORMAT.md"],
    "Инструменты (doctool, навыки, хуки)": ["html-view/doctool.py", "AGENTS.md", ".claude/skills/doc-*/SKILL.md", ".githooks/*", ".claude/settings.json"],
    "User Stories": ["html-view/stories.py", "html-view/stories_extra/*.md", "docs/stories/*.md"],
    "R&D": ["docs/rnd/*.md"],
    "design.md": ["openspec/changes/*/design.md"],
    "architecture.md": ["architecture.md"],
    "Данные сайта (components.py)": ["html-view/components.py", "html-view/subcomponents.py", "html-view/rationale.py"],
    "spec.md": ["openspec/changes/*/specs/*/spec.md"],
    "interfaces.md": ["openspec/changes/*/specs/*/interfaces.md"],
    "traceability.md": ["openspec/changes/*/specs/*/traceability.md"],
    "Схема capability": ["html-view/archgen.py"],
    "Интеграции и Данные (datamodel.py)": ["html-view/datamodel.py", "docs/api/*.md"],
    "Как работает (docs/how)": ["docs/how/*.md"],
    "Deploy (docs/techspec)": ["docs/techspec/*.md"],
    "Задачи (docs/tasks)": ["docs/tasks/*.md"],
    "tasks.md change": ["html-view/tasksmd.py"],
    "ROADMAP": ["docs/ROADMAP.md"],
    "TASKS": ["docs/TASKS.md"],
    "BACKLOG": ["docs/BACKLOG.md"],
}

# (от, к, что проверить)
EDGES = [
    ("Методология (docs/rules)", "Инструменты (doctool, навыки, хуки)", "проверки, выжимка route, навыки — до правки документов"),
    ("Инструменты (doctool, навыки, хуки)", "Методология (docs/rules)", "команды и проверки, упомянутые в методологии"),
    ("Запрос / ревью", "User Stories", "новая или изменённая история"),
    ("Запрос / ревью", "R&D", "вопрос выбора"),
    ("User Stories", "spec.md", "требования и сценарии из критериев приёмки"),
    ("User Stories", "traceability.md", "колонка User Story"),
    ("R&D", "design.md", "решение D-номер"),
    ("R&D", "Данные сайта (components.py)", "RATIONALE, REFS, SUB"),
    ("design.md", "architecture.md", "раздел и «Обоснование»"),
    ("design.md", "Deploy (docs/techspec)", "технология, образ, поставка"),
    ("architecture.md", "Данные сайта (components.py)", "BLOCKS, ABOUT"),
    ("architecture.md", "Интеграции и Данные (datamodel.py)", "новая связь — I-код, кто вызывает"),
    ("architecture.md", "spec.md", "границы и названия"),
    ("Данные сайта (components.py)", "Схема capability", "блоки схемы"),
    ("spec.md", "traceability.md", "строка RTM"),
    ("spec.md", "interfaces.md", "конфигурация, хранилища, интерфейсы, FMEA"),
    ("spec.md", "Как работает (docs/how)", "порядок работы"),
    ("spec.md", "Задачи (docs/tasks)", "приёмка, ссылка на требование"),
    ("interfaces.md", "Интеграции и Данные (datamodel.py)", "I-коды, хранилища S, модели, срок хранения"),
    ("interfaces.md", "Как работает (docs/how)", "параметры и протоколы"),
    ("interfaces.md", "Deploy (docs/techspec)", "значения в примере конфигурации, переменные"),
    ("interfaces.md", "Задачи (docs/tasks)", "задача 2.8 и модульные"),
    ("Интеграции и Данные (datamodel.py)", "Как работает (docs/how)", "имена моделей в порядке работы"),
    ("Интеграции и Данные (datamodel.py)", "Задачи (docs/tasks)", "доработки форка и новые таблицы"),
    ("traceability.md", "Задачи (docs/tasks)", "разрыв → задача или «не в MVP»"),
    ("Задачи (docs/tasks)", "tasks.md change", "строка задачи"),
    ("Задачи (docs/tasks)", "ROADMAP", "строка и итоги"),
    ("Задачи (docs/tasks)", "TASKS", "сводная таблица"),
    ("Задачи (docs/tasks)", "Данные сайта (components.py)", "tids компонента"),
    ("Задачи (docs/tasks)", "BACKLOG", "«не в MVP»"),
]


def table_md() -> str:
    """Таблица связей для doc-graph.md — из EDGES, без ручной копии."""
    L = ["| От | К | Что проверить | Файлы «к» |", "|---|---|---|---|"]
    L += [f"| {a} | {b} | {w} | {', '.join(f'`{p}`' for p in PATHS.get(b, [])) or '—'} |" for a, b, w in EDGES]
    return "\n".join(L)
