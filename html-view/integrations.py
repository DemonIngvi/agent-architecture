"""Разделы карточек «Интеграции», «Контракты данных», «Хранилища и модель данных» и страница «Модель данных».

Данные — datamodel.py, interfaces.md спек (протокол, аутентификация, таймауты), docs/api/*.md (эндпоинты), icplan_schema.json (код форка).
"""
import json
import re
from pathlib import Path

import datamodel as DM

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SCHEMA = json.loads((HERE / "icplan_schema.json").read_text(encoding="utf-8"))
BY_VAR = {k: v["table"] for k, v in SCHEMA.items()}
BADGE = {"GET": "m-get", "POST": "m-post", "PUT": "m-put", "PATCH": "m-patch", "DELETE": "m-del"}


def _esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _unlink(s):
    """Markdown-ссылки внутри HTML-карточек не рисуются — оставляем текст."""
    return re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s)


def iface_rows() -> dict:
    """I-код → поля строки «Интерфейсы обмена» (первая найденная)."""
    out = {}
    for f in sorted(ROOT.glob("openspec/changes/*/specs/*/interfaces.md")):
        for l in f.read_text(encoding="utf-8").splitlines():
            m = re.match(r"^\| (I\d+) \|", l)
            if m and m.group(1) not in out:
                c = [x.strip() for x in re.split(r"(?<!\\)\|", l)[1:-1]]
                if len(c) >= 9:
                    c = [_unlink(x).replace("`", "") for x in c]
                    out[m.group(1)] = dict(what=c[1], proto=c[2], fmt=c[3], auth=c[4], mode=c[5], timeout=c[6], retry=c[7], idem=c[8])
    return out


def api_rows() -> dict:
    """I-код → [(метод, путь, назначение, страница каталога)] из docs/api/*.md."""
    out = {}
    for f in sorted((ROOT / "docs/api").glob("*.md")):
        if f.name == "README.md":
            continue
        for l in f.read_text(encoding="utf-8").splitlines():
            if not l.startswith("| <span class=\"m "):
                continue
            c = [x.strip() for x in re.split(r"(?<!\\)\|", l)[1:-1]]
            meth = re.sub(r"<[^>]+>", "", c[0]).strip()
            for i in re.findall(r"I\d+", c[-1]):
                out.setdefault(i, []).append((meth, _unlink(c[1]), _unlink(c[3]), f.stem))
    return out


def names(components) -> dict:
    return {c[0]: c[1] for c in components}


def _who(x, nm):
    return x.strip("«»") if x.startswith("«") else nm.get(x, x)


def involved(slug):
    for i, (a, b, via, what, models) in DM.INTEG.items():
        if slug in (a, b, via) or slug in DM.ALSO.get(i, []):
            yield i, a, b, via, what, models


def io_lists(slug, nm):
    """Получает / отдаёт — из интеграций (вместо ручного списка)."""
    got, gave = [], []
    for i, a, b, via, what, models in involved(slug):
        if a == b == slug:
            continue
        lab = ", ".join(f"`{m}`" for m in models) or what
        if b == slug or (via == slug and a != slug):
            got.append(f"{lab} ← {_who(a, nm)} ({i})")
        if a == slug or via == slug:
            gave.append(f"{lab} → {_who(b, nm)} ({i})")
    return got, gave


def integrations_md(slug, page, nm, href) -> list:
    rows, api = iface_rows(), api_rows()
    L = ["## Интеграции", "", "Все стыки компонента: с кем, через что и по какому контракту. Протокол, аутентификация и таймауты — из `interfaces.md` спек, эндпоинты — из [каталога API](../../docs/api/README.md).", "",
         '<div class="integ">']
    for i, a, b, via, what, models in sorted(involved(slug), key=lambda x: int(x[0][1:])):
        r = rows.get(i, {})
        if a == slug and b != slug:
            dirc, cls = "отдаёт", "out"
        elif b == slug or (via == slug and a != slug and b != slug):
            dirc, cls = "получает", "in"
        else:
            dirc, cls = "участвует", "mid"
        path = _who(a, nm) + (f" → {_who(via, nm)}" if via else "") + f" → {_who(b, nm)}"
        eps = api.get(i, [])
        ep_html = "".join(f'<li><span class="m {BADGE.get(m.split()[0], "m-none")}">{_esc(m.split()[0])}</span> <code>{_esc(p.strip("`"))}</code> <small>{_esc(d.replace(chr(96), ""))}</small></li>'
                          for m, p, d, _ in eps[:8])
        more = f'<li><small>ещё {len(eps) - 8} — в каталоге API</small></li>' if len(eps) > 8 else ""
        mods = " ".join(f'<a class="mdl" href="#model-{m.lower()}">{m}</a>' for m in models)
        L.append(
            f'<div class="integ-card {cls}"><div class="integ-h"><span class="integ-i">{i}</span><span class="integ-dir">{dirc}</span><b>{_esc(path)}</b></div>'
            f'<p>{_esc(what)}</p>'
            f'<div class="integ-meta"><span><i>канал</i> {_esc(r.get("proto", "—"))}</span><span><i>доступ</i> {_esc(r.get("auth", "—"))}</span>'
            f'<span><i>режим</i> {_esc(r.get("mode", "—"))} · таймаут {_esc(r.get("timeout", "—"))} · повтор {_esc(re.sub(r"^повтор\s*", "", r.get("retry", "—")))}</span></div>'
            + (f'<div class="integ-models"><i>данные</i> {mods}</div>' if mods else "")
            + (f'<ul class="integ-ep">{ep_html}{more}</ul>' if ep_html else "")
            + "</div>")
    L += ["</div>", ""]
    return L


def models_of(slug):
    seen = []
    for i, a, b, via, what, models in involved(slug):
        for m in models:
            if m not in seen:
                seen.append(m)
    # вложенные модели
    for m in list(seen):
        for _, typ, _, _ in DM.MODELS.get(m, ("", []))[1]:
            for sub in re.findall(r"\b([A-Z][A-Za-z0-9]+)\b", typ):
                if sub in DM.MODELS and sub not in seen:
                    seen.append(sub)
    return seen


def models_md(slug) -> list:
    ms = models_of(slug)
    if not ms:
        return []
    L = ["## Контракты данных", "", "Структуры, которыми компонент обменивается с соседями. Примеры JSON — в [каталоге API](../../docs/api/README.md).", ""]
    for m in ms:
        purpose, fields = DM.MODELS[m]
        L += [f'### {m} {{#model-{m.lower()}}}', "", f"_{purpose}_", "", "| Поле | Тип | Обязательное | Описание |", "|---|---|---|---|"]
        L += [f"| `{f}` | {t} | {'да' if req else '—'} | {d or '—'} |" for f, t, req, d in fields]
        L.append("")
    return L


def _mtype(t):
    return re.sub(r"[^A-Za-z0-9_]", "", t) or "text"


def _ccol(n):
    return re.sub(r"[^A-Za-z0-9_]", "_", n)


def er_tables(slug):
    """[(таблица, колонки[(имя, тип, ключ, описание)], источник)] для компонента."""
    out = []
    for key, note in DM.ICPLAN_TABLES.get(slug, []):
        v = SCHEMA[key]
        cols = [(c["name"], c["type"], ("PK" if c["pk"] else "") + (("FK " + BY_VAR.get(c["ref"], c["ref"])) if c["ref"] else ""), "") for c in v["cols"]]
        out.append((v["table"], cols, "код форка" + (f"; {note}" if note else "")))
    for t, (store, owner, cols) in DM.PLATFORM_TABLES.items():
        if owner == slug or (slug == "observability" and t == "run_event") or (slug == "agent-runner" and t == "run_event"):
            out.append((t, cols, f"проект схемы, {store}"))
    if slug == "llm-gateway":
        out += [(t, cols, "schema.prisma LiteLLM") for t, cols in DM.LITELLM_TABLES.items()]
    if slug == "observability":
        out += [("LiteLLM_SpendLogs", DM.LITELLM_TABLES["LiteLLM_SpendLogs"], "schema.prisma LiteLLM, чтение")]
    if slug == "memory":
        pass
    return out


def mermaid_er(tables, key_only=True) -> list:
    names_ = {t for t, _, _ in tables}
    L = ["```mermaid", "erDiagram"]
    rels = []
    for t, cols, _ in tables:
        L.append(f"  {t} {{")
        shown = [c for c in cols if c[2]] + [c for c in cols if not c[2]]
        for n, typ, key, d in (shown[:9] if key_only else shown):
            k = " PK" if key.startswith("PK") else (" FK" if "FK" in key else "")
            L.append(f'    {_mtype(typ)} {_ccol(n)}{k}')
            m = re.search(r"FK (\w+)", key)
            if m and m.group(1) in names_ and m.group(1) != t:
                rels.append(f'  {m.group(1)} ||--o{{ {t} : "{_ccol(n)}"')
        L.append("  }")
    L += sorted(set(rels)) + ["```"]
    return L


def stores_md(slug, page, href) -> list:
    tables = er_tables(slug)
    stores = DM.STORES.get(slug, [])
    L = ["## Хранилища и модель данных", "",
         f"Хранилища компонента: {', '.join(stores) or '—'} ([все хранилища и общая модель](../../data-model.md)). На диаграмме — ключи и основные поля; все поля — в таблицах ниже.", ""]
    if tables:
        L += mermaid_er(tables) + [""]
        for t, cols, src in tables:
            L += [f'??? note "{t} — {src}"', "", "    | Колонка | Тип | Ключ | Описание |", "    |---|---|---|---|"]
            L += [f"    | `{n}` | {typ} | {key or '—'} | {d or '—'} |" for n, typ, key, d in cols]
            L.append("")
    for s in stores:
        if s in DM.TREES:
            title, lines = DM.TREES[s]
            L += [f"**{s} · {title}**", "", "```"] + lines + ["```", ""]
    return L


def data_model_page(components) -> str:
    nm = names(components)
    L = ["# Модель данных", "", "← [Архитектура](architecture.md) · [типы данных](docs/flows/data-types.md) · [каталог API](docs/api/README.md)", "",
         "Все хранилища платформы и их таблицы. **Источник** у каждой таблицы: код форка ICPlan (`packages/db/src/schema/app.ts`, действующая схема), "
         "проект схемы платформы (по спекам и решениям D4, D17–D20 — до реализации) или `schema.prisma` LiteLLM.", "",
         "| Хранилище | Где | Владелец |", "|---|---|---|",
         "| S1 | Postgres, БД `itsaplan`, схема `public` | ICPlan |", "| S2 | схема `platform` | Platform module |", "| S3 | схема `platform`: `run_event`, `scheduler_slot`, `setup_cache` | Agent Runner, Observability |",
         "| S4 | схема `platform`: `memory_m3`, позже `m4_fact` | Memory |", "| S5 | схема `harness_ckpt`: `run_checkpoint` | Agent Runner |", "| S6 | БД `litellm` | LiteLLM |",
         "| S7 | RustFS `planner-attachments` | ICPlan, Инфраструктура |", "| S8 | git | git-провайдер |", "| S9 | конфиг деплоя | эксплуатация |", "| S10 | `/workspace` среды | Sandbox |", "| S11 | OPA в памяти | Guardrails |", ""]
    # S1: процесс и агенты — ICPlan + новые таблицы D17/D20
    s1 = er_tables("icplan")
    L += ["## S1 · ICPlan: задачи, процессы, агенты, запуски {#s1}", "", "Таблицы форка (код) и новые таблицы процесса (D17, D20).", ""] + mermaid_er(s1) + [""]
    L += ["## S1 · ICPlan: тулы, навыки, MCP, интеграции {#s1-tools}", ""] + mermaid_er(er_tables("mcp-tools")) + [""]
    s2 = [(t, c, f"проект схемы, {st}") for t, (st, o, c) in DM.PLATFORM_TABLES.items() if st == "S2"]
    L += ["## S2 · Platform module: настройки, профили, доступы {#s2}", ""] + mermaid_er(s2 + [("ai_agent", [("id", "serial", "PK", "")], "код форка"), ("project", [("id", "serial", "PK", "")], "код форка")], key_only=False) + [""]
    s345 = [(t, c, f"проект схемы, {st}") for t, (st, o, c) in DM.PLATFORM_TABLES.items() if st in ("S3", "S4", "S5")]
    L += ["## S3–S5 · события, слоты, память M3 / M4, checkpoint {#s3}", ""] + mermaid_er(s345 + [("agent_run", [("id", "serial", "PK", "")], "код форка"), ("issue", [("id", "serial", "PK", "")], "код форка")], key_only=False) + [""]
    L += ["## S6 · LiteLLM {#s6}", ""] + mermaid_er([(t, c, "") for t, c in DM.LITELLM_TABLES.items()], key_only=False) + [""]
    L += ["## Нереляционные хранилища", ""]
    for s, (title, lines) in DM.TREES.items():
        L += [f"**{s} · {title}**", "", "```"] + lines + ["```", ""]
    L += ["## Все поля", ""]
    allt = s1 + [x for x in er_tables("mcp-tools") if x[0] not in {t for t, _, _ in s1}] + s2 + s345 + [(t, c, "schema.prisma LiteLLM") for t, c in DM.LITELLM_TABLES.items()]
    for t, cols, src in allt:
        L += [f'??? note "{t} — {src}"', "", "    | Колонка | Тип | Ключ | Описание |", "    |---|---|---|---|"]
        L += [f"    | `{n}` | {typ} | {key or '—'} | {d or '—'} |" for n, typ, key, d in cols]
        L.append("")
    return "\n".join(L) + "\n"


ENVELOPE = {"run", "messages", "input", "result"}  # транспортные обёртки ответа, не поля модели


def _vocab(name, seen):
    """Имена полей модели и вложенных моделей (по типам полей)."""
    v = set()
    for f in DM.MODELS[name][1]:
        txt = " ".join(str(x) for x in f)
        v |= {w.replace("_", "").lower() for w in re.findall(r"[A-Za-z_]\w*", txt)}
        for other in DM.MODELS:
            if other != name and other in txt and other not in seen:
                seen.add(other)
                v |= _vocab(other, seen)
    return v


def api_examples_check() -> list:
    """Примеры JSON в docs/api/README.md используют только поля моделей datamodel (О-43)."""
    t = (ROOT / "docs/api/README.md").read_text(encoding="utf-8")
    issues = []
    for m in re.finditer(r"^### (.+?)\n(.*?)(?=^### |\Z)", t, re.M | re.S):
        names = [x.strip() for x in m.group(1).split("/")]
        miss = [n for n in names if n not in DM.MODELS]
        issues += [f"API: пример {n} — нет модели в datamodel.MODELS" for n in miss]
        v = set().union(*[_vocab(n, {n}) for n in names if n in DM.MODELS] or [set()])
        js = "".join(re.findall(r"```json\n(.*?)```", m.group(2), re.S))
        keys = {k.replace("_", "").lower() for k in re.findall(r'"(\w+)"\s*:', js)} - ENVELOPE
        issues += [f"API: пример {m.group(1)} — поле {k} не описано в модели" for k in sorted(keys - v)]
    return issues


def check(components) -> list:
    """Сверка: каждый I-код матрицы описан в INTEG; модели из INTEG описаны; I-коды есть в interfaces.md."""
    issues = []
    dt = (ROOT / "docs/flows/data-types.md").read_text(encoding="utf-8")
    codes = set(re.findall(r"^\| (I\d+) \|", dt, re.M))
    issues += [f"интеграция {c} есть в матрице, но не в datamodel.INTEG" for c in sorted(codes - set(DM.INTEG))]
    issues += [f"{i}: модель {m} не описана в datamodel.MODELS" for i, v in DM.INTEG.items() for m in v[4] if m not in DM.MODELS]
    rows = iface_rows()
    issues += [f"{i}: нет строки в «Интерфейсы обмена» спек" for i in DM.INTEG if i not in rows]
    slugs = {c[0] for c in components}
    issues += [f"{i}: неизвестный компонент {x}" for i, v in DM.INTEG.items() for x in v[:3] if x and not x.startswith("«") and x not in slugs]
    issues += api_examples_check()
    # таблицы описываются только в datamodel.py; SQL-черновики в документах расходятся (О-43)
    for f in [*ROOT.glob("docs/**/*.md"), *ROOT.glob("openspec/**/*.md")]:
        if re.search(r"(?i)^\s*create table", f.read_text(encoding="utf-8"), re.M):
            issues.append(f"{f.relative_to(ROOT).as_posix()}: SQL-описание таблицы — перенести в datamodel.py, в документе ссылка на «Модель данных»")
    # карточка компонента = «Интерфейсы обмена» его спеки (О-41, О-42)
    for c in components:
        m = re.search(r"/specs/([\w-]+)/spec\.md", str(c))
        f = m and ROOT / "openspec/changes/define-agent-platform/specs" / m.group(1) / "interfaces.md"
        if not f or not f.exists():
            continue
        spec = set(re.findall(r"^\| (I\d+) \|", f.read_text(encoding="utf-8"), re.M))
        card = {x[0] for x in involved(c[0])}
        main = {x[0] for x in involved(c[0]) if c[0] in x[1:4]}  # ALSO — сопутствующие (Postgres, S3)
        issues += [f"{c[0]}: {i} есть в interfaces.md спеки, нет в карточке (datamodel.INTEG / ALSO)" for i in sorted(spec - card)]
        issues += [f"{c[0]}: {i} есть в карточке, нет в interfaces.md спеки" for i in sorted(main - spec)]
    return issues
