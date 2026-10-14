"""Покрытие: сценарии требований и блоки схем компонентов должны иметь подзадачу / строку бэклога.
Предупреждения (не ошибки): doctool coverage [компонент] [--file]; в check — число и файл списка."""
import re
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent.parent
SPECS = ROOT / "openspec" / "changes"
TASKS = ROOT / "docs" / "tasks"
OUT = ROOT / "html-view" / ".coverage.txt"
STOP = set("при при если для как что или все всё без над под из на по от до не нет его ее её они этот это тот через после перед между только уже ещё еще".split())


def stems(s):
    out = []
    for w in re.findall(r"[A-Za-zА-Яа-яЁё0-9_]+", s.lower()):
        if w in STOP or len(w) < 4 and not re.search(r"\d", w):
            continue
        out.append(w[:5])
    return out


def covered(title, text):
    st = stems(title)
    if not st:
        return True
    t = text.lower()
    if title.lower() in t:
        return True
    code = re.match(r"([A-Za-z]{1,2}\d)", title)  # блок с кодом («M3 задачная»): достаточно кода
    if code:
        return bool(re.search(r"\b" + code.group(1).lower() + r"\b", t)) or any(
            code.group(1) in expand(m) for m in re.findall(r"[A-Z]{1,2}\d\s*[–-]\s*[A-Z]{0,2}\d", text))
    hit = sum(1 for x in st if x in t)
    return hit * 2 >= len(st) + (1 if len(st) > 1 else 0) - (1 if len(st) > 2 else 0) and hit >= 1


def expand(s, ranges_only=False):
    codes = set() if ranges_only else set(re.findall(r"\b([A-Z]{1,2}\d)\b", s))
    for m in re.finditer(r"\b([A-Z]{1,2})(\d)\s*(?:[–-]|\.{3}|…)\s*(?:[A-Z]{1,2})?(\d)\b", s):
        for k in range(int(m.group(2)), int(m.group(3)) + 1):
            codes.add(f"{m.group(1)}{k}")
    return codes


def subtasks(path):
    """Текст строк таблицы «Декомпозиция» (без итога)."""
    s = path.read_text(encoding="utf-8")
    m = re.search(r"^## Декомпозиция.*?(?=^## |\Z)", s, re.S | re.M)
    if not m:
        return ""
    return "\n".join(l for l in m.group(0).splitlines() if re.match(r"\|\s*\d+\.\d+\.\d+", l))


def acceptance(path, rid):
    """Строки раздела «Приёмка» с кодом rid; если код нигде не указан — весь раздел."""
    s = path.read_text(encoding="utf-8")
    m = re.search(r"^## Приёмка.*?(?=^## |\Z)", s, re.S | re.M)
    if not m:
        return ""
    ls = [l for l in m.group(0).splitlines() if l.lstrip().startswith(("-", "|"))]
    mine = [l for l in ls if rid in l]
    return "\n".join(mine or ls)


def task_files():
    d = {}
    for f in TASKS.glob("*.md"):
        m = re.match(r"(\d+\.\d+)-", f.name)
        if m:
            d[m.group(1)] = f
    return d


def spec_items():
    """(comp_spec, req_id, req_title, [tasks], [scenarios], statement)"""
    out = []
    for f in SPECS.glob("*/specs/*/spec.md"):
        s = f.read_text(encoding="utf-8")
        for blk in re.split(r"(?=^### Requirement:)", s, flags=re.M)[1:]:
            title = re.match(r"### Requirement:\s*(.+)", blk).group(1).strip()
            m = re.search(r"\*\*ID:\*\*\s*`(R-[A-Z]+-\d+)`\s*·\s*\*\*Реализует задача:\*\*\s*(.+)", blk)
            if not m:
                continue
            tids = re.findall(r"\[(\d+\.\d+)\]\(", m.group(2))
            if not tids:
                continue
            scen = re.findall(r"^#### Scenario:\s*(.+)$", blk, re.M)
            stmt = "\n".join(l for l in blk.splitlines()[1:6] if not l.startswith("#"))
            out.append((f.parent.name, m.group(1), title, tids, [x.strip() for x in scen], stmt))
    return out


def blocks(node):
    if isinstance(node, dict):
        if "title" in node:
            yield node
        for v in node.values():
            yield from blocks(v)
    elif isinstance(node, list):
        for x in node:
            yield from blocks(x)


def collect():
    """[(компонент, текст находки)]"""
    tf = task_files()
    res = []
    sub_cache = {}
    # сценарии
    for spec, rid, title, tids, scen, stmt in spec_items():
        comp = spec
        text = ""
        for t in tids:
            if t in tf:
                sub_cache.setdefault(t, subtasks(tf[t]))
                text += sub_cache[t] + "\n" + acceptance(tf[t], rid) + "\n"  # покрыт подзадачей или строкой приёмки + acceptance(tf[t], rid) + "\n"  # покрыт подзадачей или строкой приёмки
        if not text:
            continue
        for sc in scen:
            if not covered(sc, text):
                res.append((comp, f"{rid}: сценарий «{sc}» без подзадачи в {', '.join(tids)}"))
        want = expand(stmt, ranges_only=True)  # перечень задан диапазоном «M0–M6»
        if len(want) >= 3:
            full = "\n".join(tf[t].read_text(encoding="utf-8") for t in tids if t in tf)  # диапазон «G1–G4» может стоять в любом месте задачи
            have = expand(text + "\n" + full)
            for c in sorted(want - have):
                res.append((comp, f"{rid}: элемент {c} перечня без подзадачи в {', '.join(tids)}"))
    # блоки схем
    backlog = (ROOT / "docs" / "BACKLOG.md").read_text(encoding="utf-8")
    for f in sorted((ROOT / "data" / "components").glob("*.yaml")):
        d = yaml.safe_load(f.read_text(encoding="utf-8"))
        if not isinstance(d, dict):
            continue
        ctasks = [str(x) for x in d.get("tasks") or []]
        ttext = "\n".join(tf[t].read_text(encoding="utf-8") for t in ctasks if t in tf)
        for b in blocks(d.get("blocks")):
            ttl = str(b.get("title"))
            if b.get("kind") == "back":
                if not covered(ttl, backlog):
                    res.append((f.stem, f"блок «{ttl}» (back) без строки в BACKLOG"))
            elif b.get("st") == "todo":
                if not ctasks:
                    res.append((f.stem, f"блок «{ttl}» (todo): у компонента нет задач"))
                elif not covered(ttl, ttext):
                    res.append((f.stem, f"блок «{ttl}» (todo) не упомянут в задачах {', '.join(ctasks)}"))
    return res


def run(comp=None, to_file=False, quiet=False):
    res = collect()
    if comp:
        res = [r for r in res if r[0] == comp]
    from collections import Counter
    cnt = Counter(c for c, _ in res)
    if to_file or len(res) > 40:
        OUT.write_text("\n".join(f"{c}: {m}" for c, m in sorted(res)), encoding="utf-8")
    if not quiet:
        if len(res) > 40:
            print(f"⚠️ покрытие: находок {len(res)} (список — {OUT.relative_to(ROOT).as_posix()}): " + ", ".join(f"{c} {n}" for c, n in cnt.most_common()))
        else:
            for c, m in sorted(res):
                print(f"⚠️ покрытие {c}: {m}")
            print(f"покрытие: находок {len(res)}" + (": " + ", ".join(f"{c} {n}" for c, n in cnt.most_common()) if res else ""))
    return res, cnt
