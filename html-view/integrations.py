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


GLOSSARY = [
    "| Термин | Что это |", "|---|---|",
    "| **ICPlan**, форк | таск-трекер It's a Plan; «форк» — наша копия его кода, куда добавляем доработки 🛠 |",
    "| **Agent Runner** | наш сервис: забирает запуски из ICPlan, готовит среду, передаёт задание Harness, отдаёт события и итог в ICPlan |",
    "| **Harness** | цикл агента (LangGraph) внутри одноразовой среды: модель → тулы → модель; учётных данных БД нет |",
    "| **Sandbox** | одноразовый контейнер запуска; выход в сеть — только через egress-прокси |",
    "| **Platform module** | модуль в api ICPlan: настройки агентов, профили, бюджеты, доступы, бандл правил |",
    "| **Memory API** | наш сервис памяти агентов (M3, позже M4); Harness ходит к нему по токену запуска |",
    "| **LiteLLM** | шлюз к моделям: алиасы, ключи агентов, бюджеты, журнал затрат |",
    "| **OPA**, Guardrails | движок правил (Rego): G1 — допуск запуска, G2 — проверка действия агента, G3 — сетевая изоляция, G4 — проверка ответов модели |",
    "| **RustFS** | объектное хранилище (S3) для файлов задач и артефактов |",
    "| **Запуск** | одна работа агента по задаче: от выдачи из очереди до итога (`agent_run`) |",
    "| **Шаг процесса** | этап задачи: колонка + агент + переходы (`ProcessStep`, строковый `id`) |",
    "| **Итерация цикла** | один круг Harness «модель → тулы» (`Checkpoint.iteration`, `STEP_*` AG-UI, `usage.iterations`) |",
    "| **Лента задачи**, карточка итога | панель «Агент» в задаче: события запуска и итог с критериями и кнопками вердикта (D21) |",
    "| **M0–M6** | уровни памяти: M0 рабочая, M1 переписка, M2 итоги прошлых запусков, M3 состояние задачи, M4 факты, M5 агент, M6 документы проекта |",
    "| **L0–L3** | уровни конфигурации: L0 развёртывание, L1 проект, L2 агент, L3 запуск; нижний уровень переопределяет верхний |",
    "| **R0–R5** | автономия агента: R0 — каждое действие с подтверждением … R5 — без подтверждений |",
    "| **I1–I23, S1–S11, Т1–Т8** | интерфейсы, хранилища, типы данных ([матрица](docs/data-types.md)) |",
    "| **D1–D21, R-…, US-…** | решения design, требования спек, истории пользователей |",
]


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
        if i in DM.DATA_IN_RESPONSE:  # стрелка — кто вызывает; данные идут в ответе
            a, b = b, a
        lab = ", ".join(f"`{m}`" for m in models) or what
        if b == slug or (via == slug and a != slug):
            got.append(f"{lab} ← {_who(a, nm)} ({i})")
        if a == slug or via == slug:
            gave.append(f"{lab} → {_who(b, nm)} ({i})")
    return got, gave


def integrations_md(slug, page, nm, href) -> list:
    rows, api = iface_rows(), api_rows()
    L = ["## Интеграции {#integrations}", "", "Все стыки компонента: с кем, через что и по какому контракту. Протокол, аутентификация и таймауты — из `interfaces.md` спек, эндпоинты — из [каталога API](../../docs/api/README.md).", "",
         '<div class="integ">']
    for i, a, b, via, what, models in sorted(involved(slug), key=lambda x: int(x[0][1:])):
        r = rows.get(i, {})
        caller = _who(a, nm)
        if i in DM.DATA_IN_RESPONSE:  # стрелка — кто вызывает; данные идут в ответе
            a, b = b, a
        if a == slug and b != slug:
            dirc, cls = "отдаёт", "out"
        elif b == slug or (via == slug and a != slug and b != slug):
            dirc, cls = "получает", "in"
        else:
            dirc, cls = "участвует", "mid"
        path = _who(a, nm) + (f" → {_who(via, nm)}" if via else "") + f" → {_who(b, nm)}"
        if i in DM.DATA_IN_RESPONSE:
            path += f" (вызывает {caller}, данные — в ответе)"
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
    L = ["## Контракты данных {#contracts}", "", "Структуры, которыми компонент обменивается с соседями: поля, откуда взяты, почему такие, пример. "
         "Правило имён — [на странице «Модель данных»](../../data-model.md#naming).", ""]
    for m in ms:
        L += model_block(m)
    return L


OPENAPI = json.loads((HERE / "icplan_openapi.json").read_text(encoding="utf-8"))


def _api_examples() -> dict:
    """Модель → пример JSON из docs/api/README.md (единственное место примеров)."""
    t = (ROOT / "docs/api/README.md").read_text(encoding="utf-8")
    out = {}
    for m in re.finditer(r"^### (.+?)\n(.*?)(?=^### |\Z)", t, re.M | re.S):
        js = "\n".join(re.findall(r"```json\n(.*?)```", m.group(2), re.S)).strip()
        for n in (x.strip() for x in m.group(1).split("/")):
            if js:
                out[n] = js
    return out


def _schema_at(op, part, pointer):
    """Свойства схемы операции OpenAPI форка по пути «a.b» (с раскрытием anyOf)."""
    s = (OPENAPI["operations"].get(op) or {}).get(part)
    for key in [k for k in (pointer or "").split(".") if k]:
        s = _unwrap(s)
        s = (s or {}).get("properties", {}).get(key)
    return _unwrap(s)


def _unwrap(s):
    if isinstance(s, dict):
        for k in ("anyOf", "oneOf"):
            if k in s:
                return next((_unwrap(x) for x in s[k] if x.get("type") != "null"), None)
    return s


def _names(field):
    return [x.strip() for x in field.split("/")]


def field_origin(m, field):
    if field in DM.FIELD_SRC.get(m, {}):
        return DM.FIELD_SRC[m][field]
    kind = DM.MODEL_META[m][0]
    if kind == "fork":
        plan = DM.PLANNED.get(m, {})
        hit = next((plan[n] for n in _names(field) if n in plan), None)
        return f"🛠 {hit}" if hit else "✅ форк"
    return {"ext": "📘 протокол", "ours": "🧩 наше"}[kind]


def model_block(m, base="../../") -> list:
    purpose, fields = DM.MODELS[m]
    meta = DM.MODEL_META[m]
    users = [i for i, v in DM.INTEG.items() if m in v[4]]
    if meta[0] == "fork":
        src = f"✅ подтверждено OpenAPI ICPlan {OPENAPI['version']}: `{meta[1]}` → {meta[2]}; поля 🛠 — доработка форка"
    elif meta[0] == "ext":
        src = f"📘 внешняя спецификация: [{re.sub(r'^https?://', '', meta[1]).split('/')[0]}]({meta[1]})"
    else:
        src = f"🧩 наш контракт: {meta[1]}"
    parents = [o for o, (_, fs) in DM.MODELS.items() if o != m and any(re.search(rf"\b{m}\b", f[1]) for f in fs)]
    where = (f" · интерфейсы: {', '.join(users)}" if users else "") + (f" · вложена в: {', '.join(f'[{x}](#model-{x.lower()})' for x in parents)}" if parents else "")
    L = [f'### {m} {{#model-{m.lower()}}}', "", f"_{purpose}_" + where, "",
         f"**Источник:** {src}.", "",
         "| Поле | Тип | Обязательное | Откуда | Описание |", "|---|---|---|---|---|"]
    esc = lambda s: s.replace("|", "\\|")
    L += [f"| `{f}` | {esc(t)} | {'да' if req else '—'} | {field_origin(m, f)} | {esc(d) or '—'} |" for f, t, req, d in fields]
    L += ["", f"**Почему так.** {meta[-1]} Имена — по [правилу]({base}data-model.md#naming).", ""]
    ex = _api_examples().get(m)
    if ex:
        L += [f'??? example "Пример {m}"', "", "    ```json"] + [f"    {x}" for x in ex.split("\n")] + ["    ```", ""]
    return L


def _flat(s, pre="", out=None, depth=0):
    """Поля схемы OpenAPI списком (имя, тип, обязательное, описание)."""
    out = [] if out is None else out
    s = _unwrap(s)
    if not isinstance(s, dict) or depth > 3:
        return out
    if s.get("type") == "array" and "items" in s:
        return _flat(s["items"], pre.rstrip(".") + "[].", out, depth + 1)
    req = set(s.get("required", []))
    for k, v in (s.get("properties") or {}).items():
        u = _unwrap(v) or {}
        typ = "enum: " + " · ".join(map(str, u["enum"])) if "enum" in u else \
            " / ".join(str(x.get("const", x.get("type"))) for x in v["anyOf"]) if "anyOf" in v else u.get("type", "object")
        out.append((pre + k, typ, k in req, (v.get("description") or u.get("description") or "").replace("|", "/")[:120]))
        if u.get("type") in ("object", "array"):
            _flat(u, pre + k + ".", out, depth + 1)
    return out


def _op_key(method, path):
    return f"{method} " + re.sub(r":(\w+)", r"{\1}", path)


def _io_cell(x, base):
    """Модель → ссылка на её поля; иначе — структура как есть."""
    def link(m):
        n = m.group(1)
        return f"[`{n}`]({base}data-model.md#model-{n.lower()})" if n in DM.MODELS else f"`{n}`"
    return re.sub(r"\b([A-Z][A-Za-z0-9]+)\b", link, x.replace("|", "/"))


def api_structure(method, path, base="../../") -> list:
    """Блок «запрос / ответ» эндпоинта: из OpenAPI форка и / или datamodel.ENDPOINT_IO (О-45). [] — структуры нет."""
    keys = [f"{method} {path}", f"{method} {path.split('?')[0]}"]
    io_ = next((DM.ENDPOINT_IO[k] for k in keys if k in DM.ENDPOINT_IO), None)
    op = OPENAPI["operations"].get(_op_key(method, path.split("?")[0]))
    if not io_ and not op:
        return []
    L = []
    if op:
        L += [f"✅ **Из OpenAPI ICPlan {OPENAPI['version']}** — {op['summary']}.", ""]
        if op["params"]:
            L += ["Параметры: " + ", ".join(f"`{p['name']}` ({p['in']}{', обяз.' if p['required'] else ''})" for p in op["params"]), ""]
        for title, part in (("Запрос", op["request"]), (f"Ответ {op['status']}", op["response"])):
            rows = _flat(part)
            if rows:
                L += [f"**{title}:**", "", "| Поле | Тип | Обязательное | Описание |", "|---|---|---|---|"]
                L += [f"| `{n}` | {t} | {'да' if r else '—'} | {d or '—'} |" for n, t, r, d in rows[:30]]
                L.append("")
            elif title.startswith("Ответ"):
                L += [f"**{title}:** без тела.", ""]
    if io_:
        req, resp, note = io_
        L += [("🛠 **Доработка:**" if op else "**Контракт:**") + f" запрос — {_io_cell(req, base)}; ответ — {_io_cell(resp, base)}." + (f" {note}." if note else ""), ""]
    return L


def api_page_structure(text, base="../../") -> str:
    """Страница каталога API: после каждой таблицы — структура запросов и ответов её эндпоинтов."""
    out, block = [], []
    lines = text.split("\n")
    for i, l in enumerate(lines):
        out.append(l)
        if l.startswith('| <span class="m '):
            c = [x.strip() for x in re.split(r"(?<!\\)\|", l)[1:-1]]
            meth = re.sub(r"<[^>]+>", "", c[0]).strip()
            mm = re.search(r"`([^`]+)`", c[1])
            path = (mm.group(1) if mm else _unlink(c[1])).split(" ")[0]
            block.append((meth, path))
        nxt = lines[i + 1] if i + 1 < len(lines) else ""
        if block and not nxt.startswith("|"):
            out += ["", "??? info \"Структура запросов и ответов\"", ""]
            for meth, path in block:
                body = api_structure(meth, path, base)
                out += [f"    #### {meth} `{path}`", ""] + [("    " + x if x else "") for x in (body or ["структура не описана"])] + [""]
            block = []
    return "\n".join(out)


def api_structure_check() -> list:
    """У каждого эндпоинта каталога есть структура (OpenAPI форка или ENDPOINT_IO); 🛠 — с записью доработки (О-45)."""
    issues = []
    for f in sorted((ROOT / "docs/api").glob("*.md")):
        if f.name == "README.md":
            continue
        for l in f.read_text(encoding="utf-8").splitlines():
            if not l.startswith('| <span class="m '):
                continue
            c = [x.strip() for x in re.split(r"(?<!\\)\|", l)[1:-1]]
            meth = re.sub(r"<[^>]+>", "", c[0]).strip()
            mm = re.search(r"`([^`]+)`", c[1])
            path = (mm.group(1) if mm else _unlink(c[1])).split(" ")[0]
            if meth not in BADGE or "](" in c[1]:
                continue  # строка-отсылка к другой странице каталога
            if not api_structure(meth, path):
                issues.append(f"docs/api/{f.name}: {meth} {path} — нет структуры (OpenAPI форка или datamodel.ENDPOINT_IO)")
            elif "доработка" in c[2] and not any(k in DM.ENDPOINT_IO for k in (f"{meth} {path}", f"{meth} {path.split('?')[0]}")):
                issues.append(f"docs/api/{f.name}: {meth} {path} — доработка без записи в ENDPOINT_IO")
    return issues


def fork_models_check() -> list:
    """Модели «fork»: поля = схема OpenAPI форка; чего нет в форке — только с решением в PLANNED (О-45)."""
    issues = []
    for m, meta in DM.MODEL_META.items():
        if meta[0] != "fork":
            continue
        s = _schema_at(meta[1], *meta[2].split(".", 1)) if "." in meta[2] else _schema_at(meta[1], meta[2], "")
        if not s or "properties" not in s:
            issues.append(f"{m}: в снимке OpenAPI нет схемы {meta[1]} → {meta[2]} (python html-view/openapi_import.py)")
            continue
        real = set(s["properties"])
        ours = {n for f, *_ in DM.MODELS[m][1] for n in _names(f)}
        issues += [f"{m}.{n}: поля нет в форке и нет решения в datamodel.PLANNED" for n in sorted(ours - real) if n not in DM.PLANNED.get(m, {})]
        issues += [f"{m}.{n}: поле есть в форке, но не описано в модели" for n in sorted(real - ours)]
    issues += [f"{m}: нет источника в datamodel.MODEL_META" for m in DM.MODELS if m not in DM.MODEL_META]
    return issues


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
        out += [(t, cols, DM.LITELLM_REF) for t, cols in DM.LITELLM_TABLES.items()]
    if slug == "observability":
        out += [("LiteLLM_SpendLogs", DM.LITELLM_TABLES["LiteLLM_SpendLogs"], DM.LITELLM_REF + ", чтение")]
    if slug == "memory":
        pass
    return out


def policy_md(t, ind="") -> list:
    """Индексы, срок хранения, очистка и миграции таблицы проекта схемы."""
    if t not in DM.TABLE_POLICY:
        return []
    idx, keep, clean, mig = DM.TABLE_POLICY[t]
    L = ["", f"{ind}**Индексы:** " + ("; ".join(f"{k} ({c}) — {w}" for k, c, w in idx) if idx else "только первичный ключ"),
         "", f"{ind}**Срок:** {keep} · **очистка:** {clean} · **миграции:** {DM.MIGRATE[mig]}"]
    return L


PARAM_MIRRORS = {  # параметр в control-plane → (спека-владелец, параметр там)
    "limits.max_steps": ("agent-harness", "limits.max_steps"), "limits.timeout_s": ("agent-runner", "timeout_s"),
    "sandbox.egress_allow": ("agent-sandbox", "network.egress_allow"), "sandbox.pool.size": ("agent-sandbox", "pool.size"),
    "memory_profile.read": ("agent-memory", "read"), "memory_profile.write": ("agent-memory", "write"),
    "memory.m2_last_runs": ("agent-memory", "m2_last_runs"), "memory.retention": ("agent-memory", "retention"),
}


def param_mirror_check() -> list:
    """Значение и границы параметра в спеке-настройщике = в спеке-владельце (О-44)."""
    specs = ROOT / "openspec/changes/define-agent-platform/specs"

    def rows(spec):
        out = {}
        for line in (specs / spec / "interfaces.md").read_text(encoding="utf-8").splitlines():
            m = re.match(r"^\| `([\w.]+)` \|(.*)", line)
            if m:
                c = [x.strip() for x in m.group(2).split("|")]
                out[m.group(1)] = c
        return out

    norm = lambda s: re.sub(r"\s*\(.*?\)\s*$|`|scheduling\.", "", s).strip()
    cp, issues = rows("control-plane"), []
    for k, (spec, name) in PARAM_MIRRORS.items():
        a, b = cp.get(k), rows(spec).get(name)
        if not a or not b:
            issues.append(f"параметр {k}: нет строки в control-plane или в {spec} ({name})")
            continue
        for i, what in ((3, "значение"), (5, "минимум"), (6, "максимум")):
            if norm(a[i]) != norm(b[i]):
                issues.append(f"параметр {k}: {what} в control-plane «{a[i]}», в {spec} «{b[i]}»")
    return issues


def policy_check() -> list:
    """У каждой таблицы проекта схемы — политика; каждый FK покрыт индексом (О-44)."""
    issues = [f"{t}: нет политики хранения в datamodel.TABLE_POLICY" for t in DM.PLATFORM_TABLES if t not in DM.TABLE_POLICY]
    for t, (_, _, cols) in DM.PLATFORM_TABLES.items():
        if t not in DM.TABLE_POLICY:
            continue
        pk = [n for n, _, k, _ in cols if "PK" in k]
        firsts = {c.split(",")[0].strip() for _, c, _ in DM.TABLE_POLICY[t][0]} | ({pk[0]} if pk else set())
        issues += [f"{t}.{n}: FK без индекса (Postgres не индексирует FK сам)" for n, _, k, _ in cols if "FK" in k and n not in firsts]
    return issues


def mermaid_er(tables, key_only=True) -> list:
    names_ = {t for t, _, _ in tables}
    L = ["```mermaid", "erDiagram"]
    rels = []
    stubs = {}
    for t, cols, _ in tables:
        L.append(f"  {t} {{")
        shown = [c for c in cols if c[2]] + [c for c in cols if not c[2]]
        for n, typ, key, d in (shown[:9] if key_only else shown):
            k = ", ".join(x for x in ("PK" if "PK" in key else "", "FK" if "FK" in key else "") if x)
            L.append(f'    {_mtype(typ)} {_ccol(n)}{" " + k if k else ""}')
            m = re.search(r"FK (\w+)", key)
            if m:
                rels.append(f'  {m.group(1)} ||--o{{ {t} : "{_ccol(n)}"')  # в том числе ссылка на себя
                if m.group(1) not in names_:
                    stubs[m.group(1)] = _pk_of(m.group(1))
        L.append("  }")
    # таблицы, на которые ссылаются, но которые вне диаграммы: только ключ
    for t, (typ, n) in sorted(stubs.items()):
        L += [f"  {t} {{", f"    {_mtype(typ)} {_ccol(n)} PK", "  }"]
    L += sorted(set(rels)) + ["```"]
    return L


def _pk_of(table):
    """Тип и имя первичного ключа таблицы (форк ICPlan или проект схемы)."""
    for v in SCHEMA.values():
        if v["table"] == table:
            pk = next((c for c in v["cols"] if c["pk"]), None)
            return (pk["type"], pk["name"]) if pk else ("text", "id")
    for t, (_, _, cols) in DM.PLATFORM_TABLES.items():
        if t == table:
            pk = next((c for c in cols if "PK" in c[2]), None)
            return (pk[1], pk[0]) if pk else ("text", "id")
    return ("text", "id")


def stores_md(slug, page, href) -> list:
    tables = er_tables(slug)
    stores = DM.STORES.get(slug, [])
    L = ["## Хранилища и модель данных {#stores}", "",
         f"Хранилища компонента: {', '.join(stores) or '—'} ([все хранилища и общая модель](../../data-model.md)). На диаграмме — ключи и основные поля; все поля — в таблицах ниже.", ""]
    if tables:
        L += mermaid_er(tables) + [""]
        for t, cols, src in tables:
            L += [f'??? note "{t} — {src}"', "", "    | Колонка | Тип | Ключ | Описание |", "    |---|---|---|---|"]
            L += [f"    | `{n}` | {typ} | {key or '—'} | {d or '—'} |" for n, typ, key, d in cols]
            L += policy_md(t, "    ") + [""]
    for s in stores:
        if s in DM.TREES:
            title, lines = DM.TREES[s]
            L += [f"**{s} · {title}**", "", "```"] + lines + ["```", ""]
    return L


def data_model_page(components) -> str:
    nm = names(components)
    L = ["# Модель данных", "", "← [Архитектура](architecture.md) · [типы данных](docs/data-types.md) · [каталог API](docs/api/README.md)", "",
         "Все хранилища платформы и их таблицы. **Источник** у каждой таблицы: код форка ICPlan (`packages/db/src/schema/app.ts`, действующая схема), "
         "проект схемы платформы (по спекам и решениям D4, D17–D20 — до реализации) или `schema.prisma` LiteLLM.", "",
         "| Хранилище | Где | Владелец |", "|---|---|---|",
         "| S1 | Postgres, БД `itsaplan`, схема `public` | ICPlan |", "| S2 | схема `platform` | Platform module |", "| S3 | схема `platform`: `run_event`, `scheduler_slot`, `setup_cache` | Agent Runner, Observability |",
         "| S4 | схема `platform`: `memory_m3`, позже `m4_fact` | Memory |", "| S5 | схема `harness_ckpt`: `run_checkpoint` | Agent Runner |", "| S6 | БД `litellm` | LiteLLM |",
         "| S7 | RustFS `planner-attachments` | ICPlan, Инфраструктура |", "| S8 | git | git-провайдер |", "| S9 | конфиг деплоя | эксплуатация |", "| S10 | `/workspace` среды | Sandbox |", "| S11 | OPA в памяти | Guardrails |", ""]
    # S1: процесс и агенты — ICPlan + новые таблицы D17/D20
    s1 = er_tables("icplan")
    L += ["## S1 · ICPlan: задачи, процессы, агенты, запуски {#s1}", "",
          "Таблицы форка (код) и новые таблицы процесса (D17, D20). Диаграмма разбита по доменам; таблицы другого домена показаны только ключом.", ""]
    for title, names_ in DM.S1_DOMAINS:
        L += [f"### {title}", ""] + mermaid_er([x for x in s1 if x[0] in names_]) + [""]
    rest = sorted({x[0] for x in s1} - {n for _, ns in DM.S1_DOMAINS for n in ns})
    assert not rest, f"таблицы S1 без домена: {rest} — добавить в datamodel.S1_DOMAINS"
    L += ["## S1 · ICPlan: тулы, навыки, MCP, интеграции {#s1-tools}", ""] + mermaid_er(er_tables("mcp-tools")) + [""]
    s2 = [(t, c, f"проект схемы, {st}") for t, (st, o, c) in DM.PLATFORM_TABLES.items() if st == "S2"]
    L += ["## S2 · Platform module: настройки, профили, доступы {#s2}", ""] + mermaid_er(s2 + [("ai_agent", [("id", "serial", "PK", "")], "код форка"), ("project", [("id", "serial", "PK", "")], "код форка")], key_only=False) + [""]
    s345 = [(t, c, f"проект схемы, {st}") for t, (st, o, c) in DM.PLATFORM_TABLES.items() if st in ("S3", "S4", "S5")]
    L += ["## S3–S5 · события, слоты, память M3 / M4, checkpoint {#s3}", ""] + mermaid_er(s345 + [("agent_run", [("id", "serial", "PK", "")], "код форка"), ("issue", [("id", "serial", "PK", "")], "код форка")], key_only=False) + [""]
    L += ["## S6 · LiteLLM {#s6}", ""] + mermaid_er([(t, c, "") for t, c in DM.LITELLM_TABLES.items()], key_only=False) + [""]
    L += ["## Нереляционные хранилища", ""]
    for s, (title, lines) in DM.TREES.items():
        L += [f"**{s} · {title}**", "", "```"] + lines + ["```", ""]
    L += ["## Контракты обмена {#models}", "",
          "Модели JSON, которыми обмениваются компоненты. Это единственное описание полей: потоки ссылаются сюда, "
          "примеры — в [каталоге API](docs/api/README.md) (сборка сверяет ключи примеров с полями). "
          "У каждой модели — источник, у поля — откуда оно: ✅ поле есть в OpenAPI форка ICPlan; 🛠 поля в форке ещё нет — доработка по решению D… или требованию R-…; 📘 поле задаёт внешняя спецификация (OpenAI, MCP, AG-UI, LiteLLM); 🧩 наш контракт.", "",
          "Строка `a / b` — несколько полей одного назначения, обязательность и тип — у каждого; «в запросе» / «в ответе» — в какой части вызова поле есть; `…` в примерах — сокращение, не часть JSON.", "",
          "### Термины и коды {#terms}", "", *GLOSSARY, "",
          "### Правило имён {#naming}", "", DM.NAMING, ""]
    for m in DM.MODELS:
        L += model_block(m, base="")
    L += ["## Все поля", ""]
    allt = s1 + [x for x in er_tables("mcp-tools") if x[0] not in {t for t, _, _ in s1}] + s2 + s345 + [(t, c, DM.LITELLM_REF) for t, c in DM.LITELLM_TABLES.items()]
    for t, cols, src in allt:
        L += [f'??? note "{t} — {src}"', "", "    | Колонка | Тип | Ключ | Описание |", "    |---|---|---|---|"]
        L += [f"    | `{n}` | {typ} | {key or '—'} | {d or '—'} |" for n, typ, key, d in cols]
        L += policy_md(t, "    ") + [""]
    return "\n".join(L) + "\n"


ENVELOPE = {"run", "messages", "input", "result"}  # транспортные обёртки ответа, не поля модели


def _vocab(name, seen):
    """Имена полей модели и вложенных моделей (по типам полей)."""
    v = set()
    for f in DM.MODELS[name][1]:
        txt = " ".join(str(x) for x in f)
        v |= {w for w in re.findall(r"[A-Za-z_]\w*", txt)}
        for other in DM.MODELS:
            if other != name and other in txt and other not in seen:
                seen.add(other)
                v |= _vocab(other, seen)
    return v


def _free_fields(names):
    """Поля свободного вида (object, map): их содержимое не сверяется."""
    out, todo, seen = set(), list(names), set()
    while todo:
        n = todo.pop()
        if n in seen or n not in DM.MODELS:
            continue
        seen.add(n)
        for f, typ, *_ in DM.MODELS[n][1]:
            if typ.startswith(("object", "map")):
                out |= {x.strip().split(".")[-1] for x in f.split("/")}
            todo += [o for o in DM.MODELS if o in typ]
    return out


def _strip_free(js, free):
    """Убрать значения-объекты полей свободного вида."""
    for k in free:
        while (m := re.search(rf'"{k}"\s*:\s*\{{', js)):
            depth, i = 0, m.end() - 1
            for i in range(m.end() - 1, len(js)):
                depth += {"{": 1, "}": -1}.get(js[i], 0)
                if depth == 0:
                    break
            js = js[:m.start()] + js[i + 1:]
    return js


def example_issues(where, names, js) -> list:
    """Ключи примера JSON ⊆ поля моделей (и вложенных); числовые ключи — идентификаторы."""
    miss = [n for n in names if n not in DM.MODELS]
    issues = [f"{where}: модели {n} нет в datamodel.MODELS" for n in miss]
    v = set().union(*[_vocab(n, {n}) for n in names if n in DM.MODELS] or [set()])
    js = _strip_free(js, _free_fields(names))
    keys = {k for k in re.findall(r'"(\w+)"\s*:', js) if not k.isdigit()} - ENVELOPE
    return issues + [f"{where}: поле {k} не описано в модели {' / '.join(names)}" for k in sorted(keys - v)]


def api_examples_check() -> list:
    """Примеры JSON в docs/api/README.md используют только поля моделей datamodel (О-43);
    в потоках пример допускается только с подписью-моделью и сверяется так же (О-44)."""
    t = (ROOT / "docs/api/README.md").read_text(encoding="utf-8")
    issues = []
    for m in re.finditer(r"^### (.+?)\n(.*?)(?=^### |\Z)", t, re.M | re.S):
        names = [x.strip() for x in m.group(1).split("/")]
        js = "".join(re.findall(r"```json\n(.*?)```", m.group(2), re.S))
        issues += example_issues(f"API: пример {m.group(1)}", names, js)
    for f in sorted((ROOT / "docs/techspec").glob("*.md")):  # JSON — только с подписью-моделью (О-46, О-52)
        L = f.read_text(encoding="utf-8").split("\n")
        for i, line in enumerate(L):
            if line.strip() != "```json":
                continue
            cap = next((L[k] for k in range(i - 1, max(-1, i - 4), -1) if L[k].strip()), "")
            j = next(k for k in range(i + 1, len(L)) if L[k].strip() == "```")
            names = [n for n in re.findall(r"`(\w+)`", cap) if n in DM.MODELS]
            where = f"docs/techspec/{f.name}:{i + 1}"
            if not names:
                issues.append(f"{where}: пример JSON без модели в подписи — модель в datamodel.py, пример в docs/api/README.md")
            else:
                issues += example_issues(where, names, "\n".join(L[i + 1:j]))
    return issues


FLOW_NON_MODELS = {"AgentChatPanel"}  # имена в потоках, которые не модели (компоненты UI)


def _link_models(text, base):
    """`Модель` вне блоков кода → ссылка на её поля."""
    parts = re.split(r"(```.*?```)", text, flags=re.S)
    for k in range(0, len(parts), 2):
        parts[k] = re.sub(r"(?<!\[)`([A-Z][A-Za-z0-9]+)`(?!\])",
                          lambda m: f"[`{m.group(1)}`]({base}data-model.md#model-{m.group(1).lower()})" if m.group(1) in DM.MODELS else m.group(0), parts[k])
    return "".join(parts)


def flow_page(text, slug, nm, base="../../") -> str:
    """Страница потоков: модели — ссылками; раздел «Данные» — ссылки на контракты, хранилища и API, без копий (О-46)."""
    used = [m for m in DM.MODELS if re.search(rf"`{m}`", text)]
    data = ["Поля, источник и пример каждой структуры — по ссылке; здесь они не повторяются ([правило](../rules/doc-types.md#tabs)).", ""]
    if used:
        data += ["**Структуры в этих потоках:** " + " · ".join(f"[`{m}`](../../data-model.md#model-{m.lower()})" for m in used), ""]
    if slug in nm:
        data += [f"**Компонент {nm[slug]}:** [контракты данных](../../components/{slug}/index.md#contracts) · [хранилища](../../components/{slug}/index.md#stores) · "
                 f"[интеграции](../../components/{slug}/index.md#integrations)" + (f" · [API](../api/{slug}.md)" if (ROOT / f"docs/api/{slug}.md").exists() else "")
                 + (f" · [техспека и пример конфигурации](../techspec/{slug}.md)" if (ROOT / f"docs/techspec/{slug}.md").exists() else ""), ""]
    text = text.replace("<!-- flow-data -->", "\n".join(data))
    if "<!-- iface-matrix -->" in text:
        rows = ["Стрелка «от → к» — кто вызывает кого (инициатор запроса); данные идут и в запросе, и в ответе — это в колонке «Что».", "",
                "| I-код | От → к | Что | Модели | Типы данных |", "|---|---|---|---|---|"]
        for i in sorted(DM.INTEG, key=lambda x: int(x[1:])):
            a, b, via, what, models = DM.INTEG[i]
            path = _who(a, nm) + (f" → {_who(via, nm)}" if via else "") + f" → {_who(b, nm)}"
            path = "ICPlan web → ICPlan api" if a == b == "icplan" else path
            rows.append(f"| {i} | {path} | {what} | {', '.join(f'`{m}`' for m in models) or '—'} | {DM.INTEG_TYPES.get(i, '—')} |")
        text = text.replace("<!-- iface-matrix -->", "\n".join(rows))
    return _link_models(text, base)


def flows_check() -> list:
    """Вкладки «Потоки» нет (О-52); «Как работает» в техспеке — порядок работы без конфигов и с существующими моделями."""
    issues = []
    if (ROOT / "docs/flows").exists():
        issues.append("docs/flows: вкладка «Потоки» упразднена — порядок работы в техспеке («Как работает»), процесс пользователя в историях, взаимодействие — в architecture.md")
    for f in sorted((ROOT / "docs/techspec").glob("*.md")):
        t = f.read_text(encoding="utf-8")
        how = t.split("## Как работает", 1)[1].split("\n## ", 1)[0] if "## Как работает" in t else ""
        if re.search(r"^```(yaml|rego)", how, re.M):
            issues.append(f"docs/techspec/{f.name}: конфиг в «Как работает» — место в «Пример конфигурации»")
        body = re.sub(r"```.*?```", "", how, flags=re.S)
        for n in sorted(set(re.findall(r"`([A-Z][a-z]+[A-Z][A-Za-z]*)`", body)) - set(DM.MODELS) - FLOW_NON_MODELS):
            issues.append(f"docs/techspec/{f.name}: `{n}` — нет такой модели в datamodel.MODELS")
    return issues


def check(components) -> list:
    """Сверка: каждый I-код матрицы описан в INTEG; модели из INTEG описаны; I-коды есть в interfaces.md."""
    issues = []
    issues += [f"{i}: нет типов данных в datamodel.INTEG_TYPES" for i in DM.INTEG if i not in DM.INTEG_TYPES]
    issues += [f"{i}: типы данных для неизвестного интерфейса" for i in DM.INTEG_TYPES if i not in DM.INTEG]
    issues += flows_check()
    issues += [f"{i}: модель {m} не описана в datamodel.MODELS" for i, v in DM.INTEG.items() for m in v[4] if m not in DM.MODELS]
    rows = iface_rows()
    issues += [f"{i}: нет строки в «Интерфейсы обмена» спек" for i in DM.INTEG if i not in rows]
    slugs = {c[0] for c in components}
    issues += [f"{i}: неизвестный компонент {x}" for i, v in DM.INTEG.items() for x in v[:3] if x and not x.startswith("«") and x not in slugs]
    issues += api_examples_check()
    issues += policy_check()
    issues += fork_models_check()
    issues += api_structure_check()
    # architecture.md — карта и решения, без значений параметров и конфигов (О-49, doc-work.md#architecture)
    arch = (ROOT / "architecture.md").read_text(encoding="utf-8")
    if re.search(r"^```(yaml|json)", arch, re.M):
        issues.append("architecture.md: блок конфигурации — место в техспеке или interfaces.md")
    for h in re.findall(r"^\| ([^|\n]+) \|.*$", arch, re.M):
        if re.search(r"Порог|По умолчанию|Значение|Переменная", h):
            issues.append(f"architecture.md: таблица значений «{h.strip()}» — значения живут в interfaces.md спек")
    issues += param_mirror_check()
    # схема ICPlan не отстала от форка (О-44): коммит app.ts в форке = коммит импорта
    meta = json.loads((HERE / "icplan_schema.meta.json").read_text(encoding="utf-8"))
    import schema_import as SI
    if SI.DEFAULT.exists():
        cur = SI.fork_commit(SI.DEFAULT)
        if cur and cur != meta["commit"]:
            issues.append(f"схема ICPlan изменилась в форке ({meta['commit'][:8]} → {cur[:8]}): python html-view/schema_import.py")
    ver = re.search(r"v\d+\.\d+\.\d+", DM.LITELLM_REF).group(0)
    tech = (ROOT / "docs/TECHNOLOGIES.md").read_text(encoding="utf-8")
    if not re.search(rf"LiteLLM[^\n]*{re.escape(ver)}", tech):
        issues.append(f"таблицы LiteLLM сняты со схемы {ver}, а в TECHNOLOGIES.md закреплена другая версия — пересверить schema.prisma")
    for v in SCHEMA.values():
        for c in v["cols"]:
            if c["ref"] and c["ref"] not in SCHEMA:
                issues.append(f"{v['table']}.{c['name']}: FK на неизвестную таблицу {c['ref']}")
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
