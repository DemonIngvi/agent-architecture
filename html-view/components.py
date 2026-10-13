"""Компоненты архитектуры для сайта.

Сайт разделён на типы документации (вкладки): Архитектура, Спеки, Задачи, Справка.
Во вкладке «Архитектура» у каждого компонента — блочная схема внутреннего устройства
(BLOCKS), соседние компоненты на ней ведут на их схемы. Спеки и задачи — отдельные вкладки,
на них ведёт панель «Другая документация» внизу страницы компонента.

Данные — data/components/<slug>.yaml, по файлу на компонент (yamldata.py; правило: docs/rules/data-methodology.md#yaml):
name, status (done|part|todo), guardrails, desc, links (пусто: связи — из data/integrations.yaml и HOST), specs [[подпись, путь]], tasks,
about (chain [[подпись, slug|null]], purpose, does) → ABOUT, blocks (ряды схемы: строка-подпись, список блоков, зона) → BLOCKS.
Порядок компонентов — data/components/_order.yaml. Встроенные (HOST: владелец или (компонент, блок) → хост) — data/hosts.yaml.
Здесь только загрузка, имена прежние.
"""
import yamldata as _Y

DAP = "openspec/changes/define-agent-platform"
ICI = "openspec/changes/add-icplan-integration"
AP = "openspec/changes/icplan-agent-autopickup"

_D = _Y.components()
# slug, название, статус (done|part|todo), guardrails, описание, связи, спеки [(подпись, путь)], задачи
COMPONENTS = _D["COMPONENTS"]
# Встроенные: владелец (компонент или (компонент, блок)) → хост, внутри которого работает (процесс, образ, контейнер).
# Источник фактов — «Что разворачивается» на страницах Deploy; правило — architecture-methodology.md#connectivity.
HOST = _D["HOST"]

STATUS = {"done": "✅ есть", "part": "⚠️ частично", "todo": "⬜ не начато"}
BY_SLUG = {c[0]: c for c in COMPONENTS}


def B(title, desc="", kind="", st="", g="", to=""):
    """Блок схемы. kind: core | ext (другой компонент, to=slug) | store | user | back (бэклог)."""
    return dict(title=title, desc=desc, kind=kind, st=st, g=g, to=to)


def Z(title, rows, cls="", g="", note=""):
    """Зона (контейнер) с вложенными рядами."""
    return dict(zone=title, rows=rows, cls=cls, g=g, note=note)


# Внутреннее устройство компонентов: ряды блоков сверху вниз; строка — подпись потока между рядами
BLOCKS = _D["BLOCKS"]
# Краткая справка: цепочка позиции в системе (подпись, slug|None), назначение, что делает
ABOUT = _D["ABOUT"]
