"""Каталоги для перечислений схемы данных (data/): строятся автоматически из данных и документов, руками не ведутся.

Каталог — множество допустимых значений поля: компоненты, блоки, участники, модели, таблицы, I-коды, R-коды, US, задачи,
D-номера, роли, спеки, требования спек, эндпоинты, параметры компонента (из interfaces.md его спек) и их типы.
Используется yaml-check (значение не из каталога — ошибка с подсказкой ближайшего) и yaml-schema (enum в JSON Schema).
Методология: docs/rules/data-methodology.md#yaml-units.
"""
import difflib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
DATA = ROOT / "data"
_C = {}


def clear():
    _C.clear()


def _cached(name, fn):
    if name not in _C:
        _C[name] = fn()
    return _C[name]


def _Y():
    import yamldata as Y
    return Y


def _stems(sub):
    return sorted(f.stem for f in (DATA / sub).glob("*.yaml") if not f.stem.startswith("_"))


def _sortkey(x):
    return [int(n) if n.isdigit() else n for n in re.split(r"(\d+)", str(x))]


# ---------------------------------------------------------------- каталоги
def components():
    return _cached("components", lambda: _stems("components"))


def component_names():
    return _cached("component_names", lambda: [c[1] for c in _Y().components()["COMPONENTS"]])


def blocks(comp=None):
    """Названия блоков компонента (или всех)."""
    allb = _cached("blocks", lambda: [(c, t) for (c, t) in _Y().sub()])
    return sorted({t for c, t in allb if comp is None or c == comp})


def roles():
    return _cached("roles", lambda: sorted(set(_Y().stories()["ROLES"]) | set(_Y().stories()["PERSONAS"])))


def participants():
    """С кем блок обменивается (io.with, ops.who): компонент (slug или имя), блок, «Компонент · Блок», роль (код или имя)."""
    def build():
        Y = _Y()
        comps = Y.components()["COMPONENTS"]
        names = {c[0]: c[1] for c in comps}
        out = set(names) | set(names.values())
        for (c, t) in Y.sub():
            out.add(t)
            out.add(f"{names.get(c, c)} · {t}")
        st = Y.stories()
        out |= set(st["ROLES"]) | set(st["ROLES"].values())
        return sorted(out)
    return _cached("participants", build)


def models():
    return _cached("models", lambda: _stems("models"))


def tables():
    def build():
        schema = json.loads((HERE / "icplan_schema.json").read_text(encoding="utf-8"))
        d = _Y().datamodel()
        return sorted(set(d["PLATFORM_TABLES"]) | {v["table"] for v in schema.values()} | set(d["LITELLM_TABLES"]) | set(d["FORK_COLUMNS"]))
    return _cached("tables", build)


def icplan_keys():
    return _cached("icplan_keys", lambda: sorted(json.loads((HERE / "icplan_schema.json").read_text(encoding="utf-8"))))


def table_columns(t):
    """Колонки таблицы (платформа, LiteLLM, форк — из data/tables)."""
    d = _Y().datamodel()
    cols = d["PLATFORM_TABLES"].get(t, (None, None, None))[2] or d["LITELLM_TABLES"].get(t) or d["FORK_COLUMNS"].get(t) or []
    return [c[0] for c in cols]


def icodes():
    return _cached("icodes", lambda: sorted(_Y().datamodel()["INTEG"], key=_sortkey))


def reqs():
    def build():
        txt = "".join(f.read_text(encoding="utf-8") for f in ROOT.glob("openspec/changes/*/specs/*/spec.md"))
        return sorted(set(re.findall(r"`(R-[A-Z]+-\d+)`", txt)), key=_sortkey)
    return _cached("reqs", build)


def stories():
    return _cached("stories", lambda: sorted((f.stem for f in DATA.glob("stories/*/*.yaml") if not f.stem.startswith("_")), key=_sortkey))


def tasks():
    def build():
        return sorted({m.group(1) for f in (ROOT / "docs/tasks").glob("*.md") for m in [re.match(r"(\d+\.\d+)-", f.name)] if m}, key=_sortkey)
    return _cached("tasks", build)


def decisions():
    def build():
        txt = "".join(f.read_text(encoding="utf-8") for f in ROOT.glob("openspec/changes/*/design.md"))
        return sorted(set(re.findall(r"^### (D\d+)\.", txt, flags=re.M)), key=_sortkey)
    return _cached("decisions", build)


def specs():
    return _cached("specs", lambda: sorted({f.parent.name for f in ROOT.glob("openspec/changes/*/specs/*/spec.md")}))


def spec_requirements(spec):
    """Заголовки «### Requirement: …» спеки."""
    def build():
        out = {}
        for f in ROOT.glob("openspec/changes/*/specs/*/spec.md"):
            out.setdefault(f.parent.name, []).extend(re.findall(r"^### Requirement: (.+?)\s*$", f.read_text(encoding="utf-8"), flags=re.M))
        return out
    return _cached("spec_reqs", build).get(spec, [])


def endpoints():
    """«МЕТОД путь» из data/endpoints (страницы API) и операций форка ICPlan (html-view/icplan_openapi.json)."""
    def build():
        ops = json.loads((HERE / "icplan_openapi.json").read_text(encoding="utf-8"))["operations"]
        return sorted(set(_Y().datamodel()["ENDPOINT_IO"]) | {re.sub(r"\{(\w+)\}", r":\1", k) for k in ops})  # {runId} → :runId, как в документах
    return _cached("endpoints", build)


def rnd_files():
    return _cached("rnd", lambda: sorted(f.name for f in (ROOT / "docs/rnd").glob("*.md")))


def stores():
    """Хранилища S<N> — строки таблиц хранилищ interfaces.md спек."""
    def build():
        return sorted({m for f in ROOT.glob("openspec/changes/*/specs/*/interfaces.md")
                       for m in re.findall(r"^\| (S\d+) \| ", f.read_text(encoding="utf-8"), flags=re.M)}, key=_sortkey)
    return _cached("stores", build)


# ---------------------------------------------------------------- параметры из interfaces.md
def _spec_param_rows(itf: Path) -> list:
    """Строки таблиц «Параметры модуля» interfaces.md: [{колонка: значение}]."""
    lines = itf.read_text(encoding="utf-8").splitlines()
    out = []
    for i, l in enumerate(lines):
        if not l.startswith("| Параметр | Что задаёт |"):
            continue
        cols = [c.strip() for c in l.strip("|").split("|")]
        for row in lines[i + 2:]:
            if not row.startswith("|"):
                break
            cells = [c.strip() for c in re.split(r"(?<!\\)\|", row.strip())[1:-1]]
            out.append(dict(zip(cols, cells)))
    return out


def comp_specs(comp):
    """Папки спек компонента (по полю specs компонента)."""
    def build():
        out = {}
        for c in _Y().components()["COMPONENTS"]:
            out[c[0]] = [ROOT / p for _, p in c[6] if p.endswith("/spec.md")]
        return out
    return _cached("comp_specs", build).get(comp, [])


def params(comp):
    """Параметры компонента: имя → {spec, default, min, max, type}. Первый по порядку спек (как build.component_params)."""
    def build():
        out = {}
        for c in components():
            d = {}
            for sp in comp_specs(c):
                itf = sp.with_name("interfaces.md")
                if not itf.exists():
                    continue
                for r in _spec_param_rows(itf):
                    name = r.get("Параметр", "").strip("`")
                    if name and name not in d:
                        d[name] = {"spec": sp.parent.name, "default": r.get("По умолчанию", ""), "min": r.get("Мин", ""),
                                   "max": r.get("Макс", ""), "what": r.get("Что задаёт", "")}
                        d[name]["type"] = param_type(d[name])
            out[c] = d
        return out
    return _cached("params", build).get(comp, {})


_NUM = r"(\d[\d  ]*(?:[.,]\d+)?)"
_UNITS = ("$", "%", "КБ", "МБ", "ГБ")
_DUR = {"с": 1, "сек": 1, "мин": 60, "ч": 3600, "д": 86400, "дн": 86400, "дня": 86400, "дней": 86400, "день": 86400}
_ONOFF = [{"вкл", "выкл"}, {"true", "false"}, {"да", "нет"}, {"включён", "выключен"}]


def _clean(s):
    return re.sub(r"\s*\([^)]*\)$", "", s.strip()).strip()


def parse_num(s):
    """(число, единица) или None: «200 000», «5 $», «0,1 $», «80%»."""
    m = re.fullmatch(_NUM + r"\s*(\$|%|КБ|МБ|ГБ)?", _clean(s))
    if not m:
        return None
    return float(re.sub(r"[  ]", "", m.group(1)).replace(",", ".")), m.group(2) or ""


def parse_dur(s):
    """Секунды или None: «24 ч», «15 мин», «7 дней»."""
    m = re.fullmatch(_NUM + r"\s*(с|сек|мин|ч|д|дн|дня|дней|день)", _clean(s))
    if not m:
        return None
    return float(re.sub(r"[  ]", "", m.group(1)).replace(",", ".")) * _DUR[m.group(2)]


def param_type(r):
    """Формальный тип параметра по колонкам «По умолчанию», «Мин», «Макс» или None (описан словами)."""
    d, mn, mx = (_clean(r[k]) for k in ("default", "min", "max"))
    nd, nmn, nmx = parse_num(d), parse_num(mn), parse_num(mx)
    if nd and nmn and nd[1] == nmn[1]:
        mxv = nmx[0] if nmx and nmx[1] == nd[1] else None
        if mxv is not None and mxv < nmn[0]:  # «0 (полная история)» — особое значение, не граница: словами
            return None
        return {"kind": "number", "unit": nd[1], "min": nmn[0], "max": mxv}
    dd, dmn, dmx = parse_dur(d), parse_dur(mn), parse_dur(mx)
    if dd is not None and dmn is not None:
        return {"kind": "duration", "min": dmn, "max": dmx}
    for s in _ONOFF:
        if {d, mn, mx} <= s:
            return {"kind": "enum", "values": sorted(s)}
    if all(re.fullmatch(r"[a-z][a-z0-9_\-]*", x) for x in (d, mn, mx)):
        return {"kind": "enum", "values": sorted({d, mn, mx})}
    g = [re.fullmatch(r"([A-Z])(\d)", x) for x in (d, mn, mx)]
    if all(g) and len({x.group(1) for x in g}) == 1:
        lo, hi = int(g[1].group(2)), int(g[2].group(2))
        return {"kind": "enum", "values": [f"{g[0].group(1)}{i}" for i in range(lo, hi + 1)]}
    return None


def type_text(t) -> str:
    if t["kind"] == "number":
        u = f" {t['unit']}" if t["unit"] else ""
        return f"число{u} от {t['min']:g}" + (f" до {t['max']:g}" if t["max"] is not None else "")
    if t["kind"] == "duration":
        return "длительность (с, мин, ч, д)" + f" от {t['min']:g} с" + (f" до {t['max']:g} с" if t["max"] is not None else "")
    return "одно из: " + ", ".join(t["values"])


def value_ok(t, v: str) -> bool:
    """Значение параметра соответствует формальному типу."""
    if t["kind"] == "number":
        n = parse_num(v)
        return bool(n) and n[1] == t["unit"] and n[0] >= t["min"] and (t["max"] is None or n[0] <= t["max"])
    if t["kind"] == "duration":
        n = parse_dur(v)
        return n is not None and n >= t["min"] and (t["max"] is None or n <= t["max"])
    return v in t["values"]


# ---------------------------------------------------------------- проверка ссылки
def suggest(v, cat) -> str:
    near = difflib.get_close_matches(str(v), [str(x) for x in cat], n=3, cutoff=0.5)
    return f" — может быть: {', '.join(near)}" if near else ""


CATALOGS = {
    "component": (components, "slug компонента — файл data/components/<slug>.yaml"),
    "participant": (participants, "компонент, блок, «Компонент · Блок» или роль; иначе — label"),
    "model": (models, "модель — файл data/models/<Имя>.yaml"),
    "table": (tables, "таблица — data/tables, схема форка (icplan_schema.json) или LiteLLM"),
    "icplan_key": (icplan_keys, "ключ html-view/icplan_schema.json"),
    "icode": (icodes, "I-код из data/integrations.yaml"),
    "req": (reqs, "код R-… из spec.md"),
    "story": (stories, "история — файл data/stories/<компонент>/<US-ID>.yaml"),
    "task": (tasks, "номер задачи docs/tasks/<номер>-*.md"),
    "decision": (decisions, "решение «### D<N>.» в openspec/changes/*/design.md"),
    "role": (roles, "ключ roles / personas в data/personas.yaml"),
    "spec": (specs, "папка спеки openspec/changes/*/specs/<спека>"),
    "endpoint": (endpoints, "«МЕТОД путь» из data/endpoints или icplan_openapi.json"),
    "rnd": (rnd_files, "файл в docs/rnd"),
    "store": (stores, "хранилище S<N> — таблица хранилищ interfaces.md спек"),
}


def values(cat, comp=None):
    if cat == "param":
        return sorted(params(comp)) if comp else sorted({n for c in components() for n in params(c)})
    return CATALOGS[cat][0]()


def check(cat, v, comp=None):
    """None или сообщение «значения нет в каталоге — может быть: …»."""
    if cat == "param":
        if not comp:
            return None
        cv = params(comp)
        return None if v in cv else f"«{v}» нет среди параметров interfaces.md спек компонента {comp}{suggest(v, cv)}"
    if cat == "ref":  # смешанный список ID: по префиксу
        k = id_kind(v)
        return check(k, v) if k else f"«{v}» — не ID (I…, R-…, D…, US-…)"
    fn, what = CATALOGS[cat]
    cv = fn()
    return None if v in cv else f"«{v}» нет в каталоге: {what}{suggest(v, cv)}"


def id_kind(v):
    for rx, k in ((r"I\d+", "icode"), (r"R-[A-Z]+-\d+", "req"), (r"D\d+", "decision"), (r"US-[A-Z]+-\d+", "story")):
        if re.fullmatch(rx, v):
            return k
    return None
