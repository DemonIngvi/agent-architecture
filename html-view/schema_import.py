"""Импорт схемы БД форка ICPlan (Drizzle) в icplan_schema.json.

    python html-view/schema_import.py [путь к форку]   # по умолчанию D:/АИ агент/itsaplan

Читает packages/db/src/schema/{app,auth,scim}.ts: таблицы pgTable, колонки, первичные ключи
(в том числе составные primaryKey({ columns })), NOT NULL и внешние ключи references().
Коммит форка записывается в icplan_schema.meta.json; сборка сверяет его с форком (О-44).
"""
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
DEFAULT = Path("D:/АИ агент/itsaplan")
REL = "packages/db/src/schema"
FILES = ["app.ts", "auth.ts", "scim.ts"]  # приложение, Better Auth (user, apikey), SCIM


def _strip_comments(s):
    s = re.sub(r"/\*.*?\*/", "", s, flags=re.S)
    return re.sub(r"(?m)^\s*//.*$|(?<=[,;{(])\s*//.*$", "", s)


def _match(s, i, o="{", c="}"):
    """Индекс закрывающей скобки для s[i] == o."""
    depth = 0
    for k in range(i, len(s)):
        depth += (s[k] == o) - (s[k] == c)
        if depth == 0:
            return k
    raise ValueError("скобки не сбалансированы")


def _split_top(body):
    """Разбить тело объекта колонок по запятым верхнего уровня."""
    parts, depth, cur, q = [], 0, [], None
    for ch in body:
        if q:
            q = None if ch == q else q
        elif ch in "'\"`":
            q = ch
        elif ch in "({[":
            depth += 1
        elif ch in ")}]":
            depth -= 1
        elif ch == "," and depth == 0:
            parts.append("".join(cur))
            cur = []
            continue
        cur.append(ch)
    parts.append("".join(cur))
    return [p.strip() for p in parts if p.strip()]


def parse(src: str) -> dict:
    src = _strip_comments(src)
    out = {}
    for m in re.finditer(r"""export const (\w+) = pgTable\(\s*['"]([a-z_0-9]+)['"],\s*\{""", src):
        var, table = m.group(1), m.group(2)
        a = m.end() - 1
        b = _match(src, a)
        cols, by_prop = [], {}
        for part in _split_top(src[a + 1:b]):
            cm = re.match(r"(\w+):\s*(\w+)\(\s*['\"]([a-zA-Z_0-9]+)['\"]", part)
            if not cm:
                continue
            ref = re.search(r"references\(\s*\([^)]*\)\s*(?::\s*\w+\s*)?=>\s*(\w+)\.", part)
            col = {"name": cm.group(3), "type": cm.group(2), "pk": ".primaryKey()" in part,
                   "nn": ".notNull()" in part or ".primaryKey()" in part, "ref": ref.group(1) if ref else None}
            cols.append(col)
            by_prop[cm.group(1)] = col
        # третий аргумент pgTable: составной первичный ключ
        end = _match(src, src.index("(", m.start()), "(", ")")
        for pk in re.finditer(r"primaryKey\(\{\s*columns:\s*\[([^\]]*)\]", src[b:end]):
            for prop in re.findall(r"\w+\.(\w+)", pk.group(1)):
                if prop in by_prop:
                    by_prop[prop]["pk"] = by_prop[prop]["nn"] = True
        out[var] = {"table": table, "cols": cols}
    n = len(re.findall(r"=\s*pgTable\(", src))
    assert len(out) == n, f"разобрано {len(out)} таблиц из {n} — разборщик отстал от синтаксиса схемы"
    return out


def fork_commit(fork: Path) -> str:
    r = subprocess.run(["git", "-C", str(fork), "log", "-1", "--format=%H", "--", REL], capture_output=True, text=True)
    return r.stdout.strip()


def main():
    fork = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT
    data = {}
    for f in FILES:
        data.update(parse((fork / REL / f).read_text(encoding="utf-8")))
    (HERE / "icplan_schema.json").write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    meta = {"source": REL, "commit": fork_commit(fork), "tables": len(data)}
    (HERE / "icplan_schema.meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"таблиц {len(data)}, коммит {meta['commit'][:8]}")


if __name__ == "__main__":
    main()
