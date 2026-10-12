"""Нестрогие проверки методологий (`./tools/doc lint`): не блокируют коммит, показывают пробелы по компонентам.

Правила из методологий, которые ещё не выполнены во всех компонентах: строгой проверкой они остановили бы любой коммит
до того, как компонент пройдёт свою проверку ролями. Компонент, прошедший проверку, должен давать пустой отчёт.
"""
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
WRITE = re.compile(r"^(POST|PUT|PATCH|DELETE) ")
ENDPOINT = re.compile(r"`(GET|POST|PUT|PATCH|DELETE) /|`/[a-z]")


def _api_status():
    """(метод путь) → (страница, статус) из таблиц docs/api/*.md."""
    out = {}
    for f in (ROOT / "docs/api").glob("*.md"):
        for l in f.read_text(encoding="utf-8").splitlines():
            if l.startswith('| <span class="m '):
                c = [x.strip() for x in re.split(r"(?<!\\)\|", l)[1:-1]]
                m = re.sub(r"<[^>]+>", "", c[0]).strip()
                p = c[1].strip("`").split(" ")[0]
                out[f"{m} {p}"] = (f.stem, "new" if "🆕" in c[2] else "fork" if "🛠" in c[2] else "ok")
    return out


def lint() -> dict:
    """→ {компонент: [замечание]}."""
    import sys
    sys.path.insert(0, str(HERE))
    import datamodel as DM
    from components import BLOCKS, COMPONENTS, HOST
    from stories import BPMN
    from subcomponents import SUB
    res = {}

    def add(slug, msg):
        res.setdefault(slug, []).append(msg)

    # блоки: экраны «новое» / «доработка» без эндпоинта; S-коды вместо таблиц (block-methodology.md)
    for (slug, title), s in SUB.items():
        for sc in s.get("screens", []):
            if sc[3] in ("новое", "доработка") and not ENDPOINT.search(sc[2]) and "не решено" not in sc[1]:
                add(slug, f"блок «{title}», экран «{sc[0]}» ({sc[3]}): нет эндпоинта для действий")
        for d, _ in s.get("data", []):
            if re.match(r"S\d+\b", d):
                add(slug, f"блок «{title}»: в «Данных» S-код «{d[:30]}» вместо имён таблиц")
    # API: изменяющие эндпоинты 🆕 / 🛠 без кодов ошибок (api-methodology.md)
    for key, (page, st) in _api_status().items():
        if st in ("new", "fork") and WRITE.match(key):
            io = DM.ENDPOINT_IO.get(key)
            if io and "ошибк" not in io[2]:
                add(page, f"{key} ({'🆕' if st == 'new' else '🛠'}): нет кодов ошибок в ENDPOINT_IO")
    # задачи: нумерация с N.M.1 и подзадачи 2–8 ч (task-methodology.md)
    tid_owner = {t: c[0] for c in COMPONENTS for t in c[7]}
    for f in sorted((ROOT / "docs/tasks").glob("*.md")):
        tid = f.name.split("-")[0]
        rows = re.findall(rf"^\| ({re.escape(tid)}\.(\d+)) \| [^|]+\| (\d+(?:\.\d+)?) \|", f.read_text(encoding="utf-8"), re.M)
        owner = tid_owner.get(tid, "задачи")
        if rows and rows[0][1] != "1":
            add(owner, f"задача {tid}: подзадачи начинаются с {rows[0][0]}, а не {tid}.1")
        for num, _, h in rows:
            if not 2 <= float(h) <= 8:
                add(owner, f"задача {tid}: подзадача {num} — {h} ч (нужно 2–8)")
    # истории: у каждого процесса BPMN — ветка ошибки (us-methodology.md)
    for slug, procs in BPMN.items():
        for p in (procs if isinstance(procs, list) else [procs]):
            if not any(st[2] == "error" for st in p.get("steps", [])):
                add(slug, f"процесс «{p.get('title', 'основной')}»: нет ветки ошибки")
    # архитектура: встроенный — внутри зоны хоста на карте (architecture-methodology.md)
    for owner, host in HOST.items():
        if isinstance(owner, tuple):
            continue

        def zone_refs(rows, inzone=False):
            for r in rows:
                if isinstance(r, dict):
                    yield from zone_refs(r["rows"], True)
                elif isinstance(r, list):
                    for b in r:
                        if b.get("to") == owner and inzone:
                            yield b
        if not list(zone_refs(BLOCKS.get(host, []))):
            add(host, f"карта: встроенный «{owner}» не внутри зоны хоста")
    # задачи: новые таблицы и колонки компонента названы хотя бы в одной его задаче — иначе миграцию никто не делает (task-methodology.md)
    tasks_text = {c[0]: " ".join((p.read_text(encoding="utf-8") for t in c[7] for p in (ROOT / "docs/tasks").glob(f"{t}-*.md"))) for c in COMPONENTS}
    for t, (store, owner, cols) in DM.PLATFORM_TABLES.items():
        if owner in tasks_text and t not in tasks_text[owner]:
            add(owner, f"таблица `{t}`: не названа ни в одной задаче компонента (миграция)")
    for t, cols in DM.FORK_COLUMNS.items():
        for col, *_ in cols:
            if f"{t}.{col}" not in tasks_text.get("icplan", "") and f"`{col}`" not in tasks_text.get("icplan", ""):
                add("icplan", f"колонка `{t}.{col}`: не названа ни в одной задаче ICPlan (миграция форка)")
    # R&D: в микропрезентации есть слайд объёма доработки (rnd-methodology.md#deck)
    from rationale import REFS
    for slug, refs in REFS.items():
        for _, p in refs:
            f = ROOT / p
            if p.startswith("docs/rnd/") and f.exists():
                txt = f.read_text(encoding="utf-8")
                if "## Э10." in txt and "```deck" in txt and not re.search(r"^# Объём", txt.split("```deck", 1)[1].split("```", 1)[0], re.M):
                    add(slug, f"R&D {f.name}: в deck нет слайда «Объём доработки»")
    # блоки: карточка заполнена полностью — иначе роли Р и Т отказывают (block-methodology.md#ready)
    import contextlib
    import io as _io
    with contextlib.redirect_stdout(_io.StringIO()):
        import build as B
    for (slug, title), s in SUB.items():
        if not s["tech"].startswith("→ "):
            _, miss = B.block_card(slug, title, s)
            if miss:
                add(slug, f"блок «{title}»: карточка не заполнена — {', '.join(miss)}")
    # Deploy: у компонента с данными — «Обновление и откат» (tech-spec.md)
    for c in COMPONENTS:
        f = ROOT / f"docs/techspec/{c[0]}.md"
        if DM.STORES.get(c[0]) and f.exists() and "## Обновление и откат" not in f.read_text(encoding="utf-8"):
            add(c[0], "Deploy: нет раздела «Обновление и откат»")
    return res
