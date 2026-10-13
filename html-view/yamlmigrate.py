"""yaml-migrate: перевод data/*.yaml из прежнего позиционного вида строк ([a, b, c]) в именованные поля (идемпотентно).

Файл читается прежней схемой вида (POSITIONAL) или новой (уже переведён) → значение в Python (прежние структуры модулей) →
записывается новой схемой: строки таблиц — словари с именованными полями, ID (I…, R-…, D…, модели, таблицы, эндпоинты)
вынесены из текста в поля там, где текст собирается обратно без потерь (страницы сайта не меняются).
Что не извлеклось однозначно, остаётся текстом и выводится списком для ручного разбора (leftovers).
Методология: docs/rules/data-methodology.md#yaml-units.
"""
import re
from pathlib import Path

import yamldata as Y
from yamldata import Bool, Int, Lazy, Lst, Map, OneOf, Opt, Rec, Str, TRec, Tup, Any_

S = Str()
_CELL = Rec(("title", S), ("desc", S, ("def", "")), ("kind", Str(choices=("core", "ext", "store", "user", "back", ""))), ("st", S, ("def", "")),
            ("g", S, ("def", "")), ("to", S, ("def", "")), flow=True, tag="title")
_R = Lazy(lambda: _ROWO, "row_old")
_ZONE = Rec(("zone", S), ("rows", Lst(_R)), ("cls", S, ("def", "")), ("g", S, ("def", "")), ("note", S, ("def", "")), tag="zone")
_ROWO = OneOf(S, Lst(_CELL), _ZONE)

# прежний позиционный вид строк таблиц (как в yamldata.py до yaml-migrate): читается при переводе;
# им же review.py строит компактные карточки проверки (строка — значения подряд, без имён полей)
POSITIONAL = {
    "component": Rec(
        ("name", S), ("status", S), ("guardrails", S), ("desc", S), ("links", Lst(Any_()), ("def", list)),
        ("specs", Lst(Tup(S, S))), ("tasks", Lst(S)),
        ("about", TRec(("chain", Lst(Tup(S, Opt(S)))), ("purpose", S), ("does", Lst(S))), "opt"),
        ("stores", Lst(S), "opt"), ("icplan_tables", Lst(Tup(S, S)), "opt"), ("blocks", Lst(_R), "opt")),
    "block": Rec(
        ("title", S), ("tech", S), ("kind", S, "opt"), ("stories", Lst(S), "opt"),
        ("screens", Lst(TRec(("name", S), ("where", S), ("what", S), ("status", S), ("code", S), ("stories", S))), "opt"),
        ("params", OneOf(S, Lst(Tup(S, S))), "opt"), ("does", Lst(S), "opt"),
        ("io", Lst(Tup(S, S, S)), "opt"), ("data", OneOf(S, Lst(Tup(S, S))), "opt"),
        ("reqs", Lst(S), "opt"), ("tasks", Lst(S), "opt"), ("failures", Lst(S), "opt"), ("why", S, "opt"), ("rnd", S, "opt"),
        ("ops", Lst(Tup(S, S, S)), "opt"), ("schema", S, "opt"), ("iface", Lst(S), "opt")),
    "model": Rec(
        ("purpose", S), ("fields", Lst(Tup(S, S, Bool(), S))),
        ("source", TRec(("kind", S), ("ref", S), ("part", S, "opt"), ("why", S))),
        ("field_src", Map(S, S), "opt"), ("planned", Map(S, S), "opt")),
    "table": Rec(
        ("kind", S), ("store", S, "opt"), ("owner", S, "opt"), ("schema", S, "opt"), ("written", Bool(), "opt"),
        ("columns", Lst(Tup(S, S, S, S)), "opt"),
        ("policy", TRec(("indexes", Opt(Lst(Tup(S, S, S)))), ("retention", S), ("cleanup", S), ("migrate", S)), "opt")),
    "databases": Rec(
        ("cluster", Map(S, S)),
        ("databases", Map(S, Rec(("owner", S), ("schemas", Map(S, Rec(("owner", S), ("role", S), ("stores", S), ("migrate", S), ("what", S))))))),
        ("grants", Lst(Tup(S, S, S, S))), ("migrate", Map(S, S))),
    "datamodel": Rec(
        ("naming", S), ("litellm_ref", S), ("s1_domains", Lst(Tup(S, Lst(S)))),
        ("trees", Map(S, TRec(("title", S), ("lines", Lst(S)))))),
    "story": Rec(
        ("role", S), ("want", S), ("so_that", S), ("accept", Lst(S)), ("reqs", Lst(S)), ("entry", S, "opt"),
        ("chain", TRec(("path", Lst(S)), ("end", S)), "opt")),
    "processes": Rec(
        ("processes", Lst(Rec(
            ("title", S), ("stories", Lst(S)), ("lanes", Lst(S)),
            ("steps", Lst(Tup(S, Int(), S, S, Lst(Tup(S, S))))),
            ("artifacts", Map(S, Lst(S)), ("def", dict))))),
        ("artifacts", Map(S, Lst(S)), "opt")),
}


def migrate() -> tuple:
    """(изменённые файлы, ошибки). Идемпотентно: переведённый файл записывается тем же."""
    Y.LEGACY.update(POSITIONAL)
    Y._CACHE.clear()
    changed, errors = [], []
    try:
        vals = {}
        for f in Y.unit_files():
            kind = Y.kind_of(f)
            if not kind or kind == "order":
                continue
            v, errs = Y.load_unit(f, kind)
            if errs:
                errors.append(f"{rel(f)}: " + "; ".join(errs[:3]))
                continue
            vals[f] = (kind, v)
        lossy = set()
        for f, (kind, v) in vals.items():  # каталоги (yamlcat) уже собраны из прежнего вида — пишем новый
            lost = Y.ref_ids(Y._read(f)) - Y.ref_ids(Y.dump_unit(f, kind, v))  # сначала всё собрать: ошибка сборки — до записи
            if lost:  # ID из полей via/reqs/decisions пропал бы (join_ids не повторяет ID, уже стоящий в тексте)
                lossy.add(f)
                errors.append(f"{rel(f)}: не записан — пропали бы ID из полей: {', '.join(sorted(lost))}")
        for f, (kind, v) in vals.items():
            if f not in lossy and Y.write_unit(f, kind, v):
                changed.append(rel(f))
    finally:
        Y.LEGACY.clear()
        Y._CACHE.clear()
    for f, (kind, v) in vals.items():  # без прежних схем: новый вид читается в то же значение
        v2, errs = Y.load_unit(f, kind)
        if errs or v2 != v:
            errors.append(f"{rel(f)}: после перевода значение не совпало ({'; '.join(errs[:2]) or 'другое значение'})")
    return changed, errors


def rel(f) -> str:
    return Path(f).resolve().relative_to(Y.ROOT.resolve()).as_posix()


# ---------------------------------------------------------------- что осталось текстом (для ручного разбора)
_TEXT = {  # вид → (поле-список строк, текстовые поля строки)
    "block": [("io", ("label", "what")), ("data", ("why",)), ("ops", ("op", "label", "via_note")), ("failures", ("when", "then")),
              ("screens", ("what",)), ("params", ("note",))],
    "model": [("fields", ("desc",))],
    "table": [("columns", ("key", "desc"))],
    "story": [("reqs", ("text",))],
}


def leftovers() -> list:
    """Строки, где в текстовом поле остались ID (I…, R-…, D…, US-…, `Модель`, `таблица`, `МЕТОД путь`) или участник не из каталога."""
    import yamlcat as C
    models, tables = set(C.models()), set(C.tables())
    out = []
    for f in Y.unit_files():
        kind = Y.kind_of(f)
        if kind not in _TEXT:
            continue
        raw = Y._read(f) or {}
        for field, texts in _TEXT[kind]:
            rows = raw.get(field)
            if not isinstance(rows, list):
                continue
            for n, r in enumerate(rows):
                if not isinstance(r, dict):
                    continue
                found = []
                for t in texts:
                    s = str(r.get(t, ""))
                    ids = re.findall(r"\bI\d+\b|\bR-[A-Z]+-\d+\b|\bD\d+\b|\bUS-[A-Z]+-\d+\b", s)
                    ids += [f"`{m}`" for m in re.findall(r"`([A-Za-z_]\w*)`", s) if m in models or m in tables]
                    ids += [f"`{m}`" for m in re.findall(r"`((?:GET|POST|PUT|PATCH|DELETE) [^`]+)`", s)]
                    have = {str(x) for k in ("via", "reqs", "decisions", "model") for x in (r.get(k) or [])}
                    have |= {f"`{r[k]}`" for k in ("endpoint", "table") if r.get(k)} | {f"`{x}`" for x in (r.get("model") or [])}
                    ids = [i for i in ids if i not in have]
                    found += [f"{t}: {', '.join(dict.fromkeys(ids))}"] if ids else []
                if field in ("io", "ops") and "label" in r:
                    found.append(f"участник «{r['label']}» не из каталога")
                if field == "data" and "access" not in r:
                    found.append("доступ не распознан")
                if found:
                    out.append(f"{rel(f)}: {field}[{n}] — " + "; ".join(found))
    return out
