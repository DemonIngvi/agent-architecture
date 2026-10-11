"""Граф связности документов: изменение в документе слева требует проверки документов справа.

Источник для docs/rules/doc-graph.md (раскрывается в SVG при сборке) и для change-process.md.
"""

LAYERS = [
    ("Запрос", ["Запрос / ревью", "User Stories"]),
    ("Решение", ["R&D", "design.md"]),
    ("Архитектура", ["architecture.md", "Данные сайта (components.py)"]),
    ("Спека", ["spec.md", "interfaces.md", "traceability.md", "Схема capability"]),
    ("Поведение", ["Потоки (flows)", "BPMN (stories.py)"]),
    ("Работа", ["Задачи (docs/tasks)", "tasks.md change"]),
    ("Сводки", ["ROADMAP", "TASKS", "BACKLOG"]),
]

# (от, к, что проверить)
EDGES = [
    ("Запрос / ревью", "User Stories", "новая или изменённая история"),
    ("Запрос / ревью", "R&D", "вопрос выбора"),
    ("User Stories", "spec.md", "требования и сценарии из критериев приёмки"),
    ("User Stories", "BPMN (stories.py)", "процесс и ветки ошибок"),
    ("User Stories", "traceability.md", "колонка User Story"),
    ("R&D", "design.md", "решение D-номер"),
    ("R&D", "Данные сайта (components.py)", "RATIONALE, REFS, SUB"),
    ("design.md", "architecture.md", "раздел и «Обоснование»"),
    ("architecture.md", "Данные сайта (components.py)", "BLOCKS, ABOUT; интеграции и данные — datamodel.py"),
    ("architecture.md", "spec.md", "границы и названия"),
    ("Данные сайта (components.py)", "Схема capability", "блоки схемы"),
    ("spec.md", "traceability.md", "строка RTM"),
    ("spec.md", "interfaces.md", "конфигурация, хранилища, интерфейсы, FMEA"),
    ("spec.md", "Потоки (flows)", "типы данных"),
    ("spec.md", "Задачи (docs/tasks)", "Приёмка, ссылка на требование"),
    ("interfaces.md", "Потоки (flows)", "форматы и протоколы"),
    ("interfaces.md", "Задачи (docs/tasks)", "задача 2.8 и модульные"),
    ("traceability.md", "Задачи (docs/tasks)", "разрыв → задача или «не в MVP»"),
    ("Задачи (docs/tasks)", "tasks.md change", "строка задачи"),
    ("Задачи (docs/tasks)", "ROADMAP", "строка и итоги"),
    ("Задачи (docs/tasks)", "TASKS", "сводная таблица"),
    ("Задачи (docs/tasks)", "Данные сайта (components.py)", "tids компонента"),
    ("Задачи (docs/tasks)", "BACKLOG", "«не в MVP»"),
]
