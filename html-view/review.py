"""Пакет проверки документа ролью (`./tools/doc review-pack <страница> <буква>`): весь нужный контекст в одном файле.

Экономит токены проверяющего: вместо чтения методологий, спек и замечаний целиком — страница, вопрос роли,
чек-лист методологии её типа, требования страницы (заголовки и сценарии), открытые вопросы по ним, прежние замечания,
пробелы lint компонента (approval-methodology.md, «Экономная проверка»).
"""
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
METHOD = {"Блок": "block-methodology.md", "Архитектура компонента": "architecture-methodology.md", "Интеграции": "api-methodology.md",
          "Данные": "data-methodology.md", "Deploy": "tech-spec.md", "User Stories": "us-methodology.md", "Задача": "task-methodology.md",
          "R&D": "rnd-methodology.md", "Решения (design)": "decision-methodology.md", "Методология": "support-docs-methodology.md",
          "Главная": "architecture-methodology.md"}


def _section(text, title_re):
    m = re.search(rf"^## {title_re}[^\n]*\n(.*?)(?=^## |\Z)", text, re.M | re.S)
    return m.group(1).strip() if m else ""


def _reqs(text):
    """Заголовки и сценарии требований, на которые ссылается страница."""
    ids = sorted(set(re.findall(r"\bR-[A-Z]+-\d+\b", text)), key=lambda x: (x.split("-")[1], int(x.split("-")[2])))
    out, qs = [], set()
    specs = list(ROOT.glob("openspec/changes/*/specs/*/spec.md"))
    for rid in ids:
        for f in specs:
            t = f.read_text(encoding="utf-8")
            if f"`{rid}`" not in t:
                continue
            for block in re.split(r"\n(?=### Requirement: )", t):
                if f"`{rid}`" in block:
                    title = block.split("\n", 1)[0].replace("### Requirement: ", "")
                    sc = re.findall(r"#### Scenario: ([^\n]+)\n- \*\*WHEN\*\* ([^\n]+)\n- \*\*THEN\*\* ([^\n]+)", block)
                    out.append(f"- **{rid}** {title}: " + "; ".join(f"«{n}» — когда {w} → {th}" for n, w, th in sc))
                    qs.add(f.parent / "open-questions.md")
            break
    return out, qs


def pack(page: str, letter: str) -> Path:
    import sys
    sys.path.insert(0, str(HERE))
    import approvals as A
    import lint as LN
    built = HERE / ".build/docs" / page
    if not built.exists():
        raise SystemExit(f"{page}: нет собранной страницы — python html-view/build.py")
    text = built.read_text(encoding="utf-8")
    rule = A.rule_of(page)
    kind = rule[0] if rule else "—"
    roles = (ROOT / "docs/rules/approval-methodology.md").read_text(encoding="utf-8")
    role_row = next((l for l in roles.splitlines() if l.startswith(f"| **{letter}** |")), "")
    meth = (ROOT / "docs/rules" / METHOD.get(kind, "doc-types.md")).read_text(encoding="utf-8")
    check = _section(meth, "Чек-лист") or _section(meth, "Из чего состоит")
    reqs, qfiles = _reqs(text)
    oq = [l for f in qfiles if f.exists() for l in f.read_text(encoding="utf-8").splitlines() if l.startswith("| ОВ-")]
    comp = page.split("/")[1] if page.startswith(("components/", "data-by-component/")) else Path(page).stem
    ff = ROOT / f"docs/reviews/findings/{comp}.md"
    prev = [l for l in (ff.read_text(encoding="utf-8").splitlines() if ff.exists() else []) if l.startswith("| Z-") and (page in l or Path(page).parent.name in l)]
    lint = LN.lint().get(comp, [])
    reg = [c for k, c in A.read_registry().items() if k == (page, letter)]
    L = [f"# Пакет проверки: `{page}` × {letter}", "",
         f"**Тип:** {kind}. **Вопрос роли:** {role_row}", "",
         "**Как решать (экономная проверка):** отказ — только за то, что мешает ответить на вопрос роли, с фактом-источником; "
         "не больше 3 замечаний; механическое уже проверил lint (ниже) — не повторять. Повторная проверка — только изменённое и закрытие прежних замечаний.", "",
         f"**Прежнее решение:** {(' | '.join(reg[0][5:8])) if reg else '—'}", "",
         "## Чек-лист методологии типа", "", check, "",
         f"## Требования страницы ({len(reqs)})", "", *(reqs or ["—"]), "",
         "## Открытые вопросы спек этих требований", "", *(oq or ["—"]), "",
         "## Прежние замечания по странице", "", *(prev or ["—"]), "",
         f"## lint компонента ({len(lint)})", "", *([f"- {x}" for x in lint] or ["—"]), "",
         "## Страница", "", text]
    out = HERE / ".review" / (page.replace("/", "__") + f"__{letter}.md")
    out.parent.mkdir(exist_ok=True)
    out.write_text("\n".join(L), encoding="utf-8")
    return out


# ---------------------------------------------------------------- пакетная проверка (approval-methodology.md#economy)
# Карточка страницы — то, что нужно всем ролям сразу, без ссылок, mermaid и HTML: ~1–1,5 тыс. токенов на документ за все роли.
CARD_MAX, BLOCK_MAX = 2500, 1500
_SPEC = {}


def _clean(s) -> str:
    s = str(s)
    s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s)  # ссылки → текст
    s = re.sub(r"</?(?:span|div|b|i|a|br|sup|sub|small|em|strong|code|details|summary)\b[^>]*>|\s*\{#[^}]*\}", "", s)  # HTML и якоря {#…}
    return re.sub(r"\s+", " ", s.replace("`", "").replace("**", "")).strip()


def _cut(s: str, n: int) -> str:
    return s if len(s) <= n else s[: max(n - 1, 0)].rstrip() + "…"


def _flat(v) -> str:
    if isinstance(v, dict):
        return ", ".join(f"{k}: {_flat(x)}" for k, x in v.items() if x not in ("", [], {}, None))
    if isinstance(v, list):
        rows = all(isinstance(x, (list, tuple)) for x in v)
        return "; ".join((" · " if rows else "; ").join(_flat(y) for y in x if y not in ("", None)) if isinstance(x, (list, tuple))
                         else _flat(x) for x in v if x not in ("", [], {}, None))
    return _clean(v)


def _fit(lines: list, budget: int) -> list:
    """Обрезать строки одинаковым потолком, пока сумма не влезет в бюджет."""
    cap = max((len(l) for l in lines), default=0)
    while cap > 60 and sum(min(len(l), cap) + 1 for l in lines) > budget - 20:
        cap -= 10
    out, total = [], 0
    for l in lines:
        l = _cut(l, cap)
        if total + len(l) + 1 > budget - 20:  # место под «… ещё строк»
            out.append(f"… ещё строк: {len(lines) - len(out)}")
            break
        out.append(l)
        total += len(l) + 1
    return out


def _specs_index() -> dict:
    """R-ID → (название, [(когда, то)])."""
    if not _SPEC:
        for f in ROOT.glob("openspec/changes/*/specs/*/spec.md"):
            for blk in re.split(r"\n(?=### Requirement: )", f.read_text(encoding="utf-8")):
                m = re.search(r"`(R-[A-Z]+-\d+)`", blk)
                if m and blk.startswith("### Requirement: "):
                    sc = re.findall(r"#### Scenario: [^\n]+\n- \*\*WHEN\*\* ([^\n]+)\n- \*\*THEN\*\* ([^\n]+)", blk)
                    _SPEC[m.group(1)] = (blk.split("\n", 1)[0][17:].strip(), [(_clean(w), _clean(t)) for w, t in sc])
    return _SPEC


def _sort_ids(ids):
    return sorted(set(ids), key=lambda x: (x.split("-")[1], int(x.split("-")[2])))


def _req_lines(ids, budget: int) -> list:
    """«R-XXX-NN Название: WHEN→THEN; …» — не больше 3 сценариев; при нехватке места сценарии короче и меньше."""
    idx = _specs_index()
    ids = [i for i in _sort_ids(ids) if i in idx]
    lines = []
    for n, k in ((3, 90), (3, 60), (2, 50), (1, 50), (1, 35), (0, 0)):
        lines = [f"{i} {idx[i][0]}" + (": " + "; ".join(f"{_cut(w, k)}→{_cut(t, k)}" for w, t in idx[i][1][:n]) if n and idx[i][1] else "")
                 for i in ids]
        if sum(len(l) + 1 for l in lines) <= budget:
            return lines
    return _fit(lines, budget)


def _findings(page: str, comp: str) -> list:
    ff = ROOT / f"docs/reviews/findings/{comp}.md"
    if not ff.exists():
        return []
    keys = {page.removesuffix("/index.md"), page}
    if page.startswith("components/") and page.count("/") == 3:
        keys.add(page.split("/")[2])
    out = []
    for l in ff.read_text(encoding="utf-8").splitlines():
        if l.startswith("| Z-"):
            c = [x.strip() for x in l.strip().strip("|").split("|")]
            if not c[-1].startswith("✅") and any(k in c[1] for k in keys):
                out.append(_cut(f"{c[0]} ({c[2]}): {_clean(c[3])} → {_clean(c[4])}", 200))
    return out


def _yaml(path: Path):
    """Единица data/ в компактном позиционном виде (строки таблиц — [a, b, c]): карточка не растёт от имён полей."""
    import yamldata as Y
    import yamlmigrate as M
    if not path.exists():
        return None
    kind = Y.kind_of(path)
    if kind in M.POSITIONAL:
        v, errs = Y.load_unit(path, kind)
        if not errs:
            return M.POSITIONAL[kind].dump(v)
    return Y._read(path)


def _components() -> dict:
    return {f.stem: (_yaml(f) or {}) for f in (ROOT / "data/components").glob("*.yaml") if not f.stem.startswith("_")}


def comp_of(page: str) -> str:
    """Компонент страницы реестра ('' — общая страница)."""
    p = page.split("/")
    if p[0] in ("components", "data-by-component") and len(p) > 2:
        return p[1]
    if page.startswith(("docs/api/", "docs/techspec/", "docs/stories/")):
        return Path(page).stem
    if page.startswith("docs/tasks/"):
        tid = Path(page).name.split("-")[0]
        return next((c for c, u in _components().items() if tid in [str(t) for t in u.get("tasks", [])]), "")
    if page.startswith("docs/rnd/") and (ROOT / page).exists():
        m = re.search(r"компонент: \*\*([^*]+)\*\*", (ROOT / page).read_text(encoding="utf-8"))
        if m:
            return next((c for c, u in _components().items() if u.get("name") == m.group(1).strip()), "")
    return ""


def _source(page: str) -> str:
    for f in (HERE / ".build/docs" / page, ROOT / page):
        if f.exists():
            return f.read_text(encoding="utf-8")
    return ""


def _sections(text: str, budget: int) -> list:
    """Заголовки разделов и первые строки (Deploy, R&D, прочее): «Раздел: строка / строка»."""
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    text = re.sub(r"<!--.*?-->|</?div[^>]*>", "", text, flags=re.S)
    out, left = [], 0
    for l in text.splitlines():
        s = l.strip()
        if re.match(r"#{1,3} ", l):
            out.append([_clean(l.lstrip("# ")), []])
            left = 2
        elif out and left and s and not re.fullmatch(r"\|[-| :]+\|", s) and not s.startswith(("←", ">", "!!!", "???", "<")):
            t = " · ".join(_clean(x) for x in s.strip("|").split("|")) if s.startswith("|") else _clean(s.lstrip("-* "))
            if t:
                out[-1][1].append(t)
                left -= 1
    return _fit([h + (": " + " / ".join(b) if b else "") for h, b in out], budget)


def _comp_lines(comp: str) -> list:
    u = _components().get(comp, {})
    ab = u.get("about") or {}
    blocks = []

    def walk(x):
        if isinstance(x, dict):
            if "title" in x and x.get("kind") not in (None, "ext"):
                blocks.append(x["title"])
            for v in x.values():
                walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)
    walk(u.get("blocks", []))
    L = [f"компонент {u.get('name', comp)} · статус {u.get('status', '—')} · {_clean(u.get('desc', ''))}"]
    if ab.get("purpose"):
        L.append("назначение: " + _clean(ab["purpose"]))
    if ab.get("does"):
        L.append("делает: " + "; ".join(_clean(x) for x in ab["does"]))
    if blocks:
        L.append("блоки: " + ", ".join(dict.fromkeys(blocks)))
    if u.get("stores"):
        L.append("хранилища: " + ", ".join(map(str, u["stores"])))
    if u.get("tasks"):
        L.append("задачи: " + ", ".join(map(str, u["tasks"])))
    return L


def _endpoint_lines(comp: str) -> list:
    import lint as LN
    st = {k: v[1] for k, v in LN._api_status().items()}
    out = []
    for k, e in (_yaml(ROOT / f"data/endpoints/{comp}.yaml") or {}).items():
        note = _clean((e or {}).get("note", ""))
        err = re.findall(r"\b([45]\d\d)\b", note.split("ошибки:", 1)[1]) if "ошибки:" in note else []
        out.append(f"{k} · {st.get(k, '—')} · {_clean((e or {}).get('response', ''))} · ошибки: {', '.join(dict.fromkeys(err)) or '—'}")
    return out


def _table_lines(comp: str) -> list:
    out = []
    for f in sorted((ROOT / "data/tables").glob("*.yaml")):
        if f.stem.startswith("_"):
            continue
        u = _yaml(f) or {}
        if (u.get("owner") or {"fork": "icplan", "litellm": "llm-gateway"}.get(u.get("kind"), "")) != comp:
            continue
        pol = u.get("policy") or {}
        out.append(f"таблица {f.stem} ({u.get('kind', '')}{', ' + str(u['store']) if u.get('store') else ''}): "
                   + ", ".join(str(c[0]) for c in u.get("columns", []))
                   + (f" · хранение: {_clean(pol['retention'])}" if pol.get("retention") else ""))
    return out


def _story_lines(comp: str) -> list:
    out = []
    for f in sorted((ROOT / f"data/stories/{comp}").glob("US-*.yaml"), key=lambda f: int(f.stem.split("-")[-1])):
        s = _yaml(f) or {}
        out.append(f"{f.stem} {s.get('role', '')}: {_clean(s.get('want', ''))} → {_clean(s.get('so_that', ''))} · приёмка: "
                   + "; ".join(_clean(a) for a in s.get("accept", [])))
    return out


def _task_lines(text: str) -> list:
    L = [_clean(text.splitlines()[0].lstrip("# "))] if text else []
    m = re.search(r"^\| Этап[^\n]*\n\|[-| ]+\|\n(\|[^\n]+)", text, re.M)
    if m:
        L.append("этап · компонент · зависит · человек · агент · токены: " + " · ".join(_clean(x) for x in m.group(1).strip().strip("|").split("|")))
    sub = re.findall(r"^\| (\d+\.\d+\.\d+) \| ([^|]+)\| ([\d.]+) \| ([^|]+)\|", text, re.M)
    if sub:
        L.append("подзадачи: " + "; ".join(f"{n} {_cut(_clean(t), 70)} {h} ч — {_cut(_clean(g), 60)}" for n, t, h, g in sub))
    acc = [_clean(l[5:]) for l in _section(text, "Приёмка").splitlines() if l.startswith("- [")]
    if acc:
        L.append("приёмка: " + "; ".join(acc))
    q = [_clean(l[5:]) for l in _section(text, "Что проработать").splitlines() if l.startswith("- [ ]")]
    if q:
        L.append("открыто: " + "; ".join(q))
    return L


def card(page: str) -> str:
    """Компактная карточка страницы реестра для всех ролей сразу (≤ 2500 символов, блок ≤ 1500)."""
    import sys
    sys.path.insert(0, str(HERE))
    import approvals as A
    rule = A.rule_of(page)
    kind = rule[0] if rule else "—"
    comp = comp_of(page)
    text = _source(page)
    budget = BLOCK_MAX if kind == "Блок" else CARD_MAX
    ids = re.findall(r"\bR-[A-Z]+-\d+\b", text)
    if kind == "Блок":
        u = _yaml(ROOT / f"data/blocks/{comp}/{page.split('/')[2]}.yaml") or {}
        ids = list(u.get("reqs", [])) or ids
        body = [f"блок {u.get('title', '')} · {u.get('kind', '')} · {_clean(u.get('tech', ''))}"]
        body += [f"{k}: {_flat(v)}" for k, v in u.items() if k not in ("title", "kind", "tech", "reqs", "why", "rnd") and v not in ("", [], {}, None)]
    elif kind in ("Архитектура компонента", "Данные", "Интеграции"):
        body = _comp_lines(comp) + _endpoint_lines(comp) + (_table_lines(comp) if kind != "Интеграции" else [])
    elif kind == "Задача":
        body = _task_lines(text)
        ids = re.findall(r"\bR-[A-Z]+-\d+\b", _section(text, "Закрывает требования"))
        if ids:
            body.insert(2, "закрывает: " + ", ".join(_sort_ids(ids)))
    elif kind == "User Stories":
        body = _story_lines(comp)
    else:  # Deploy, R&D, решения, методологии: разделы и первые строки
        body, ids = _sections(text, budget), (ids if kind == "Deploy" else [])
    fnd = _findings(page, comp)
    tail = ["незакрытые замечания: " + " | ".join(fnd)] if fnd else []
    reserve = min(budget // 2, 60 + sum(len(f"{i} {_specs_index().get(i, ("",))[0]}") + 80 for i in set(ids))) if ids else 0
    body = _fit(body, budget - reserve - sum(len(x) + 1 for x in tail))
    reqs = _req_lines(ids, budget - sum(len(x) + 1 for x in body + tail) - 25) if ids else []
    return "\n".join(body + ([f"требования ({len(reqs)}):"] + reqs if reqs else []) + tail)


def _role_questions() -> dict:
    """Буква → вопрос роли одной строкой: таблица doc-reviewer, иначе «Роли и буквы» методологии подтверждений."""
    q = {}
    for l in (ROOT / "docs/rules/approval-methodology.md").read_text(encoding="utf-8").splitlines():
        m = re.match(r"\| \*\*(.)\*\* \| ([^|]+)\| ([^|]+)\|", l)
        if m:
            q[m.group(1)] = f"{m.group(2).strip()}: {m.group(3).strip()}"
    for l in (ROOT / ".claude/agents/doc-reviewer.md").read_text(encoding="utf-8").splitlines():
        m = re.match(r"\| (\S) ([^|/]+)\| ([^|]+)\|", l)
        if m and m.group(1) in q:
            q[m.group(1)] = f"{m.group(2).strip()} — отказ, если {m.group(3).strip()}"
    return q


def batch(comp: str, maxn: int = 40) -> list:
    """Пачки ⏳-страниц компонентов (через запятую) в .review/batch-<компоненты>-<N>.md → [(путь, страниц, пар, символов, [(страница, символов)])]."""
    import sys
    sys.path.insert(0, str(HERE))
    import approvals as A
    pages = {}
    for p, letter in A.queue():
        if comp_of(p) in comp.split(","):
            pages.setdefault(p, []).append(letter)
    order = list(A.ROLES)
    items = sorted(pages.items())
    q = _role_questions()
    res = []
    for n, i in enumerate(range(0, len(items), maxn), 1):
        chunk = items[i:i + maxn]
        letters = sorted({x for _, ls in chunk for x in ls}, key=order.index)
        out = HERE / ".review" / f"batch-{comp.replace(',', '+')}-{n}.md"
        jf = out.with_suffix(".json").relative_to(ROOT).as_posix()
        H = [f"# Пачка проверки: {comp} · {n}", "", "Вопросы ролей:", *[f"- {x} {q.get(x, A.ROLES[x])}" for x in letters], "",
             "Правило: отказ (ok=false) — только за блокирующее, с фактом из карточки; ≤2 причины; механику не повторять — её ловит lint. "
             "Каждую пару решай отдельно по вопросу её роли; комментарий ok — что именно проверено в карточке (ID, поле, номер), ≥ 40 символов, у каждой пары свой. "
             "Решения не генерировать скриптом и не копировать: approve-batch отклонит шаблон целиком. "
             f"Ответ — JSON-массив {{\"page\",\"role\",\"ok\",\"comment\"}} по всем парам ниже в файл {jf}, затем "
             f"python html-view/doctool.py approve-batch {jf}", ""]
        cards = []
        for p, ls in chunk:
            c = card(p)
            cards.append((p, len(c)))
            H += [f"## {p} · роли: {''.join(sorted(ls, key=order.index))}", "", c, ""]
        out.parent.mkdir(exist_ok=True)
        txt = "\n".join(H)
        out.write_text(txt, encoding="utf-8")
        res.append((out, len(chunk), sum(len(ls) for _, ls in chunk), len(txt), cards))
    return res
