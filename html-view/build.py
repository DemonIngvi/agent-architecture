"""Собирает HTML-сайт документации (MkDocs Material) из Markdown репозитория.

Запуск из корня репозитория:
    pip install -r html-view/requirements.txt
    python html-view/build.py           # сборка в html-view/site
    python html-view/build.py serve     # локальный просмотр на http://127.0.0.1:8000
"""
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from rationale import RATIONALE  # noqa: E402
from components import ABOUT, AP, IO, BLOCKS, BY_SLUG, COMPONENTS, STATUS  # noqa: E402

ROOT = HERE.parent
BUILD = HERE / ".build"
SRC = BUILD / "docs"
SITE = HERE / "site"

# Что попадает на сайт (только Markdown)
SOURCES = ["README.md", "architecture.md", "FORMAT.md", "docs", "openspec/changes"]


def title_of(path: Path, fallback: str) -> str:
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            t = line[2:].strip()
            return fallback if t in ("Spec Delta",) else t
    return fallback


def natural(p: Path):
    return [int(x) if x.isdigit() else x for x in re.split(r"(\d+)", p.name)]


def q(s: str) -> str:
    return '"' + s.replace('"', '\\"') + '"'


def task_files() -> dict:
    """id задачи → путь относительно SRC, например '1.3' → 'docs/tasks/1.3-harness-core.md'."""
    out = {}
    for f in sorted((SRC / "docs/tasks").glob("*.md"), key=natural):
        out[f.name.split("-", 1)[0]] = f"docs/tasks/{f.name}"
    return out


def relink_readme(text: str, src: Path) -> str:
    """Ссылки на корневой README.md ведут на overview.md."""
    def fix(m):
        target = m.group(2)
        if (src.parent / target).resolve() == (ROOT / "README.md").resolve():
            target = target[: -len("README.md")] + "overview.md"
        return f"]({target}{m.group(3) or ''})"
    return re.sub(r"\]\(()((?:\.\./)*README\.md)(#[^)]*)?\)", fix, text)


def copy_sources():
    shutil.rmtree(SRC, ignore_errors=True)
    files = []
    for item in SOURCES:
        src = ROOT / item
        files += [src] if src.is_file() else list(src.rglob("*.md"))
    for f in files:
        rel = f.relative_to(ROOT)
        # Корневой README на сайте — страница «Компоненты» (overview.md); главная — карта из home.md
        dst = SRC / ("overview.md" if rel.as_posix() == "README.md" else rel)
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(relink_readme(f.read_text(encoding="utf-8"), f), encoding="utf-8")
    shutil.copy2(HERE / "home.md", SRC / "index.md")
    (SRC / "assets").mkdir(parents=True, exist_ok=True)
    shutil.copy2(HERE / "assets" / "extra.css", SRC / "assets" / "extra.css")
    write_component_pages()
    write_pagebar_map()


def write_pagebar_map():
    """src-путь страницы → slug компонента: по нему верхняя панель строит ссылки на типы документации."""
    tasks = task_files()
    pages = {}
    for slug, name, st, g, desc, links, docs, tids in COMPONENTS:
        for p in [f"components/{slug}/index.md", f"specs-by-component/{slug}/index.md", f"tasks-by-component/{slug}/index.md"]:
            pages[p] = slug
        for _, p in docs:
            pages.setdefault(p, slug)
        for t in tids:
            if t in tasks:
                pages[tasks[t]] = slug
    pages.setdefault(f"{AP}/tasks.md", "icplan")
    for slug, *_ in COMPONENTS:
        pages[f"docs/flows/{slug}.md"] = slug
    data = {"pages": pages, "names": {c[0]: c[1] for c in COMPONENTS}}
    (BUILD / "pagebar.json").write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")


def rel(from_dir: str, target: str) -> str:
    return os.path.relpath(target, from_dir).replace("\\", "/")


def url_of(path: str) -> str:
    """Путь .md → URL каталога (use_directory_urls)."""
    p = path[:-3]
    if p == "index" or p.endswith("/index"):
        p = p[: -len("index")]
    else:
        p += "/"
    return p


def href(from_md: str, to_md: str) -> str:
    """Относительная ссылка между страницами для сырого HTML."""
    a, b = url_of(from_md), url_of(to_md)
    r = os.path.relpath(b or ".", a or ".").replace("\\", "/")
    return "./" if r == "." else r + "/"


def task_meta(path: str) -> list:
    """Строка оценки из документа задачи: этап, компонент, зависит, человек, агент, токены."""
    rows = [l for l in (SRC / path).read_text(encoding="utf-8").splitlines() if l.startswith("| ") and "---" not in l]
    return [c.strip() for c in rows[1].strip("|").split("|")] if len(rows) > 1 else []


def code(s: str) -> str:
    """`x` → <code>x</code> для сырого HTML."""
    return re.sub(r"`([^`]+)`", lambda m: f"<code>{m.group(1)}</code>", esc(s))


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def render_block(b: dict, page: str) -> str:
    cls = f"card blk {b['kind']}".strip()
    inner = []
    if b["st"]:
        inner.append(f'<i class="st st-{b["st"]}"></i>')
    title = esc(b["title"]) + (f' <span class="g">{b["g"]}</span>' if b["g"] else "")
    inner.append(f"<b>{title}</b>")
    if b["desc"]:
        inner.append(f"<small>{esc(b['desc'])}</small>")
    if b["kind"] == "back":
        inner.append('<span class="tag-back">бэклог</span>')
    if b["kind"] == "ext" and b["to"]:
        inner.append('<span class="go">схема компонента →</span>')
        return f'<a class="{cls}" href="{href(page, f"components/{b["to"]}/index.md")}">' + "".join(inner) + "</a>"
    return f'<div class="{cls}">' + "".join(inner) + "</div>"


def render_rows(rows: list, page: str) -> str:
    out = []
    for r in rows:
        if isinstance(r, str):
            out.append(f'<div class="flow">{esc(r)}</div>')
        elif isinstance(r, dict):
            g = f' <span class="g">{r["g"]}</span>' if r.get("g") else ""
            out.append(f'<div class="zone zone-{r.get("cls") or "plain"}"><div class="zone-title">{esc(r["zone"])}{g}</div>'
                       f'<div class="map">{render_rows(r["rows"], page)}</div></div>')
        else:
            out.append(f'<div class="crow" style="grid-template-columns:repeat({len(r)},1fr)">'
                       + "".join(render_block(b, page) for b in r) + "</div>")
    return "".join(out)


def cell(s: str) -> str:
    return s.replace("|", "/")


def rationale_md(slug: str) -> list:
    """Нижний блок страницы компонента: почему так и полная конфигурация."""
    r = RATIONALE.get(slug)
    if not r:
        return []
    L = ["## Почему так", "", "**Почему выбран**", ""] + [f"- {x}" for x in r["why"]]
    L += ["", "**Что даёт**", ""] + [f"- {x}" for x in r["gain"]]
    L += ["", "**Отвергнутые альтернативы**", "", "| Вариант | Почему нет |", "|---|---|"]
    L += [f"| {cell(a)} | {cell(b)} |" for a, b in r["alts"]]
    L += ["", "## Конфигурация", "",
          "Что можно настроить и как это влияет на результат работы агента.", "",
          "| Параметр | Что задаёт | Как влияет на результат | По умолчанию | Где задаётся |", "|---|---|---|---|---|"]
    L += [f"| `{cell(n)}` | {cell(w)} | {cell(e)} | {cell(d)} | {cell(where)} |" for n, w, e, d, where in r["config"]]
    return L + [""]


def write_component_pages():
    tasks = task_files()
    for slug, name, st, g, desc, links, docs, tids in COMPONENTS:
        page = f"components/{slug}/index.md"
        spec_page = f"specs-by-component/{slug}/index.md"
        task_page = f"tasks-by-component/{slug}/index.md"
        docs_ok = [(l, p) for l, p in docs if (SRC / p).exists()]
        ts = [t for t in tids if t in tasks]
        gtxt = f' <span class="g">{g}</span>' if g else ""
        head = f'<div class="comp-head"><span class="pill">{STATUS[st]}</span>{gtxt}</div>'
        chain, purpose, does = ABOUT.get(slug, ([], desc, []))
        ch = []
        for label, s in chain:
            if s == slug:
                ch.append(f'<span class="ch-item ch-cur">{esc(label)}</span>')
            elif s:
                ch.append(f'<a class="ch-item" href="{href(page, f"components/{s}/index.md")}">{esc(label)}</a>')
            else:
                ch.append(f'<span class="ch-item ch-plain">{esc(label)}</span>')
        spec_links = "".join(f'<li><a href="{href(page, p)}">{esc(l)}</a></li>' for l, p in docs_ok)
        task_links = "".join(
            f'<li><a href="{href(page, tasks[t])}"><span class="tid">{t}</span> {esc(title_of(SRC / tasks[t], t).split(". ", 1)[-1])}</a></li>'
            for t in ts)
        about = (
            '<div class="about"><div class="about-main">'
            '<div class="about-label">Позиция в системе</div>'
            f'<div class="chain">{"<span class=ch-arrow>→</span>".join(ch)}</div>'
            '<div class="about-label">Для чего</div>'
            f'<p class="purpose">{esc(purpose)}</p>'
            '<div class="about-label">Что делает</div>'
            f'<ul class="does">{"".join(f"<li>{esc(x)}</li>" for x in does)}</ul>'
            '<div class="io"><div><div class="about-label">Получает</div>'
            f'<ul class="does">{"".join(f"<li>{code(x)}</li>" for x in IO.get(slug, ([], []))[0])}</ul></div>'
            '<div><div class="about-label">Отдаёт</div>'
            f'<ul class="does">{"".join(f"<li>{code(x)}</li>" for x in IO.get(slug, ([], []))[1])}</ul></div></div>'
            '</div><aside class="about-side">'
            f'<div class="side-card"><div class="side-head"><span class="dtype dtype-flow">ПОТОКИ</span>'
            f'<a class="side-all" href="{href(page, f"docs/flows/{slug}.md")}">открыть →</a></div>'
            '<ul><li>Шаги, типы данных, примеры</li></ul></div>'
            f'<div class="side-card"><div class="side-head"><span class="dtype dtype-spec">СПЕКА</span>'
            f'<a class="side-all" href="{href(page, spec_page)}">все →</a></div><ul>{spec_links}</ul></div>'
            f'<div class="side-card"><div class="side-head"><span class="dtype dtype-task">ЗАДАЧИ</span>'
            f'<a class="side-all" href="{href(page, task_page)}">все →</a></div><ul>{task_links}</ul></div>'
            '</aside></div>')
        body = [f"# {name}", "", head, "", about, "",
                "## Устройство", "",
                f'<div class="map">{render_rows(BLOCKS.get(slug, []), page)}</div>', ""]
        body += rationale_md(slug)
        (SRC / page).parent.mkdir(parents=True, exist_ok=True)
        (SRC / page).write_text("\n".join(body), encoding="utf-8")

        # Вкладка «Спеки»: страница компонента
        d = f"specs-by-component/{slug}"
        L = [f"# Спеки: {name}", "",
             desc, "", "| Документ | Тип |", "|---|---|"]
        for label, p in docs_ok:
            kind = "схема" if p.endswith("architecture.md") else "proposal" if p.endswith("proposal.md") else "спека"
            L.append(f"| [{label}]({rel(d, p)}) | {kind} |")
        (SRC / d).mkdir(parents=True, exist_ok=True)
        (SRC / d / "index.md").write_text("\n".join(L) + "\n", encoding="utf-8")

        # Вкладка «Задачи»: страница компонента
        d = f"tasks-by-component/{slug}"
        L = [f"# Задачи: {name}", "",
             "| # | Задача | Этап | Человек | Агент | Токены |", "|---|---|---|---|---|---|"]
        for t in ts:
            m = task_meta(tasks[t])
            title = title_of(SRC / tasks[t], t).split(". ", 1)[-1]
            cells = [m[0], m[3], m[4], m[5]] if len(m) >= 6 else ["", "", "", ""]
            L.append(f"| {t} | [{title}]({rel(d, tasks[t])}) | {' | '.join(cells)} |")
        if slug == "icplan" and (SRC / f"{AP}/tasks.md").exists():
            L += ["", f"Детальный список задач ICPlan по автоподхвату: [icplan-agent-autopickup/tasks.md]({rel(d, f'{AP}/tasks.md')})"]
        (SRC / d).mkdir(parents=True, exist_ok=True)
        (SRC / d / "index.md").write_text("\n".join(L) + "\n", encoding="utf-8")

    # Обзорные страницы вкладок «Спеки» и «Задачи»
    for d, title, sub in (("specs-by-component", "Спеки по компонентам", "Требования (OpenSpec) и схемы каждого компонента."),
                          ("tasks-by-component", "Задачи по компонентам", "Доработки каждого компонента. Порядок и оценки — в Roadmap.")):
        L = [f"# {title}", "", sub, "", '<div class="links3">']
        for slug, name, st, g, desc, *_ in COMPONENTS:
            L.append(f'<a class="card" href="{slug}/"><i class="st st-{st}"></i><b>{esc(name)}</b><small>{esc(desc)}</small></a>')
        L.append("</div>")
        (SRC / d / "index.md").write_text("\n".join(L) + "\n", encoding="utf-8")


def nav_yaml() -> str:
    tasks = task_files()
    used = set()

    def item(indent, label, path):
        used.add(path)
        return f"{' ' * indent}- {q(label)}: {path}"

    L = ["nav:", "  - Архитектура:", item(4, "Главная — карта", "index.md")]
    for slug, name, *_ in COMPONENTS:
        L.append(item(4, name, f"components/{slug}/index.md"))

    L += ["  - Потоки:", item(4, "Сквозной поток", "docs/flows/README.md")]
    for slug, name, *_ in COMPONENTS:
        if (SRC / f"docs/flows/{slug}.md").exists():
            L.append(item(4, name, f"docs/flows/{slug}.md"))
    L += ["  - Спеки:", item(4, "Спеки по компонентам", "specs-by-component/index.md")]
    for slug, name, st, g, desc, links, docs, tids in COMPONENTS:
        L.append(f"    - {q(name)}:")
        L.append(item(6, name, f"specs-by-component/{slug}/index.md"))
        for label, p in docs:
            if (SRC / p).exists():
                L.append(item(6, label, p))
    L.append("    - Решения (OpenSpec):")
    for ch in sorted(p for p in (SRC / "openspec/changes").iterdir() if p.is_dir() and p.name != "archive"):
        rest = [f"openspec/changes/{ch.name}/{n}" for n in ("proposal.md", "design.md", "tasks.md")]
        rest += [p.relative_to(SRC).as_posix() for p in sorted(ch.rglob("*.md")) if "specs" in p.parts]
        rest = [p for p in rest if (SRC / p).exists() and p not in used]
        if rest:
            L.append(f"      - {q(ch.name)}:")
            L += [item(8, title_of(SRC / p, Path(p).parent.name), p) for p in rest]

    L += ["  - Задачи:", item(4, "Roadmap MVP", "docs/ROADMAP.md"), item(4, "Сводная таблица", "docs/TASKS.md"),
          item(4, "Задачи по компонентам", "tasks-by-component/index.md")]
    for slug, name, st, g, desc, links, docs, tids in COMPONENTS:
        L.append(f"    - {q(name)}:")
        L.append(item(6, name, f"tasks-by-component/{slug}/index.md"))
        L += [item(6, title_of(SRC / tasks[t], t), tasks[t]) for t in tids if t in tasks]
    left = [t for t in tasks.values() if t not in used]
    if left:
        L.append("    - Прочие задачи:")
        L += [item(6, title_of(SRC / t, t), t) for t in left]

    L += ["  - Справка:", item(4, "Компоненты (таблица)", "overview.md"), item(4, "Как читать", "docs/HOW-TO-READ.md"),
          item(4, "Схемы C1 / C2 (текст)", "architecture.md"), item(4, "Бэклог", "docs/BACKLOG.md"),
          item(4, "План документации", "docs/PLAN.md"), item(4, "Формат схем", "FORMAT.md")]
    return "\n".join(L) + "\n"


def write_config(serve: bool = False):
    cfg = (HERE / "mkdocs.base.yml").read_text(encoding="utf-8")
    if serve:
        # Локально сайт в корне, а не под /agent-architecture/ (путь GitHub Pages)
        cfg = re.sub(r"(?m)^site_url:.*$", "site_url: http://127.0.0.1:8000/", cfg)
        # Пересобирать при правке исходных .md: hook копирует их перед каждой сборкой
        watched = [ROOT / s for s in SOURCES] + [HERE / "home.md", HERE / "assets", HERE / "components.py"]
        watch = "\n".join(f"  - {q(p.as_posix())}" for p in watched)
        cfg += f"\nwatch:\n{watch}\n"
    hooks = [HERE / "pagebar.py"] + ([HERE / "hooks.py"] if serve else [])
    cfg += "\nhooks:\n" + "".join(f"  - {q(h.as_posix())}\n" for h in hooks)
    (BUILD / "mkdocs.yml").write_text(cfg + "\n" + nav_yaml(), encoding="utf-8")


def main():
    serve = len(sys.argv) > 1 and sys.argv[1] == "serve"
    copy_sources()
    write_config(serve)
    cmd = [sys.executable, "-m", "mkdocs"]
    if serve:
        subprocess.run(cmd + ["serve", "-f", str(BUILD / "mkdocs.yml"), "-a", "127.0.0.1:8000"], check=True)
    else:
        subprocess.run(cmd + ["build", "-f", str(BUILD / "mkdocs.yml"), "-d", str(SITE), "--clean"], check=True)
        print(f"Готово: {SITE / 'index.html'}")


if __name__ == "__main__":
    main()
