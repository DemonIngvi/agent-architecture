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


PIPE = re.compile(r"(?<!\\)\|")
TECH_REQS = ("Конфигурация модуля", "Интерфейсы обмена")  # проверяются общей подзадачей (Z-ICP-93 отклонено)
TECH_SUB = "Хранилища данных"  # тоже, если есть подзадача «… по `interfaces.md`»


def _sec(t, h):
    """Тело раздела «## h» до следующего «## »."""
    m = re.search(rf"^## {h}[^\n]*\n(.*?)(?=^## |\Z)", t, re.M | re.S)
    return m.group(1) if m else ""


def _specs():
    """[(путь spec.md, имя capability, {R-ID: (заголовок, {задачи}, [сценарии])})]."""
    out = []
    for sp in sorted(ROOT.glob("openspec/changes/*/specs/*/spec.md")):
        req = {}
        for blk in re.split(r"\n(?=<a id=\"r-)", sp.read_text(encoding="utf-8"))[1:]:
            m = re.search(r"\*\*ID:\*\* `(R-[A-Z]+-\d+)` · \*\*Реализует задача:\*\* ([^\n]*)", blk)
            h = re.search(r"### Requirement: (.*)", blk)
            if m and h:
                req[m.group(1)] = (h.group(1).strip(), set(re.findall(r"tasks/(\d\.\d)-", m.group(2))),
                                   [s.strip() for s in re.findall(r"#### Scenario: (.*)", blk)])
        out.append((sp, sp.parent.name, req))
    return out


def _tasks():
    """[(id, имя файла, текст)] — без закрытых дублей."""
    return [(f.name.split("-")[0], f.name, t) for f in sorted((ROOT / "docs/tasks").glob("*.md"))
            if "**Статус:** ❌ закрыта" not in (t := f.read_text(encoding="utf-8"))]


def rule_acceptance(specs, tasks):
    """task-methodology 2б: каждое требование из «Закрывает требования» названо в «Приёмке» или подзадаче (R-код или имя сценария)."""
    req = {r: v for _, _, rs in specs for r, v in rs.items()}
    for tid, _, t in tasks:
        body = _sec(t, "Приёмка") + _sec(t, "Декомпозиция")
        low = body.lower()
        tech = TECH_REQS + ((TECH_SUB,) if "interfaces.md" in _sec(t, "Декомпозиция") else ())
        miss = [r for r in re.findall(r"\[(R-[A-Z]+-\d+)\]", _sec(t, "Закрывает требования"))
                if r not in body and req.get(r, ("",))[0] not in tech
                and not any(len(s) > 6 and s.lower() in low for s in req.get(r, ("", set(), []))[2])]
        if miss:
            yield tid, (f"задача {tid}: приёмка и подзадачи не покрывают {', '.join(miss)} → строка приёмки "
                        "«сценарий → результат (R-код)» по сценариям требования, включая отказы")


def rule_estimate(tasks):
    """task-methodology 2: «Итого» = сумма подзадач, сумма в днях (8 ч) — в диапазоне шапки «Человек»."""
    for tid, _, t in tasks:
        hrs = [float(h) for h in re.findall(rf"^\| {re.escape(tid)}\.\d+ \| [^|]+\| (\d+(?:\.\d+)?) \|", t, re.M)]
        tot = re.search(r"\*\*Итого\*\* \| \*\*(\d+(?:\.\d+)?) ч", t)
        rng = re.search(r"\| (\d+(?:\.\d+)?)(?:–(\d+(?:\.\d+)?))? дн \|", t.split("<!-- req-tasks -->")[0])
        if not hrs:
            continue
        if tot and abs(float(tot.group(1)) - sum(hrs)) > 0.01:
            yield tid, f"задача {tid}: «Итого» {tot.group(1)} ч ≠ сумме подзадач {sum(hrs):g} ч → пересчитать итог"
        if rng and not float(rng.group(1)) - 0.25 <= sum(hrs) / 8 <= float(rng.group(2) or rng.group(1)) + 0.25:
            yield tid, (f"задача {tid}: подзадачи {sum(hrs):g} ч ≈ {sum(hrs) / 8:.1f} дн вне оценки шапки "
                        f"{rng.group(1)}–{rng.group(2) or rng.group(1)} дн → поправить оценку или подзадачи (и Roadmap)")


def rule_open_questions(tasks, sub):
    """task-methodology 2а: открытый пункт задачи и карточка блока ссылаются только на открытый ОВ (есть в open-questions.md)."""
    opened = {q for f in ROOT.glob("openspec/changes/*/specs/*/open-questions.md")
              for q in re.findall(r"^\| (ОВ-[\w-]+-\d+) \|", f.read_text(encoding="utf-8"), re.M)}
    for tid, _, t in tasks:
        for l in _sec(t, "Что проработать").splitlines():
            for q in re.findall(r"ОВ-[a-z][\w-]*-\d+", l) if l.startswith("- [ ]") else []:
                if q not in opened:
                    yield tid, f"задача {tid}: открытый пункт ссылается на {q}, которого нет среди открытых → [x] со ссылкой на решение (D, требование) или вернуть вопрос в open-questions.md"
    for (slug, title), s in sub.items():
        for q in set(re.findall(r"ОВ-[a-z][\w-]*-\d+", repr(s))) - opened:
            yield slug, f"блок «{title}»: упомянут закрытый {q} → заменить ссылкой на решение (D, требование)"


def rule_fmea(specs):
    """spec-criteria §3, change-process: у каждой строки FMEA interfaces.md — сценарий отказа в спеке (имя отказа = имя сценария; хранилище S<n> — «S<n> недоступно»)."""
    for sp, cap, req in specs:
        itf = sp.with_name("interfaces.md")
        fm = _sec(itf.read_text(encoding="utf-8"), r"Отказы \(FMEA\)") if itf.exists() else ""
        norm = lambda x: re.sub(r"\s*\([^)]*\)|`", "", x).strip().lower()
        scen = {norm(s) for _, _, sc in req.values() for s in sc}
        for l in fm.splitlines():
            if not l.startswith("| ") or l.startswith(("| Отказ", "|---")):
                continue
            row = PIPE.split(l)[1].strip()
            n = norm(row)
            if any(n == s or n.startswith(s + " ") or s.startswith(n + " ") for s in scen):
                continue
            if any(f"s{k} недоступн" in " ".join(scen) for k in re.findall(r"\bS(\d+)\b", row)):
                continue
            yield cap, f"{cap}: строка FMEA «{row}» без сценария отказа в spec.md → сценарий с тем же именем в «Поведение при отказах» (или «S<n> недоступно» в «Хранилищах данных»)"


def rule_rtm(specs, stories):
    """spec-criteria §5: строка RTM = требование — та же задача («Реализует задача»), то же число сценариев, те же истории."""
    for sp, cap, req in specs:
        st = {}  # заголовок требования → истории, ссылающиеся на него («<capability>: <заголовок>»)
        for s in (x for lst in stories.values() for x in lst):
            for r in s[5]:
                if r.startswith(cap + ": "):
                    st.setdefault(r.split(": ", 1)[1].strip(), set()).add(s[0])
        rtm = sp.with_name("traceability.md")
        for l in rtm.read_text(encoding="utf-8").splitlines() if rtm.exists() else []:
            c = PIPE.split(l)[1:-1] if l.startswith("| [R-") else []
            rid = re.search(r"R-[A-Z]+-\d+", c[0]).group(0) if len(c) >= 5 else None
            if rid not in req:
                continue
            title, tasks, sc = req[rid]
            us = set(re.findall(r"US-[A-Z]+-\d+", c[1]))
            if st.get(title, set()) - us:
                yield cap, f"{cap}: RTM {rid} — нет историй {sorted(st[title] - us)}, которые ссылаются на требование → добавить в колонку User Story"
            rt = set(re.findall(r"tasks/(\d\.\d)-", c[3]))
            if rt != tasks:
                yield cap, f"{cap}: RTM {rid} — задачи {sorted(rt)}, в spec.md «Реализует задача» {sorted(tasks)} → выровнять traceability.md"
            if c[4].strip().isdigit() and int(c[4]) != len(sc):
                yield cap, f"{cap}: RTM {rid} — «Сценариев» {c[4].strip()}, в spec.md {len(sc)} → поправить traceability.md"


def rule_screen_endpoints(sub, api, endpoint_io):
    """block-methodology, api-methodology: эндпоинт с экрана блока есть на странице API; 🆕 / 🛠 — и в ENDPOINT_IO."""
    for (slug, title), s in sub.items():
        for sc in s.get("screens", []):
            for m, p in re.findall(r"`(GET|POST|PUT|PATCH|DELETE) (/[^`\s?]*)", sc[2]):
                k = f"{m} {p}"
                if k not in api:
                    yield slug, f"блок «{title}», экран «{sc[0]}»: {k} нет на странице API → строка в docs/api/*.md (🆕 / 🛠)"
                elif api[k][1] != "ok" and k not in endpoint_io:
                    yield slug, f"блок «{title}», экран «{sc[0]}»: {k} нет в ENDPOINT_IO → тело, ответ, ошибки в datamodel.ENDPOINT_IO"


def rule_block_refs(sub, tables):
    """block-methodology: R-код и таблица, названные в карточке (экраны, операции, сбои, технология), — в её «Требованиях» и «Данных»."""
    for (slug, title), s in sub.items():
        if s.get("tech", "").startswith("→ "):
            continue
        txt = repr({k: v for k, v in s.items() if k not in ("data", "io", "stories", "tasks", "reqs")})
        miss = sorted(set(re.findall(r"R-[A-Z]+-\d+", txt)) - set(s.get("reqs", [])))
        if miss and s.get("reqs"):  # пустые reqs / data — уже «карточка не заполнена»
            yield slug, f"блок «{title}»: {', '.join(miss)} названы в карточке, но не в «Требованиях» (reqs) → добавить"
        data = {x.split(" ")[0].strip("`") for x, _ in s.get("data", [])}
        tbl = sorted((set(re.findall(r"`([a-z][a-z0-9_]+)(?:\.[a-z0-9_]+)?`", txt)) & tables) - data)
        if tbl and data:
            yield slug, f"блок «{title}»: таблицы {', '.join(tbl)} названы в карточке, но не в «Данных» → добавить с доступом (чтение / запись)"


def rule_deploy(components, platform_tables, fork_columns):
    """tech-spec.md: «Обновление и откат» у компонента с таблицами говорит о миграциях; параметры в S9 (values) → «Пример конфигурации»."""
    s9 = {}
    for f in ROOT.glob("openspec/changes/*/specs/*/interfaces.md"):
        for l in f.read_text(encoding="utf-8").splitlines():
            c = PIPE.split(l)
            if l.startswith("| `") and len(c) > 5 and "S9" in c[4]:
                s9.setdefault(f.parent.name, []).append(c[1].strip(" `"))
    owners = {v[1] for v in platform_tables.values()} | ({"icplan"} if fork_columns else set())
    for c in components:
        f = ROOT / f"docs/techspec/{c[0]}.md"
        if not f.exists():
            continue
        t = f.read_text(encoding="utf-8")
        up = _sec(t, "Обновление и откат")
        if c[0] in owners and up and "миграц" not in up.lower():
            yield c[0], "Deploy «Обновление и откат»: у компонента есть таблицы, но нет миграций → порядок миграции, откат после миграции"
        caps = [Path(p).parent.name for _, p in c[6] if p.endswith("spec.md")]
        ps = [p for cap in caps for p in s9.get(cap, [])]
        if ps and "## Пример конфигурации" not in t:
            yield c[0], f"Deploy: нет «Пример конфигурации», хотя параметры в values (S9): {', '.join(ps[:3])}{' …' if len(ps) > 3 else ''}"


def lint() -> dict:
    """→ {компонент: [замечание]}."""
    import sys
    sys.path.insert(0, str(HERE))
    import datamodel as DM
    from components import BLOCKS, COMPONENTS, HOST
    from stories import BPMN, STORIES
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
    # правила по данным вместо проверки ролью (замечания Z-ICP / Z-RUN, классы «механизируемо»)
    import json
    specs, tasks = _specs(), _tasks()
    cap_owner = {Path(p).parent.name: c[0] for c in COMPONENTS for _, p in c[6] if p.endswith("spec.md")}
    schema = json.loads((HERE / "icplan_schema.json").read_text(encoding="utf-8"))
    tables = set(DM.PLATFORM_TABLES) | {v["table"] for v in schema.values()} | set(DM.LITELLM_TABLES)
    for gen in (rule_acceptance(specs, tasks), rule_estimate(tasks), rule_open_questions(tasks, SUB)):
        for key, msg in gen:
            add(tid_owner.get(key, "задачи") if re.match(r"\d+\.\d+$", key) else key, msg)
    for gen in (rule_fmea(specs), rule_rtm(specs, STORIES)):
        for cap, msg in gen:
            add(cap_owner.get(cap, cap), msg)
    for gen in (rule_screen_endpoints(SUB, _api_status(), DM.ENDPOINT_IO), rule_block_refs(SUB, tables),
                rule_deploy(COMPONENTS, DM.PLATFORM_TABLES, DM.FORK_COLUMNS)):
        for slug, msg in gen:
            add(slug, msg)
    return res
