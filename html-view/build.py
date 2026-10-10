"""Собирает HTML-сайт документации (MkDocs Material) из Markdown репозитория.

Запуск из корня репозитория:
    pip install -r html-view/requirements.txt
    python html-view/build.py           # сборка в html-view/site
    python html-view/build.py serve     # локальный просмотр на http://127.0.0.1:8000
"""
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
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


def relink_readme(text: str, src: Path) -> str:
    """Ссылки на корневой README.md ведут на overview.md."""
    def fix(m):
        target = m.group(2)
        if (src.parent / target).resolve() == (ROOT / "README.md").resolve():
            target = target[: -len("README.md")] + "overview.md"
        return f"]({target}{m.group(3) or ''}"
    return re.sub(r"\]\(()((?:\.\./)*README\.md)(#[^)]*)?\)", lambda m: fix(m) + ")", text)


def q(s: str) -> str:
    return '"' + s.replace('"', '\\"') + '"'


def nav_yaml() -> str:
    L = ["nav:",
         "  - Главная: index.md",
         "  - Обзор:",
         "    - Компоненты: overview.md",
         "    - Как читать: docs/HOW-TO-READ.md",
         "    - Архитектура: architecture.md",
         "    - Формат схем: FORMAT.md",
         "  - Roadmap:",
         "    - Roadmap MVP: docs/ROADMAP.md",
         "    - Сводная таблица задач: docs/TASKS.md",
         "    - Бэклог: docs/BACKLOG.md",
         "    - План документации: docs/PLAN.md",
         "  - Задачи:"]
    for f in sorted((SRC / "docs/tasks").glob("*.md"), key=natural):
        L.append(f"    - {q(title_of(f, f.stem))}: docs/tasks/{f.name}")
    L.append("  - Спеки:")
    for ch in sorted(p for p in (SRC / "openspec/changes").iterdir() if p.is_dir() and p.name != "archive"):
        L.append(f"    - {q(ch.name)}:")
        for name, label in (("proposal.md", "Proposal"), ("design.md", "Design"), ("tasks.md", "Tasks")):
            if (ch / name).exists():
                L.append(f"      - {label}: openspec/changes/{ch.name}/{name}")
        specs = ch / "specs"
        if specs.exists():
            for cap in sorted(p for p in specs.iterdir() if p.is_dir()):
                L.append(f"      - {q(cap.name)}:")
                if (cap / "spec.md").exists():
                    L.append(f"        - Спека: openspec/changes/{ch.name}/specs/{cap.name}/spec.md")
                if (cap / "architecture.md").exists():
                    L.append(f"        - Схема: openspec/changes/{ch.name}/specs/{cap.name}/architecture.md")
    return "\n".join(L) + "\n"


def write_config(serve: bool = False):
    cfg = (HERE / "mkdocs.base.yml").read_text(encoding="utf-8")
    if serve:
        # Локально сайт в корне, а не под /agent-architecture/ (путь GitHub Pages)
        cfg = re.sub(r"(?m)^site_url:.*$", "site_url: http://127.0.0.1:8000/", cfg)
        # Пересобирать при правке исходных .md: hook копирует их перед каждой сборкой
        watched = [ROOT / s for s in SOURCES] + [HERE / "home.md", HERE / "assets"]
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
