"""Данные сайта в YAML по единице (data/): схема, загрузка, выгрузка, проверка, формат, карточка единицы.

Единица — один файл 1–3 КБ: блок, компонент, модель, таблица, эндпоинты страницы API, истории и процессы компонента.
Модули datamodel.py, subcomponents.py, stories.py, components.py только загружают отсюда значения (имена прежние).
Методология: docs/rules/data-methodology.md#yaml (схема единиц — #yaml-units). Команды: doctool yaml-check | yaml-fmt | unit | yaml-schema | yaml-migrate | yaml-export.
Каталоги для полей-ссылок — html-view/yamlcat.py; прежний позиционный вид и перевод — html-view/yamlmigrate.py.

Раскладка (порядок — data/<вид>/_order.yaml: список имён файлов без .yaml):
    data/components/<slug>.yaml        COMPONENTS, ABOUT, BLOCKS (схема), datamodel.STORES, ICPLAN_TABLES
    data/blocks/<компонент>/<slug>.yaml  subcomponents.SUB[(компонент, title)]
    data/hosts.yaml                    components.HOST
    data/models/<Имя>.yaml             MODELS, MODEL_META (source), FIELD_SRC, PLANNED
    data/tables/<имя>.yaml             PLATFORM_TABLES, SCHEMA_OF, TABLE_POLICY, FORK_COLUMNS, FORK_WRITTEN, LITELLM_TABLES
    data/endpoints/<страница API>.yaml ENDPOINT_IO (страница = docs/api/<страница>.md)
    data/integrations.yaml             INTEG, INTEG_TYPES, ALSO, DATA_IN_RESPONSE
    data/databases.yaml                DB_CLUSTER, DATABASES, DB_GRANTS, MIGRATE
    data/datamodel.yaml                NAMING, LITELLM_REF, S1_DOMAINS, TREES
    data/stories/<компонент>/<US-ID>.yaml  STORIES (история), CHAINS (chain)
    data/processes/<компонент>.yaml    BPMN, ARTIFACTS
    data/personas.yaml                 ROLES, PERSONAS
    data/costs.yaml                    журнал расхода токенов (html-view/cost.py, docs/rules/token-costs.md)
"""
import json
import re
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
DATA = ROOT / "data"
_Loader = getattr(yaml, "CSafeLoader", yaml.SafeLoader)


# ---------------------------------------------------------------- схема
class Ctx:
    """Контекст проверки: ошибки, (для yaml-check) проверка ссылок по каталогам, компонент файла (для имён параметров)."""

    def __init__(self, refs=False, comp=None):
        self.errors, self.refs, self.comp = [], refs, comp

    def err(self, p, msg):
        self.errors.append(f"{p or '<корень>'} → {msg}")


def _kind(v):
    return {str: "строка", int: "число", bool: "да/нет", list: "список", dict: "словарь", float: "дробное", type(None): "null"}.get(type(v), type(v).__name__)


def _jsre(rx):
    return "^(?:" + rx + ")$"


class Any_:
    scalar = True
    desc = ""

    def load(self, v, p, c):
        return v

    def dump(self, v):
        return v

    def accepts(self, v):
        return True

    def js(self, ctx):
        return {}


class Str(Any_):
    def __init__(self, choices=None, pattern=None, ref=None, hint="", desc=""):
        self.choices, self.pattern, self.ref, self.hint, self.desc = choices, pattern, ref, hint, desc

    def accepts(self, v):
        return isinstance(v, str)

    def load(self, v, p, c):
        if not isinstance(v, str):
            c.err(p, f"нужна строка, а не {_kind(v)} — возьми значение в кавычки")
            return v
        if not c.refs:  # загрузка модулем — только структура и типы; значения и ссылки — yaml-check
            return v
        if self.choices and v not in self.choices:
            c.err(p, f"«{v}» — допустимо: {', '.join(x or '«»' for x in self.choices)}" + _cat().suggest(v, self.choices))
        if self.pattern and v and not re.fullmatch(self.pattern, v):
            c.err(p, f"«{v}» не по формату {self.hint or self.pattern}")
        if self.ref and v:
            bad = REF[self.ref](v)
            if bad:
                c.err(p, bad)
        return v

    def js(self, ctx):
        out = {"type": "string"}
        if self.choices:
            out["enum"] = list(self.choices)
        elif self.pattern:
            out["pattern"] = _jsre(self.pattern)
        return out


def _cat():
    import yamlcat
    return yamlcat


class Ref(Str):
    """Значение из каталога (yamlcat): не из списка — ошибка yaml-check с подсказкой ближайшего; в JSON Schema — enum."""

    def __init__(self, cat, desc="", also=None):
        super().__init__(desc=desc)
        self.cat, self.also = cat, also  # also — регулярка допустимых значений вне каталога (S<N> вместо таблицы)

    def load(self, v, p, c):
        if not isinstance(v, str):
            c.err(p, f"нужна строка, а не {_kind(v)} — возьми значение в кавычки")
            return v
        if c.refs and v and not (self.also and re.fullmatch(self.also, v)):
            bad = _cat().check(self.cat, v, c.comp)
            if bad:
                c.err(p, bad)
        return v

    def js(self, ctx):
        if self.cat == "ref":
            return {"type": "string", "pattern": _jsre(r"I\d+|R-[A-Z]+-\d+|D\d+|US-[A-Z]+-\d+")}
        if self.cat == "param" and not ctx.get("comp"):
            return {"type": "string"}
        if self.cat == "param":
            out = {"type": "string", "enum": [str(x) for x in _cat().values(self.cat, ctx.get("comp"))]}
        else:  # каталоги — один раз в catalog.schema.json
            out = {"$ref": f"catalog.schema.json#/definitions/{self.cat}"}
        alts = [out] + ([{"type": "string", "pattern": _jsre(self.also)}] if self.also else []) + [{"const": ""}]  # пусто — как в yaml-check
        return {"anyOf": alts}


class Int(Any_):
    def accepts(self, v):
        return isinstance(v, int) and not isinstance(v, bool)

    def load(self, v, p, c):
        if not self.accepts(v):
            c.err(p, f"нужно целое число, а не {_kind(v)}")
        return v

    def js(self, ctx):
        return {"type": "integer"}


class Bool(Any_):
    def accepts(self, v):
        return isinstance(v, bool)

    def load(self, v, p, c):
        if not isinstance(v, bool):
            c.err(p, f"нужно true или false, а не {_kind(v)}")
        return v

    def js(self, ctx):
        return {"type": "boolean"}


class Opt(Any_):
    """Значение или null."""

    def __init__(self, inner):
        self.inner = inner
        self.scalar = inner.scalar

    def accepts(self, v):
        return v is None or self.inner.accepts(v)

    def load(self, v, p, c):
        return None if v is None else self.inner.load(v, p, c)

    def dump(self, v):
        return None if v is None else self.inner.dump(v)

    def js(self, ctx):
        return {"anyOf": [{"type": "null"}, self.inner.js(ctx)]}


class FlowList(list):
    pass


class FlowDict(dict):
    pass


class Lst(Any_):
    """Список. flow=True — в одну строку: [a, b] (короткие ID)."""
    scalar = False

    def __init__(self, item, flow=False):
        self.item, self.flow = item, flow

    def accepts(self, v):
        return isinstance(v, list)

    def load(self, v, p, c):
        if not isinstance(v, list):
            c.err(p, f"нужен список, а не {_kind(v)}")
            return v
        return [self.item.load(x, f"{p}[{i}]", c) for i, x in enumerate(v)]

    def dump(self, v):
        out = [self.item.dump(x) for x in v]
        return FlowList(out) if self.flow else out

    def js(self, ctx):
        return {"type": "array", "items": self.item.js(ctx)}


class Tup(Any_):
    """Строка таблицы: [a, b, c] в YAML, кортеж в Python (прежний позиционный вид; в схемах единиц — только для yaml-migrate)."""
    scalar = False

    def __init__(self, *items, names=()):
        self.items, self.names = items, names

    def accepts(self, v):
        return isinstance(v, list)

    def load(self, v, p, c):
        if not isinstance(v, list) or len(v) != len(self.items):
            hint = f" [{', '.join(self.names)}]" if self.names else ""
            c.err(p, f"нужна строка из {len(self.items)} значений{hint}, а не {_kind(v) if not isinstance(v, list) else len(v)}")
            return tuple(v) if isinstance(v, list) else v
        return tuple(s.load(x, f"{p}[{i}]", c) for i, (s, x) in enumerate(zip(self.items, v)))

    def dump(self, v):
        return FlowList(s.dump(x) for s, x in zip(self.items, v))

    def js(self, ctx):
        return {"type": "array", "items": [s.js(ctx) for s in self.items], "minItems": len(self.items), "maxItems": len(self.items)}


class Fields(Any_):
    """Общее для записей: fields = [(имя, схема, режим, описание)], режим: "req" | "opt" | ("def", значение по умолчанию)."""
    scalar = False

    def __init__(self, *fields, flow=False, tag=None, one_of=()):
        self.fields = [tuple(f) + ("req", "")[len(f) - 2:] if len(f) < 4 else tuple(f) for f in fields]
        self.flow, self.tag, self.one_of = flow, tag, one_of  # one_of — хотя бы одно из полей (with | label)
        self.names = [f[0] for f in self.fields]

    def accepts(self, v):
        return isinstance(v, dict) and (self.tag is None or self.tag in v)

    def _load_map(self, v, p, c):
        if not isinstance(v, dict):
            c.err(p, f"нужен словарь с полями {', '.join(self.names)}, а не {_kind(v)}")
            return None
        for k in v:
            if k not in self.names:
                c.err(f"{p}.{k}" if p else str(k), f"лишнее поле — допустимы: {', '.join(self.names)}" + _cat().suggest(k, self.names))
        out = {}
        for name, sch, mode, _ in self.fields:
            q = f"{p}.{name}" if p else name
            if name in v:
                out[name] = sch.load(v[name], q, c)
            elif mode == "req":
                c.err(q, "обязательное поле не заполнено")
            elif isinstance(mode, tuple):
                out[name] = mode[1]() if callable(mode[1]) else mode[1]
        if self.one_of and not any(v.get(k) for k in self.one_of):
            c.err(p, f"нужно хотя бы одно из полей: {', '.join(self.one_of)}")
        return out

    def js(self, ctx):
        props = {}
        for name, sch, mode, desc in self.fields:
            j = dict(sch.js(ctx))
            d = desc or getattr(sch, "desc", "")
            if d:
                j["description"] = d
            props[name] = j
        out = {"type": "object", "properties": props, "additionalProperties": False,
               "required": [n for n, _, m, _ in self.fields if m == "req"]}
        if self.one_of:
            out["anyOf"] = [{"required": [k]} for k in self.one_of]
        return out


class Rec(Fields):
    """Словарь с известными полями (в Python — dict в порядке схемы)."""

    def load(self, v, p, c):
        out = self._load_map(v, p, c)
        return v if out is None else out

    def dump(self, v):
        out = {}
        for name, sch, mode, _ in self.fields:
            if name not in v:
                continue
            if isinstance(mode, tuple) and v[name] == (mode[1]() if callable(mode[1]) else mode[1]):
                continue
            out[name] = sch.dump(v[name])
        return FlowDict(out) if self.flow else out


class TRec(Fields):
    """Словарь в YAML, кортеж в Python (поля по порядку; необязательное поле без значения пропускается)."""

    def load(self, v, p, c):
        out = self._load_map(v, p, c)
        return v if out is None else tuple(out[n] for n in self.names if n in out)

    def dump(self, v):
        opt = [i for i, f in enumerate(self.fields) if f[2] != "req"]
        idx = list(range(len(self.fields)))
        if len(v) < len(self.fields):  # без необязательных полей (не больше одного пропуска на запись)
            idx = [i for i in idx if i not in opt[:len(self.fields) - len(v)]]
        out = {self.fields[i][0]: self.fields[i][1].dump(x) for i, x in zip(idx, v)}
        return FlowDict(out) if self.flow else out


class Row(Fields):
    """Строка таблицы с именованными полями: словарь в YAML, прежнее значение в Python (кортеж или строка).

    to_py(поля) → значение для модулей (прежняя структура, тексты собираются из полей — страницы не меняются);
    from_py(значение) → варианты полей по убыванию извлечения ID; берётся первый, который собирается обратно без потерь.
    Последний вариант — без извлечения (текст как есть)."""

    def __init__(self, *fields, to_py, from_py, flow=True, tag=None, one_of=()):
        super().__init__(*fields, flow=flow, tag=tag, one_of=one_of)
        self.to_py, self.from_py = to_py, from_py

    def load(self, v, p, c):
        out = self._load_map(v, p, c)
        if out is None:
            return v
        try:
            return self.to_py(out)
        except (KeyError, TypeError) as e:
            c.err(p, f"не собрать строку из полей ({e})")
            return v

    def dump(self, v):
        for cand in self.from_py(v):
            if any(k not in self.names and x not in (None, "", [], False) for k, x in cand.items()):
                continue  # извлечённого поля нет в этой строке
            cand = {k: x for k, x in cand.items() if k in self.names and (self._required(k) or x not in (None, "", [], False))}
            full = {**{n: (m[1]() if callable(m[1]) else m[1]) for n, _, m, _ in self.fields if isinstance(m, tuple) and n not in cand}, **cand}
            try:
                same = self.to_py(full) == v
            except KeyError:
                same = False
            if same:
                out = {name: sch.dump(cand[name]) for name, sch, _, _ in self.fields if name in cand}
                return FlowDict(out) if self.flow else out
        raise ValueError(f"строка не собирается обратно: {v!r}")

    def _required(self, k):
        return next(m for n, _, m, _ in self.fields if n == k) == "req"


class Map(Any_):
    """Словарь с произвольными ключами: ключ → значение по схеме."""
    scalar = False

    def __init__(self, key, val, flow=False):
        self.key, self.val, self.flow = key, val, flow

    def accepts(self, v):
        return isinstance(v, dict)

    def load(self, v, p, c):
        if not isinstance(v, dict):
            c.err(p, f"нужен словарь, а не {_kind(v)}")
            return v
        out = {}
        for k, x in v.items():
            self.key.load(k, f"{p}[{k}]" if p else str(k), c)
            out[k] = self.val.load(x, f"{p}.{k}" if p else str(k), c)
        return out

    def dump(self, v):
        out = {k: self.val.dump(x) for k, x in v.items()}
        return FlowDict(out) if self.flow else out

    def js(self, ctx):
        out = {"type": "object", "additionalProperties": self.val.js(ctx)}
        k = self.key.js(ctx)
        if k.get("pattern") or k.get("enum"):
            out["propertyNames"] = k
        return out


class OneOf(Any_):
    """Один из вариантов — по виду значения в YAML (строка, список, словарь с полем-меткой)."""
    scalar = False

    def __init__(self, *alts, hint=""):
        self.alts, self.hint = alts, hint

    def accepts(self, v):
        return any(a.accepts(v) for a in self.alts)

    def _pick(self, v):
        return next((a for a in self.alts if a.accepts(v)), None)

    def load(self, v, p, c):
        a = self._pick(v)
        if a is None:
            c.err(p, f"не тот вид значения ({_kind(v)}): {self.hint}")
            return v
        return a.load(v, p, c)

    def dump(self, v):
        for a in self.alts:
            if (isinstance(a, Str) and isinstance(v, str)) or (isinstance(a, (Lst, Tup)) and isinstance(v, (list, tuple))) \
                    or (isinstance(a, Fields) and isinstance(v, dict) and (a.tag is None or a.tag in v)):
                return a.dump(v)
        return v

    def js(self, ctx):
        return {"anyOf": [a.js(ctx) for a in self.alts]}


class Lazy(Any_):
    scalar = False

    def __init__(self, fn, name):
        self.fn, self.name = fn, name

    def __getattr__(self, k):
        return getattr(self.fn(), k)

    def accepts(self, v):
        return self.fn().accepts(v)

    def load(self, v, p, c):
        return self.fn().load(v, p, c)

    def dump(self, v):
        return self.fn().dump(v)

    def js(self, ctx):
        defs = ctx.setdefault("definitions", {})
        if self.name not in defs:
            defs[self.name] = {}
            defs[self.name] = self.fn().js(ctx)
        return {"$ref": f"#/definitions/{self.name}"}


class NextStep(Any_):
    """Переход процесса: «куда» строкой или {to, label}; в Python — (куда, подпись)."""
    scalar = False

    def accepts(self, v):
        return isinstance(v, (str, dict))

    def load(self, v, p, c):
        if isinstance(v, str):
            return (v, "")
        if isinstance(v, dict) and set(v) <= {"to", "label"} and isinstance(v.get("to"), str) and isinstance(v.get("label", ""), str):
            return (v["to"], v.get("label", ""))
        c.err(p, "переход — id шага строкой или {to: <id шага>, label: <подпись>}")
        return ("", "")

    def dump(self, v):
        return v[0] if not v[1] else FlowDict(to=v[0], label=v[1])

    def js(self, ctx):
        return {"anyOf": [{"type": "string", "description": "id шага"},
                          {"type": "object", "properties": {"to": {"type": "string", "description": "id шага"},
                                                            "label": {"type": "string", "description": "подпись перехода (да / нет)"}},
                           "required": ["to"], "additionalProperties": False}]}


# ---------------------------------------------------------------- ссылки без каталога (yaml-check)
_REFCACHE = {}


def _cached(name, fn):
    if name not in _REFCACHE:
        _REFCACHE[name] = fn()
    return _REFCACHE[name]


def _stems(sub):
    return {f.stem for f in (DATA / sub).glob("*.yaml") if not f.stem.startswith("_")}


def _miss(what, ok, fix):
    return None if ok else f"{what} — {fix}"


REF = {
    "component*": lambda v: None if v.startswith("«") or v in _cached("comp", lambda: _stems("components"))
    else f"«{v}» — slug компонента (data/components) или внешний участник в «…»" + _cat().suggest(v, _cat().components()),
    "path": lambda v: _miss(f"файла {v} нет", (ROOT / v).exists(), "путь от корня репозитория"),
}


# ---------------------------------------------------------------- ID в тексте: хвост «(I11, R-MEM-04, D20)», «(FMEA <спека>; R-…)»
_ID = r"(?:I\d+|R-[A-Z]+-\d+|D\d+)"
_IDS = rf"{_ID}(?:, {_ID})*"


def split_ids(text):
    """(тело, fmea, [ID]) — хвост в скобках, составленный только из ID (и «FMEA <спека>»); нет такого хвоста — (text, None, [])."""
    if re.fullmatch(_IDS, text):
        return "", None, text.split(", ")
    m = re.fullmatch(rf"(.*?) \(((?:FMEA [a-z-]+)?(?:; )?(?:{_IDS})?)\)", text, flags=re.S)
    if not m or not m.group(2):
        return text, None, []
    inner = m.group(2)
    fm = re.match(r"FMEA ([a-z-]+)(?:; )?", inner)
    fmea = fm.group(1) if fm else None
    rest = inner[fm.end():] if fm else inner
    if fm and rest and not inner[fm.end() - 2:fm.end()] == "; ":
        return text, None, []
    return m.group(1), fmea, (rest.split(", ") if rest else [])


def join_ids(body, fmea=None, ids=()):
    groups = ([f"FMEA {fmea}"] if fmea else []) + ([", ".join(ids)] if ids else [])
    if not groups:
        return body
    return f"{body} ({'; '.join(groups)})" if body else "; ".join(groups)


def _by_kind(ids):
    """ID хвоста → поля via (I), reqs (R), decisions (D); порядок при сборке — via, reqs, decisions."""
    d = {"via": [], "reqs": [], "decisions": []}
    for i in ids:
        d["via" if i.startswith("I") else "reqs" if i.startswith("R-") else "decisions"].append(i)
    return d


def _ids_of(d):
    return list(d.get("via") or []) + list(d.get("reqs") or []) + list(d.get("decisions") or [])


def _sfx(text, fmea_ok=False):
    """Варианты (тело, поля хвоста): с извлечением ID и без."""
    body, fmea, ids = split_ids(text)
    out = []
    if (ids or fmea) and (fmea_ok or not fmea) and (not fmea or fmea in _cat().specs()):
        d = _by_kind(ids)
        if fmea:
            d["fmea"] = fmea
        out.append((body, d))
    out.append((text, {}))
    return out


_EP = r"(?:GET|POST|PUT|PATCH|DELETE) [^`]+"


def _known_endpoints(eps):
    return all(e in _cat().endpoints() for e in eps)


# ---------------------------------------------------------------- строки таблиц: поля ↔ прежнее значение
S = Str()
DIR = Str(choices=("→", "←", "↔"), desc="направление: → блок отдаёт, ← блок получает, ↔ в обе стороны")
VIA = Lst(Ref("icode"), flow=True)
REQS = Lst(Ref("req"), flow=True)
DECS = Lst(Ref("decision"), flow=True)
SFX = [("via", VIA, "opt", "I-коды интерфейса (data/integrations.yaml)"), ("reqs", REQS, "opt", "R-коды требований"),
       ("decisions", DECS, "opt", "решения D<N> (design.md)")]


def _models_text(models, what):
    if not models:
        return what
    return ", ".join(f"`{m}`" for m in models) + (f" — {what}" if what else "")


def _io_py(d):
    return (d["dir"], d.get("label") or d["with"], join_ids(_models_text(d.get("model"), d.get("what", "")), None, _ids_of(d)))


def _who(w, key="with"):
    return {key: w} if w in _cat().participants() else {"label": w}


def _io_from(v):
    dr, w, text = v
    for body, ids in _sfx(text):
        m = re.fullmatch(r"(`[A-Z]\w*`(?:, `[A-Z]\w*`)*)(?: — (.*))?", body, flags=re.S)
        if m:
            ms = re.findall(r"`(\w+)`", m.group(1))
            if all(x in _cat().models() for x in ms):
                yield {"dir": dr, **_who(w), "model": ms, "what": m.group(2) or "", **ids}
        yield {"dir": dr, **_who(w), "what": body, **ids}
    yield {"dir": dr, "label": w, "what": text}


IO_ROW = Row(("dir", DIR), ("with", Ref("participant"), "opt", "с кем: компонент, блок, «Компонент · Блок» или роль (каталог)"),
             ("label", S, "opt", "подпись участника, если её нет в каталоге или она отличается (текст как на странице)"),
             ("model", Lst(Ref("model"), flow=True), "opt", "модели data/models, которые передаются"),
             ("what", S, "opt", "что передаётся (без моделей и I-кодов)"), *SFX,
             to_py=_io_py, from_py=_io_from, one_of=("with", "label"))

ACCESS = {"read": "чтение", "write": "запись", "read-write": "запись, чтение", "store": "хранение", "indirect": "косвенно"}


def _data_text(d):
    if not d.get("access"):
        return d.get("why", "")
    t = ACCESS[d["access"]] + (" через " + ", ".join(d["via"]) if d.get("via") else "")
    why = d.get("why", "")
    if not why:
        return t
    return t + (" " if why[:1] == "(" or why.split(" ")[0] in ("по", "через", "при", "для") else ": ") + why


def _data_from(v):
    table, text = v
    for k, word in sorted(ACCESS.items(), key=lambda x: -len(x[1])):
        if text == word or text.startswith(word + " ") or text.startswith(word + ":"):
            rest = text[len(word):]
            m = re.match(r" через (I\d+(?:, I\d+)*)", rest)
            via = m.group(1).split(", ") if m else []
            rest = rest[m.end():] if m else rest
            why = rest[2:] if rest.startswith(": ") else rest[1:] if rest.startswith(" ") else rest
            yield {"table": table, "access": k, "via": via, "why": why}
            yield {"table": table, "access": k, "why": text[len(word):].lstrip(": ").lstrip()}
    yield {"table": table, "why": text}


DATA_ROW = Row(("table", Ref("table", also=r"S\d+"), "req", "таблица модели данных (каталог) или хранилище S<N>"),
               ("access", Str(choices=tuple(ACCESS)), "opt", "доступ: " + ", ".join(f"{k} — «{w}»" for k, w in ACCESS.items())),
               ("via", VIA, "opt", "через какой интерфейс (I-код)"), ("why", S, "opt", "что и зачем (текст)"),
               to_py=lambda d: (d["table"], _data_text(d)), from_py=_data_from)

_PARAM_COMP = []  # компонент файла при записи (для решения «значение или пояснение»)


def _param_from(v):
    name, val = v
    comp = _PARAM_COMP[-1] if _PARAM_COMP else None
    t = _cat().params(comp).get(name, {}).get("type") if comp else None
    if t and val and not _cat().value_ok(t, val) and val != _cat().params(comp)[name]["default"]:
        yield {"name": name, "note": val}
    yield {"name": name, "value": val}


PARAM_ROW = Row(("name", Ref("param"), "req", "имя параметра из таблицы «Параметры модуля» interfaces.md спек компонента"),
                ("value", S, "opt", "значение по типу из interfaces.md (число, длительность, перечисление); на странице — значение спеки"),
                ("note", S, "opt", "пояснение вместо значения (когда значение задаёт спека)"),
                to_py=lambda d: (d["name"], d["value"] if "value" in d else d.get("note", "")), from_py=_param_from)


def _screen_what(d):
    return d["what"] + (" — " + ", ".join(f"`{e}`" for e in d["endpoints"]) if d.get("endpoints") else "")


def _screen_from(v):
    name, where, what, status, code, stories = v
    base = {"name": name, "where": where, "status": status, "code": code, "stories": stories.split(", ") if stories else []}
    m = re.fullmatch(rf"(.*) — (`{_EP}`(?:, `{_EP}`)*)", what, flags=re.S)
    if m:
        eps = re.findall(r"`([^`]+)`", m.group(2))
        if _known_endpoints(eps):
            yield {**base, "what": m.group(1), "endpoints": eps}
    yield {**base, "what": what}


SCREEN_ROW = Row(("name", S, "req", "экран"), ("where", S, "req", "где в интерфейсе"), ("what", S, "req", "что на экране"),
                 ("endpoints", Lst(Ref("endpoint"), flow=True), "opt", "эндпоинты экрана «МЕТОД путь» (data/endpoints)"),
                 ("status", Str(choices=("есть", "доработка", "новое")), "req", "есть | доработка | новое"),
                 ("code", S, "req", "где код (путь в форке)"),
                 ("stories", Lst(Ref("story"), flow=True), "req", "истории US-…"),
                 to_py=lambda d: (d["name"], d["where"], _screen_what(d), d["status"], d["code"], ", ".join(d["stories"])),
                 from_py=_screen_from)


def _op_text(d):
    return join_ids((f"`{d['endpoint']}` — " if d.get("endpoint") else "") + d["op"], None, _ids_of({"reqs": d.get("reqs"), "decisions": d.get("decisions")}))


def _op_via(d):
    return ", ".join(d["via"]) if d.get("via") else "внутри" if d.get("internal") else d.get("via_note", "")


def _op_from(v):
    op, who, via = v
    vv = {"via": via.split(", ")} if re.fullmatch(r"I\d+(?:, I\d+)*", via) else {"internal": True} if via == "внутри" else {"via_note": via}
    for body, ids in _sfx(op):
        ids = {k: x for k, x in ids.items() if k in ("reqs", "decisions")} if not ids.get("via") else None
        if ids is None:
            continue
        m = re.fullmatch(rf"`({_EP})` — (.*)", body, flags=re.S)
        if m and _known_endpoints([m.group(1)]):
            yield {"op": m.group(2), "endpoint": m.group(1), **_who(who, "who"), **vv, **ids}
        yield {"op": body, **_who(who, "who"), **vv, **ids}
    yield {"op": op, "label": who, **vv}


OP_ROW = Row(("op", S, "req", "операция (текст)"), ("endpoint", Ref("endpoint"), "opt", "эндпоинт «МЕТОД путь» (data/endpoints)"),
             ("who", Ref("participant"), "opt", "кто вызывает: компонент, блок, роль (каталог)"),
             ("label", S, "opt", "кто вызывает — текстом, если нет в каталоге"),
             ("via", VIA, "opt", "I-код интерфейса"), ("internal", Bool(), "opt", "вызов внутри компонента (на странице — «внутри»)"),
             ("via_note", S, "opt", "канал текстом, если не I-код и не «внутри»"),
             ("reqs", REQS, "opt", "R-коды"), ("decisions", DECS, "opt", "решения D<N>"),
             to_py=lambda d: (_op_text(d), d.get("label") or d["who"], _op_via(d)), from_py=_op_from, one_of=("who", "label"))


def _fail_text(d):
    return join_ids(d["when"] + (f" — {d['then']}" if d.get("then") else ""), d.get("fmea"), _ids_of(d))


def _fail_from(v):
    for body, ids in _sfx(v, fmea_ok=True):
        when, sep, then = body.partition(" — ")
        yield {"when": when, "then": then, **ids}


FAIL_ROW = Row(("when", S, "req", "что сломалось"), ("then", S, "opt", "что происходит (поведение при сбое)"),
               ("fmea", Ref("spec"), "opt", "спека, в FMEA которой отказ (interfaces.md)"), *SFX,
               to_py=_fail_text, from_py=_fail_from)


def _sfx_row(names, text_field, to_tuple):
    """Строка, у которой последнее текстовое поле может кончаться хвостом ID."""
    def from_py(v):
        base = dict(zip(names, v))
        for body, ids in _sfx(base[text_field]):
            if "fmea" in ids:
                continue
            yield {**base, text_field: body, **ids}
    return from_py


def _field_py(d):
    return (d["name"], d["type"], d["required"], join_ids(d["desc"], None, _ids_of(d)))


FIELD_ROW = Row(("name", S, "req", "поле модели"), ("type", S, "req", "тип: int, string, enum: …, Модель, Модель[]"),
                ("required", Bool(), "req", "обязательное"), ("desc", S, "req", "описание"), *SFX,
                to_py=_field_py, from_py=_sfx_row(("name", "type", "required", "desc"), "desc", None))


def _key_text(d):
    return d["key"] if "key" in d else ", ".join((["PK"] if d.get("pk") else []) + ([f"FK {d['fk']}"] if d.get("fk") else []))


def _col_from(v):
    name, typ, key, desc = v
    m = re.fullmatch(r"(PK)?(?:, )?(?:FK (\w+))?", key)
    keys = [{"pk": bool(m.group(1)), "fk": m.group(2) or ""}] if m and (not m.group(2) or m.group(2) in _cat().tables()) else []
    keys.append({"key": key})
    for k in keys:
        for body, ids in _sfx(desc):
            if "fmea" not in ids:
                yield {"name": name, "type": typ, **k, "desc": body, **ids}


COLUMN_ROW = Row(("name", S, "req", "колонка"), ("type", S, "req", "тип SQL"), ("pk", Bool(), "opt", "входит в первичный ключ"),
                 ("fk", Ref("table"), "opt", "внешний ключ на таблицу (каталог)"), ("key", S, "opt", "ключ текстом, если не PK / FK <таблица>"),
                 ("desc", S, "opt", "описание"), *SFX,
                 to_py=lambda d: (d["name"], d["type"], _key_text(d), join_ids(d.get("desc", ""), None, _ids_of(d))), from_py=_col_from)

INDEX_ROW = Row(("kind", Str(choices=("unique", "index", "hnsw")), "req", "unique | index | hnsw"),
                ("columns", Lst(S, flow=True), "req", "колонки индекса (этой таблицы)"), ("why", S, "req", "зачем"),
                to_py=lambda d: (d["kind"], ", ".join(d["columns"]), d["why"]),
                from_py=lambda v: [{"kind": v[0], "columns": v[1].split(", "), "why": v[2]}])


def _src_py(d):
    return tuple([d["kind"], ", ".join(d["refs"]) if d.get("refs") else d.get("ref", "")] + ([d["part"]] if "part" in d else []) + [d["why"]])


def _src_from(v):
    kind, ref, *rest = v
    part = {"part": rest[0]} if len(rest) == 2 else {}
    why = rest[-1]
    if re.fullmatch(rf"(?:{_ID}|US-[A-Z]+-\d+)(?:, (?:{_ID}|US-[A-Z]+-\d+))*", ref):
        yield {"kind": kind, "refs": ref.split(", "), **part, "why": why}
    yield {"kind": kind, "ref": ref, **part, "why": why}


SOURCE_ROW = Row(("kind", Str(choices=("fork", "ours", "ext")), "req", "fork — форк ICPlan, ours — наша, ext — внешний стандарт"),
                 ("refs", Lst(Ref("ref"), flow=True), "opt", "основание — ID: R-…, D<N>, I…, US-…"),
                 ("ref", S, "opt", "основание текстом: URL, эндпоинт, схема форка"),
                 ("part", S, "opt", "часть источника"), ("why", S, "req", "почему так"),
                 to_py=_src_py, from_py=_src_from, flow=False, one_of=("refs", "ref"))

GRANT_ROW = Row(("role", S, "req", "роль БД"), ("right", Str(choices=("SELECT", "REFERENCES", "INSERT", "UPDATE", "DELETE")), "req", "право"),
                ("table", Str(pattern=r"\w+\.\w+\.\w+", hint="база.схема.таблица"), "req", "база.схема.таблица"), ("why", S, "req", "зачем"),
                to_py=lambda d: (d["role"], d["right"], d["table"], d["why"]),
                from_py=lambda v: [dict(zip(("role", "right", "table", "why"), v))])

DOMAIN_ROW = Row(("domain", S, "req", "домен S1"), ("tables", Lst(Ref("table"), flow=True), "req", "таблицы домена"),
                 to_py=lambda d: (d["domain"], d["tables"]), from_py=lambda v: [{"domain": v[0], "tables": v[1]}])


def _sreq_from(v):
    spec, sep, title = v.partition(": ")
    if sep and spec in _cat().specs():
        yield {"spec": spec, "title": title}
    yield {"text": v}


STORY_REQ = Row(("spec", Ref("spec"), "opt", "спека openspec/changes/*/specs/<спека>"),
                ("title", S, "opt", "требование — заголовок «### Requirement: …» спеки"),
                ("text", S, "opt", "требование текстом, если не «спека: заголовок»"),
                to_py=lambda d: d["text"] if "text" in d else f"{d['spec']}: {d['title']}", from_py=_sreq_from, one_of=("spec", "text"))

STEP_ROW = Row(("id", S, "req", "id шага (латиница)"), ("lane", Int(), "req", "дорожка: номер в lanes с 0"),
               ("type", Str(choices=("start", "task", "gateway", "end", "error")), "req", "start | task | gateway | end | error"),
               ("label", S, "req", "подпись шага"), ("next", Lst(NextStep(), flow=True), ("def", list), "переходы: id шага или {to, label}"),
               to_py=lambda d: (d["id"], d["lane"], d["type"], d["label"], d["next"]),
               from_py=lambda v: [{"id": v[0], "lane": v[1], "type": v[2], "label": v[3], "next": v[4]}])

SPEC_LINK = Row(("label", S, "req", "подпись"), ("path", Str(ref="path"), "req", "путь от корня репозитория"),
                to_py=lambda d: (d["label"], d["path"]), from_py=lambda v: [{"label": v[0], "path": v[1]}])
CHAIN_ROW = Row(("label", S, "req", "подпись звена"), ("comp", Ref("component"), "opt", "компонент (slug); нет — внешний участник"),
                to_py=lambda d: (d["label"], d.get("comp")), from_py=lambda v: [{"label": v[0], "comp": v[1]}])
ICPLAN_ROW = Row(("key", Ref("icplan_key"), "req", "ключ html-view/icplan_schema.json"), ("note", S, "req", "пометка (уровень памяти и т. п.)"),
                 to_py=lambda d: (d["key"], d["note"]), from_py=lambda v: [{"key": v[0], "note": v[1]}])

# ---------------------------------------------------------------- схемы единиц
S = Str()
SID = Ref("story")
TASK = Ref("task", desc="номер задачи «2.3» в кавычках")
REQ = Ref("req")
COMP = Ref("component")
NONE_TEXT = Str(pattern=r"нет: .+", hint="«нет: <почему>»")

BLOCK_CELL = Rec(("title", S), ("desc", S, ("def", "")), ("kind", Str(choices=("core", "ext", "store", "user", "back", ""))), ("st", S, ("def", "")),
                 ("g", S, ("def", "")), ("to", Ref("component"), ("def", "")), flow=True, tag="title")
ROW = Lazy(lambda: _ROW, "row")
ZONE = Rec(("zone", S), ("rows", Lst(ROW)), ("cls", S, ("def", "")), ("g", S, ("def", "")), ("note", S, ("def", "")), tag="zone")
_ROW = OneOf(S, Lst(BLOCK_CELL), ZONE, hint="строка-подпись потока, список блоков [{title, desc, kind, st, g, to}] или зона {zone, rows}")

SCHEMAS = {
    "component": Rec(
        ("name", S, "req", "название компонента"), ("status", Str(choices=("done", "part", "todo")), "req", "done | part | todo"),
        ("guardrails", Str(pattern=r"(G\d+([–-]G\d+)?(, )?)*", hint="G1, G1–G4 или пусто"), "req", "G1, G1–G4 или пусто"),
        ("desc", S, "req", "одна фраза о компоненте"), ("links", Lst(Any_()), ("def", list)),
        ("specs", Lst(SPEC_LINK), "req", "спеки и схемы: {label, path}"), ("tasks", Lst(TASK, flow=True), "req", "задачи компонента"),
        ("about", TRec(("chain", Lst(CHAIN_ROW)), ("purpose", S), ("does", Lst(S))), "opt", "справка: цепочка, назначение, что делает"),
        ("stores", Lst(Ref("store"), flow=True), "opt", "хранилища S<N>"),
        ("icplan_tables", Lst(ICPLAN_ROW), "opt", "таблицы форка ICPlan, которые использует компонент"),
        ("blocks", Lst(ROW), "opt", "блочная схема")),
    "block": Rec(
        ("title", S, "req", "название блока = имя файла (slug)"), ("tech", S, "req", "технология"),
        ("kind", Str(choices=("ui", "service", "store")), "opt", "ui → screens, service → ops, store → schema"),
        ("stories", Lst(SID, flow=True), "opt", "истории US-…"),
        ("screens", Lst(SCREEN_ROW), "opt", "экраны (kind: ui)"),
        ("params", OneOf(NONE_TEXT, Lst(PARAM_ROW), hint="строка «нет: …» или список {name, value}"), "opt",
         "параметры: {name, value} из interfaces.md или «нет: <почему>»"),
        ("does", Lst(S), "opt", "что делает"),
        ("io", Lst(IO_ROW), "opt", "входы и выходы: {dir, with, what, model, via}"),
        ("data", OneOf(NONE_TEXT, Lst(DATA_ROW), hint="строка «нет: …» или список {table, access, why}"), "opt",
         "таблицы: {table, access, why} или «нет: <почему>»"),
        ("reqs", Lst(REQ, flow=True), "opt", "R-коды"), ("tasks", Lst(TASK, flow=True), "opt", "задачи"),
        ("failures", Lst(FAIL_ROW), "opt", "при сбое: {when, then, reqs}"), ("why", S, "opt", "почему так"),
        ("rnd", Ref("rnd"), "opt", "R&D: файл в docs/rnd"),
        ("ops", Lst(OP_ROW), "opt", "операции (kind: service): {op, endpoint, who, via}"), ("schema", S, "opt", "схема хранения (kind: store)"),
        ("iface", Lst(Ref("icode"), flow=True), "opt", "I-коды, которые блок реализует")),
    "hosts": Lst(Rec(("owner", COMP), ("block", S, "opt"), ("host", COMP), flow=True)),
    "model": Rec(
        ("purpose", S, "req", "назначение модели"),
        ("fields", Lst(FIELD_ROW), "req", "поля: {name, type, required, desc}"),
        ("source", SOURCE_ROW, "req", "источник: {kind, refs | ref, part, why}"),
        ("field_src", Map(S, S), "opt"), ("planned", Map(S, S), "opt")),
    "table": Rec(
        ("kind", Str(choices=("platform", "fork", "litellm")), "req", "platform | fork | litellm"),
        ("store", Ref("store"), "opt", "хранилище S<N>"), ("owner", COMP, "opt", "компонент-владелец"),
        ("schema", Str(pattern=r"\w+\.\w+", hint="база.схема"), "opt", "база.схема"), ("written", Bool(), "opt", "форк: пишем в таблицу"),
        ("columns", Lst(COLUMN_ROW), "opt", "колонки: {name, type, pk, fk, desc}"),
        ("policy", TRec(("indexes", Opt(Lst(INDEX_ROW))), ("retention", S), ("cleanup", S), ("migrate", S)), "opt",
         "индексы {kind, columns, why}, хранение, очистка, миграции")),
    "endpoints": Map(Str(pattern=r"(GET|POST|PUT|PATCH|DELETE) \S.*", hint="«МЕТОД путь»"),
                     TRec(("request", S, "req", "тело или параметры запроса"), ("response", S, "req", "код · тело ответа"),
                          ("note", S, "req", "ошибки и примечания"))),
    "integrations": Map(Str(pattern=r"I\d+", hint="I<N>"), Rec(
        ("from", Str(ref="component*")), ("to", Str(ref="component*")), ("via", Str(ref="component*")), ("what", S),
        ("models", Lst(Ref("model"), flow=True)), ("types", S, "opt"), ("also", Lst(COMP, flow=True), "opt"),
        ("data_in_response", Bool(), "opt"))),
    "databases": Rec(
        ("cluster", Map(S, S)),
        ("databases", Map(S, Rec(("owner", COMP), ("schemas", Map(S, Rec(("owner", COMP), ("role", S), ("stores", S), ("migrate", S), ("what", S))))))),
        ("grants", Lst(GRANT_ROW), "req", "GRANT: {role, right, table, why}"),
        ("migrate", Map(S, S))),
    "datamodel": Rec(
        ("naming", S), ("litellm_ref", S),
        ("s1_domains", Lst(DOMAIN_ROW), "req", "домены S1: {domain, tables}"),
        ("trees", Map(Str(pattern=r"S\d+"), TRec(("title", S), ("lines", Lst(S)))))),
    "story": Rec(
        ("role", Ref("role"), "req", "роль: ключ roles / personas"), ("want", S, "req", "хочу"), ("so_that", S, "req", "чтобы"),
        ("accept", Lst(S), "req", "критерии приёмки"), ("reqs", Lst(STORY_REQ), "req", "требования: {spec, title}"),
        ("entry", S, "opt", "точка входа"),
        ("chain", TRec(("path", Lst(SID, flow=True)), ("end", S)), "opt", "цепочка историй")),
    "processes": Rec(
        ("processes", Lst(Rec(
            ("title", S), ("stories", Lst(SID, flow=True)), ("lanes", Lst(S, flow=True)),
            ("steps", Lst(STEP_ROW), "req", "шаги: {id, lane, type, label, next}"),
            ("artifacts", Map(S, Lst(S, flow=True)), ("def", dict))))),
        ("artifacts", Map(S, Lst(S, flow=True)), "opt")),
    "costs": Rec(("costs", Lst(Rec(
        ("date", Str(pattern=r"\d{4}-\d{2}-\d{2}", hint="ГГГГ-ММ-ДД")), ("process", Str(pattern=r"[a-z0-9-]+", hint="код процесса латиницей")),
        ("methodology", S), ("units", Int()), ("unit", S), ("tokens", Int()), ("model", S, "opt"), ("minutes", Int(), "opt"),
        ("expected", Lst(Int(), flow=True), "opt"), ("note", S, "opt"))))),
    "personas": Rec(
        ("roles", Map(S, S)),
        ("personas", Map(S, TRec(("name", S), ("can", S), ("wants", S), ("conflict", S), ("prompt", S))))),
}

# вид единицы по пути в data/
KIND_OF = [("components/*.yaml", "component"), ("blocks/*/*.yaml", "block"), ("hosts.yaml", "hosts"), ("models/*.yaml", "model"),
           ("tables/*.yaml", "table"), ("endpoints/*.yaml", "endpoints"), ("integrations.yaml", "integrations"),
           ("databases.yaml", "databases"), ("datamodel.yaml", "datamodel"), ("stories/*/*.yaml", "story"),
           ("processes/*.yaml", "processes"), ("personas.yaml", "personas"),
           ("costs.yaml", "costs")]


def kind_of(path) -> str:
    import fnmatch
    r = Path(path).resolve().relative_to(DATA.resolve()).as_posix()
    if Path(r).name.startswith("_"):
        return "order"
    return next((k for pat, k in KIND_OF if fnmatch.fnmatch(r, pat) and r.count("/") == pat.count("/")), "")


# ---------------------------------------------------------------- чтение и запись
class _Dumper(yaml.SafeDumper):
    pass


_Dumper.add_representer(FlowList, lambda d, v: d.represent_sequence("tag:yaml.org,2002:seq", v, flow_style=True))
_Dumper.add_representer(FlowDict, lambda d, v: d.represent_mapping("tag:yaml.org,2002:map", list(v.items()), flow_style=True))
_Dumper.add_representer(tuple, lambda d, v: d.represent_sequence("tag:yaml.org,2002:seq", v, flow_style=True))


def to_yaml(v) -> str:
    return yaml.dump(v, Dumper=_Dumper, sort_keys=False, allow_unicode=True, width=100000, default_flow_style=False)


def _read(path: Path):
    return yaml.load(path.read_text(encoding="utf-8"), Loader=_Loader)


def _header(path: Path) -> str:
    """Комментарии в начале файла сохраняются при форматировании."""
    lines = []
    for l in path.read_text(encoding="utf-8").splitlines():
        if not l.startswith("#"):
            break
        lines.append(l)
    return "".join(l + "\n" for l in lines)


class DataError(ValueError):
    pass


_CACHE = {}


def load_unit(path: Path, kind: str = "", refs=False):
    """(значение в Python, ошибки) одной единицы."""
    kind = kind or kind_of(path)
    c = Ctx(refs, comp_of(path, kind))
    try:
        raw = _read(path)
    except yaml.YAMLError as e:
        return None, [f"не YAML: {str(e).splitlines()[0]} (строка {getattr(getattr(e, 'problem_mark', None), 'line', -1) + 1})"]
    if kind == "order":
        if not isinstance(raw, list) or not all(isinstance(x, str) for x in raw):
            return raw, ["нужен список имён файлов без .yaml"]
        return raw, []
    v = SCHEMAS[kind].load(raw, "", c)
    if c.errors and LEGACY and kind in LEGACY:  # yaml-migrate: файл ещё в прежнем (позиционном) виде
        c2 = Ctx(refs, c.comp)
        v2 = LEGACY[kind].load(raw, "", c2)
        if not c2.errors:
            return v2, []
    return v, c.errors


LEGACY = {}  # прежние схемы видов — только на время yaml-migrate (yamlmigrate.POSITIONAL)


def comp_of(path, kind) -> str:
    """Компонент файла: папка блока / истории или имя файла компонента (для имён параметров и типов)."""
    p = Path(path)
    return p.parent.name if kind in ("block", "story") else p.stem if kind == "component" else ""


def _unit(path: Path, kind: str):
    key = (str(path), kind)
    if key not in _CACHE:
        v, errs = load_unit(path, kind)
        if errs:
            raise DataError(f"{path.relative_to(ROOT).as_posix()}: " + "; ".join(errs[:5]) + " (python html-view/doctool.py yaml-check)")
        _CACHE[key] = v
    return _CACHE[key]


def ordered(folder: Path) -> list:
    """Файлы единиц папки в порядке _order.yaml; не внесённые в него — в конце по алфавиту."""
    files = {f.stem: f for f in folder.glob("*.yaml") if not f.stem.startswith("_")}
    order = _read(folder / "_order.yaml") if (folder / "_order.yaml").exists() else []
    return [files[n] for n in order if n in files] + [files[n] for n in sorted(files) if n not in order]


def comp_order() -> list:
    return [f.stem for f in ordered(DATA / "components")]


def write_unit(path: Path, kind: str, value) -> bool:
    """Записать единицу (в формате схемы). True — файл изменился."""
    text = to_yaml(dump_unit(path, kind, value) if kind != "order" else value)
    if path.exists():
        text = _header(path) + text
        if path.read_text(encoding="utf-8") == text:
            return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    return True


def dump_unit(path, kind, value):
    """Значение в Python → YAML-вид единицы (именованные поля, ID извлечены из текста, где это без потерь)."""
    _PARAM_COMP.append(comp_of(path, kind))
    try:
        return SCHEMAS[kind].dump(value)
    finally:
        _PARAM_COMP.pop()


# ---------------------------------------------------------------- сборка значений модулей
def components():
    """COMPONENTS, ABOUT, BLOCKS, HOST (components.py)."""
    if "components" in _CACHE:
        return _CACHE["components"]
    out = {"COMPONENTS": [], "ABOUT": {}, "BLOCKS": {}, "HOST": {}}
    for f in ordered(DATA / "components"):
        u = _unit(f, "component")
        out["COMPONENTS"].append((f.stem, u["name"], u["status"], u["guardrails"], u["desc"], u["links"], u["specs"], u["tasks"]))
        if "blocks" in u:
            out["BLOCKS"][f.stem] = u["blocks"]
        if "about" in u:
            out["ABOUT"][f.stem] = u["about"]
    for h in _unit(DATA / "hosts.yaml", "hosts"):
        out["HOST"][(h["owner"], h["block"]) if "block" in h else h["owner"]] = h["host"]
    _CACHE["components"] = out
    return out


def sub():
    """SUB (subcomponents.py): (компонент, title) → карточка блока."""
    if "sub" in _CACHE:
        return _CACHE["sub"]
    out = {}
    for comp in comp_order():
        d = DATA / "blocks" / comp
        for f in ordered(d) if d.exists() else []:
            u = dict(_unit(f, "block"))
            out[(comp, u.pop("title"))] = u
    _CACHE["sub"] = out
    return out


def stories():
    """ROLES, STORIES, BPMN, PERSONAS, ARTIFACTS, CHAINS (stories.py)."""
    if "stories" in _CACHE:
        return _CACHE["stories"]
    p = _unit(DATA / "personas.yaml", "personas")
    out = {"ROLES": p["roles"], "STORIES": {}, "BPMN": {}, "PERSONAS": p["personas"], "ARTIFACTS": {}, "CHAINS": {}}
    for comp in comp_order():
        d = DATA / "stories" / comp
        if d.exists():
            out["STORIES"][comp] = []
            for f in ordered(d):
                u = _unit(f, "story")
                out["STORIES"][comp].append((f.stem, u["role"], u["want"], u["so_that"], u["accept"], u["reqs"]) + ((u["entry"],) if "entry" in u else ()))
                if "chain" in u:
                    out["CHAINS"][f.stem] = u["chain"]
        f = DATA / "processes" / f"{comp}.yaml"
        if f.exists():
            u = _unit(f, "processes")
            out["BPMN"][comp] = u["processes"]
            out["ARTIFACTS"][comp] = u["artifacts"] if "artifacts" in u else u["processes"][0]["artifacts"]
    _CACHE["stories"] = out
    return out


def datamodel():
    """Значения datamodel.py, собранные из единиц."""
    if "datamodel" in _CACHE:
        return _CACHE["datamodel"]
    integ = _unit(DATA / "integrations.yaml", "integrations")
    out = {
        "INTEG": {i: (r["from"], r["to"], r["via"], r["what"], r["models"]) for i, r in integ.items()},
        "INTEG_TYPES": {i: r["types"] for i, r in integ.items() if "types" in r},
        "DATA_IN_RESPONSE": {i for i, r in integ.items() if r.get("data_in_response")},
        "ALSO": {i: r["also"] for i, r in integ.items() if "also" in r},
        "MODELS": {}, "MODEL_META": {}, "FIELD_SRC": {}, "PLANNED": {},
        "ICPLAN_TABLES": {}, "PLATFORM_TABLES": {}, "LITELLM_TABLES": {}, "SCHEMA_OF": {}, "FORK_WRITTEN": [], "TABLE_POLICY": {},
        "FORK_COLUMNS": {}, "STORES": {}, "ENDPOINT_IO": {},
    }
    for f in ordered(DATA / "models"):
        u = _unit(f, "model")
        out["MODELS"][f.stem] = (u["purpose"], u["fields"])
        out["MODEL_META"][f.stem] = u["source"]
        if "field_src" in u:
            out["FIELD_SRC"][f.stem] = u["field_src"]
        if "planned" in u:
            out["PLANNED"][f.stem] = u["planned"]
    for f in ordered(DATA / "tables"):
        u, t = _unit(f, "table"), f.stem
        if u["kind"] == "platform":
            out["PLATFORM_TABLES"][t] = (u["store"], u["owner"], u["columns"])
        elif u["kind"] == "litellm":
            out["LITELLM_TABLES"][t] = u["columns"]
        elif "columns" in u:
            out["FORK_COLUMNS"][t] = u["columns"]
        if "schema" in u:
            out["SCHEMA_OF"][t] = u["schema"]
        if u.get("written"):
            out["FORK_WRITTEN"].append(t)
        if "policy" in u:
            out["TABLE_POLICY"][t] = u["policy"]
    for comp in comp_order():
        u = _unit(DATA / "components" / f"{comp}.yaml", "component")
        if "stores" in u:
            out["STORES"][comp] = u["stores"]
        if "icplan_tables" in u:
            out["ICPLAN_TABLES"][comp] = u["icplan_tables"]
        f = DATA / "endpoints" / f"{comp}.yaml"
        if f.exists():
            out["ENDPOINT_IO"].update(_unit(f, "endpoints"))
    db = _unit(DATA / "databases.yaml", "databases")
    out.update(DB_CLUSTER=db["cluster"], DATABASES=db["databases"], DB_GRANTS=db["grants"], MIGRATE=db["migrate"])
    dm = _unit(DATA / "datamodel.yaml", "datamodel")
    out.update(NAMING=dm["naming"], LITELLM_REF=dm["litellm_ref"], S1_DOMAINS=dm["s1_domains"], TREES=dm["trees"])
    _CACHE["datamodel"] = out
    return out


# ---------------------------------------------------------------- выгрузка Python → YAML (yaml-export)
TR = dict(zip("абвгдеёжзийклмнопрстуфхцчшщъыьэюя",
              ["a", "b", "v", "g", "d", "e", "e", "zh", "z", "i", "y", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u", "f",
               "h", "c", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya"]))


def slug(title: str) -> str:
    """Имя файла блока = адрес страницы блока (build.sub_slug)."""
    s = "".join(TR.get(ch, ch) for ch in title.lower())
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def _endpoint_pages(keys) -> dict:
    """Страница API эндпоинта: уже выгруженный файл data/endpoints, иначе раздел-комментарий в datamodel.py."""
    page = {}
    for f in (DATA / "endpoints").glob("*.yaml"):
        for k in _read(f) or {}:
            page.setdefault(k, f.stem)
    src = (HERE / "datamodel.py").read_text(encoding="utf-8")
    m = re.search(r"^ENDPOINT_IO = \{\n(.*?)^\}", src, flags=re.M | re.S)
    if m:
        groups = [("MCP ICPlan", "icplan"), ("Harness", "harness"), ("Agent Runner", "agent-runner"), ("Guardrails", "guardrails"),
                  ("ICPlan", "icplan"), ("LiteLLM", "llm-gateway"), ("MCP", "mcp-tools"), ("Memory", "memory"),
                  ("Platform module", "platform-module"), ("Sandbox", "sandbox")]
        cur = ""
        for l in m.group(1).splitlines():
            c = re.match(r"\s*# (.+)", l)
            if c:
                cur = next((g for t, g in groups if c.group(1).startswith(t)), cur)
                continue
            k = re.match(r'\s*"([^"]+)": \(', l)
            if k:
                page.setdefault(k.group(1), "infrastructure" if k.group(1).startswith("GET https://") else cur)
    return {k: page.get(k, "infrastructure") for k in keys}


def export(mods) -> list:
    """Выгрузить значения модулей (datamodel, subcomponents, stories, components) в data/. Возвращает изменённые файлы."""
    DM, SC, ST, CM = mods["datamodel"], mods["subcomponents"], mods["stories"], mods["components"]
    files = []

    def put(path, kind, value):
        if write_unit(path, kind, value):
            files.append(path.relative_to(ROOT).as_posix())

    comps = [c[0] for c in CM.COMPONENTS]
    put(DATA / "components/_order.yaml", "order", comps)
    for c in CM.COMPONENTS:
        u = {"name": c[1], "status": c[2], "guardrails": c[3], "desc": c[4], "links": c[5], "specs": c[6], "tasks": c[7]}
        if c[0] in CM.ABOUT:
            u["about"] = CM.ABOUT[c[0]]
        if c[0] in DM.STORES:
            u["stores"] = DM.STORES[c[0]]
        if c[0] in DM.ICPLAN_TABLES:
            u["icplan_tables"] = DM.ICPLAN_TABLES[c[0]]
        if c[0] in CM.BLOCKS:
            u["blocks"] = CM.BLOCKS[c[0]]
        put(DATA / f"components/{c[0]}.yaml", "component", u)
    put(DATA / "hosts.yaml", "hosts", [dict(owner=k[0], block=k[1], host=h) if isinstance(k, tuple) else dict(owner=k, host=h) for k, h in CM.HOST.items()])
    by_comp = {}
    for (comp, title), s in SC.SUB.items():
        by_comp.setdefault(comp, []).append(slug(title))
        put(DATA / f"blocks/{comp}/{slug(title)}.yaml", "block", {"title": title, **s})
    for comp, names in by_comp.items():
        put(DATA / f"blocks/{comp}/_order.yaml", "order", names)
    put(DATA / "models/_order.yaml", "order", list(DM.MODELS))
    for m, (purpose, fields) in DM.MODELS.items():
        u = {"purpose": purpose, "fields": fields, "source": DM.MODEL_META[m]}
        if m in DM.FIELD_SRC:
            u["field_src"] = DM.FIELD_SRC[m]
        if m in DM.PLANNED:
            u["planned"] = DM.PLANNED[m]
        put(DATA / f"models/{m}.yaml", "model", u)
    tables = {}
    for t in DM.FORK_COLUMNS:
        tables.setdefault(t, {"kind": "fork"})["columns"] = DM.FORK_COLUMNS[t]
    for t in DM.FORK_WRITTEN:
        tables.setdefault(t, {"kind": "fork"})
    for t in DM.FORK_WRITTEN:
        tables[t]["written"] = True
    for t, (store, owner, cols) in DM.PLATFORM_TABLES.items():
        tables[t] = {"kind": "platform", "store": store, "owner": owner, "columns": cols}
    for t, cols in DM.LITELLM_TABLES.items():
        tables[t] = {"kind": "litellm", "columns": cols}
    for t, s in DM.SCHEMA_OF.items():
        tables.setdefault(t, {"kind": "platform"})["schema"] = s
    for t, p in DM.TABLE_POLICY.items():
        tables.setdefault(t, {"kind": "fork"})["policy"] = p
    put(DATA / "tables/_order.yaml", "order", list(tables))
    for t, u in tables.items():
        put(DATA / f"tables/{t}.yaml", "table", {k: u[k] for k in SCHEMAS["table"].names if k in u})
    pages = _endpoint_pages(DM.ENDPOINT_IO)
    for comp in comps:
        eps = {k: v for k, v in DM.ENDPOINT_IO.items() if pages[k] == comp}
        if eps:
            put(DATA / f"endpoints/{comp}.yaml", "endpoints", eps)
    integ = {}
    for i, (a, b, via, what, models) in DM.INTEG.items():
        r = {"from": a, "to": b, "via": via, "what": what, "models": models}
        if i in DM.INTEG_TYPES:
            r["types"] = DM.INTEG_TYPES[i]
        if i in DM.ALSO:
            r["also"] = DM.ALSO[i]
        if i in DM.DATA_IN_RESPONSE:
            r["data_in_response"] = True
        integ[i] = r
    put(DATA / "integrations.yaml", "integrations", integ)
    put(DATA / "databases.yaml", "databases", {"cluster": DM.DB_CLUSTER, "databases": DM.DATABASES, "grants": DM.DB_GRANTS, "migrate": DM.MIGRATE})
    put(DATA / "datamodel.yaml", "datamodel", {"naming": DM.NAMING, "litellm_ref": DM.LITELLM_REF, "s1_domains": DM.S1_DOMAINS, "trees": DM.TREES})
    put(DATA / "personas.yaml", "personas", {"roles": ST.ROLES, "personas": ST.PERSONAS})
    for comp in comps:
        if comp in ST.STORIES:
            put(DATA / f"stories/{comp}/_order.yaml", "order", [s[0] for s in ST.STORIES[comp]])
            for s in ST.STORIES[comp]:
                u = dict(zip(("role", "want", "so_that", "accept", "reqs", "entry"), s[1:]))
                if s[0] in ST.CHAINS:
                    u["chain"] = ST.CHAINS[s[0]]
                put(DATA / f"stories/{comp}/{s[0]}.yaml", "story", u)
        if comp in ST.BPMN:
            u = {"processes": ST.BPMN[comp]}
            if comp in ST.ARTIFACTS and ST.ARTIFACTS[comp] != ST.BPMN[comp][0].get("artifacts"):
                u["artifacts"] = ST.ARTIFACTS[comp]
            put(DATA / f"processes/{comp}.yaml", "processes", u)
    return files


# ---------------------------------------------------------------- проверка (yaml-check) и формат (yaml-fmt)
def unit_files(path=None) -> list:
    base = Path(path) if path else DATA
    if not base.is_absolute():
        base = (ROOT / base) if (ROOT / base).exists() else base.resolve()
    if base.is_file():
        return [base]
    return sorted(f for f in base.rglob("*.yaml"))


def check(path=None) -> list:
    """Замечания «файл: поле → что исправить» по схеме, ссылкам (каталоги yamlcat) и порядку (_order.yaml)."""
    _REFCACHE.clear()
    _cat().clear()
    issues = []
    files = unit_files(path)
    for f in files:
        rel = f.resolve().relative_to(ROOT.resolve()).as_posix()
        kind = kind_of(f)
        if not kind:
            issues.append(f"{rel}: неизвестный вид единицы — место файла по раскладке в html-view/yamldata.py")
            continue
        v, errs = load_unit(f, kind, refs=True)
        issues += [f"{rel}: {e}" for e in errs]
        if errs or v is None:
            continue
        issues += [f"{rel}: {e}" for e in _extra(f, kind, v)]
    # порядок: каждая единица папки внесена в _order.yaml
    dirs = {f.parent for f in files}
    for d in sorted(dirs):
        if (d / "_order.yaml").exists():
            order = _read(d / "_order.yaml") or []
            stems = {f.stem for f in d.glob("*.yaml") if not f.stem.startswith("_")}
            rel = (d / "_order.yaml").relative_to(ROOT).as_posix()
            issues += [f"{rel}: нет {n}.yaml — убери имя из списка" for n in order if n not in stems]
            issues += [f"{rel}: {n} не в списке — добавь (порядок на странице) или python html-view/doctool.py yaml-fmt" for n in sorted(stems - set(order))]
    return issues


def _extra(f: Path, kind: str, v) -> list:
    """Проверки внутри единицы, которых нет в схеме."""
    out = []
    if kind == "block":
        if f.stem != slug(v["title"]):
            out.append(f"title → имя файла должно быть {slug(v['title'])}.yaml (адрес страницы блока); переименуй файл и строку в _order.yaml")
        if f.parent.name not in _cached("comp", lambda: _stems("components")):
            out.append(f"папка {f.parent.name} → нет компонента data/components/{f.parent.name}.yaml")
        raw = _read(f)
        ps = _cat().params(f.parent.name)
        for n, r in enumerate(raw.get("params") if isinstance(raw.get("params"), list) else []):
            spec = ps.get(r.get("name"), {})
            t = spec.get("type")
            if t and "value" in r and r["value"] != spec["default"] and not _cat().value_ok(t, str(r["value"])):
                out.append(f"params[{n}].value → «{r['value']}» не по типу {spec['spec']}/interfaces.md: {_cat().type_text(t)} "
                           f"(по умолчанию {spec['default']}); пояснение вместо значения — поле note")
    if kind == "table":
        cols = [c[0] for c in v.get("columns", [])]
        for n, ix in enumerate((v.get("policy") or ((),))[0] or []):
            out += [f"policy.indexes[{n}].columns → колонки {c} нет в columns таблицы{_cat().suggest(c, cols)}"
                    for c in ix[1].split(", ") if cols and c not in cols]
    if kind == "databases":
        for n, g in enumerate(v["grants"]):
            tb = g[2].split(".")[-1]
            if tb not in _cat().tables():
                out.append(f"grants[{n}].table → таблицы {tb} нет в каталоге{_cat().suggest(tb, _cat().tables())}")
    if kind == "processes":
        for n, pr in enumerate(v["processes"]):
            ids = {s[0] for s in pr["steps"]}
            for k, s in enumerate(pr["steps"]):
                if not 0 <= s[1] < len(pr["lanes"]):
                    out.append(f"processes[{n}].steps[{k}][1] → дорожка {s[1]}: номер от 0 до {len(pr['lanes']) - 1}")
                out += [f"processes[{n}].steps[{k}] → переход в шаг {to}, которого нет" for to, _ in s[4] if to not in ids]
            out += [f"processes[{n}].artifacts.{a} → шага {a} нет" for a in pr["artifacts"] if a not in ids]
    if kind == "costs":
        for n, r in enumerate(v["costs"]):
            m, _, anchor = r["methodology"].partition("#")
            doc = ROOT / "docs/rules" / m
            if not doc.exists():
                out.append(f"costs[{n}].methodology → файла docs/rules/{m} нет")
            elif anchor and "{#" + anchor + "}" not in doc.read_text(encoding="utf-8"):
                out.append(f"costs[{n}].methodology → в {m} нет якоря #{anchor}")
            if "expected" in r and (len(r["expected"]) != 2 or r["expected"][0] > r["expected"][1]):
                out.append(f"costs[{n}].expected → [минимум, максимум] токенов на единицу")
            if r["units"] <= 0:
                out.append(f"costs[{n}].units → больше нуля")
    if kind == "story":
        if not re.fullmatch(r"US-[A-Z]+-\d+", f.stem):
            out.append(f"имя файла → ID истории US-<КОМП>-<NN>.yaml")
        if f.parent.name not in _cached("comp", lambda: _stems("components")):
            out.append(f"папка {f.parent.name} → нет компонента data/components/{f.parent.name}.yaml")
        for n, r in enumerate(_read(f).get("reqs") or []):
            if isinstance(r, dict) and r.get("spec") in _cat().specs() and r.get("title") not in _cat().spec_requirements(r["spec"]):
                out.append(f"reqs[{n}].title → «{r.get('title')}» нет среди «### Requirement:» спеки {r['spec']}"
                           f"{_cat().suggest(r.get('title'), _cat().spec_requirements(r['spec']))}")
        if "chain" in v and v["chain"][0][:1] != [f.stem]:
            out.append(f"chain.path → цепочка начинается с самой истории {f.stem}")
    return out


def fmt(path=None) -> list:
    """Нормализовать формат (порядок ключей по схеме, стиль строк); _order.yaml дополнить новыми файлами. Возвращает изменённые."""
    changed = []
    for f in unit_files(path):
        kind = kind_of(f)
        if not kind:
            continue
        if kind == "order":
            stems = sorted(x.stem for x in f.parent.glob("*.yaml") if not x.stem.startswith("_"))
            order = _read(f) or []
            new = [n for n in order if n in stems] + [n for n in stems if n not in order]
            if write_unit(f, "order", new):
                changed.append(f)
            continue
        v, errs = load_unit(f, kind)
        if errs:
            continue  # сначала yaml-check
        if write_unit(f, kind, v):
            changed.append(f)
    for d in {f.parent for f in unit_files(path)}:  # новая единица без _order.yaml в папке, где он есть
        o = d / "_order.yaml"
        if o.exists() and o not in [x for x in unit_files(path)]:
            stems = sorted(x.stem for x in d.glob("*.yaml") if not x.stem.startswith("_"))
            order = _read(o) or []
            if write_unit(o, "order", order + [n for n in stems if n not in order]):
                changed.append(o)
    return [c.relative_to(ROOT).as_posix() for c in changed]


# ---------------------------------------------------------------- что перегенерируется (doctool next)
REGEN = {
    "component": "страница компонента components/{comp}/ (схема, справка, вкладки); architecture.md спек define-agent-platform — python html-view/archgen.py",
    "block": "страница блока components/{comp}/{stem}/ и схема компонента; architecture.md спек — python html-view/archgen.py",
    "hosts": "страницы встроенных компонентов, связи C1",
    "story": "docs/stories/{comp}.md, docs/stories/coverage.md (build: sync_stories); вкладка «Истории» компонента",
    "processes": "процессы BPMN на docs/stories/{stem}.md и вкладке компонента",
    "personas": "docs/stories/personas.md, docs/stories/README.md",
    "model": "страница «Модель данных» (модель {stem}), вкладки «Интеграции» компонентов, структура эндпоинтов docs/api",
    "table": "страница «Модель данных» (ER, политика хранения), вкладка «Данные» компонентов",
    "endpoints": "структура запрос / ответ на docs/api/{stem}.md",
    "integrations": "C1 и вкладки «Интеграции» компонентов, матрица типов данных",
    "databases": "страница «Модель данных»: кластер, базы, схемы, GRANT",
    "datamodel": "страница «Модель данных»: домены S1, деревья хранилищ, правила имён",
}


def regen(path) -> str:
    """Для файла data/: что перегенерируется и что проверить сразу (doctool next)."""
    f = Path(path).resolve()
    try:
        f.relative_to(DATA.resolve())
    except ValueError:
        return ""
    kind = kind_of(f)
    if kind not in REGEN:
        return ""
    comp = f.parent.name if kind in ("block", "story") else f.stem
    rel = f.relative_to(ROOT.resolve()).as_posix()
    lint = f" · python html-view/doctool.py lint {comp}" if comp in _stems("components") else ""
    return (f"Источник данных (YAML, единица «{kind}»). Сейчас: python html-view/doctool.py yaml-check {rel}{lint}.\n"
            f"Перегенерируется — один раз в конце пути изменений (python html-view/build.py): {REGEN[kind].format(comp=comp, stem=f.stem)}.")


# ---------------------------------------------------------------- карточка единицы (unit)
def _strip(v, top=True):
    """Без пустых полей записи (строки таблиц [..] не трогаем)."""
    if isinstance(v, dict):
        return type(v)({k: _strip(x, False) for k, x in v.items() if x not in ("", [], {}, None)})
    if isinstance(v, list) and not isinstance(v, FlowList):
        return [_strip(x, False) for x in v]
    return v


def _find(q: str):
    """(файл, вид, ключ внутри файла или None) по ID, имени или пути."""
    p = Path(q)
    for cand in (p, ROOT / q, DATA / q):
        if cand.suffix == ".yaml" and cand.exists():
            return cand.resolve(), kind_of(cand), None
    if (DATA / "components" / f"{q}.yaml").exists():
        return DATA / "components" / f"{q}.yaml", "component", None
    for sub_, kind in (("models", "model"), ("tables", "table")):
        if (DATA / sub_ / f"{q}.yaml").exists():
            return DATA / sub_ / f"{q}.yaml", kind, None
    comp, _, rest = q.partition("/")
    for f in DATA.glob("blocks/*/*.yaml"):
        if f.stem.startswith("_"):
            continue
        if (rest and f.parent.name == comp and (f.stem == rest or f.stem == slug(rest))) or f.stem == slug(q):
            return f, "block", None
    if re.fullmatch(r"I\d+", q):
        return DATA / "integrations.yaml", "integrations", q
    if q.startswith("US-"):
        f = next(DATA.glob(f"stories/*/{q}.yaml"), None)
        if f:
            return f, "story", None
    if re.match(r"(GET|POST|PUT|PATCH|DELETE) ", q):
        for f in DATA.glob("endpoints/*.yaml"):
            if q in (_read(f) or {}):
                return f, "endpoints", q
    for f in DATA.glob("blocks/*/*.yaml"):  # по названию блока
        if not f.stem.startswith("_") and (_read(f) or {}).get("title", "").lower() == q.lower():
            return f, "block", None
    return None, "", None


def related(kind, v, key=None) -> list:
    """Связанные ID одной строкой: что ещё затронет правка."""
    txt = json.dumps(v, ensure_ascii=False)
    ids = []
    for rx in (r"\bUS-[A-Z]+-\d+\b", r"\bR-[A-Z]+-\d+\b", r"\bI\d+\b", r"\bD\d+\b", r"\bS\d+\b"):
        ids += sorted(set(re.findall(rx, txt)), key=lambda x: [int(n) if n.isdigit() else n for n in re.split(r"(\d+)", x)])
    if kind == "block":
        ids += [f"задача {t}" for t in v.get("tasks", [])]
        ids += [f"таблица {d['table']}" for d in v.get("data", []) if not isinstance(v.get("data"), str)]
    if kind == "story" and key:
        ids += [f"блок {c}/{t}" for (c, t), s in sub().items() if key in s.get("stories", [])]
        ids += [f"процесс «{p['title']}»" for lst in stories()["BPMN"].values() for p in lst if key in p["stories"]]
        ids += [f"цепочка {k}" for k, (ch, _) in stories()["CHAINS"].items() if key in ch and k != key]
    if kind == "integrations" and key:
        ids += [f"блок {c}/{t}" for (c, t), s in sub().items() if re.search(rf"\b{key}\b"," ".join(x[2] + " " + x[1] for x in s.get("io", [])))]
    if kind == "component" and key:
        ids += [f"блок {key}/{t}" for (c, t) in sub() if c == key]
        ids += [f"интерфейс {i}" for i, r in datamodel()["INTEG"].items() if key in r[:3] or key in datamodel()["ALSO"].get(i, [])]
    if kind in ("model", "table") and key:
        dm = datamodel()
        if kind == "model":
            ids += [f"интерфейс {i}" for i, r in dm["INTEG"].items() if key in r[4]]
            ids += [f"эндпоинт «{k}»" for k, r in dm["ENDPOINT_IO"].items() if re.search(rf"\b{key}\b", " ".join(r[:2]))]
        else:
            ids += [f"блок {c}/{t}" for (c, t), s in sub().items() if not isinstance(s.get("data"), str) for d in s.get("data", []) if d[0].split(" ")[0].strip("`") == key]
    return ids


def card(q: str) -> str:
    f, kind, key = _find(q)
    if not f:
        return f"{q}: единица не найдена — ID (US-…, I…, «МЕТОД путь»), slug компонента, блок «компонент/slug», модель, таблица или путь data/…"
    v, errs = load_unit(Path(f), kind)
    rel = Path(f).resolve().relative_to(ROOT.resolve()).as_posix()
    raw = _read(Path(f)) if errs or kind == "order" else dump_unit(f, kind, v)  # в формате схемы: строки таблиц — в одну строку
    if key is not None:
        raw = {key: raw[key]}
    name = key or Path(f).stem
    head = f"# {rel}" + (f" · {key}" if key else "") + f" · вид {kind}" + (f" · ⚠️ {len(errs)} замечаний схемы" if errs else "")
    rel_ids = related(kind, raw, key or (Path(f).stem if kind in ("model", "table", "story", "component") else None))
    tail = ["связано: " + ", ".join(dict.fromkeys(rel_ids))] if rel_ids else []
    tail.append(f"править: {rel} → python html-view/doctool.py yaml-check {rel}")
    return head + "\n" + to_yaml(_strip(raw)).rstrip("\n") + "\n" + "\n".join(tail) + ("" if name else "")


# ---------------------------------------------------------------- JSON Schema для редактора (yaml-schema)
SCHEMA_DIR = DATA / "_schema"
_GLOB = {"components/*.yaml": "data/components/[!_]*.yaml", "blocks/*/*.yaml": None, "stories/*/*.yaml": "data/stories/*/[!_]*.yaml",
         "models/*.yaml": "data/models/[!_]*.yaml", "tables/*.yaml": "data/tables/[!_]*.yaml", "endpoints/*.yaml": "data/endpoints/*.yaml",
         "processes/*.yaml": "data/processes/*.yaml"}


def json_schemas() -> dict:
    """Имя файла data/_schema → (JSON Schema, glob файлов) по SCHEMAS; enum'ы — из каталогов (yamlcat), описания полей — по-русски.
    Блоки — по компоненту (имена параметров из interfaces.md его спек): block-<компонент>.schema.json."""
    _cat().clear()

    def one(kind, ctx, title):
        c = dict(ctx)
        body = SCHEMAS[kind].js(c)
        out = {"$schema": "http://json-schema.org/draft-07/schema#", "title": title,
               "description": f"Единица data/ вида «{kind}». Генерируется: python html-view/doctool.py yaml-schema (не править руками)."}
        out.update(body)
        if c.get("definitions"):
            out["definitions"] = c["definitions"]
        return out

    res = {}
    for pat, kind in KIND_OF:
        if kind == "block":
            for comp in _cat().components():
                res[f"block-{comp}.schema.json"] = (one("block", {"comp": comp}, f"Блок компонента {comp}"), f"data/blocks/{comp}/[!_]*.yaml")
            continue
        res[f"{kind}.schema.json"] = (one(kind, {}, f"Единица «{kind}»"), _GLOB.get(pat) or f"data/{pat}")
    res["catalog.schema.json"] = ({"$schema": "http://json-schema.org/draft-07/schema#", "title": "Каталоги data/",
                                   "description": "Перечисления для полей-ссылок; строятся из данных и документов (html-view/yamlcat.py).",
                                   "definitions": {k: {"type": "string", "description": what, "enum": [str(x) for x in fn()]}
                                                   for k, (fn, what) in _cat().CATALOGS.items()}}, None)
    res["order.schema.json"] = ({"$schema": "http://json-schema.org/draft-07/schema#", "title": "Порядок единиц папки",
                                 "description": "Имена файлов папки без .yaml в порядке на странице.", "type": "array",
                                 "items": {"type": "string"}}, "data/**/_order.yaml")
    return res


def schema_files() -> dict:
    """Путь → текст: data/_schema/*.schema.json и сопоставление для .vscode/settings.json (yaml.schemas)."""
    out = {}
    for name, (sch, _) in json_schemas().items():
        out[SCHEMA_DIR / name] = json.dumps(sch, ensure_ascii=False, indent=1) + "\n"
    return out


def vscode_settings() -> str:
    """.vscode/settings.json с yaml.schemas (прочие настройки файла сохраняются)."""
    f = ROOT / ".vscode/settings.json"
    cur = json.loads(f.read_text(encoding="utf-8")) if f.exists() and f.read_text(encoding="utf-8").strip() else {}
    m = {k: v for k, v in (cur.get("yaml.schemas") or {}).items() if not k.startswith("./data/_schema/")}
    for name, (_, glob) in json_schemas().items():
        if glob:
            m[f"./data/_schema/{name}"] = glob
    cur["yaml.schemas"] = m
    return json.dumps(cur, ensure_ascii=False, indent=2) + "\n"


def write_schemas() -> list:
    changed = []
    files = schema_files()
    files[ROOT / ".vscode/settings.json"] = vscode_settings()
    for p, text in files.items():
        if not p.exists() or p.read_text(encoding="utf-8") != text:
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(text, encoding="utf-8", newline="\n")
            changed.append(p.relative_to(ROOT).as_posix())
    stale = [p for p in SCHEMA_DIR.glob("*.schema.json") if p not in files]
    for p in stale:
        p.unlink()
        changed.append(p.relative_to(ROOT).as_posix() + " (удалён)")
    return changed


def schemas_stale() -> list:
    """Замечания check: JSON Schema редактора не совпадает с SCHEMAS и каталогами."""
    files = schema_files()
    out = [f"{p.relative_to(ROOT).as_posix()}: устарела — python html-view/doctool.py yaml-schema"
           for p, text in files.items() if not p.exists() or p.read_text(encoding="utf-8") != text]
    out += [f"{p.relative_to(ROOT).as_posix()}: лишняя — python html-view/doctool.py yaml-schema" for p in SCHEMA_DIR.glob("*.schema.json") if p not in files]
    vs = ROOT / ".vscode/settings.json"  # локальный файл (.vscode/ в .gitignore): проверяется, если есть; создаёт yaml-schema / tools/setup
    if vs.exists() and vs.read_text(encoding="utf-8") != vscode_settings():
        out.append(".vscode/settings.json: yaml.schemas устарело — python html-view/doctool.py yaml-schema")
    return out
