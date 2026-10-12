"""Hook MkDocs: верхняя панель на каждой странице.

Слева — «Назад» (история браузера) и «На уровень выше» (родитель в дереве навигации).
Справа — вкладки компонента: Архитектура, User Stories, Спеки, Задачи, Интеграции, Данные, Deploy, R&D; Справка — общие правила.
Если страница относится к компоненту, ссылки ведут на документацию этого компонента.
"""
import json
import os
import re
from pathlib import Path

MAP_FILE = Path(__file__).resolve().parent / ".build" / "pagebar.json"
DATA = {"pages": {}, "names": {}}

TYPES = [  # (ключ, подпись, раздел навигации, URL компонента, URL без компонента; None — вкладки нет вне компонента)
    ("arch", "Архитектура", "Архитектура", "components/{}/", ""),
    ("us", "User Stories", "User Stories", "docs/stories/{}/", None),
    ("spec", "Спеки", "Спеки", "specs-by-component/{}/", None),
    ("task", "Задачи", "Задачи", "tasks-by-component/{}/", "tasks-by-component/"),
    ("api", "Интеграции", "Интеграции", "docs/api/{}/", None),
    ("data", "Данные", "Данные", "data-by-component/{}/", None),
    ("tech", "Deploy", "Deploy", "docs/techspec/{}/", None),
    ("rnd", "R&D", "R&D", "rnd-by-component/{}/", "rnd-by-component/"),
    ("find", "Замечания", "Замечания", "docs/reviews/findings/{}/", None),
    ("ref", "Справка", "Справка", None, "docs/rules/"),
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


def _doc_type(src: str) -> str:
    if src == "index.md" or src.startswith("components/"):
        return "Архитектура"
    if src.startswith("docs/stories/"):
        return "User Stories"
    if src.startswith("specs-by-component/") or "/specs/" in src:
        return "Спеки"
    if src.startswith(("tasks-by-component/", "docs/tasks/", "docs/ROADMAP", "docs/TASKS", "docs/BACKLOG")) or src.endswith("/tasks.md"):
        return "Задачи"
    if src.startswith("data-by-component/"):
        return "Данные"
    if src.startswith("docs/api/"):
        return "Интеграции"
    if src.startswith("docs/techspec/"):
        return "Deploy"
    if src.startswith("docs/reviews/findings/"):
        return "Замечания"
    if src.startswith(("docs/rnd/", "rnd-by-component/")):
        return "R&D"
    return "Справка"


def on_page_markdown(markdown, page, config, files, **kwargs):
    src = page.file.src_uri
    slug = DATA["pages"].get(src)
    current = _doc_type(src)
    up = _up(page)

    nav = []
    if page.url != "":
        nav.append('<a class="tb-btn" href="#" onclick="history.back();return false;" title="Предыдущая просмотренная страница">← Назад</a>')
    is_block = re.match(r"components/([^/]+)/[^/]+/index\.md$", src)  # у блока нет своих вкладок — только «↑ компонент»
    if is_block:
        nav.append(f'<a class="tb-btn" href="{_rel(page.url, f"components/{is_block.group(1)}/")}" title="Компонент блока">↑ {DATA["names"].get(is_block.group(1), is_block.group(1))}</a>')
    elif up is not None:
        nav.append(f'<a class="tb-btn" href="{_rel(page.url, up.url)}" title="Уровень выше в дереве">↑ {up.title}</a>')

    types = []
    for key, label, section, comp_url, plain_url in ([] if is_block else TYPES):
        target = comp_url.format(slug) if (slug and comp_url) else plain_url
        if target is None:
            continue  # у вкладки нет общей страницы (О-54)
        active = " active" if section == current else ""
        types.append(f'<a class="tb-type t-{key}{active}" href="{_rel(page.url, target)}">{label}</a>')

    ctx = f'<span class="tb-ctx">{DATA["names"].get(slug, "")}</span>' if slug else ""
    nav.append(f'<a class="tb-help" href="{_rel(page.url, "docs/rules/")}" title="Правила работы с документацией">правила</a>')
    bar = (f'<div class="topbar"><span class="tb-nav">{"".join(nav)}</span>'
           f'<span class="tb-types">{ctx}{"".join(types)}</span></div>')
    ap = DATA.get("approvals", {}).get(src)  # значки ролей, подтвердивших документ (approval-methodology.md)
    if ap:
        cls = {"✅": "ok", "❌": "no"}
        def dot(letter, name, s, who, prev=""):
            state = dict(ok="подтвердил", no="отказ").get(cls.get(s, ""), "ждёт" + (f" повторной проверки, было: {dict(ok='подтвердил', no='отказ')[cls[prev]]}" if prev in cls else ""))
            was = f" ap-was-{cls[prev]}" if prev in cls else ""
            return f'<span class="ap-dot ap-{cls.get(s, "wait")}{was}" title="{name}: {state}{" (" + who + ")" if who and who != "—" else ""}">{letter}</span>'
        dots = "".join(dot(*x) for x in ap)
        bar = bar.replace('<div class="topbar">', f'<div class="topbar"><a class="ap-badges" href="{_rel(page.url, "docs/approvals-summary/")}" title="Подтверждения ролей">{dots}</a>', 1)
    rd = DATA.get("readiness", {}).get(src)
    if rd:
        oq_url = _rel(page.url, page.file.src_uri.rsplit("/", 1)[0] + "/open-questions")
        bar += rd.replace("{rules}", _rel(page.url, "docs/rules/spec-criteria/")).replace("{oq}", oq_url).replace("{appr}", _rel(page.url, page.file.src_uri.rsplit("/", 1)[0] + "/approvals"))
    return bar + "\n\n" + markdown
