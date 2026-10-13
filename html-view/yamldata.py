"""Данные сайта в YAML по единице (data/): схема, загрузка, выгрузка, проверка, формат, карточка единицы.

Единица — один файл 1–3 КБ: блок, компонент, модель, таблица, эндпоинты страницы API, истории и процессы компонента.
Модули datamodel.py, subcomponents.py, stories.py, components.py только загружают отсюда значения (имена прежние).
Методология: docs/rules/data-methodology.md#yaml. Команды: doctool yaml-check | yaml-fmt | unit | yaml-export.

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
    """Контекст проверки: ошибки и (для yaml-check) проверка ссылок на другие единицы."""

    def __init__(self, refs=False):
        self.errors, self.refs = [], refs

    def err(self, p, msg):
        self.errors.append(f"{p or '<корень>'} → {msg}")


def _kind(v):
    return {str: "строка", int: "число", bool: "да/нет", list: "список", dict: "словарь", float: "дробное", type(None): "null"}.get(type(v), type(v).__name__)


class Any_:
    scalar = True

    def load(self, v, p, c):
        return v

    def dump(self, v):
        return v

    def accepts(self, v):
        return True


class Str(Any_):
    def __init__(self, choices=None, pattern=None, ref=None, hint=""):
        self.choices, self.pattern, self.ref, self.hint = choices, pattern, ref, hint

    def accepts(self, v):
        return isinstance(v, str)

    def load(self, v, p, c):
        if not isinstance(v, str):
            c.err(p, f"нужна строка, а не {_kind(v)} — возьми значение в кавычки")
            return v
        if not c.refs:  # загрузка модулем — только структура и типы; значения и ссылки — yaml-check
            return v
        if self.choices and v not in self.choices:
            c.err(p, f"«{v}» — допустимо: {', '.join(x or '«»' for x in self.choices)}")
        if self.pattern and v and not re.fullmatch(self.pattern, v):
            c.err(p, f"«{v}» не по формату {self.hint or self.pattern}")
        if self.ref and v:
            bad = REF[self.ref](v)
            if bad:
                c.err(p, bad)
        return v


class Int(Any_):
    def accepts(self, v):
        return isinstance(v, int) and not isinstance(v, bool)

    def load(self, v, p, c):
        if not self.accepts(v):
            c.err(p, f"нужно целое число, а не {_kind(v)}")
        return v


class Bool(Any_):
    def accepts(self, v):
        return isinstance(v, bool)

    def load(self, v, p, c):
        if not isinstance(v, bool):
            c.err(p, f"нужно true или false, а не {_kind(v)}")
        return v


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


class Tup(Any_):
    """Строка таблицы: [a, b, c] в YAML, кортеж в Python. names — подписи полей для сообщений и карточки."""
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


class Fields(Any_):
    """Общее для записей: fields = [(имя, схема, режим)], режим: "req" | "opt" | ("def", значение по умолчанию)."""
    scalar = False

    def __init__(self, *fields, flow=False, tag=None):
        self.fields = [f if len(f) == 3 else (*f, "req") for f in fields]
        self.flow, self.tag = flow, tag
        self.names = [f[0] for f in self.fields]

    def accepts(self, v):
        return isinstance(v, dict) and (self.tag is None or self.tag in v)

    def _load_map(self, v, p, c):
        if not isinstance(v, dict):
            c.err(p, f"нужен словарь с полями {', '.join(self.names)}, а не {_kind(v)}")
            return None
        for k in v:
            if k not in self.names:
                c.err(f"{p}.{k}" if p else str(k), f"лишнее поле — допустимы: {', '.join(self.names)}")
        out = {}
        for name, sch, mode in self.fields:
            q = f"{p}.{name}" if p else name
            if name in v:
                out[name] = sch.load(v[name], q, c)
            elif mode == "req":
                c.err(q, "обязательное поле не заполнено")
            elif isinstance(mode, tuple):
                out[name] = mode[1]() if callable(mode[1]) else mode[1]
        return out


class Rec(Fields):
    """Словарь с известными полями (в Python — dict в порядке схемы)."""

    def load(self, v, p, c):
        out = self._load_map(v, p, c)
        return v if out is None else out

    def dump(self, v):
        out = {}
        for name, sch, mode in self.fields:
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


class Lazy(Any_):
    scalar = False

    def __init__(self, fn):
        self.fn = fn

    def __getattr__(self, k):
        return getattr(self.fn(), k)

    def accepts(self, v):
        return self.fn().accepts(v)

    def load(self, v, p, c):
        return self.fn().load(v, p, c)

    def dump(self, v):
        return self.fn().dump(v)


# ---------------------------------------------------------------- ссылки (yaml-check)
_REFCACHE = {}


def _cached(name, fn):
    if name not in _REFCACHE:
        _REFCACHE[name] = fn()
    return _REFCACHE[name]


def _stems(sub):
    return {f.stem for f in (DATA / sub).glob("*.yaml") if not f.stem.startswith("_")}


def _story_ids():
    return {f.stem for f in DATA.glob("stories/*/*.yaml") if not f.stem.startswith("_")}


def _spec_text():
    return "".join(f.read_text(encoding="utf-8") for f in ROOT.glob("openspec/changes/*/specs/*/spec.md"))


def _tables():
    schema = json.loads((HERE / "icplan_schema.json").read_text(encoding="utf-8"))
    d = datamodel()
    return set(d["PLATFORM_TABLES"]) | {v["table"] for v in schema.values()} | set(d["LITELLM_TABLES"]) | set(d["FORK_COLUMNS"])


def _miss(what, ok, fix):
    return None if ok else f"{what} — {fix}"


REF = {
    "component": lambda v: _miss(f"компонента «{v}» нет", v in _cached("comp", lambda: _stems("components")), "есть data/components/<slug>.yaml"),
    "component*": lambda v: None if v.startswith("«") or v in _cached("comp", lambda: _stems("components"))
    else f"«{v}» — slug компонента (data/components) или внешний участник в «…»",
    "story": lambda v: _miss(f"истории {v} нет", v in _cached("stories", _story_ids), "файл data/stories/<компонент>/<US-ID>.yaml"),
    "stories": lambda v: next((f"истории {x} нет — id из data/stories" for x in re.split(r",\s*", v) if x.startswith("US-")
                               and x not in _cached("stories", _story_ids)), None),
    "req": lambda v: _miss(f"требования {v} нет", f"`{v}`" in _cached("spec", _spec_text), "код R-… из spec.md"),
    "task": lambda v: _miss(f"задачи {v} нет", bool(list((ROOT / "docs/tasks").glob(f"{v}-*.md"))), "номер файла docs/tasks/<номер>-*.md"),
    "icode": lambda v: _miss(f"интерфейса {v} нет", v in _cached("integ", lambda: set(datamodel()["INTEG"])), "I-код из data/integrations.yaml"),
    "model": lambda v: _miss(f"модели {v} нет", v in _cached("models", lambda: _stems("models")), "имя файла data/models/<Имя>.yaml"),
    "rnd": lambda v: _miss(f"R&D {v} нет", (ROOT / "docs/rnd" / v).exists(), "файл в docs/rnd или пусто"),
    "role": lambda v: _miss(f"роли {v} нет", v in _cached("roles", lambda: set(stories()["ROLES"]) | set(stories()["PERSONAS"])), "ключ roles / personas в data/personas.yaml"),
    "table": lambda v: None if re.match(r"S\d+", v.split(" ")[0].strip("`")) or v.split(" ")[0].strip("`") in _cached("tables", _tables)
    else f"таблицы `{v.split(' ')[0].strip('`')}` нет в модели данных — data/tables, схема форка или LiteLLM",
    "path": lambda v: _miss(f"файла {v} нет", (ROOT / v).exists(), "путь от корня репозитория"),
    "irefs": lambda v: next((f"I-код {i} нет в data/integrations.yaml" for i in re.findall(r"\bI\d+\b", v)
                             if i not in _cached("integ", lambda: set(datamodel()["INTEG"]))), None),
}

# ---------------------------------------------------------------- схемы единиц
S = Str()
SID = Str(ref="story", pattern=r"US-[A-Z]+-\d+", hint="US-<КОМП>-<NN>")
TASK = Str(ref="task", pattern=r"\d+\.\d+", hint="номер задачи «2.3» в кавычках")
REQ = Str(ref="req", pattern=r"R-[A-Z]+-\d+", hint="R-<КОМП>-<NN>")
COMP = Str(ref="component")

BLOCK_CELL = Rec(("title", S), ("desc", S, ("def", "")), ("kind", Str(choices=("core", "ext", "store", "user", "back", ""))), ("st", S, ("def", "")),
                 ("g", S, ("def", "")), ("to", Str(ref="component"), ("def", "")), flow=True, tag="title")
ROW = Lazy(lambda: _ROW)
ZONE = Rec(("zone", S), ("rows", Lst(ROW)), ("cls", S, ("def", "")), ("g", S, ("def", "")), ("note", S, ("def", "")), tag="zone")
_ROW = OneOf(S, Lst(BLOCK_CELL), ZONE, hint="строка-подпись потока, список блоков [{title, desc, kind, st, g, to}] или зона {zone, rows}")

SCHEMAS = {
    "component": Rec(
        ("name", S), ("status", Str(choices=("done", "part", "todo"))), ("guardrails", Str(pattern=r"(G\d+([–-]G\d+)?(, )?)*", hint="G1, G1–G4 или пусто")),
        ("desc", S), ("links", Lst(Any_()), ("def", list)),
        ("specs", Lst(Tup(S, Str(ref="path"), names=("подпись", "путь")))), ("tasks", Lst(TASK, flow=True)),
        ("about", TRec(("chain", Lst(Tup(S, Opt(COMP), names=("подпись", "slug|null")))), ("purpose", S), ("does", Lst(S))), "opt"),
        ("stores", Lst(Str(pattern=r"S\d+", hint="S<N>"), flow=True), "opt"),
        ("icplan_tables", Lst(Tup(S, S, names=("ключ icplan_schema.json", "пометка"))), "opt"),
        ("blocks", Lst(ROW), "opt")),
    "block": Rec(
        ("title", S), ("tech", S), ("kind", Str(choices=("ui", "service", "store")), "opt"),
        ("stories", Lst(SID, flow=True), "opt"),
        ("screens", Lst(TRec(("name", S), ("where", S), ("what", S), ("status", S), ("code", S), ("stories", Str(ref="stories")), flow=True)), "opt"),
        ("params", OneOf(S, Lst(Tup(S, S, names=("параметр", "значение"))), hint="строка «нет: …» или список [параметр, значение]"), "opt"),
        ("does", Lst(S), "opt"),
        ("io", Lst(Tup(Str(choices=("→", "←", "↔")), Str(ref="irefs"), Str(ref="irefs"), names=("→|←", "с кем", "что (I-код)"))), "opt"),
        ("data", Lst(Tup(Str(ref="table"), S, names=("таблица", "доступ"))), "opt"),
        ("reqs", Lst(REQ, flow=True), "opt"), ("tasks", Lst(TASK, flow=True), "opt"),
        ("failures", Lst(S), "opt"), ("why", S, "opt"), ("rnd", Str(ref="rnd"), "opt"),
        ("ops", Lst(Tup(S, S, S)), "opt"), ("schema", S, "opt"), ("iface", Lst(S), "opt")),
    "hosts": Lst(Rec(("owner", COMP), ("block", S, "opt"), ("host", COMP), flow=True)),
    "model": Rec(
        ("purpose", S),
        ("fields", Lst(Tup(S, S, Bool(), S, names=("поле", "тип", "обязательное", "описание")))),
        ("source", TRec(("kind", Str(choices=("fork", "ours", "ext"))), ("ref", S), ("part", S, "opt"), ("why", S))),
        ("field_src", Map(S, S), "opt"), ("planned", Map(S, S), "opt")),
    "table": Rec(
        ("kind", Str(choices=("platform", "fork", "litellm"))), ("store", Str(pattern=r"S\d+"), "opt"), ("owner", COMP, "opt"),
        ("schema", Str(pattern=r"\w+\.\w+", hint="база.схема"), "opt"), ("written", Bool(), "opt"),
        ("columns", Lst(Tup(S, S, S, S, names=("колонка", "тип", "ключ", "описание"))), "opt"),
        ("policy", TRec(("indexes", Opt(Lst(Tup(Str(choices=("unique", "index", "hnsw")), S, S, names=("вид", "колонки", "зачем"))))),
                        ("retention", S), ("cleanup", S), ("migrate", S)), "opt")),
    "endpoints": Map(Str(pattern=r"(GET|POST|PUT|PATCH|DELETE) \S.*", hint="«МЕТОД путь»"),
                     TRec(("request", S), ("response", S), ("note", S))),
    "integrations": Map(Str(pattern=r"I\d+", hint="I<N>"), Rec(
        ("from", Str(ref="component*")), ("to", Str(ref="component*")), ("via", Str(ref="component*")), ("what", S),
        ("models", Lst(Str(ref="model"), flow=True)), ("types", S, "opt"), ("also", Lst(COMP, flow=True), "opt"),
        ("data_in_response", Bool(), "opt"))),
    "databases": Rec(
        ("cluster", Map(S, S)),
        ("databases", Map(S, Rec(("owner", COMP), ("schemas", Map(S, Rec(("owner", COMP), ("role", S), ("stores", S), ("migrate", S), ("what", S))))))),
        ("grants", Lst(Tup(S, Str(choices=("SELECT", "REFERENCES", "INSERT", "UPDATE", "DELETE")), S, S, names=("роль", "право", "таблица", "зачем")))),
        ("migrate", Map(S, S))),
    "datamodel": Rec(
        ("naming", S), ("litellm_ref", S),
        ("s1_domains", Lst(Tup(S, Lst(S, flow=True), names=("домен", "таблицы")))),
        ("trees", Map(Str(pattern=r"S\d+"), TRec(("title", S), ("lines", Lst(S)))))),
    "story": Rec(
        ("role", Str(ref="role")), ("want", S), ("so_that", S), ("accept", Lst(S)), ("reqs", Lst(S)), ("entry", S, "opt"),
        ("chain", TRec(("path", Lst(SID, flow=True)), ("end", S)), "opt")),
    "processes": Rec(
        ("processes", Lst(Rec(
            ("title", S), ("stories", Lst(SID, flow=True)), ("lanes", Lst(S, flow=True)),
            ("steps", Lst(Tup(S, Int(), Str(choices=("start", "task", "gateway", "end", "error")), S,
                              Lst(Tup(S, S)), names=("id", "дорожка", "тип", "подпись", "[[куда, подпись]]")))),
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
    c = Ctx(refs)
    try:
        raw = _read(path)
    except yaml.YAMLError as e:
        return None, [f"не YAML: {str(e).splitlines()[0]} (строка {getattr(getattr(e, 'problem_mark', None), 'line', -1) + 1})"]
    if kind == "order":
        if not isinstance(raw, list) or not all(isinstance(x, str) for x in raw):
            return raw, ["нужен список имён файлов без .yaml"]
        return raw, []
    v = SCHEMAS[kind].load(raw, "", c)
    return v, c.errors


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
    text = to_yaml(SCHEMAS[kind].dump(value) if kind != "order" else value)
    if path.exists():
        text = _header(path) + text
        if path.read_text(encoding="utf-8") == text:
            return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    return True


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
    """Замечания «файл: поле → что исправить» по схеме, ссылкам и порядку (_order.yaml)."""
    _REFCACHE.clear()
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
        ids += [f"таблица {d[0].split(' ')[0].strip('`')}" for d in v.get("data", [])]
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
            ids += [f"блок {c}/{t}" for (c, t), s in sub().items() for d in s.get("data", []) if d[0].split(" ")[0].strip("`") == key]
    return ids


def card(q: str) -> str:
    f, kind, key = _find(q)
    if not f:
        return f"{q}: единица не найдена — ID (US-…, I…, «МЕТОД путь»), slug компонента, блок «компонент/slug», модель, таблица или путь data/…"
    v, errs = load_unit(Path(f), kind)
    rel = Path(f).resolve().relative_to(ROOT.resolve()).as_posix()
    raw = _read(Path(f)) if errs or kind == "order" else SCHEMAS[kind].dump(v)  # в формате схемы: строки таблиц — в одну строку
    if key is not None:
        raw = {key: raw[key]}
    name = key or Path(f).stem
    head = f"# {rel}" + (f" · {key}" if key else "") + f" · вид {kind}" + (f" · ⚠️ {len(errs)} замечаний схемы" if errs else "")
    rel_ids = related(kind, raw, key or (Path(f).stem if kind in ("model", "table", "story", "component") else None))
    tail = ["связано: " + ", ".join(dict.fromkeys(rel_ids))] if rel_ids else []
    tail.append(f"править: {rel} → python html-view/doctool.py yaml-check {rel}")
    return head + "\n" + to_yaml(_strip(raw)).rstrip("\n") + "\n" + "\n".join(tail) + ("" if name else "")
