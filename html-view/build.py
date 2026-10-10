"""Собирает HTML-сайт документации (MkDocs Material) из Markdown репозитория.

Запуск из корня репозитория:
    pip install -r html-view/requirements.txt
    python html-view/build.py           # сборка в html-view/site
    python html-view/build.py serve     # локальный просмотр на http://127.0.0.1:8000
"""
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from components import BY_SLUG, COMPONENTS, STATUS  # noqa: E402

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


def rel(from_dir: str, target: str) -> str:
    return os.path.relpath(target, from_dir).replace("\\", "/")


def write_component_pages():
    tasks = task_files()
    for slug, name, st, g, desc, links, docs, tids in COMPONENTS:
        d = f"components/{slug}"
        L = [f"# {name}", "",
             f"← [Главная]({rel(d, 'index.md')}) · [все компоненты]({rel(d, 'overview.md')}) · [Roadmap]({rel(d, 'docs/ROADMAP.md')})", "",
             f"**Статус:** {STATUS[st]}" + (f" · **Guardrails:** `{g}`" if g else ""), "", desc, "",
             "## Документы", ""]
        L += [f"- [{label}]({rel(d, path)})" for label, path in docs if (SRC / path).exists()]
        L += ["", "## Задачи", "", "| # | Задача |", "|---|---|"]
        for t in tids:
            if t in tasks:
                L.append(f"| {t} | [{title_of(SRC / tasks[t], t).split('. ', 1)[-1]}]({rel(d, tasks[t])}) |")
        L += ["", "## Связи", ""]
        L += [f"- [{BY_SLUG[s][1]}]({rel(d, f'components/{s}/index.md')})" for s in links]
        (SRC / d).mkdir(parents=True, exist_ok=True)
        (SRC / d / "index.md").write_text("\n".join(L) + "\n", encoding="utf-8")


def nav_yaml() -> str:
    tasks = task_files()
    used = set()

    def item(indent, label, path):
        used.add(path)
        return f"{' ' * indent}- {q(label)}: {path}"

    L = ["nav:",
         item(2, "Главная", "index.md"),
         "  - Обзор:",
         item(4, "Компоненты", "overview.md"),
         item(4, "Как читать", "docs/HOW-TO-READ.md"),
         item(4, "Архитектура C1 / C2", "architecture.md"),
         item(4, "Roadmap MVP", "docs/ROADMAP.md"),
         item(4, "Сводная таблица задач", "docs/TASKS.md"),
         item(4, "Бэклог", "docs/BACKLOG.md"),
         item(4, "План документации", "docs/PLAN.md"),
         item(4, "Формат схем", "FORMAT.md"),
         "  - Компоненты:"]
    for slug, name, st, g, desc, links, docs, tids in COMPONENTS:
        L.append(f"    - {q(name)}:")
        L.append(item(6, name, f"components/{slug}/index.md"))
        for label, path in docs:
            if (SRC / path).exists():
                L.append(item(6, label, path))
        ts = [t for t in tids if t in tasks]
        if ts:
            L.append("      - Задачи:")
            for t in ts:
                L.append(item(8, title_of(SRC / tasks[t], t), tasks[t]))
    # Решения (OpenSpec changes) — то, что не попало в компоненты
    L.append("  - Решения:")
    for ch in sorted(p for p in (SRC / "openspec/changes").iterdir() if p.is_dir() and p.name != "archive"):
        rest = [f"openspec/changes/{ch.name}/{n}" for n in ("proposal.md", "design.md", "tasks.md")]
        rest += [p.relative_to(SRC).as_posix() for p in sorted(ch.rglob("*.md")) if "specs" in p.parts]
        rest = [p for p in rest if (SRC / p).exists() and p not in used]
        if rest:
            L.append(f"    - {q(ch.name)}:")
            for p in rest:
                L.append(item(6, title_of(SRC / p, Path(p).parent.name), p))
    left = [t for t in tasks.values() if t not in used]
    if left:
        L.append("  - Прочие задачи:")
        L += [item(4, title_of(SRC / t, t), t) for t in left]
    return "\n".join(L) + "\n"


def write_config(serve: bool = False):
    cfg = (HERE / "mkdocs.base.yml").read_text(encoding="utf-8")
    if serve:
        # Локально сайт в корне, а не под /agent-architecture/ (путь GitHub Pages)
        cfg = re.sub(r"(?m)^site_url:.*$", "site_url: http://127.0.0.1:8000/", cfg)
        # Пересобирать при правке исходных .md: hook копирует их перед каждой сборкой
        watched = [ROOT / s for s in SOURCES] + [HERE / "home.md", HERE / "assets", HERE / "components.py"]
        watch = "\n".join(f"  - {q(p.as_posix())}" for p in watched)
        cfg += f"\nhooks:\n  - {q((HERE / 'hooks.py').as_posix())}\nwatch:\n{watch}\n"
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
