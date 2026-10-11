"""Собирает HTML-сайт документации (MkDocs Material) из Markdown репозитория.

Запуск из корня репозитория:
    pip install -r html-view/requirements.txt
    python html-view/build.py           # сборка в html-view/site
    python html-view/build.py serve     # локальный просмотр на http://127.0.0.1:8000
"""
import html
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
from stories import ARTIFACTS, BPMN, CHAINS, PERSONAS, ROLES, STORIES  # noqa: E402
from diagrams import bpmn_svg, graph_svg  # noqa: E402
import docgraph  # noqa: E402
from components import ABOUT, AP, BLOCKS, BY_SLUG, COMPONENTS, STATUS  # noqa: E402
import integrations as IG  # noqa: E402

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


SPEC_PATH = {}


def spec_path_of(cap: str) -> str:
    if not SPEC_PATH:
        for f in (ROOT / "openspec/changes").glob("*/specs/*/spec.md"):
            SPEC_PATH[f.parent.name] = f.relative_to(ROOT).as_posix()
    return SPEC_PATH.get(cap, "")


def _write_if_changed(path: Path, text: str):
    if not path.exists() or path.read_text(encoding="utf-8") != text:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")


def sync_stories():
    """docs/stories/*.md генерируются из html-view/stories.py (источник — stories.py)."""
    d = ROOT / "docs/stories"
    idx = ["# User Stories", "", "← [README](../../README.md) · [правила](../rules/README.md)", "",
           "> Сгенерировано из `html-view/stories.py` — правьте там.", "",
           "Истории пользователей по компонентам: роль, цель, критерии приёмки (включая ошибки), связанные требования спек и процесс в нотации BPMN.", "",
           "| Роль | Кто |", "|---|---|"] + [f"| {k} | {v} |" for k, v in ROLES.items()] + ["", "| Компонент | Историй | Процессов BPMN |", "|---|---|---|"]
    for slug, name, *_ in COMPONENTS:
        lst = STORIES.get(slug, [])
        if not lst:
            continue
        procs = BPMN.get(slug, [])
        idx.append(f"| [{name}]({slug}.md) | {len(lst)} | {len(procs) or '—'} |")
        L = [f"# User Stories: {name}", "", "← [Все истории](README.md) · [как работает](../techspec/" + slug + ".md#how)", "",
             "> Сгенерировано из `html-view/stories.py` — правьте там.", ""]
        typ = {"start": "начало", "task": "задача", "gateway": "развилка", "end": "конец", "error": "ошибка"}
        for i, pr in enumerate(procs):
            L += [f"## Процесс {i + 1}. {pr['title']}", "", "Покрывает истории: " + ", ".join(f"[{s}](#{s.lower()})" for s in pr["stories"]), "",
                  f"<!-- bpmn:{slug}:{i} -->", "", "| Шаг | Дорожка | Тип | Переходы | Артефакты шага |", "|---|---|---|---|---|"]
            names = {s[0]: s[3] for s in pr["steps"]}
            for sid, lane, ty, label, nxt in pr["steps"]:
                tr = "; ".join(f"{lab + ' → ' if lab else '→ '}{names[x]}" for x, lab in nxt) or "—"
                L.append(f"| {label} | {pr['lanes'][lane]} | {typ[ty]} | {tr} | {', '.join(pr['artifacts'].get(sid, [])) or '—'} |")
            L.append("")
        loose = [s[0] for s in lst if not any(s[0] in pr["stories"] for pr in procs)]
        if loose:
            print("⚠️ истории без процесса BPMN:", slug, loose)
        where = {s[0]: c for c, l2 in STORIES.items() for s in l2}
        if slug == "icplan":
            L += ["## Сквозная трассировка", "", "Каждая история ICPlan проходит через истории других компонентов и заканчивается логической точкой.", "",
                  "| История | Цепочка историй | Логическая точка |", "|---|---|---|"]
            for sid0, (chain, end) in CHAINS.items():
                L.append(f"| [{sid0}](#{sid0.lower()}) | " + " → ".join(f"[{x}]({where[x]}.md#{x.lower()})" for x in chain) + f" | {end} |")
            L.append("")
        extra = HERE / "stories_extra" / f"{slug}.md"  # процесс и правила пользователя вне BPMN (О-52)
        if extra.exists():
            L += [extra.read_text(encoding="utf-8").strip(), ""]
        L += ["## Сводка", "", "| История | Персона | Хочу | Точка входа | Требований |", "|---|---|---|---|---|"]
        L += [f"| [{s[0]}](#{s[0].lower()}) | {PERSONAS.get(s[1], (ROLES.get(s[1], s[1]),))[0]} | {s[2]} | {s[6] if len(s) > 6 else '—'} | {len(s[5]) or '⚠️ 0'} |" for s in lst]
        L += ["", "## Истории", ""]
        for sid, role, want, so, crit, reqs, *rest in lst:
            pname = PERSONAS.get(role, (ROLES.get(role, role),))[0]
            L += [f"### {sid} {{#{sid.lower()}}}", "", f"**Как** {pname.lower()} ([персона {role}](personas.md#{role.lower()}-{pname.lower().replace(' ', '-').replace('(', '').replace(')', '')})), **я хочу** {want}, **чтобы** {so}.", ""]
            if rest and rest[0]:
                L += [f"**Точка входа:** {rest[0]}", ""]
            used_in = [k for k, (ch, _) in CHAINS.items() if sid in ch and k != sid]
            if used_in:
                L += ["**Участвует в цепочках ICPlan:** " + ", ".join(f"[{k}](icplan.md#{k.lower()})" for k in used_in), ""]
            L += ["**Критерии приёмки:**", ""]
            L += [f"- [ ] {c}" for c in crit]
            L += ["", "**Требования:** " + ("⚠️ нет — открытый вопрос, см. open-questions спек" if not reqs else "") + " · ".join(
                f"[{r.split(': ', 1)[1]}](../../{spec_path_of(r.split(': ', 1)[0])})" if spec_path_of(r.split(": ", 1)[0]) else r for r in reqs), ""]
        _write_if_changed(d / f"{slug}.md", "\n".join(L) + "\n")
    _write_if_changed(d / "README.md", "\n".join(idx + ["", "Персоны для отыгрыша: [personas.md](personas.md)."]) + "\n")
    _write_if_changed(d / "coverage.md", stories_coverage())
    _write_if_changed(d / "personas.md", personas_page())


def persona_anchor(role: str, pname: str) -> str:
    """Якорь персоны — тот же, что в ссылках из историй (sync_stories)."""
    return f"{role.lower()}-{pname.lower().replace(' ', '-').replace('(', '').replace(')', '')}"


def personas_page() -> str:
    """docs/stories/personas.md из PERSONAS (stories.py): кто что может, хочет, с кем конфликт, промпт для отыгрыша."""
    L = ["# Персоны", "", "← [Все истории](README.md) · [методика историй](../rules/us-methodology.md) · [роли документации](../rules/roles.md) · [отыгрыш](../rules/rnd-methodology.md#personas)", "",
         "> Сгенерировано из `html-view/stories.py` (PERSONAS) — правьте там.", "",
         "Персоны продукта — участники процесса, от лица которых пишутся истории и разыгрываются конфликты и споры ролей в R&D.", "",
         "| Код | Персона | Историй |", "|---|---|---|"]
    n = {k: sum(1 for l in STORIES.values() for s in l if s[1] == k) for k in PERSONAS}
    L += [f"| {k} | [{v[0]}](#{persona_anchor(k, v[0])}) | {n[k]} |" for k, v in PERSONAS.items()]
    for k, (name, can, want, conflict, prompt) in PERSONAS.items():
        L += ["", f"## {k} · {name} {{#{persona_anchor(k, name)}}}", "",
              f"**Может:** {can}", "", f"**Хочет:** {want}", "", f"**Конфликты:** {conflict}", "",
              "??? note \"Промпт для отыгрыша\"", "", "    " + prompt]
    return "\n".join(L) + "\n"




def check_req_tasks() -> list:
    """Правило трассировки: требование ↔ задача в обе стороны, все требования покрыты задачами."""
    req_side, task_side, issues = {}, {}, []
    for spec in ROOT.glob("openspec/changes/*/specs/*/spec.md"):
        for rid, impl in re.findall(r'\*\*ID:\*\* `(R-[A-Z]+-\d+)` · \*\*Реализует задача:\*\* ([^\n]*)', spec.read_text(encoding="utf-8")):
            req_side[rid] = set(re.findall(r"tasks/(\d\.\d)-", impl))
            if not req_side[rid] and "BACKLOG" not in impl and "есть в ICPlan" not in impl:
                issues.append(f"{rid}: нет задачи")
        if spec.read_text(encoding="utf-8").count("### Requirement:") != len(re.findall(r'<a id="r-', spec.read_text(encoding="utf-8"))):
            issues.append(f"{spec.parent.name}: не у всех требований есть ID")
        # якорь — у заголовка своего требования, ID в подписи того же блока (ссылка открывает начало требования)
        for blk in re.split(r"\n(?=<a id=\"r-)", spec.read_text(encoding="utf-8"))[1:]:
            a = re.match(r'<a id="(r-[a-z]+-\d+)"></a>\n### Requirement:', blk)
            idm = re.search(r"\*\*ID:\*\* `(R-[A-Z]+-\d+)`", blk)
            if not a or not idm or a.group(1) != idm.group(1).lower():
                issues.append(f"{spec.parent.name}: якорь {a.group(1) if a else '?'} не у заголовка своего требования")
    for tf in ROOT.glob("docs/tasks/*.md"):
        t, txt = tf.name.split("-")[0], tf.read_text(encoding="utf-8")
        if "**Статус:** ❌ закрыта" in txt:  # закрытая как дубль: должна ссылаться на существующие требования
            refs = set(re.findall(r"#(r-[a-z]+-\d+)\)", txt))
            if not refs:
                issues.append(f"задача {t} закрыта без ссылки на требование")
            issues += [f"задача {t} закрыта со ссылкой на несуществующее {r.upper()}" for r in refs if r.upper() not in req_side]
            continue
        task_side[t] = set(re.findall(r"\[(R-[A-Z]+-\d+)\]", txt.split("## Зачем")[0]))
        if not task_side[t]:
            issues.append(f"задача {t}: нет требований")
    for rid, ts in req_side.items():
        issues += [f"{rid} → {t}, но в задаче {t} нет {rid}" for t in ts if rid not in task_side.get(t, set())]
    for t, rs in task_side.items():
        issues += [f"задача {t} → {r}, но у {r} нет задачи {t}" for r in rs if t not in req_side.get(r, set())]
    for l in (ROOT / "docs/TASKS.md").read_text(encoding="utf-8").splitlines():
        c = re.split(r"(?<!\\)\|", l)
        if len(c) > 4 and c[1].strip() in ("⬜", "⚠️") and "tasks/" not in c[3] and "tasks.md" not in c[3] and "документация" not in c[4]:
            issues.append(f"TASKS: открытая строка без документа задачи: {c[2].strip()[:50]}")
    for f in ("docs/TASKS.md", "docs/ROADMAP.md"):
        for l in (ROOT / f).read_text(encoding="utf-8").splitlines():
            if "❗ нет требования" in l:
                issues.append(f"{f}: строка без требования: {l[:60]}")
    for i in issues:
        print("⚠️ трассировка:", i)
    print(f"трассировка: требований {len(req_side)}, задач {len(task_side)}, замечаний {len(issues)}")
    return issues


def stories_coverage() -> str:
    """Покрытие историй по методике docs/rules/us-methodology.md, раздел 8."""
    comps = [(c[0], c[1]) for c in COMPONENTS if STORIES.get(c[0])]
    roles = list(dict.fromkeys(list(ROLES) + list(PERSONAS)))
    name = lambda k: (PERSONAS.get(k) or (ROLES.get(k),))[0]
    L = ["# Покрытие историй", "", "← [Все истории](README.md) · [методика](../rules/us-methodology.md) · [персоны](personas.md)", "",
         "> Сгенерировано при сборке из `html-view/stories.py`.", "",
         "## Персона × компонент", "", "Число историй; «·» — проверить, нет ли у персоны цели в этом компоненте ([методика, шаг 1](../rules/us-methodology.md)).", "",
         "| Персона | " + " | ".join(n for _, n in comps) + " | Всего |", "|---|" + "---|" * (len(comps) + 1)]
    for r in roles:
        cnt = [sum(1 for s in STORIES[c] if s[1] == r) for c, _ in comps]
        L.append(f"| {name(r)} ({r}) | " + " | ".join(str(x) if x else "·" for x in cnt) + f" | **{sum(cnt)}** |")
    few = [(c, s[0], len(s[4])) for c, _ in comps for s in STORIES[c] if len(s[4]) < 3]
    noreq = [(c, s[0]) for c, _ in comps for s in STORIES[c] if not s[5]]
    L += ["", f"## Истории с менее чем 3 критериями приёмки ({len(few)})", "", "Нет альтернативных потоков или исключений ([шаг 4](../rules/us-methodology.md)).", ""]
    L += [f"- [{sid}]({c}.md) — {n}" for c, sid, n in few] or ["— нет"]
    L += ["", f"## Истории без требований ({len(noreq)})", ""] + ([f"- [{sid}]({c}.md)" for c, sid in noreq] or ["— нет"])
    nobp = [(c, s[0]) for c, _ in comps for s in STORIES[c] if not any(s[0] in pr["stories"] for pr in BPMN.get(c, []))]
    L += ["", f"## Истории без процесса BPMN ({len(nobp)})", ""] + ([f"- [{sid}]({c}.md)" for c, sid in nobp] or ["— нет"])
    total = sum(len(STORIES[c]) for c, _ in comps)
    L += ["", f"Всего историй: **{total}**, персон: **{len(roles)}**, компонентов с историями: **{len(comps)}**."]
    return "\n".join(L) + "\n"


SPEC_KIND = {"icplan-integration": "icplan", "agent-registry": "icplan", "control-plane": "icplan", "icplan-agent-autopickup": "icplan",
             "platform-infrastructure": "infra"}  # docs/rules/spec-kinds.md
CFG_ROLES = {"service": ["Разработчик", "DevOps-инженер"], "icplan": ["Разработчик", "Администратор"], "infra": ["DevOps-инженер"]}
XC_ROLES = {"Хранилища данных": ["Архитектор", "DevOps-инженер"], "Интерфейсы обмена": ["Архитектор", "Разработчик"],
            "Поведение при отказах зависимостей": ["DevOps-инженер", "Тестировщик"], "Нагрузка и производительность": ["DevOps-инженер", "Тестировщик"],
            "Развёртывание": ["DevOps-инженер"]}
PERSONA_ROLE = {"П": "Пользователь", "А": "Администратор", "Б": "Безопасность", "Э": "DevOps-инженер", "ВП": "Владелец продукта",
                "QA": "Тестировщик", "Аг": "Разработчик", "АгР": "Разработчик"}
APPR_HEAD = "| Требование | Роль | Кто | Тип | Дата | Решение | Версия текста | Комментарий |\n|---|---|---|---|---|---|---|---|\n"


def strip_id(s: str) -> str:
    """Убрать якорь требования (стоит перед заголовком) и строку ID (подпись после требования)."""
    return re.sub(r'<a id="r-[a-z]+-\d+"></a>\n?|\*\*ID:\*\* `R-[A-Z]+-\d+`[^\n]*\n?', "", s)


def req_version(block: str) -> str:
    """Короткий хэш текста требования (без строки ID): изменился текст — подтверждение устарело."""
    import hashlib
    body = strip_id(block)
    return hashlib.sha1(re.sub(r"\s+", " ", body).strip().encode("utf-8")).hexdigest()[:8]


def required_approvals(spec: Path) -> list:
    """[(ID, имя требования, роль, версия текста)] — обязательные подтверждения по docs/rules/spec-kinds.md."""
    cap = spec.parent.name
    t = spec.read_text(encoding="utf-8")
    out = []
    for block in re.split(r"\n### Requirement: ", t)[1:]:
        name = block.split("\n", 1)[0].strip()
        m = re.search(r"`(R-[A-Z]+-\d+)`", block)
        if not m:
            continue
        ver = req_version(block)
        if name == "Конфигурация модуля":
            roles = list(CFG_ROLES[SPEC_KIND.get(cap, "service")])
        elif name in XC_ROLES:
            roles = list(XC_ROLES[name])
        else:
            roles = ["Аналитик историй", "Тестировщик"] + [PERSONA_ROLE[s[1]] for lst in STORIES.values() for s in lst if f"{cap}: {name}" in s[5] and s[1] in PERSONA_ROLE]
        if cap in ("guardrails", "agent-sandbox"):
            roles.append("Безопасность")
        out += [(m.group(1), name, r, ver) for r in dict.fromkeys(roles)]
    return out


STALE_WITHOUT_VERSION = {"agent-runner", "guardrails"}  # одноразовая миграция: текст изменён после подтверждения


def sync_approvals():
    """approvals.md: строки ⏳ для недостающих подтверждений; решение по изменённому тексту требования сбрасывается в ⏳."""
    for spec in ROOT.glob("openspec/changes/*/specs/*/spec.md"):
        cap = spec.parent.name
        f = spec.parent / "approvals.md"
        old = {}
        for l in (f.read_text(encoding="utf-8").splitlines() if f.exists() else []):
            if l.startswith("| R-"):
                c = [x.strip() for x in l.strip().strip("|").split("|")]
                if len(c) == 7:  # старый формат без версии
                    c = c[:6] + ["?"] + c[6:]
                old[(c[0], c[1])] = c
        rows = []
        for rid, name, role, ver in required_approvals(spec):
            c = old.get((rid, role)) or [rid, role, "—", "—", "—", "⏳", ver, name]
            if c[6] == "?":
                c[6] = "" if (cap in STALE_WITHOUT_VERSION and name == "Конфигурация модуля") else ver
            if c[6] != ver and c[5] != "⏳":
                c = [rid, role, "—", "—", "—", "⏳", ver, f"{name} (текст изменён после решения «{c[5]}» от {c[2]})"]
            c[6] = ver
            rows.append("| " + " | ".join(c) + " |")
        rows.sort(key=lambda l: (int(re.search(r"R-[A-Z]+-(\d+)", l).group(1)), l))
        body = (f"# {cap} — подтверждения требований\n\n← [spec.md](spec.md) · [правило](../../../../../docs/rules/spec-kinds.md#approvals)\n\n"
                "Строки ⏳ добавляет сборка по обязательным ролям; роль меняет только свою строку: кто, 👤 / 🤖, дата, ✅ / ❌, комментарий. "
                "«Версия текста» — хэш требования: если текст изменился после решения, сборка сбрасывает решение в ⏳.\n\n" + APPR_HEAD + "\n".join(rows) + "\n")
        _write_if_changed(f, body)


def approval_stats(folder: Path) -> tuple:
    f = folder / "approvals.md"
    rows = [l for l in f.read_text(encoding="utf-8").splitlines() if l.startswith("| R-")] if f.exists() else []
    ok = sum(1 for l in rows if "| ✅ |" in l)
    return ok, len(rows), sum(1 for l in rows if "| ❌ |" in l)


def check_docs() -> list:
    """Проверки правил из журнала отклонений (docs/rules/deviations.md)."""
    issues = []
    for itf in ROOT.glob("openspec/changes/*/specs/*/interfaces.md"):
        t = itf.read_text(encoding="utf-8")
        fm = t.split("## Отказы (FMEA)")[-1] if "## Отказы (FMEA)" in t else ""
        stores = t.split("## Хранилища данных")[1].split("\n## ")[0] if "## Хранилища данных" in t else ""
        for kind, skw, fkw in (("Postgres", r"Postgres|PostgreSQL", r"БД|Postgres"), ("объектное хранилище", r"RustFS", r"RustFS|S3|объектн")):  # О-10
            if re.search(r"^\| S\d+ \|[^|]*(" + skw + ")", stores, re.M) and not re.search(fkw, fm, re.I):
                issues.append(f"{itf.parent.name}: в FMEA нет отказа своего хранилища ({kind})")
        if "Почему так по умолчанию" not in t:  # таблица параметров
            issues.append(f"{itf.parent.name}: таблица параметров без обоснований и границ")
    import datamodel as DM  # О-16, О-46: типы данных интерфейсов — datamodel.INTEG_TYPES
    codes = {c for itf in ROOT.glob("openspec/changes/*/specs/*/interfaces.md") for c in re.findall(r"^\| (I\d+) \|", itf.read_text(encoding="utf-8"), re.M)}
    issues += [f"интерфейс {c} не отнесён к типам данных (datamodel.INTEG_TYPES)" for c in sorted(codes) if c not in DM.INTEG_TYPES]  # О-16
    ids = {s[0] for l in STORIES.values() for s in l}  # О-20: сквозная трассировка историй ICPlan
    issues += [f"история {s[0]} без цепочки сквозной трассировки" for s in STORIES.get("icplan", []) if s[0] not in CHAINS]
    issues += [f"цепочка {k}: нет истории {x}" for k, (ch, _) in CHAINS.items() for x in ch if x not in ids]
    issues += [f"цепочка {k} без логической конечной точки" for k, (_, end) in CHAINS.items() if not end.strip()]
    for sp in ROOT.glob("openspec/changes/*/specs/*/spec.md"):  # О-30: строка RTM на каждое требование
        n_req = len(re.findall(r"^### Requirement: ", sp.read_text(encoding="utf-8"), re.M))
        rtm = sp.parent / "traceability.md"
        n_rtm = sum(1 for l in rtm.read_text(encoding="utf-8").splitlines() if l.startswith("| [R-")) if rtm.exists() else 0
        if n_req != n_rtm:
            issues.append(f"{sp.parent.name}: требований {n_req}, строк RTM {n_rtm}")
    import tasksmd  # О-39: tasks.md изменений = ROADMAP
    issues += tasksmd.check()
    issues += IG.check(COMPONENTS)  # О-41: интеграции и модели
    rd = (ROOT / "docs/rnd/README.md").read_text(encoding="utf-8")  # О-34: структура R&D v3
    for f in sorted((ROOT / "docs/rnd").glob("*.md")):
        if f.name == "README.md":
            continue
        row = next((l for l in rd.splitlines() if f"]({f.name})" in l), "")
        if not row:
            issues.append(f"R&D {f.name} нет в реестре docs/rnd/README.md")
        elif row.rstrip(" |").split("|")[-1].strip().startswith("v3"):
            t = f.read_text(encoding="utf-8")
            miss = [k for k in ('class="rnd-hero"', 'class="rnd-grid"', "```deck", "## Э10.", "**Утверждение", "Когда неверно" if "Когда неверно" in t else "Опровержение", "## Источники")
                    if k not in t]
            miss += [f"Э{n} / G{n}" for n in range(1, 11) if f"## Э{n}." not in t or f'gate">G{n}</span> ✅' not in t]
            if miss:
                issues.append(f"R&D {f.name} (v3): нет {', '.join(miss)}")
    for c in COMPONENTS:  # О-17: техспека у каждого компонента
        ts = ROOT / f"docs/techspec/{c[0]}.md"
        if not ts.exists():
            issues.append(f"{c[0]}: нет техспеки (docs/rules/tech-spec.md)")
            continue
        miss = [h for h in ("## Образы", "## Запуск", "## Переменные и секреты", "## Сборка и поставка", "## Проверка после развёртывания") if h not in ts.read_text(encoding="utf-8")]
        if miss:
            issues.append(f"{c[0]}: в техспеке нет разделов {miss}")
    for i in issues:
        print("⚠️ правила:", i)
    return issues


HL = [  # О-35: цветовая разметка R&D — слово в начале ячейки → класс
    (r"не закрывает|не брать[^|]*|нет\b|\*\*нет\*\*|✗|обратная", "no"),
    (r"закрывает с доработкой|закрывает частично|с доработкой|частично|можно добавить", "part"),
    (r"закрывает|проходит|брать|оставить|да\b|✅", "ok"),
    (r"адаптировать|заменить", "info"),
    (r"безразличная", "mute"),
    (r"базовая", "kano-base"), (r"линейная", "kano-lin"), (r"привлекательная", "kano-att"),
    (r"И[34]\b", "ok"), (r"И[12]\b", "part"), (r"И0\b", "no"),
]
EV = {"А": "a", "Б": "b", "В": "c", "Г": "d"}


def rnd_highlight(txt: str) -> str:
    """Подсветка R&D: оценки и решения в начале ячеек, уровни доказательства, рамка «Вывод этапа»."""
    out, fence = [], False
    for line in txt.split("\n"):
        if line.startswith("```"):
            fence = not fence
        if not fence and line.startswith("|") and not re.match(r"^\|[\s:|-]+\|?$", line):
            cells = re.split(r"(?<!\\)\|", line)
            for i in range(1, len(cells) - 1):
                c = cells[i]
                m = re.match(r"(\s*)(\*\*)?(.*)$", c)
                body = m.group(3)
                for pat, cls in HL:
                    mm = re.match(r"(" + pat + r")(\*\*)?", body)
                    if mm and (m.group(2) is None or mm.group(2)):
                        word = (m.group(2) or "") + mm.group(1) + (mm.group(2) or "")
                        cells[i] = m.group(1) + f'<span class="hl {cls}">{word}</span>' + body[mm.end():]
                        break
            line = "|".join(cells)
        line = re.sub(r"\(([АБВГ])\)", lambda m: f'<span class="ev {EV[m.group(1)]}">{m.group(1)}</span>', line)
        out.append(line)
    txt = "\n".join(out)
    txt = re.sub(r"^\*\*Вывод этапа\.\*\*(.*?)(?=\n\n)", lambda m: f'<div class="rnd-concl" markdown>\n\n**Вывод этапа.**{m.group(1)}\n\n</div>', txt, flags=re.M | re.S)
    parts = re.split(r"(````.*?````)", txt, flags=re.S)  # примеры разметки в ```` не превращаются в слайды
    return "".join(p if p.startswith("````") else re.sub(r"^```deck\n(.*?)^```", lambda m: deck_html(m.group(1)), p, flags=re.S | re.M)
                   for p in parts)


def deck_html(src: str) -> str:
    """Микропрезентация R&D: слайды 16:9 из компактной разметки (docs/rules/rnd-methodology.md#deck)."""
    slides, cur = [], None
    for raw in src.strip().split("\n"):
        s = raw.strip()
        if not s:
            continue
        if s.startswith("# "):
            cur = {"title": s[2:], "body": []}
            slides.append(cur)
            continue
        if cur is None:
            continue
        kind, _, rest = s.partition(" ")
        b = cur["body"]
        if kind == ">":
            b.append(f'<div class="sl-take">{md_inline(rest)}</div>')
        elif kind == "stack":  # stack Метка: 6 ok, 2 part, 0 no
            lab, _, parts = rest.partition(":")
            segs = [(int(n), c) for n, c in re.findall(r"(\d+)\s*(ok|part|no|info|mute)", parts)]
            tot = sum(n for n, _ in segs) or 1
            bar = "".join(f'<span class="seg {c}" style="flex:{n}">{n}</span>' for n, c in segs if n)
            b.append(f'<div class="sl-row"><span class="sl-lab">{md_inline(lab)}</span><span class="sl-stack">{bar}</span></div>')
        elif kind == "bar":  # bar Метка: 3/4 подпись [ok|part|no|info]
            lab, _, v = rest.partition(":")
            mm = re.match(r"\s*([\d.]+)\s*/\s*([\d.]+)\s*(.*?)\s*(ok|part|no|info|mute)?$", v)
            val, mx, cap, cls = float(mm.group(1)), float(mm.group(2)), mm.group(3), mm.group(4) or "info"
            b.append(f'<div class="sl-row"><span class="sl-lab">{md_inline(lab)}</span><span class="sl-bar"><span class="fill {cls}" style="width:{100 * val / mx:.0f}%"></span><em>{md_inline(cap)}</em></span></div>')
        elif kind == "side":  # side Левый | Правый
            l, _, r = rest.partition("|")
            b.append(f'<div class="sl-side"><span>{md_inline(l.strip())}</span><span>{md_inline(r.strip())}</span></div>')
        elif kind == "pos":  # pos Роль: -2..2 | довод
            lab, _, v = rest.partition(":")
            n, _, why = v.partition("|")
            x = (float(n) + 2) / 4 * 100
            b.append(f'<div class="sl-row"><span class="sl-lab">{md_inline(lab)}</span><span class="sl-track"><span class="dot" style="left:{x:.0f}%"></span></span><span class="sl-why">{md_inline(why.strip())}</span></div>')
        elif kind == "-":
            b.append(f'<div class="sl-li">{md_inline(rest)}</div>')
        else:
            b.append(f'<div class="sl-li">{md_inline(s)}</div>')
    body = "".join(f'<div class="slide"><div class="sl-n">{i}/{len(slides)}</div><div class="sl-title">{md_inline(sl["title"])}</div>{"".join(sl["body"])}</div>'
                   for i, sl in enumerate(slides, 1))
    return f'<div class="deck">{body}</div>\n'


def md_inline(s: str) -> str:
    s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"==(.+?)==", r"<mark>\1</mark>", s)
    return re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', s)


def copy_sources():
    sync_stories()
    sync_approvals()
    check_docs()
    check_req_tasks()
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
        txt = relink_readme(f.read_text(encoding="utf-8"), f)
        txt = re.sub(r"<!-- bpmn:([a-z-]+):(\d+) -->", lambda m: bpmn_svg(BPMN[m.group(1)][int(m.group(2))]) if m.group(1) in BPMN else "", txt)
        txt = txt.replace("<!-- docgraph -->", graph_svg(docgraph.LAYERS, docgraph.EDGES))
        if rel.as_posix().startswith("docs/rnd/") or rel.as_posix() == "docs/rules/rnd-methodology.md":
            txt = rnd_highlight(txt)
        if rel.as_posix().startswith("docs/techspec/") or rel.as_posix() in ("docs/data-types.md", "architecture.md"):
            base = "../" * (len(rel.parts) - 1)
            txt = IG.flow_page(txt, rel.stem, IG.names(COMPONENTS), base)  # О-46, О-52: модели — ссылками, матрица интерфейсов — из datamodel
        if rel.as_posix().startswith("docs/api/") and rel.name != "README.md":
            txt = IG.api_page_structure(txt)  # О-45: структура запросов и ответов из OpenAPI форка и datamodel
        dst.write_text(txt, encoding="utf-8")
    shutil.copy2(HERE / "home.md", SRC / "index.md")
    (SRC / "assets").mkdir(parents=True, exist_ok=True)
    shutil.copy2(HERE / "assets" / "extra.css", SRC / "assets" / "extra.css")
    write_component_pages()
    write_rnd_consequences()
    (SRC / "data-model.md").write_text(IG.data_model_page(COMPONENTS), encoding="utf-8")
    write_pagebar_map()
    check_links()


def check_links() -> list:
    """Битые относительные ссылки в собранных исходниках сайта (О-40)."""
    bad = []
    for f in SRC.rglob("*.md"):
        t = re.sub(r"```.*?```|`[^`\n]*`", "", f.read_text(encoding="utf-8"), flags=re.S)
        for m in re.finditer(r"\]\(([^)\s]+)\)", t):
            u = m.group(1).split("#")[0]
            if not u or re.match(r"^(https?:|mailto:)", u):
                continue
            tgt = f.parent / u
            if not tgt.exists():
                bad.append(f"{f.relative_to(SRC).as_posix()} → {m.group(1)}")
    for b in bad:
        print("⚠️ ссылка:", b)
    print(f"ссылки: битых {len(bad)}")
    return bad


def write_rnd_consequences():
    """Сводка последствий R&D (Э10): что из исследований внесено, предложено, не требуется (О-35)."""
    rows = []
    for f in sorted((ROOT / "docs/rnd").glob("*.md")):
        t = f.read_text(encoding="utf-8")
        if "## Э10." not in t:
            continue
        sec = re.split(r"\n## |\n<details", t.split("## Э10.", 1)[1])[0]
        title = title_of(f, f"docs/rnd/{f.name}").replace("R&D: ", "")
        for l in sec.splitlines():
            if not l.startswith("| ") or l.startswith("| Изменение") or re.match(r"^\|[\s:|-]+\|$", l):
                continue
            c = [x.strip() for x in re.split(r"(?<!\\)\|", l)[1:-1]]
            if len(c) < 3:
                continue
            doc = re.sub(r"\]\((?!https?:|#)([^)#]+)(#[^)]*)?\)",
                         lambda m: "](" + rel(".", os.path.normpath(os.path.join("docs/rnd", m.group(1)))) + (m.group(2) or "") + ")", c[1])
            rows.append((c[2][:1], f"[{title}](docs/rnd/{f.name}#e10)", c[0], doc, c[2]))
    order = {"📌": 0, "✅": 1}
    rows.sort(key=lambda r: order.get(r[0], 2))
    n = lambda s: sum(1 for r in rows if r[0] == s)
    L = ["# Последствия R&D", "",
         "Что из исследований меняет решения, спеки, задачи и техспеки ([правило](docs/rules/rnd-methodology.md#consequences)). "
         "Собирается из раздела «Э10. Последствия» каждого R&D. Предложения 📌 разбираются по [процессу изменений](docs/rules/change-process.md).", "",
         f"**Предложено:** {n('📌')} · **внесено или подтверждено:** {n('✅')} · **не требуется:** {len(rows) - n('📌') - n('✅')}", "",
         "| R&D | Изменение | Документ | Статус |", "|---|---|---|---|"]
    L += [f"| {r[1]} | {r[2]} | {r[3]} | {r[4]} |" for r in rows]
    (SRC / "rnd-consequences.md").write_text("\n".join(L) + "\n", encoding="utf-8")


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
        pages[f"docs/stories/{slug}.md"] = slug
    for slug, name, st, g, desc, links, docs, tids in COMPONENTS:
        for _, p in docs:
            for fp in spec_family(p):
                pages.setdefault(fp, slug)
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
        oqf = SRC / Path(sp).parent / "open-questions.md"
        qs = [l.split("|") for l in oqf.read_text(encoding="utf-8").splitlines() if l.startswith("| ОВ-")] if oqf.exists() else []
        qhtml = ("<div class=\"oq-list\"><b>Открытые вопросы:</b><ul>" + "".join(f'<li>{q[3].strip()} {html.escape(q[2].strip())}' + (' <i>блокирует</i>' if q[4].strip() == "да" else '') + '</li>' for q in qs)
                 + f'</ul><a href="{{oq}}">все вопросы →</a></div>') if qs else ""
        lists = [("Шаблонный текст (совпадает с другой спекой)", [f"{d[0]} ≈ {d[1]} «{d[2]}» {d[3]}%" for d in r["dup"]]),
                 ("Пользовательские требования без User Story", r["no_us"]),
                 ("Открыто в последнем ревью — готовность не выше 90", r["review_open"])]
        qhtml += "".join(f'<div class="oq-list"><b>{h}:</b><ul>' + "".join(f"<li>{html.escape(x)}</li>" for x in xs) + "</ul></div>" for h, xs in lists if xs)
        ok, al, bad = r["approvals"]
        qhtml += f'<div class="oq-list"><b>Подтверждения ролей:</b> {ok} из {al}' + (f', замечаний {bad}' if bad else '') + ' — <a href="{appr}">кто подтвердил →</a></div>' 
        rd[sp] = ('<div class="rd-head"><span class="about-label">Готовность спеки</span>' + rd_bar(r, True)
                  + "".join((f'<span class="rd-part">{k} <b>{v}</b>/{m}</span>' if m else f'<span class="rd-part rd-neg">{k} <b>{v}</b></span>') for k, (v, m) in r["parts"].items() if m or v) + qhtml
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
    L += [f"| `{cell(n)}` | {cell(w)} | {cell(e)} | {cell(spec_value(n, slug, d))} | {cell(where)} |" for n, w, e, d, where in r["config"]]
    return L + [""]


_SPEC_PARAMS = {}


def spec_params() -> dict:
    """Имя параметра → [(спека, значение по умолчанию)] из таблиц «Параметры модуля» interfaces.md."""
    if not _SPEC_PARAMS:
        for f in ROOT.glob("openspec/changes/*/specs/*/interfaces.md"):
            for l in f.read_text(encoding="utf-8").splitlines():
                m = re.match(r"^\| `([\w.]+)` \|(.*)", l)
                if m:
                    c = [x.strip() for x in m.group(2).split("|")]
                    if len(c) > 3:
                        _SPEC_PARAMS.setdefault(m.group(1), []).append((f.parent.name, c[3]))
    return _SPEC_PARAMS


def spec_value(name: str, slug: str, fallback: str) -> str:
    """Значение параметра из interfaces.md спеки (один источник, О-50); нет в спеке — как в данных сайта."""
    ps = spec_params()
    specs = {Path(p).parent.name for _, p in BY_SLUG[slug][6] if p.endswith("spec.md")} if slug in BY_SLUG else set()
    cands = [name] if name in ps else ([k for k in ps if k.endswith("." + name)] if "_" in name or "." in name else [])
    vals = [v for k in cands for s, v in ps[k] if not specs or s in specs] or [v for k in cands for _, v in ps[k]]
    vals = list(dict.fromkeys(vals))
    if len(vals) != 1 or vals[0].startswith(("—", "нет", "из ")):
        return fallback
    return vals[0]


# ---------- Готовность спек ----------
RD_BANDS = [(90, "#2e7d32", "готова"), (75, "#7cb342", "почти"), (60, "#f9a825", "в работе"), (40, "#ef6c00", "черновик"), (0, "#d32f2f", "заготовка")]


def rd_color(p: int):
    return next((c, n) for lim, c, n in RD_BANDS if p >= lim)


USER_WORDS = re.compile(r"пользовател|администратор|владел|в задач|истори[ия] задачи|уведомлен|кнопк|экран|UI\b|видит", re.I)
TECH_REQS = ("Конфигурация модуля", "Хранилища данных", "Интерфейсы обмена", "Поведение при отказах", "Нагрузка и производительность", "Развёртывание")
_CACHE = {}


def _req_bodies() -> dict:
    """{(cap, имя): нормализованный текст требования} по всем спекам — для проверки уникальности."""
    if "bodies" not in _CACHE:
        out = {}
        for sp in (SRC / "openspec/changes").glob("*/specs/*/spec.md"):
            for r in re.split(r"\n### Requirement: ", sp.read_text(encoding="utf-8"))[1:]:
                name, body = r.split("\n", 1)
                body = strip_id(body)
                out[(sp.parent.name, name.strip())] = re.sub(r"\s+", " ", body.lower()).strip()
        _CACHE["bodies"] = out
    return _CACHE["bodies"]


def duplicates(cap: str) -> list:
    """Требования спеки, текст которых совпадает с требованием другой спеки больше чем на 80% (по словесным триграммам)."""
    if "sh" not in _CACHE:
        def sh(t):
            w = re.findall(r"\w+", t)
            return {" ".join(w[i:i + 3]) for i in range(max(len(w) - 2, 1))}
        _CACHE["sh"] = {k: sh(v) for k, v in _req_bodies().items()}
    S = _CACHE["sh"]; out = []
    for (c, n), a in S.items():
        if c != cap:
            continue
        best = max(((2 * len(a & b) / (len(a) + len(b)), c2, n2) for (c2, n2), b in S.items() if c2 != cap), default=(0, "", ""))
        if best[0] > 0.8:
            out.append((n, best[1], best[2], round(best[0] * 100)))
    return out


def task_side() -> dict:
    """{ID требования: {задачи}} по разделам «Закрывает требования» документов задач."""
    if "tasks" not in _CACHE:
        side = {}
        for tf in (ROOT / "docs/tasks").glob("*.md"):
            txt = tf.read_text(encoding="utf-8")
            if "**Статус:** ❌ закрыта" in txt:
                continue
            for rid in set(re.findall(r"\[(R-[A-Z]+-\d+)\]", txt.split("## Зачем")[0])):
                side.setdefault(rid, set()).add(tf.name.split("-")[0])
        _CACHE["tasks"] = side
    return _CACHE["tasks"]


def review_open(cap: str) -> list:
    """Открытые (❓ / 📌) замечания по спеке в последнем ревью."""
    revs = sorted((ROOT / "docs/reviews").glob("*.md"), key=lambda f: (f.name[:10], int(m.group(1)) if (m := re.search(r"-(\d+)\.md$", f.name)) else 1))
    if not revs:
        return []
    out, hdr = [], None
    for l in revs[-1].read_text(encoding="utf-8").splitlines():
        if not l.startswith("|"):
            hdr = None; continue
        c = [x.strip() for x in l.strip().strip("|").split("|")]
        if hdr is None:
            hdr = c; continue
        if set(l) <= set("|-: "):
            continue
        col = next((i for i, h in enumerate(hdr) if h in ("Спека", "Спеки")), None)
        if col is None or len(c) != len(hdr):
            continue
        specs = c[col]
        if (cap in specs or specs.startswith("все")) and re.search("❓|📌", c[-1]):
            out.append(c[0])
    return out


def spec_readiness(spec: str) -> dict:
    """Процент готовности спеки по docs/rules/spec-criteria.md (раздел 6)."""
    if ("rd", spec) not in _CACHE:
        _CACHE[("rd", spec)] = _spec_readiness(spec)
    return _CACHE[("rd", spec)]


def _spec_readiness(spec: str) -> dict:
    t = (SRC / spec).read_text(encoding="utf-8")
    folder = SRC / Path(spec).parent
    reqs = [strip_id(r) for r in re.split(r"\n### Requirement: ", t)[1:]]
    cap = Path(spec).parent.name
    purpose = re.search(r"## Purpose\n\n([^\n]+)", t)
    fmt = (4 if purpose and len(purpose.group(1)) >= 50 else 0)
    fmt += 4 if reqs and all(re.search(r"\b(SHALL|MUST)\b", r.split("####")[0]) for r in reqs) else 0
    fmt += 4 if reqs and all("#### Scenario:" in r for r in reqs) else 0
    fmt += 3 if reqs and all(len(r.split("#### Scenario:")[0]) <= 520 for r in reqs) else 0
    cov = round(25 * sum(min(r.count("#### Scenario:"), 3) / 3 for r in reqs) / len(reqs)) if reqs else 0
    rtm = (folder / "traceability.md")
    rows = [l for l in rtm.read_text(encoding="utf-8").splitlines() if l.startswith("| ") and "---" not in l][1:] if rtm.exists() else []
    ts = task_side(); ok2 = 0
    for rid, impl in re.findall(r'`(R-[A-Z]+-\d+)` · \*\*Реализует задача:\*\* ([^\n]*)', t):
        tasks = set(re.findall(r"tasks/(\d\.\d)-", impl))
        ok2 += 1 if (("BACKLOG" in impl or "есть в ICPlan" in impl) and not tasks) or (tasks and tasks <= ts.get(rid, set())) else 0
    trace = round(20 * ok2 / len(reqs)) if reqs else 0  # двусторонняя связь требование ↔ задача
    why = (5 if "Обоснование:" in t else 0) + (5 if rows and all("⚠️ нет |" not in l for l in rows) else 0)
    itf = folder / "interfaces.md"
    it = itf.read_text(encoding="utf-8") if itf.exists() else ""
    fail = sum(2 for h in ("## Параметры модуля", "## Хранилища данных", "## Интерфейсы обмена", "## Отказы (FMEA)") if h in it)
    fr = next((r for r in reqs if r.startswith("Поведение при отказах")), "")
    fail += 3 if fr.count("#### Scenario:") >= 3 else 0
    fail += 2 if any(r.startswith("Нагрузка и производительность") for r in reqs) and any(r.startswith("Развёртывание") for r in reqs) else 0
    slug = next((c[0] for c in COMPONENTS for _, pth in c[6] if pth == spec), None)
    conn = 5 if (folder / "architecture.md").exists() else 0
    conn += 5 if f"specs/{cap}/spec.md" in (SRC / "architecture.md").read_text(encoding="utf-8") else 0
    conn += 5 if slug and "## Как работает" in ((SRC / f"docs/techspec/{slug}.md").read_text(encoding="utf-8") if (SRC / f"docs/techspec/{slug}.md").exists() else "") else 0
    for h in ("## Нагрузка и развёртывание",):
        fail += 2 if h in it else 0
    fail = min(fail, 15)
    oqf = folder / "open-questions.md"
    oq = [l for l in oqf.read_text(encoding="utf-8").splitlines() if l.startswith("| ") and re.search(r"\| (❓|📌) \|", l)] if oqf.exists() else []  # О-38: по колонке типа, а не по префиксу ID
    n_q = sum(1 for l in oq if "| ❓ |" in l); n_d = sum(1 for l in oq if "| 📌 |" in l)
    pen = min(2 * n_q, 10) + min(4 * n_d, 16)
    dup = duplicates(cap)
    pen_dup = min(2 * len(dup), 10)
    no_us = []
    for l in rows:
        c = [x.strip() for x in l.strip("|").split("|")]
        nm = re.sub(r"^\[R-[A-Z]+-\d+\]\([^)]*\)\s*", "", c[0])
        body = next((r for r in reqs if r.startswith(nm + "\n")), "")
        if len(c) > 1 and c[1] == "техническое" and not nm.startswith(TECH_REQS) and USER_WORDS.search(body):
            no_us.append(nm)
    pen_us = min(2 * len(no_us), 10)
    parts = {"Формат": (fmt, 15), "Сценарии": (cov, 25), "Трассировка": (trace, 20), "Обоснование": (why, 10), "Интерфейсы, отказы, нагрузка": (fail, 15), "Связность": (conn, 15)}
    base = sum(v for v, _ in parts.values())
    parts["Открытые вопросы"] = (-pen, 0)
    parts["Шаблонный текст"] = (-pen_dup, 0)
    parts["Без User Story"] = (-pen_us, 0)
    rev = review_open(cap)
    pct = max(base - pen - pen_dup - pen_us, 0)
    cut = pct - 90 if rev and pct > 90 else 0  # потолок 90, пока в последнем ревью есть открытое
    pct -= cut
    parts["Потолок без ревью"] = (-cut, 0)
    a_ok, a_all, a_bad = approval_stats(folder)
    cut2 = pct - 90 if a_ok < a_all and pct > 90 else 0  # потолок 90, пока не все обязательные роли подтвердили
    pct -= cut2
    parts["Потолок без подтверждений"] = (-cut2, 0)
    return {"pct": pct, "base": base, "oq": (n_q, n_d), "parts": parts, "reqs": len(reqs), "single": sum(1 for r in reqs if r.count("#### Scenario:") == 1),
            "dup": dup, "no_us": no_us, "review_open": rev, "approvals": (a_ok, a_all, a_bad)}


def rd_bar(r: dict, wide: bool = False) -> str:
    c, name = rd_color(r["pct"])
    tip = " · ".join(f"{k} {v}/{m}" if m else f"{k} {v}" for k, (v, m) in r["parts"].items())
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
        got, gave = IG.io_lists(slug, IG.names(COMPONENTS))  # из интеграций, не вручную
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
            f'<ul class="does">{"".join(f"<li>{code(x)}</li>" for x in got)}</ul></div>'
            '<div><div class="about-label">Отдаёт</div>'
            f'<ul class="does">{"".join(f"<li>{code(x)}</li>" for x in gave)}</ul></div></div>'
            '</div><aside class="about-side">'
            f'<div class="side-card"><div class="side-head"><span class="dtype dtype-flow">КАК РАБОТАЕТ</span>'
            f'<a class="side-all" href="{href(page, f"docs/techspec/{slug}.md")}#how">открыть →</a></div>'
            '<ul><li>Порядок работы, запуск, конфигурация</li></ul></div>'
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
                    + "".join(f'<span class="kp"><code>{esc(n)}</code> {esc(spec_value(n, slug, d))}</span>' for n, _, _, d, _ in cfg)
                    + '<a class="side-all" href="#_5">все параметры ↓</a></div>')
        body = [f"# {name}", "", head, "", keyp, "", about, "",
                "## Устройство", "",
                f'<div class="map">{render_rows(BLOCKS.get(slug, []), page, slug)}</div>', ""]
        body += rationale_md(slug)
        body += [""] + IG.integrations_md(slug, page, IG.names(COMPONENTS), href) + IG.models_md(slug) + IG.stores_md(slug, page, href)
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
             "| Параметр | Значение |", "|---|---|"] + [f"| `{cell(a)}` | {cell(spec_value(a, slug, b))} |" for a, b in s["params"]]
        L += ["", "## Что делает", ""] + [f"- {x}" for x in s["does"]]
        L += ["", "## Почему так", "", s["why"]]
        if s["rnd"]:
            L += ["", f"**Исследование:** [R&D]({rel(d, 'docs/rnd/' + s['rnd'])})"]
        (SRC / d).mkdir(parents=True, exist_ok=True)
        (SRC / page).write_text("\n".join(L) + "\n", encoding="utf-8")

    for slug, name, *_ in COMPONENTS:
        d = f"rnd-by-component/{slug}"
        L = [f"# R&D: {name}", "", "Исследования, на которых основаны решения по компоненту. Методология — [методология R&D](" + rel(d, "docs/rules/rnd-methodology.md") + ").", "",
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
        rows.append(f"| [{Path(sp).parent.name}]({rel('specs-by-component', sp)}) | {Path(sp).parts[2]} | {r['reqs']} | ❓ {r['oq'][0]} · 📌 {r['oq'][1]} | {rd_bar(r)} |")
    avg = round(sum(spec_readiness(s)["pct"] for s in specs) / len(specs)) if specs else 0
    readiness_md = ["## Готовность спек", "", f"Средняя готовность: {rd_bar({'pct': avg, 'parts': {}}, True)}", "", rd_scale(), "",
                    "Считается по [критериям полноты](" + rel("specs-by-component", "docs/rules/spec-criteria.md") + "): формат 15, сценарии 25, трассировка 20, обоснование 10, интерфейсы / отказы / нагрузка 15, связность 15; минус открытые вопросы (❓ −2, 📌 −4), шаблонный текст (−2 за требование), пользовательские требования без User Story (−2); потолок 90, пока в последнем ревью есть открытое по спеке. Наведите на шкалу — разбивка.", "",
                    "| Спека | Change | Требований | Открытые вопросы | Готовность |", "|---|---|---|---|---|"] + rows + [""]

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


def spec_family(path: str) -> list:
    """Спека и её соседние документы (схема, интерфейсы, трассировка)."""
    out = [path]
    if path.endswith("/spec.md"):
        base = path[: -len("spec.md")]
        out += [base + n for n in ("interfaces.md", "traceability.md", "open-questions.md", "approvals.md") if (SRC / (base + n)).exists()]
    return out


def nav_yaml() -> str:
    tasks = task_files()
    used = set()

    def item(indent, label, path):
        used.add(path)
        return f"{' ' * indent}- {q(label)}: {path}"

    LBL = {"interfaces.md": "Интерфейсы, данные, отказы", "traceability.md": "Трассировка (RTM)", "open-questions.md": "Открытые вопросы", "approvals.md": "Подтверждения"}
    L = ["nav:", item(2, "Главная", "index.md")]
    for slug, name, st, g, desc, links, docs, tids in COMPONENTS:
        L.append(f"  - {q(name)}:")
        L.append(item(4, name, f"components/{slug}/index.md"))
        subs = [title for (s, title) in SUB if s == slug]
        if subs:
            L.append("    - Компоненты:")
            L += [item(6, title, sub_page(slug, title)) for title in subs]
        if (SRC / f"docs/stories/{slug}.md").exists():
            L += ["    - User Stories:", item(6, "User Stories " + name, f"docs/stories/{slug}.md")]
        L += ["    - Спеки:", item(6, "Спеки " + name, f"specs-by-component/{slug}/index.md")]
        for label, p in docs:
            for fp in spec_family(p):
                if (SRC / fp).exists() and fp not in used:
                    L.append(item(6, LBL.get(Path(fp).name, label) if fp != p else label, fp))
        L += ["    - Задачи:", item(6, "Задачи " + name, f"tasks-by-component/{slug}/index.md")]
        L += [item(6, title_of(SRC / tasks[t], t), tasks[t]) for t in tids if t in tasks]
        if slug == "icplan" and (SRC / f"{AP}/tasks.md").exists():
            L.append(item(6, "Автоподхват: задачи ICPlan", f"{AP}/tasks.md"))
        rs = [p for _, p in REFS.get(slug, []) if p.startswith("docs/rnd/") and (SRC / p).exists() and p not in used]
        if (SRC / f"docs/api/{slug}.md").exists():
            L += ["    - API:", item(6, "API " + name, f"docs/api/{slug}.md")]
        if (SRC / f"docs/techspec/{slug}.md").exists():
            L += ["    - Техспека:", item(6, "Техспека " + name, f"docs/techspec/{slug}.md")]
        L += ["    - R&D:", item(6, "R&D " + name, f"rnd-by-component/{slug}/index.md")]
        L += [item(6, title_of(SRC / p, p).replace("R&D: ", ""), p) for p in rs]
    # Разделы сайта (doc-types.md#tabs): архитектура → требования → R&D → план → справка
    L += ["  - Архитектура:", item(4, "Компоненты (таблица)", "overview.md"), item(4, "Схемы C1 / C2", "architecture.md"),
          item(4, "Типы данных и интерфейсы", "docs/data-types.md"),
          item(4, "Модель данных", "data-model.md"), item(4, "Каталог API", "docs/api/README.md"), item(4, "Техспеки компонентов", "docs/techspec/README.md")]
    L.append("    - Решения (OpenSpec):")
    for ch in sorted(p for p in (SRC / "openspec/changes").iterdir() if p.is_dir() and p.name != "archive"):
        rest = [f"openspec/changes/{ch.name}/{n}" for n in ("proposal.md", "design.md", "tasks.md")]
        rest += [x.relative_to(SRC).as_posix() for x in sorted(ch.rglob("*.md")) if "specs" in x.parts]
        rest = [x for x in rest if (SRC / x).exists() and x not in used]
        if rest:
            L.append(f"      - {q(ch.name)}:")
            L += [item(8, title_of(SRC / x, Path(x).parent.name), x) for x in rest]
    L += ["  - Требования:", item(4, "Все User Stories", "docs/stories/README.md"), item(4, "Покрытие историй", "docs/stories/coverage.md"),
          item(4, "Спеки по компонентам", "specs-by-component/index.md")]
    if (SRC / "docs/stories/personas.md").exists() and "docs/stories/personas.md" not in used:
        L.append(item(4, "Персоны", "docs/stories/personas.md"))
    L += ["  - R&D:", item(4, "Все R&D", "docs/rnd/README.md"), item(4, "R&D по компонентам", "rnd-by-component/index.md"), item(4, "Последствия R&D", "rnd-consequences.md")]
    rleft = [f"docs/rnd/{f.name}" for f in sorted((SRC / "docs/rnd").glob("*.md")) if f"docs/rnd/{f.name}" not in used]
    if rleft:
        L.append("    - Сквозные исследования:")
        L += [item(6, title_of(SRC / x, x).replace("R&D: ", ""), x) for x in rleft]
    L += ["  - План и задачи:", item(4, "Roadmap MVP", "docs/ROADMAP.md"), item(4, "Сводная таблица задач", "docs/TASKS.md"),
          item(4, "Задачи по компонентам", "tasks-by-component/index.md"), item(4, "Бэклог", "docs/BACKLOG.md"), item(4, "План документации", "docs/PLAN.md")]
    left = [x for x in tasks.values() if x not in used]
    if left:
        L.append("    - Сквозные задачи:")
        L += [item(6, title_of(SRC / x, x), x) for x in left]
    L += ["  - Справка:", item(4, "Как читать", "docs/HOW-TO-READ.md"), item(4, "Формат схем", "FORMAT.md"),
          "    - Правила документации:", item(6, "Правила документации", "docs/rules/README.md"),
          item(6, "Типы документов и вкладки", "docs/rules/doc-types.md"), item(6, "Работа с документами", "docs/rules/doc-work.md"), item(6, "Процесс изменения", "docs/rules/change-process.md"),
          item(6, "Граф связности документов", "docs/rules/doc-graph.md"), item(6, "Роли", "docs/rules/roles.md"), item(6, "Промпты", "docs/rules/prompts.md"),
          item(6, "Критерии полноты спеки", "docs/rules/spec-criteria.md"), item(6, "Виды спек и подтверждение", "docs/rules/spec-kinds.md"),
          item(6, "Методология архитектуры", "docs/rules/architecture-methodology.md"), item(6, "Методология данных и интеграций", "docs/rules/data-methodology.md"), item(6, "Методология API", "docs/rules/api-methodology.md"), item(6, "Методология решений", "docs/rules/decision-methodology.md"), item(6, "Методология задач и плана", "docs/rules/task-methodology.md"), item(6, "Методология ревью и отклонений", "docs/rules/review-methodology.md"), item(6, "Методология сопровождающих документов", "docs/rules/support-docs-methodology.md"), item(6, "Методология SDD", "docs/rules/sdd-methodology.md"), item(6, "Методика User Stories", "docs/rules/us-methodology.md"),
          item(6, "Методология R&D", "docs/rules/rnd-methodology.md"), item(6, "Техническая спецификация", "docs/rules/tech-spec.md"),
          item(6, "Проверка двумя читателями", "docs/rules/dual-read.md"), item(6, "Журнал отклонений", "docs/rules/deviations.md")]
    revs = sorted((SRC / "docs/reviews").glob("*.md")) if (SRC / "docs/reviews").exists() else []
    if revs:
        L.append("    - Ревью:")
        L += [item(6, title_of(f, f.stem), f"docs/reviews/{f.name}") for f in revs]
    return "\n".join(L) + "\n"


def write_config(serve: bool = False):
    cfg = (HERE / "mkdocs.base.yml").read_text(encoding="utf-8")
    if serve:
        # Локально сайт в корне, а не под /agent-architecture/ (путь GitHub Pages)
        cfg = re.sub(r"(?m)^site_url:.*$", "site_url: http://127.0.0.1:8000/", cfg)
        # Пересобирать при правке исходных .md: hook копирует их перед каждой сборкой
        watched = [ROOT / s for s in SOURCES] + [HERE / "home.md", HERE / "assets", HERE / "components.py", HERE / "stories.py"]
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
        check_anchors()
        print(f"Готово: {SITE / 'index.html'}")


def check_anchors() -> list:
    """Ссылки «файл.md#якорь» ведут на существующий id в собранной странице (О-44)."""
    def page(md):
        rel_ = md.relative_to(SRC).with_suffix("")
        if rel_.name in ("index", "README"):
            rel_ = rel_.parent
        return SITE / rel_ / "index.html"
    ids, bad = {}, []
    for f in SRC.rglob("*.md"):
        t = re.sub(r"```.*?```|`[^`\n]*`", "", f.read_text(encoding="utf-8"), flags=re.S)
        for m in re.finditer(r"\]\(([^)\s#]*\.md)#([^)\s]+)\)", t):
            tgt = (f.parent / m.group(1)).resolve()
            if not tgt.exists():
                continue  # битый файл ловит check_links
            h = page(tgt)
            if h not in ids:
                ids[h] = set(re.findall(r'id="([^"]+)"', h.read_text(encoding="utf-8"))) if h.exists() else None
            if ids[h] is not None and m.group(2) not in ids[h]:
                bad.append(f"{f.relative_to(SRC).as_posix()} → {m.group(1)}#{m.group(2)}")
    for b in bad:
        print("⚠️ якорь:", b)
    print(f"якоря: битых {len(bad)}")
    return bad


if __name__ == "__main__":
    main()
