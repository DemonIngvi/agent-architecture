"""Пакет проверки документа ролью (`./tools/doc review-pack <страница> <буква>`): весь нужный контекст в одном файле.

Экономит токены проверяющего: вместо чтения методологий, спек и замечаний целиком — страница, вопрос роли,
чек-лист методологии её типа, требования страницы (заголовки и сценарии), открытые вопросы по ним, прежние замечания,
пробелы lint компонента (approval-methodology.md, «Экономная проверка»).
"""
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
METHOD = {"Блок": "block-methodology.md", "Архитектура компонента": "architecture-methodology.md", "Интеграции": "api-methodology.md",
          "Данные": "data-methodology.md", "Deploy": "tech-spec.md", "User Stories": "us-methodology.md", "Задача": "task-methodology.md",
          "R&D": "rnd-methodology.md", "Решения (design)": "decision-methodology.md", "Методология": "support-docs-methodology.md",
          "Главная": "architecture-methodology.md"}


def _section(text, title_re):
    m = re.search(rf"^## {title_re}[^\n]*\n(.*?)(?=^## |\Z)", text, re.M | re.S)
    return m.group(1).strip() if m else ""


def _reqs(text):
    """Заголовки и сценарии требований, на которые ссылается страница."""
    ids = sorted(set(re.findall(r"\bR-[A-Z]+-\d+\b", text)), key=lambda x: (x.split("-")[1], int(x.split("-")[2])))
    out, qs = [], set()
    specs = list(ROOT.glob("openspec/changes/*/specs/*/spec.md"))
    for rid in ids:
        for f in specs:
            t = f.read_text(encoding="utf-8")
            if f"`{rid}`" not in t:
                continue
            for block in re.split(r"\n(?=### Requirement: )", t):
                if f"`{rid}`" in block:
                    title = block.split("\n", 1)[0].replace("### Requirement: ", "")
                    sc = re.findall(r"#### Scenario: ([^\n]+)\n- \*\*WHEN\*\* ([^\n]+)\n- \*\*THEN\*\* ([^\n]+)", block)
                    out.append(f"- **{rid}** {title}: " + "; ".join(f"«{n}» — когда {w} → {th}" for n, w, th in sc))
                    qs.add(f.parent / "open-questions.md")
            break
    return out, qs


def pack(page: str, letter: str) -> Path:
    import sys
    sys.path.insert(0, str(HERE))
    import approvals as A
    import lint as LN
    built = HERE / ".build/docs" / page
    if not built.exists():
        raise SystemExit(f"{page}: нет собранной страницы — python html-view/build.py")
    text = built.read_text(encoding="utf-8")
    rule = A.rule_of(page)
    kind = rule[0] if rule else "—"
    roles = (ROOT / "docs/rules/approval-methodology.md").read_text(encoding="utf-8")
    role_row = next((l for l in roles.splitlines() if l.startswith(f"| **{letter}** |")), "")
    meth = (ROOT / "docs/rules" / METHOD.get(kind, "doc-types.md")).read_text(encoding="utf-8")
    check = _section(meth, "Чек-лист") or _section(meth, "Из чего состоит")
    reqs, qfiles = _reqs(text)
    oq = [l for f in qfiles if f.exists() for l in f.read_text(encoding="utf-8").splitlines() if l.startswith("| ОВ-")]
    comp = page.split("/")[1] if page.startswith(("components/", "data-by-component/")) else Path(page).stem
    ff = ROOT / f"docs/reviews/findings/{comp}.md"
    prev = [l for l in (ff.read_text(encoding="utf-8").splitlines() if ff.exists() else []) if l.startswith("| Z-") and (page in l or Path(page).parent.name in l)]
    lint = LN.lint().get(comp, [])
    reg = [c for k, c in A.read_registry().items() if k == (page, letter)]
    L = [f"# Пакет проверки: `{page}` × {letter}", "",
         f"**Тип:** {kind}. **Вопрос роли:** {role_row}", "",
         "**Как решать (экономная проверка):** отказ — только за то, что мешает ответить на вопрос роли, с фактом-источником; "
         "не больше 3 замечаний; механическое уже проверил lint (ниже) — не повторять. Повторная проверка — только изменённое и закрытие прежних замечаний.", "",
         f"**Прежнее решение:** {(' | '.join(reg[0][5:8])) if reg else '—'}", "",
         "## Чек-лист методологии типа", "", check, "",
         f"## Требования страницы ({len(reqs)})", "", *(reqs or ["—"]), "",
         "## Открытые вопросы спек этих требований", "", *(oq or ["—"]), "",
         "## Прежние замечания по странице", "", *(prev or ["—"]), "",
         f"## lint компонента ({len(lint)})", "", *([f"- {x}" for x in lint] or ["—"]), "",
         "## Страница", "", text]
    out = HERE / ".review" / (page.replace("/", "__") + f"__{letter}.md")
    out.parent.mkdir(exist_ok=True)
    out.write_text("\n".join(L), encoding="utf-8")
    return out
