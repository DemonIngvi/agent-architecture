"""Инструмент правил документации: правило в момент правки вместо чтения всех правил (R&D doc-automation, О-51).

    python html-view/doctool.py route <файл>      тип документа, выжимка правил, методология (из doc-types.md, doc-work.md)
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
    hit = None
    for t in types:
        for pat in _patterns(t.get("Где", "")):
            if fnmatch.fnmatch(r, pat) or fnmatch.fnmatch(r, pat.rstrip("/") + "/*") or r == pat.rstrip("/"):
                hit = t
                break
        if hit:
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
        w = next((x for x in work if key and key in _plain(x.get("Документ", "")).lower()), None)
        if w:
            L.append(f"- Источник: {_plain(w.get('Что править (источник)', ''))}. Проверка: {_plain(w.get('Проверка', ''))}.")
    L.append("- После правки: python html-view/doctool.py check")
    return "\n".join(L)


def check() -> list:
    """Проверки сборки без сборки сайта."""
    sys.path.insert(0, str(HERE))
    with contextlib.redirect_stdout(io.StringIO()):
        import build as B
        issues = B.check_docs() + B.check_req_tasks()
    return issues


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
        issues = check() if re.search(r"\.(md|py)$", f) else []
        if issues:
            ctx += "\n\nЗамечания проверок после правки:\n" + "\n".join(f"- {i}" for i in issues[:15])
        if ctx:
            print(json.dumps({"hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": ctx}}, ensure_ascii=False))
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
