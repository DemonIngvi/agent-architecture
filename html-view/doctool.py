"""Инструмент правил документации: правило в момент правки вместо чтения всех правил (R&D doc-automation, О-51).

    python html-view/doctool.py route <файл>      тип документа, выжимка правил, методология (из doc-types.md, doc-work.md)
    python html-view/doctool.py next <файл>       следующие документы по графу связности и их методологии
    python html-view/doctool.py diagram <файл>    mermaid-схемы файла → HTML-страница (посмотреть отрисованной)
    python html-view/doctool.py move <старый> <новый>  переименовать документ и сразу обновить все ссылки на него
    python html-view/doctool.py blocks             заполненность карточек блоков: чего не хватает для реализации
    python html-view/doctool.py approve <страница> <буква> ok|no <комментарий> [--human]  решение роли по документу
    python html-view/doctool.py review-queue [буква]  что ждёт решения роли
    python html-view/doctool.py generated <файл>  если файл генерируется — откуда и чем; иначе пусто
    python html-view/doctool.py check             все проверки сборки без сборки сайта (секунды)
    python html-view/doctool.py rnd <slug> <тема> заготовка R&D v3.1, проходящая проверку структуры
    python html-view/doctool.py pre <файл>         до правки: код 2 и источник, если файл генерируется (любой агент)
    python html-view/doctool.py post <файл>        после правки: выжимка правил и замечания проверок (любой агент)
    python html-view/doctool.py staged             проверки для git pre-commit (код 1 при замечаниях)
    python html-view/doctool.py hook-pre|hook-post  то же для хуков Claude Code (JSON на stdin)

Выжимка строится из таблиц правил при каждом вызове — копий правил здесь нет.
"""
import contextlib
import fnmatch
import io
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
RULES = ROOT / "docs/rules"

# Генерируемые файлы: шаблон пути → (чем генерируется, что править)
GENERATED = [
    ("docs/stories/*.md", "html-view/build.py (sync_stories)", "html-view/stories.py"),
    ("openspec/changes/*/tasks.md", "python html-view/tasksmd.py", "docs/ROADMAP.md и docs/tasks/*.md"),
    ("openspec/changes/define-agent-platform/specs/*/architecture.md", "python html-view/archgen.py", "html-view/components.py, R&D «Риски и пересмотр»"),
    ("html-view/icplan_schema.json", "python html-view/schema_import.py", "схема форка ICPlan"),
    ("html-view/icplan_schema.meta.json", "python html-view/schema_import.py", "схема форка ICPlan"),
    ("html-view/icplan_openapi.json", "python html-view/openapi_import.py", "OpenAPI работающего ICPlan"),
    ("html-view/.build/*", "python html-view/build.py", "исходники в docs/, openspec/, html-view/*.py"),
    ("html-view/site/*", "python html-view/build.py", "исходники в docs/, openspec/, html-view/*.py"),
]


def rel(path) -> str:
    p = Path(path)
    try:
        return p.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return ""


def generated(path):
    r = rel(path)
    for pat, how, src in GENERATED:
        if fnmatch.fnmatch(r, pat):
            return how, src
    return None


def _rows(md: Path, header_start: str):
    """Строки таблицы, чей заголовок начинается с header_start: [{колонка: значение}]."""
    lines = md.read_text(encoding="utf-8").splitlines()
    out = []
    for i, l in enumerate(lines):
        if l.startswith(header_start):
            cols = [c.strip() for c in l.strip("|").split("|")]
            for row in lines[i + 2:]:
                if not row.startswith("|"):
                    break
                cells = [c.strip() for c in re.split(r"(?<!\\)\|", row.strip())[1:-1]]
                out.append(dict(zip(cols, cells)))
    return out


def _patterns(where: str):
    """Пути из ячейки «Где»: `docs/flows/<компонент>.md` → docs/flows/*.md."""
    pats = []
    for p in re.findall(r"`([^`]+)`", where):
        p = re.sub(r"<[^>]+>", "*", p).lstrip("./")
        p = p.replace(".../", "openspec/changes/*/specs/*/")
        pats.append(p if "/" in p or p.endswith(".md") else p)
    return pats


def _plain(s: str) -> str:
    return re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", s).replace("**", "")


def route(path) -> str:
    r = rel(path)
    if not r:
        return ""
    gen = generated(path)
    types = _rows(RULES / "doc-types.md", "| Тип |")
    work = _rows(RULES / "doc-work.md", "| Документ |")
    hit, best = None, None
    for t in types:  # побеждает строка, где путь стоит раньше: основное место документа (О-56)
        for k, pat in enumerate(_patterns(t.get("Где", ""))):
            if fnmatch.fnmatch(r, pat) or fnmatch.fnmatch(r, pat.rstrip("/") + "/*") or r == pat.rstrip("/"):
                score = (0 if "*" not in pat else 1, k)  # точный путь важнее шаблона, затем порядок в «Где»
                if best is None or score < best:
                    hit, best = t, score
                break
    if not hit and not gen:
        return ""
    L = [f"Правила для `{r}` (doctool route; подробно — docs/rules/doc-work.md):"]
    if gen:
        L.append(f"- ГЕНЕРИРУЕТСЯ ({gen[0]}): правь {gen[1]}, затем перегенерируй.")
    if hit:
        name = _plain(hit.get("Тип", ""))
        L.append(f"- Тип: {name}. Обязательно: {_plain(hit.get('Обязательные разделы', ''))}.")
        L.append(f"- Правила: {_plain(hit.get('Правила', ''))}.")
        if hit.get("Методология"):
            L.append("- Методология: " + re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1 (docs/rules/\2)", hit["Методология"]) + ".")
        L.append(f"- Синхронизировать: {_plain(hit.get('Синхронизировать', ''))}.")
        key = name.split()[0].lower() if name else ""
        # целым словом: «spec» не должен совпасть с «техспека» (О-58)
        w = next((x for x in work if key and re.search(rf"(?<![\w-]){re.escape(key)}(?![\w-])", _plain(x.get("Документ", "")).lower())), None)
        if w:
            L.append(f"- Источник: {_plain(w.get('Что править (источник)', ''))}. Проверка: {_plain(w.get('Проверка', ''))}.")
    L.append("- Перед правкой прочитай методологию; если она отстала от того, что меняешь, — сначала поправь её (и инструменты), потом документ.")
    L.append("- После правки: python html-view/doctool.py check; следующий документ — python html-view/doctool.py next <файл>")
    return "\n".join(L)


def node_of(path):
    """Узел графа связности (docgraph.PATHS), к которому относится файл."""
    sys.path.insert(0, str(HERE))
    import docgraph as G
    r = rel(path)
    gen = generated(path)
    for name, pats in G.PATHS.items():
        if any(fnmatch.fnmatch(r, p) for p in pats):
            return name
    if gen:  # генерируемый файл — узел его источника
        for name, pats in G.PATHS.items():
            if any(p in gen[1] or gen[1] in p for p in pats):
                return name
    return None


def next_docs(path) -> str:
    """Следующие документы по графу: по одному, у каждого — своя методология (О-58)."""
    sys.path.insert(0, str(HERE))
    import docgraph as G
    node = node_of(path)
    if not node:
        return f"{rel(path)}: нет узла в графе связности (html-view/docgraph.py PATHS) — проверь doc-types.md «Синхронизировать»."
    L = [f"Узел `{rel(path)}`: {node}. Дальше — по одному документу, в этом порядке:"]
    for a, b, what in G.EDGES:
        if a != node:
            continue
        sample = next((f for p in G.PATHS.get(b, []) for f in sorted(ROOT.glob(p))), None)
        meth = ""
        if sample:
            m = re.search(r"- Методология: (.+)\.", route(sample))
            meth = f" · методология: {m.group(1)}" if m else ""
        L.append(f"- {b} — проверить: {what} · файлы: {', '.join(G.PATHS.get(b, [])) or '—'}{meth}")
    name = Path(path).name
    if node.startswith("Методология") and name.endswith(".md"):  # после инструментов — документы, которые ведутся по этой методологии
        for t in _rows(RULES / "doc-types.md", "| Тип |"):
            if f"]({name}" in t.get("Методология", ""):
                L.append(f"- затем документы типа «{_plain(t.get('Тип', ''))}»: {', '.join(_patterns(t.get('Где', ''))) or '—'} — привести к новой методологии")
    if len(L) == 1:
        L.append("- исходящих связей нет: цепочка на этом узле заканчивается")
    L.append("Для каждого: прочитай методологию → устарела — сначала поправь её → правка → doctool check → doctool next <файл>. "
             "Документ не изменился по смыслу — дальше по его стрелкам не идёшь.")
    return "\n".join(L)


def tooling_check() -> list:
    """Инструменты соответствуют правилам (О-56): методологии из таблицы существуют, пути в навыках и AGENTS.md есть,
    route узнаёт основной путь каждого типа документа."""
    issues = []
    types = _rows(RULES / "doc-types.md", "| Тип |")
    for t in types:
        for f in re.findall(r"\]\(([\w.-]+\.md)", t.get("Методология", "")):
            if not (RULES / f).exists():
                issues.append(f"doc-types.md: методология {f} не найдена")
        pats = _patterns(t.get("Где", ""))
        if pats and "*" not in pats[0] and (ROOT / pats[0]).is_file():
            got = route(ROOT / pats[0])
            name = _plain(t.get("Тип", ""))
            if got and f"Тип: {name}." not in got:
                issues.append(f"doctool route {pats[0]}: выдаёт правила другого типа, ожидался «{name}»")
    # вкладки сайта = таблица «Вкладки компонента» методологии структуры (structure-methodology.md)
    sm = RULES / "structure-methodology.md"
    if sm.exists():
        tabs = [_plain(r.get("Вкладка", "")) for r in _rows(sm, "| Вкладка | Страница |")]
        import pagebar as PB
        site = [label for _, label, *_ in PB.TYPES]
        issues += [f"structure-methodology.md: вкладки «{x}» нет в pagebar.TYPES" for x in tabs if x not in site]
        issues += [f"pagebar.TYPES: вкладка «{x}» не описана в structure-methodology.md" for x in site if x not in tabs]
    sys.path.insert(0, str(HERE))
    import docgraph as G
    names = {n for _, ns in G.LAYERS for n in ns}
    issues += [f"docgraph.EDGES: узел «{x}» не в LAYERS" for e in G.EDGES for x in e[:2] if x not in names]
    issues += [f"docgraph.PATHS: у узла «{n}» нет ни одного файла" for n, ps in G.PATHS.items() if not any(ROOT.glob(p) for p in ps)]
    for f in [ROOT / "AGENTS.md", *ROOT.glob(".claude/skills/doc-*/SKILL.md"), *ROOT.glob(".claude/agents/*.md")]:
        for p in re.findall(r"`((?:html-view|docs|tools|\.claude|\.githooks)/[\w./-]+?)`", f.read_text(encoding="utf-8")):
            if "<" in p or "*" in p:
                continue
            if not (ROOT / p).exists():
                issues.append(f"{f.relative_to(ROOT).as_posix()}: путь `{p}` не существует")
    return issues


def check() -> list:
    """Проверки сборки без сборки сайта + соответствие инструментов правилам."""
    sys.path.insert(0, str(HERE))
    with contextlib.redirect_stdout(io.StringIO()):
        import build as B
        issues = B.check_docs() + B.check_req_tasks()
    return issues + tooling_check()


RND = """# R&D: {title}

← [Все R&D](README.md) · [методология R&D v3.1](../rules/rnd-methodology.md)

<div class="rnd-hero" markdown>
<div class="rnd-q">Вопрос</div>
…

<div class="rnd-a">Ответ: …</div>

<span class="rnd-badge assess">Assess</span> черновик · данные …
</div>

```deck
# Покрытие потребностей
> …
stack A. …: 0 ok, 0 part, 0 no
```

<div class="rnd-grid" markdown>
<div class="take" markdown>
**Берём**

- …
</div>
<div class="adapt" markdown>
**Адаптируем**

- …
</div>
<div class="drop" markdown>
**Не берём**

- …
</div>
</div>

<div class="rnd-grid" markdown>
<div class="no" markdown>
**Отсеяны до сравнения**

- …
</div>
<div class="risk" markdown>
**Риски и пересмотр**

- …
</div>
</div>

{stages}
## Источники

- …
"""


def rnd(slug: str, title: str) -> Path:
    names = ["Вопрос", "Потребности", "Опорное решение: как сейчас", "Аналоги и их ключевые функции", "Ценность функций",
             "Перенос и критерии", "Отсев и встраивание", "Спор ролей", "Выбор", "Последствия"]
    st = ""
    for n, name in enumerate(names, 1):
        body = "- **Утверждение.** …\n- **Когда неверно.** …\n" if n == 9 else \
            "| Изменение | Документ | Статус |\n|---|---|---|\n| … | … | 📌 предложено |\n" if n == 10 else "…\n"
        st += f"## Э{n}. {name} {{#e{n}}}\n\n{body}\n<span class=\"gate\">G{n}</span> ✅ …\n\n"
    p = ROOT / f"docs/rnd/{slug}.md"
    if p.exists():
        raise SystemExit(f"{p} уже есть")
    p.write_text(RND.format(title=title, stages=st), encoding="utf-8")
    return p


def diagram(path) -> Path:
    """Отрисовать mermaid-схемы файла (ответ по архитектуре, R&D, спека) в HTML-страницу (FORMAT.md)."""
    src = Path(path)
    text = src.read_text(encoding="utf-8")
    blocks = re.findall(r"```mermaid\n(.*?)```", text, flags=re.S)
    if not blocks:
        raise SystemExit(f"{src}: нет блоков ```mermaid")
    import html as H
    title = next((l[2:].strip() for l in text.splitlines() if l.startswith("# ")), src.stem)
    body = "\n".join(f'<pre class="mermaid">{H.escape(b)}</pre>' for b in blocks)
    page = (f'<!doctype html><html lang="ru"><head><meta charset="utf-8"><title>{H.escape(title)}</title>'
            '<style>body{font-family:system-ui,sans-serif;margin:24px;background:#fff;color:#212121}pre.mermaid{margin:32px 0}</style></head>'
            f'<body><h1>{H.escape(title)}</h1>{body}'
            '<script type="module">import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11.4.1/dist/mermaid.esm.min.mjs";'
            'mermaid.initialize({startOnLoad:true,securityLevel:"loose",flowchart:{htmlLabels:true}});</script></body></html>')
    out = HERE / ".diagrams" / (src.stem + ".html")
    out.parent.mkdir(exist_ok=True)
    out.write_text(page, encoding="utf-8")
    return out


def move(old, new) -> list:
    """Переименование или перенос документа одним шагом (change-process.md#links): файл + все ссылки и упоминания пути."""
    import os
    import subprocess
    o, n = (ROOT / old).resolve(), (ROOT / new).resolve()
    if not o.exists():
        raise SystemExit(f"{old}: нет такого файла")
    n.parent.mkdir(parents=True, exist_ok=True)
    if subprocess.run(["git", "mv", str(o), str(n)], cwd=ROOT, capture_output=True).returncode:
        o.rename(n)
    ro, rn = o.relative_to(ROOT).as_posix(), n.relative_to(ROOT).as_posix()
    changed = []
    for f in [*ROOT.rglob("*.md"), *ROOT.glob("html-view/*.py"), *ROOT.glob(".claude/skills/*/SKILL.md")]:
        if any(p in f.parts for p in (".build", "site", ".venv", "node_modules", ".git")):
            continue
        t0 = t = f.read_text(encoding="utf-8")

        def fix(m):  # относительная ссылка, указывающая на старый путь
            u, anchor = (m.group(2).split("#", 1) + [""])[:2]
            if not u or re.match(r"^(https?:|mailto:)", u):
                return m.group(0)
            base = (n.parent if f.resolve() == n else f.parent)
            src_dir = (o.parent if f.resolve() == n else f.parent)
            if (src_dir / u).resolve() != o:
                return m.group(0)
            r = os.path.relpath(n, base).replace("\\", "/")
            return f"{m.group(1)}({r}{'#' + anchor if anchor else ''})"
        if f.suffix == ".md":
            t = re.sub(r"(\]|\]\s?)\(([^)\s]+)\)", fix, t)
        t = t.replace(f"`{ro}`", f"`{rn}`").replace(f'"{ro}"', f'"{rn}"')
        if t != t0:
            f.write_text(t, encoding="utf-8", newline=chr(10))  # LF, как в репозитории
            changed.append(f.relative_to(ROOT).as_posix())
    return changed


def _hook_input():
    try:
        d = json.loads(sys.stdin.buffer.read().decode("utf-8"))
    except Exception:
        return None
    return (d.get("tool_input") or {}).get("file_path") or (d.get("tool_input") or {}).get("notebook_path")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    cmd, args = (sys.argv[1] if len(sys.argv) > 1 else ""), sys.argv[2:]
    if cmd == "route":
        print(route(args[0]) or "нет правил для этого пути")
    elif cmd == "approve":  # решение роли по документу (approval-methodology.md)
        sys.path.insert(0, str(HERE))
        import approvals as AP
        human = "--human" in args
        rest = [x for x in args if x != "--human"]
        print(AP.set_decision(rest[0], rest[1], rest[2] in ("ok", "✅", "да"), " ".join(rest[3:]), human=human))
    elif cmd == "review-queue":  # что ждёт решения роли
        sys.path.insert(0, str(HERE))
        import approvals as AP
        q = AP.queue(args[0] if args else "")
        print(f"ждёт решения: {len(q)}")
        for p, r in q[:200]:
            print(f"- {p} × {r}")
    elif cmd == "review-pack":  # пакет проверки: весь контекст роли в одном файле (approval-methodology.md)
        sys.path.insert(0, str(HERE))
        import review as RV
        p = RV.pack(args[0], args[1])
        print(f"{p} — {len(p.read_text(encoding='utf-8')) // 4} ток. (примерно)")
    elif cmd == "lint":  # нестрогие проверки методологий по компонентам (не блокируют коммит)
        sys.path.insert(0, str(HERE))
        import lint as LN
        res = LN.lint()
        for comp in sorted(res):
            if args and comp != args[0]:
                continue
            print(f"{comp}: {len(res[comp])}")
            for m in res[comp]:
                print(f"  - {m}")
        if not res or (args and args[0] not in res):
            print("пробелов нет")
    elif cmd == "finding":  # статус замечания на вкладке «Замечания» (review-methodology.md#findings)
        comp, fid, st = args[0], args[1], args[2]
        note = " ".join(args[3:])
        f = ROOT / f"docs/reviews/findings/{comp}.md"
        lines = f.read_text(encoding="utf-8").split(chr(10))
        mark = {"ok": "✅", "wait": "⏳", "owner": "📌"}[st]
        n = 0
        for i, l in enumerate(lines):
            for one in fid.split(","):
                if l.startswith(f"| {one.strip()} |"):
                    cells = l.rstrip().rstrip("|").split(" | ")
                    cells[-1] = mark + (f" {note}" if note else "")
                    lines[i] = " | ".join(cells) + " |"
                    n += 1
        f.write_text(chr(10).join(lines), encoding="utf-8", newline=chr(10))
        print(f"{comp}: обновлено {n}")
    elif cmd == "blocks":  # заполненность карточек блоков (block-methodology.md)
        sys.path.insert(0, str(HERE))
        with contextlib.redirect_stdout(io.StringIO()):
            import build as B
        rows = [(slug, title, *B.block_card(slug, title, s)) for (slug, title), s in B.SUB.items() if not s["tech"].startswith("→ ")]
        full = sum(1 for r in rows if not r[3])
        print(f"блоков {len(rows)}, карточка заполнена полностью у {full}")
        for slug, title, ok, miss in rows:
            if miss:
                print(f"- {slug} / {title}: {len(ok)}/{len(ok) + len(miss)}, нет: {', '.join(miss)}")
    elif cmd == "move":
        ch = move(args[0], args[1])
        print(f"перенесено: {args[0]} → {args[1]}; ссылки обновлены в {len(ch)} файлах" + ("".join(f"\n- {c}" for c in ch)))
        print("Проверь: python html-view/build.py (битые ссылки и «сироты»)")
    elif cmd == "diagram":
        print(diagram(args[0]).as_uri())
    elif cmd == "next":
        print(next_docs(args[0]))
    elif cmd == "generated":
        g = generated(args[0])
        print(f"генерируется: {g[0]}; править: {g[1]}" if g else "")
    elif cmd == "check":
        issues = check()
        print("\n".join(f"⚠️ {i}" for i in issues) or "замечаний нет")
        sys.exit(1 if issues else 0)
    elif cmd == "rnd":
        print(rnd(args[0], " ".join(args[1:]) or args[0]))
    elif cmd == "pre":
        g = generated(args[0])
        if g:
            print(f"{rel(args[0])} генерируется ({g[0]}). Правь источник: {g[1]}.", file=sys.stderr)
            sys.exit(2)
    elif cmd == "post":
        out = route(args[0])
        issues = check()
        print(out + ("\n\nЗамечания проверок:\n" + "\n".join(f"- {i}" for i in issues) if issues else ""))
    elif cmd == "staged":
        import subprocess
        files = subprocess.run(["git", "diff", "--cached", "--name-only"], capture_output=True, text=True, encoding="utf-8").stdout.split()
        bad = [f for f in files if generated(ROOT / f) and not f.startswith("html-view/") and not f.startswith("docs/stories/") and not f.endswith("tasks.md") and not f.endswith("architecture.md")]
        issues = check()
        for f in bad:
            print(f"⚠️ {f}: генерируемый файл изменён — правь источник ({generated(ROOT / f)[1]})")
        for i in issues:
            print(f"⚠️ {i}")
        sys.exit(1 if issues or bad else 0)
    elif cmd == "hook-pre":
        f = _hook_input()
        g = generated(f) if f else None
        if g and not rel(f).startswith("html-view/"):  # данные импорта правят скрипты, не руками
            print(f"{rel(f)} генерируется ({g[0]}). Правь источник: {g[1]}.", file=sys.stderr)
            sys.exit(2)
        if g and rel(f).endswith(".json"):
            print(f"{rel(f)} генерируется ({g[0]}). Не правь руками: {g[1]}.", file=sys.stderr)
            sys.exit(2)
    elif cmd == "hook-post":
        f = _hook_input()
        if not f or not rel(f):
            return
        ctx = route(f)
        if ctx and node_of(f):
            ctx += "\n\n" + next_docs(f)
        issues = check() if re.search(r"\.(md|py)$", f) else []
        if issues:
            ctx += "\n\nЗамечания проверок после правки:\n" + "\n".join(f"- {i}" for i in issues[:15])
        if ctx:
            print(json.dumps({"hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": ctx}}, ensure_ascii=False))
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
