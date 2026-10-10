"""Hook MkDocs: верхняя панель на каждой странице.

Слева — «Назад» (история браузера) и «На уровень выше» (родитель в дереве навигации).
Справа — переход между типами документации: Архитектура / Спеки / Задачи / Справка.
Если страница относится к компоненту, ссылки ведут на документацию этого компонента.
"""
import json
import os
from pathlib import Path

MAP_FILE = Path(__file__).resolve().parent / ".build" / "pagebar.json"
DATA = {"pages": {}, "names": {}}

TYPES = [  # (ключ, подпись, раздел навигации, URL компонента, URL без компонента)
    ("arch", "Архитектура", "Архитектура", "components/{}/", ""),
    ("flow", "Потоки", "Потоки", "docs/flows/{}/", "docs/flows/"),
    ("spec", "Спеки", "Спеки", "specs-by-component/{}/", "specs-by-component/"),
    ("task", "Задачи", "Задачи", "tasks-by-component/{}/", "tasks-by-component/"),
    ("rnd", "R&D", "R&D", None, "docs/rnd/"),
    ("ref", "Справка", "Справка", None, "overview/"),
]


def on_nav(nav, config, files, **kwargs):
    global DATA
    if MAP_FILE.exists():
        DATA = json.loads(MAP_FILE.read_text(encoding="utf-8"))
    return nav


def _rel(page_url: str, target: str) -> str:
    r = os.path.relpath(target or ".", page_url or ".").replace("\\", "/")
    return "./" if r == "." else r + "/"


def _first_page(section):
    for c in section.children:
        if c.is_page:
            return c
        if c.is_section:
            p = _first_page(c)
            if p:
                return p
    return None


def _up(page):
    parent = page.parent
    while parent is not None and _first_page(parent) is page:
        parent = parent.parent
    return _first_page(parent) if parent is not None else None


def _top_section(page):
    node = page
    while node.parent is not None:
        node = node.parent
    return node.title if node is not page else None


def on_page_markdown(markdown, page, config, files, **kwargs):
    src = page.file.src_uri
    slug = DATA["pages"].get(src)
    current = _top_section(page) or "Архитектура"
    up = _up(page)

    nav = []
    if page.url != "":
        nav.append('<a class="tb-btn" href="#" onclick="history.back();return false;" title="Предыдущая просмотренная страница">← Назад</a>')
    if up is not None:
        nav.append(f'<a class="tb-btn" href="{_rel(page.url, up.url)}" title="Уровень выше в дереве">↑ {up.title}</a>')

    types = []
    for key, label, section, comp_url, plain_url in TYPES:
        target = comp_url.format(slug) if (slug and comp_url) else plain_url
        active = " active" if section == current else ""
        types.append(f'<a class="tb-type t-{key}{active}" href="{_rel(page.url, target)}">{label}</a>')

    ctx = f'<span class="tb-ctx">{DATA["names"].get(slug, "")}</span>' if slug else ""
    bar = (f'<div class="topbar"><span class="tb-nav">{"".join(nav)}</span>'
           f'<span class="tb-types">{ctx}{"".join(types)}</span></div>')
    return bar + "\n\n" + markdown
