"""Карта сайта (О-54): какие исходники не становятся отдельными страницами и куда ведут ссылки на них.

Исходники остаются в репозитории (GitHub, источники данных); сайт собирает главную из карты, обзора архитектуры,
терминов и типов данных, а ссылки на ушедшие страницы переводит на новые места.
"""
import os
import re
from pathlib import Path

import datamodel as DM
import integrations as IG

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

# не отдельные страницы сайта
NOT_PAGE_DIRS = ("docs/how/",)  # «Как работает» встраивается в страницу компонента
NOT_PAGES = {"README.md", "architecture.md", "docs/api/README.md", "docs/techspec/README.md",
             "docs/stories/README.md", "docs/stories/coverage.md"}

STORE_PAGE = {"s1": "icplan", "s1-tools": "mcp-tools", "s2": "platform-module", "s3": "agent-runner", "s6": "llm-gateway"}


def model_owner(name: str):
    """Компонент, на странице которого описана модель: первый по порядку компонент, где она встречается."""
    from components import COMPONENTS
    for c in COMPONENTS:
        if name in IG.models_of(c[0]):
            return c[0]
    return None


def _model_target(anchor: str):
    m = re.match(r"model-(\w+)", anchor or "")
    if not m:
        return None
    name = next((k for k in DM.MODELS if k.lower() == m.group(1)), None)
    owner = name and model_owner(name)
    return (f"docs/api/{owner}.md", f"model-{m.group(1)}") if owner else None  # контракты — на вкладке «Интеграции» (О-57)


def moved(target: str, anchor: str):
    """(путь от корня, якорь) ушедшей страницы → новое место или None."""
    m = re.match(r"docs/how/([a-z-]+)\.md$", target)
    if m:
        return f"components/{m.group(1)}/index.md", anchor or "how"
    if target == "README.md":
        return "index.md", ""
    if target == "architecture.md":
        return "index.md", anchor
    if target == "data-model.md":
        if anchor == "naming":
            return "docs/rules/data-methodology.md", "naming"
        if anchor == "terms":
            return "docs/rules/terms.md", ""
        if anchor in STORE_PAGE:
            return f"data-by-component/{STORE_PAGE[anchor]}/index.md", "stores"
        return _model_target(anchor) or ("docs/rules/data-methodology.md", "")
    if target == "docs/api/README.md":
        a = "model-" + anchor.split("-")[0] if anchor else ""
        return _model_target(a) or ("docs/rules/api-methodology.md", "")
    if target == "docs/techspec/README.md":
        return "docs/rules/tech-spec.md", ""
    if target in ("docs/stories/README.md", "docs/stories/coverage.md"):
        return "docs/stories/personas.md", ""
    if target == "specs-by-component/index.md":
        return "index.md", ""
    return None


def relink(text: str, src_rel: str, page_rel: str = None) -> str:
    """Ссылки исходника src_rel (путь от корня) для страницы page_rel: переезды и смена папки."""
    page_rel = page_rel or src_rel
    src_dir = os.path.dirname(src_rel)
    page_dir = os.path.dirname(page_rel)

    def fix(m):
        url = m.group(1)
        if re.match(r"^(https?:|mailto:|#)", url):
            return m.group(0)
        path, _, anchor = url.partition("#")
        if not path:
            return m.group(0)
        target = os.path.normpath(os.path.join(src_dir, path)).replace("\\", "/")
        new = moved(target, anchor)
        npath, nanchor = new if new else (target, anchor)
        if npath == page_rel:
            return f"](#{nanchor})" if nanchor else "](#)"
        r = os.path.relpath(npath, page_dir or ".").replace("\\", "/")
        return f"]({r}{'#' + nanchor if nanchor else ''})"
    return re.sub(r"\]\(([^)\s]+)\)", fix, text)


def home_page(home_md: str, flow_page) -> str:
    """Главная: карта (C2) + обзор архитектуры; термины и типы данных — в «Справке» (architecture-methodology.md)."""
    arch = (ROOT / "architecture.md").read_text(encoding="utf-8")
    arch = re.sub(r"^# .*\n", "", arch, count=1)
    arch = relink(arch, "architecture.md", "index.md")
    import datamodel as DM  # базы на схеме развёртывания — из DATABASES (D22)
    c = DM.DB_CLUSTER
    dbs = ['      PB["PgBouncer"] --> PG', f'      subgraph PG["{c["engine"]} · {c["operator"]}"]']
    dbs += [f'        DB_{db}[("{db}<br/>{" · ".join(d["schemas"])}")]' for db, d in DM.DATABASES.items()]
    dbs += ["      end"]
    arch = arch.replace("      %% databases — генерируется из datamodel.DATABASES (D22)", "\n".join(dbs), 1)
    body = "\n\n# Обзор архитектуры\n" + arch
    return home_md.rstrip("\n") + "\n" + flow_page(body, "index", IG.names(__import__("components").COMPONENTS), "")
