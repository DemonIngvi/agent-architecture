"""Подтверждения документов ролями (docs/rules/approval-methodology.md).

Реестр `docs/approvals.md`: строка на пару «документ × роль». Сборка добавляет ⏳ для обязательных пар и сбрасывает решение,
если текст страницы изменился (версия — хэш текста). Решение ставит роль: `./tools/doc approve <страница> <буква> ok|no "<комментарий>"`.
Спеки подтверждаются по требованиям (`approvals.md` рядом со спекой) — значок спеки собирается из них.
"""
import datetime
import fnmatch
import hashlib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REGISTRY = ROOT / "docs/approvals.md"

# Буква → роль (docs/rules/roles.md). Буквы уникальны: значок — один символ.
ROLES = {
    "В": "Владелец продукта", "А": "Архитектор", "Р": "Разработчик", "Т": "Тестировщик", "И": "Аналитик историй",
    "П": "Пользователь", "Н": "Администратор (настройки)", "Д": "DevOps-инженер", "Б": "Безопасность", "С": "Инженер сборки и поставки",
}
BY_NAME = {v: k for k, v in ROLES.items()} | {"Администратор": "Н"}

# Тип документа (страница сайта) → роли, которые подтверждают. Порядок: первое совпадение.
RULES = [
    ("Главная", "index.md", "АВ"),
    ("Блок", "components/*/*/index.md", "АРТ"),
    ("Архитектура компонента", "components/*/index.md", "АР"),
    ("Интеграции", "docs/api/*.md", "АРТ"),
    ("Данные", "data-by-component/*/index.md", "АРД"),
    ("Deploy", "docs/techspec/*.md", "СДБ"),
    ("User Stories", "docs/stories/*.md", "ИПВ"),
    ("Задача", "docs/tasks/*.md", "РТВ"),
    ("R&D", "docs/rnd/*.md", "ВА"),
    ("Решения (design)", "openspec/changes/*/design.md", "ВА"),
    ("Методология", "docs/rules/*-methodology.md", "ВА"),
    ("Методология", "docs/rules/tech-spec.md", "ВА"),
]
SKIP = {"docs/api/README.md", "docs/stories/README.md", "docs/stories/personas.md", "docs/stories/coverage.md", "docs/rnd/README.md",
        "docs/techspec/README.md", "docs/rnd/consequences.md"}
HEAD = "| Документ | Роль | Кто | 👤 / 🤖 | Дата | Решение | Версия | Комментарий |"


def rule_of(page: str):
    if page in SKIP:
        return None
    return next(((n, roles) for n, pat, roles in RULES if fnmatch.fnmatch(page, pat) and page.count("/") == pat.count("/")), None)


def version(text: str) -> str:
    """Хэш смысла страницы: без шкал готовности и пробелов (они меняются без правки текста)."""
    t = re.sub(r'<span class="rd"[^>]*>.*?</b></span>', "", text, flags=re.S)
    t = re.sub(r"\s+", " ", t)
    return hashlib.sha1(t.encode("utf-8")).hexdigest()[:8]


def read_registry() -> dict:
    rows = {}
    if REGISTRY.exists():
        for l in REGISTRY.read_text(encoding="utf-8").splitlines():
            if l.startswith("| `"):
                c = [x.strip() for x in l.strip().strip("|").split("|")]
                rows[(c[0].strip("`"), c[1])] = c
    return rows


def write_registry(rows: dict):
    body = ["# Подтверждения документов", "",
            "← [Методология подтверждений](rules/approval-methodology.md) · [сводная таблица](approvals-summary.md)", "",
            "Реестр ведёт сборка и `./tools/doc approve`; руками не правится. ⏳ — ждёт роли; ✅ — подтверждено; ❌ — отказ (причина в комментарии); "
            "решение сбрасывается в ⏳, если текст документа изменился (столбец «Версия»).", "", HEAD, "|---|---|---|---|---|---|---|---|"]
    order = list(ROLES)
    for k in sorted(rows, key=lambda k: (k[0], order.index(k[1]) if k[1] in order else 99)):
        body.append("| " + " | ".join(rows[k]) + " |")
    REGISTRY.write_text("\n".join(body) + "\n", encoding="utf-8", newline="\n")


def sync(src: Path) -> dict:
    """Строки ⏳ для обязательных пар, сброс по изменённому тексту; → {страница: [(буква, роль, состояние, кто)]}."""
    rows = read_registry()
    status, seen = {}, set()
    for f in sorted(src.rglob("*.md")):
        page = f.relative_to(src).as_posix()
        r = rule_of(page)
        if not r:
            continue
        text = f.read_text(encoding="utf-8")
        if "у владельца: блок [" in text:  # страница-ссылка хоста на встроенный блок: описания нет, подтверждать нечего
            continue
        ver = version(text)
        for letter in r[1]:
            key = (page, letter)
            seen.add(key)
            c = rows.get(key) or [f"`{page}`", letter, "—", "—", "—", "⏳", ver, r[0]]
            if c[6] != ver and c[5] != "⏳":
                c = [f"`{page}`", letter, "—", "—", "—", "⏳", ver, f"текст изменён после решения «{c[5]}» от {c[2]}"]
            c[6] = ver
            rows[key] = c
            status.setdefault(page, []).append((letter, ROLES[letter], c[5], c[3]))
    rows = {k: v for k, v in rows.items() if k in seen}  # документ удалён или правило изменилось
    write_registry(rows)
    # спеки: значок из подтверждений требований
    for f in ROOT.glob("openspec/changes/*/specs/*/approvals.md"):
        page = f.relative_to(ROOT).as_posix().replace("approvals.md", "spec.md")
        per = {}
        for l in f.read_text(encoding="utf-8").splitlines():
            if l.startswith("| R-"):
                c = [x.strip() for x in l.strip().strip("|").split("|")]
                letter = BY_NAME.get(c[1])
                if letter:
                    per.setdefault(letter, []).append(c[5])
        st = []
        for letter in ROLES:
            if letter in per:
                v = per[letter]
                s = "❌" if "❌" in v else ("✅" if all(x == "✅" for x in v) else "⏳")
                st.append((letter, ROLES[letter] + f" (требований: {len(v)})", s, ""))
        if st:
            status[page] = st
    return status


def summary_md(status: dict) -> str:
    """Сводная таблица: документ × роли (страница «Подтверждения документов»)."""
    letters = list(ROLES)
    used = [x for x in letters if any(x == s[0] for v in status.values() for s in v)]
    L = ["# Подтверждения документов", "",
         "← [Методология подтверждений](rules/approval-methodology.md) · [реестр](approvals.md)", "",
         "Кто из ролей подтвердил документ: ✅ — подтвердил, ❌ — отказ, ⏳ — ждёт, пусто — роль этот тип не подтверждает. "
         "Роли: " + ", ".join(f"**{x}** — {ROLES[x]}" for x in used) + ".", ""]
    total = sum(1 for v in status.values() for s in v)
    ok = sum(1 for v in status.values() for s in v if s[2] == "✅")
    L += [f"Подтверждено {ok} из {total} пар «документ × роль»; документов полностью подтверждено: "
          f"{sum(1 for v in status.values() if all(s[2] == '✅' for s in v))} из {len(status)}.", ""]
    L += ["| Документ | " + " | ".join(used) + " | Готов |", "|---|" + "---|" * len(used) + "---|"]
    for page in sorted(status):
        st = {s[0]: s[2] for s in status[page]}
        L.append(f"| [{page}](../{page}) | " + " | ".join(st.get(x, "") for x in used) + f" | {'✅' if all(v == '✅' for v in st.values()) else ''} |")
    return "\n".join(L) + "\n"


def set_decision(page: str, letter: str, ok: bool, comment: str, who: str = "", human: bool = False) -> str:
    """Решение роли по документу (`doctool approve`)."""
    rows = read_registry()
    letter = BY_NAME.get(letter, letter)
    key = (page, letter)
    if key not in rows:
        raise SystemExit(f"нет строки «{page} × {letter}»: соберите сайт (python html-view/build.py) или проверьте путь страницы")
    c = rows[key]
    c[2] = who or (f"Claude, роль {ROLES[letter]}" if not human else ROLES[letter])
    c[3] = "👤" if human else "🤖"
    c[4] = datetime.date.today().isoformat()
    c[5] = "✅" if ok else "❌"
    c[7] = comment.replace("|", "/") or "—"
    write_registry(rows)
    return f"{page} × {letter} ({ROLES[letter]}): {c[5]}"


def queue(letter: str = "") -> list:
    """Что ждёт решения роли (`doctool review-queue`)."""
    letter = BY_NAME.get(letter, letter)
    return [(k[0], k[1]) for k, c in read_registry().items() if c[5] == "⏳" and (not letter or k[1] == letter)]
