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
from rationale import RATIONALE, REFS  # noqa: E402
from subcomponents import SUB  # noqa: E402
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
    for (slug, title) in SUB:
        pages[sub_page(slug, title)] = slug
    for slug, *_ in COMPONENTS:
        pages[f"rnd-by-component/{slug}/index.md"] = slug
    for slug, refs in REFS.items():
        for _, p in refs:
            if p.startswith("docs/rnd/"):
                pages.setdefault(p, slug)
    rd = {}
    for sp in all_specs():
        r = spec_readiness(sp)
        rd[sp] = ('<div class="rd-head"><span class="about-label">Готовность спеки</span>' + rd_bar(r, True)
                  + "".join(f'<span class="rd-part">{k} <b>{v}</b>/{m}</span>' for k, (v, m) in r["parts"].items())
                  + f'<a class="side-all" href="{{rules}}">критерии →</a></div>')
    data = {"pages": pages, "names": {c[0]: c[1] for c in COMPONENTS}, "readiness": rd}
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


TR = dict(zip("абвгдеёжзийклмнопрстуфхцчшщъыьэюя",
              ["a", "b", "v", "g", "d", "e", "e", "zh", "z", "i", "y", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u", "f",
               "h", "c", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya"]))


def sub_slug(title: str) -> str:
    s = "".join(TR.get(ch, ch) for ch in title.lower())
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def sub_page(slug: str, title: str) -> str:
    return f"components/{slug}/{sub_slug(title)}/index.md"


def code(s: str) -> str:
    """`x` → <code>x</code> для сырого HTML."""
    return re.sub(r"`([^`]+)`", lambda m: f"<code>{m.group(1)}</code>", esc(s))


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def render_block(b: dict, page: str, comp: str = "") -> str:
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
    if comp and (comp, b["title"]) in SUB and b["kind"] != "ext":
        inner.append('<span class="go">подробнее →</span>')
        return f'<a class="{cls}" href="{href(page, sub_page(comp, b["title"]))}">' + "".join(inner) + "</a>"
    if b["kind"] == "ext" and b["to"]:
        inner.append('<span class="go">схема компонента →</span>')
        return f'<a class="{cls}" href="{href(page, f"components/{b["to"]}/index.md")}">' + "".join(inner) + "</a>"
    return f'<div class="{cls}">' + "".join(inner) + "</div>"


def render_rows(rows: list, page: str, comp: str = "") -> str:
    out = []
    for r in rows:
        if isinstance(r, str):
            out.append(f'<div class="flow">{esc(r)}</div>')
        elif isinstance(r, dict):
            g = f' <span class="g">{r["g"]}</span>' if r.get("g") else ""
            out.append(f'<div class="zone zone-{r.get("cls") or "plain"}"><div class="zone-title">{esc(r["zone"])}{g}</div>'
                       f'<div class="map">{render_rows(r["rows"], page, comp)}</div></div>')
        else:
            out.append(f'<div class="crow" style="grid-template-columns:repeat({len(r)},1fr)">'
                       + "".join(render_block(b, page, comp) for b in r) + "</div>")
    return "".join(out)


def cell(s: str) -> str:
    return s.replace("|", "/")


def rationale_md(slug: str) -> list:
    """Нижний блок страницы компонента: почему так и полная конфигурация."""
    r = RATIONALE.get(slug)
    if not r:
        return []
    d = f"components/{slug}"
    refs = " · ".join(f"[{lab}]({rel(d, p)})" for lab, p in REFS.get(slug, []) if (SRC / p).exists())
    L = ["## Почему так", ""] + ([f"**Обоснование:** {refs}", ""] if refs else []) + ["**Почему выбран**", ""] + [f"- {x}" for x in r["why"]]
    L += ["", "**Что даёт**", ""] + [f"- {x}" for x in r["gain"]]
    L += ["", "**Отвергнутые альтернативы**", "", "| Вариант | Почему нет |", "|---|---|"]
    L += [f"| {cell(a)} | {cell(b)} |" for a, b in r["alts"]]
    L += ["", "## Конфигурация", "",
          "Что можно настроить и как это влияет на результат работы агента.", "",
          "| Параметр | Что задаёт | Как влияет на результат | По умолчанию | Где задаётся |", "|---|---|---|---|---|"]
    L += [f"| `{cell(n)}` | {cell(w)} | {cell(e)} | {cell(d)} | {cell(where)} |" for n, w, e, d, where in r["config"]]
    return L + [""]


# ---------- Готовность спек ----------
RD_BANDS = [(90, "#2e7d32", "готова"), (75, "#7cb342", "почти"), (60, "#f9a825", "в работе"), (40, "#ef6c00", "черновик"), (0, "#d32f2f", "заготовка")]


def rd_color(p: int):
    return next((c, n) for lim, c, n in RD_BANDS if p >= lim)


def spec_readiness(spec: str) -> dict:
    """Процент готовности спеки по критериям docs/rules/spec-criteria.md."""
    t = (SRC / spec).read_text(encoding="utf-8")
    reqs = re.split(r"\n### Requirement: ", t)[1:]
    cap = Path(spec).parent.name
    purpose = re.search(r"## Purpose\n\n([^\n]+)", t)
    fmt = 0
    fmt += 5 if purpose and len(purpose.group(1)) >= 50 else 0
    fmt += 5 if reqs and all(re.search(r"\b(SHALL|MUST)\b", r.split("####")[0]) for r in reqs) else 0
    fmt += 5 if reqs and all("#### Scenario:" in r for r in reqs) else 0
    fmt += 5 if reqs and all(len(r.split("#### Scenario:")[0]) <= 520 for r in reqs) else 0
    cov = round(40 * sum(min(r.count("#### Scenario:"), 3) / 3 for r in reqs) / len(reqs)) if reqs else 0
    link = f"specs/{cap}/spec.md"
    srcs = list((SRC / "docs/tasks").glob("*.md")) + [SRC / Path(spec).parents[2] / "tasks.md"]
    trace = 15 if any(f.exists() and link in f.read_text(encoding="utf-8") for f in srcs) else 0
    why = 10 if "Обоснование:" in t else 0
    slug = next((c[0] for c in COMPONENTS for _, pth in c[6] if pth == spec), None)
    conn = 5 if (SRC / Path(spec).parent / "architecture.md").exists() else 0
    conn += 5 if link in (SRC / "architecture.md").read_text(encoding="utf-8") else 0
    conn += 5 if slug and (SRC / f"docs/flows/{slug}.md").exists() else 0
    parts = {"Формат": (fmt, 20), "Сценарии": (cov, 40), "Трассировка": (trace, 15), "Обоснование": (why, 10), "Связность": (conn, 15)}
    total = sum(v for v, _ in parts.values())
    return {"pct": total, "parts": parts, "reqs": len(reqs), "single": sum(1 for r in reqs if r.count("#### Scenario:") == 1)}


def rd_bar(r: dict, wide: bool = False) -> str:
    c, name = rd_color(r["pct"])
    tip = " · ".join(f"{k} {v}/{m}" for k, (v, m) in r["parts"].items())
    cls = "rd rd-wide" if wide else "rd"
    return (f'<span class="{cls}" title="{tip}"><span class="rd-track"><span class="rd-fill" style="width:{r["pct"]}%;background:{c}"></span></span>'
            f'<b class="rd-pct" style="color:{c}">{r["pct"]}%</b>' + (f'<span class="rd-name">{name}</span>' if wide else "") + "</span>")


def rd_scale() -> str:
    marks = "".join(f'<span style="left:{lim}%">{lim}</span>' for lim, _, _ in RD_BANDS[::-1] if lim)
    names = " · ".join(f'<span style="color:{c}">■</span> {n} {lim}+' for lim, c, n in RD_BANDS[::-1])
    return f'<div class="rd-scale"><div class="rd-grad"></div><div class="rd-marks">{marks}</div><div class="rd-legend">{names}</div></div>'


def all_specs() -> list:
    return sorted(p.relative_to(SRC).as_posix() for p in (SRC / "openspec/changes").glob("*/specs/*/spec.md"))


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
        spec_links = "".join(f'<li><a href="{href(page, p)}">{esc(l)}</a>' + (rd_bar(spec_readiness(p)) if p.endswith("/spec.md") else "") + '</li>' for l, p in docs_ok)
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
            f'<div class="side-card"><div class="side-head"><span class="dtype dtype-rnd">R&amp;D</span>'
            f'<a class="side-all" href="{href(page, f"rnd-by-component/{slug}/index.md")}">все →</a></div><ul>'
            + "".join(f'<li><a href="{href(page, p)}">{esc(lab)}</a></li>' for lab, p in REFS.get(slug, []) if p.startswith("docs/rnd/"))
            + '</ul></div>'
            f'<div class="side-card"><div class="side-head"><span class="dtype dtype-spec">СПЕКА</span>'
            f'<a class="side-all" href="{href(page, spec_page)}">все →</a></div><ul>{spec_links}</ul></div>'
            f'<div class="side-card"><div class="side-head"><span class="dtype dtype-task">ЗАДАЧИ</span>'
            f'<a class="side-all" href="{href(page, task_page)}">все →</a></div><ul>{task_links}</ul></div>'
            '</aside></div>')
        cfg = RATIONALE.get(slug, {}).get("config", [])[:6]
        keyp = ""
        if cfg:
            keyp = ('<div class="keyparams"><span class="about-label">Ключевые параметры</span>'
                    + "".join(f'<span class="kp"><code>{esc(n)}</code> {esc(d)}</span>' for n, _, _, d, _ in cfg)
                    + '<a class="side-all" href="#_5">все параметры ↓</a></div>')
        body = [f"# {name}", "", head, "", keyp, "", about, "",
                "## Устройство", "",
                f'<div class="map">{render_rows(BLOCKS.get(slug, []), page, slug)}</div>', ""]
        body += rationale_md(slug)
        (SRC / page).parent.mkdir(parents=True, exist_ok=True)
        (SRC / page).write_text("\n".join(body), encoding="utf-8")

        # Вкладка «Спеки»: страница компонента
        d = f"specs-by-component/{slug}"
        L = [f"# Спеки: {name}", "",
             desc, "", "| Документ | Тип | Готовность |", "|---|---|---|"]
        for label, p in docs_ok:
            kind = "схема" if p.endswith("architecture.md") else "proposal" if p.endswith("proposal.md") else "спека"
            rdy = rd_bar(spec_readiness(p)) if p.endswith("/spec.md") else ""
            L.append(f"| [{label}]({rel(d, p)}) | {kind} | {rdy} |")
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

    # Подкомпоненты
    for (slug, title), s in SUB.items():
        page = sub_page(slug, title)
        d = str(Path(page).parent).replace("\\", "/")
        name = BY_SLUG[slug][1]
        L = [f"# {title}", "",
             f"Часть компонента [{name}]({rel(d, f'components/{slug}/index.md')}).", "",
             "## Технология и ключевые параметры", "", f"**Технология:** {s['tech']}", "",
             "| Параметр | Значение |", "|---|---|"] + [f"| `{cell(a)}` | {cell(b)} |" for a, b in s["params"]]
        L += ["", "## Что делает", ""] + [f"- {x}" for x in s["does"]]
        L += ["", "## Почему так", "", s["why"]]
        if s["rnd"]:
            L += ["", f"**Исследование:** [R&D]({rel(d, 'docs/rnd/' + s['rnd'])})"]
        (SRC / d).mkdir(parents=True, exist_ok=True)
        (SRC / page).write_text("\n".join(L) + "\n", encoding="utf-8")

    for slug, name, *_ in COMPONENTS:
        d = f"rnd-by-component/{slug}"
        L = [f"# R&D: {name}", "", "Исследования, на которых основаны решения по компоненту. Методология — [METHOD](" + rel(d, "docs/rnd/METHOD.md") + ").", "",
             "| Исследование | Решение |", "|---|---|"]
        for lab, p in REFS.get(slug, []):
            if p.startswith("docs/rnd/") and (SRC / p).exists():
                dec = next((l.split("|")[2].strip() for l in (SRC / p).read_text(encoding="utf-8").splitlines() if l.startswith("| **Решение**")), "")
                L.append(f"| [{lab.replace('R&D: ', '')}]({rel(d, p)}) | {dec} |")
        (SRC / d).mkdir(parents=True, exist_ok=True)
        (SRC / d / "index.md").write_text("\n".join(L) + "\n", encoding="utf-8")

    # Обзорные страницы вкладок «Спеки» и «Задачи»
    specs = all_specs()
    rows = []
    for sp in specs:
        r = spec_readiness(sp)
        rows.append(f"| [{Path(sp).parent.name}]({rel('specs-by-component', sp)}) | {Path(sp).parts[2]} | {r['reqs']} | {r['single']} | {rd_bar(r)} |")
    avg = round(sum(spec_readiness(s)["pct"] for s in specs) / len(specs)) if specs else 0
    readiness_md = ["## Готовность спек", "", f"Средняя готовность: {rd_bar({'pct': avg, 'parts': {}}, True)}", "", rd_scale(), "",
                    "Считается по [критериям полноты](" + rel("specs-by-component", "docs/rules/spec-criteria.md") + "): формат 20, сценарии 40, трассировка 15, обоснование 10, связность 15. Наведите на шкалу — разбивка.", "",
                    "| Спека | Change | Требований | С одним сценарием | Готовность |", "|---|---|---|---|---|"] + rows + [""]

    for d, title, sub in (("rnd-by-component", "R&D по компонентам", "Исследования и выбор технологий по каждому компоненту."),
                          ("specs-by-component", "Спеки по компонентам", "Требования (OpenSpec) и схемы каждого компонента."),
                          ("tasks-by-component", "Задачи по компонентам", "Доработки каждого компонента. Порядок и оценки — в Roadmap.")):
        L = [f"# {title}", "", sub, "", '<div class="links3">']
        for slug, name, st, g, desc, *_ in COMPONENTS:
            L.append(f'<a class="card" href="{slug}/"><i class="st st-{st}"></i><b>{esc(name)}</b><small>{esc(desc)}</small></a>')
        L.append("</div>")
        if d == "specs-by-component":
            L += [""] + readiness_md
        (SRC / d / "index.md").write_text("\n".join(L) + "\n", encoding="utf-8")


def nav_yaml() -> str:
    tasks = task_files()
    used = set()

    def item(indent, label, path):
        used.add(path)
        return f"{' ' * indent}- {q(label)}: {path}"

    L = ["nav:", "  - Архитектура:", item(4, "Главная — карта", "index.md")]
    for slug, name, *_ in COMPONENTS:
        subs = [title for (s, title) in SUB if s == slug]
        if subs:
            L.append(f"    - {q(name)}:")
            L.append(item(6, name, f"components/{slug}/index.md"))
            L += [item(6, title, sub_page(slug, title)) for title in subs]
        else:
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

    L += ["  - R&D:", item(4, "R&D по компонентам", "rnd-by-component/index.md"),
          item(4, "Все R&D", "docs/rnd/README.md"), item(4, "Методология", "docs/rnd/METHOD.md")]
    for slug, name, *_ in COMPONENTS:
        rs = [p for _, p in REFS.get(slug, []) if p.startswith("docs/rnd/") and (SRC / p).exists() and p not in used]
        L.append(f"    - {q(name)}:")
        L.append(item(6, name, f"rnd-by-component/{slug}/index.md"))
        L += [item(6, title_of(SRC / p, p).replace("R&D: ", ""), p) for p in rs]
    left = [f"docs/rnd/{f.name}" for f in sorted((SRC / "docs/rnd").glob("*.md")) if f"docs/rnd/{f.name}" not in used]
    L += [item(4, title_of(SRC / p, p).replace("R&D: ", ""), p) for p in left]
    L += ["  - Справка:", item(4, "Компоненты (таблица)", "overview.md"), item(4, "Как читать", "docs/HOW-TO-READ.md"),
          item(4, "Схемы C1 / C2 (текст)", "architecture.md"), item(4, "Бэклог", "docs/BACKLOG.md"),
          item(4, "План документации", "docs/PLAN.md"), item(4, "Формат схем", "FORMAT.md"),
          "    - Правила документации:", item(6, "Правила документации", "docs/rules/README.md"),
          item(6, "Критерии полноты спеки", "docs/rules/spec-criteria.md"), item(6, "Роли", "docs/rules/roles.md"),
          item(6, "Типы документов", "docs/rules/doc-types.md"), item(6, "Процесс изменения", "docs/rules/change-process.md"),
          item(6, "Промпты", "docs/rules/prompts.md")]
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
