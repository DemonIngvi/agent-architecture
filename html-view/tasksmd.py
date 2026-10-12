"""Генерация tasks.md изменений OpenSpec из ROADMAP и документов задач (правило: docs/rules/change-process.md, О-39).

define-agent-platform/tasks.md — все задачи ROADMAP; add-icplan-integration/tasks.md — задачи с требованиями R-ICP.
Запуск: python html-view/tasksmd.py (из корня репозитория или откуда угодно).
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ARCHIVE_NOTE = ("Change архивируется (`openspec archive`) после реализации и приёмки его задач — тогда спеки становятся действующими "
                "в `openspec/specs/` ([правило](../../../docs/rules/change-process.md#archive)).")


def roadmap():
    """[(этап, [(id, title, file, reqs)])] по ROADMAP."""
    t = (ROOT / "docs/ROADMAP.md").read_text(encoding="utf-8")
    stages, cur = [], None
    for line in t.splitlines():
        m = re.match(r"^## Этап (\d)\. (.+)$", line)
        if m:
            cur = (m.group(1), m.group(2), [])
            stages.append(cur)
            continue
        m = re.match(r"^\| (\d\.\d) \| (.+?) \| (.*?) \|", line)
        if m and cur:
            title_cell = m.group(2)
            lm = re.search(r"\[([^\]]+)\]\(tasks/([^)]+)\)", title_cell)
            title = re.sub(r"~~|\s*—\s*\[закрыта\].*", "", lm.group(1) if lm else title_cell).strip()
            closed = "закрыта" in title_cell
            reqs = re.findall(r"R-[A-Z]+-\d+", m.group(3))
            cur[2].append((m.group(1), title, lm.group(2) if lm else "", reqs, closed))
    return stages


def why(file):
    p = ROOT / "docs/tasks" / file
    if not file or not p.exists():
        return ""
    t = p.read_text(encoding="utf-8")
    m = re.search(r"^## Зачем\s*\n+(.+?)(?:\n\n|\n##)", t, re.S | re.M)
    if not m:
        return ""
    s = re.split(r"(?<=[.!?])\s", m.group(1).strip().replace("\n", " "))[0]
    return re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", s)  # ссылки задачи относительны docs/tasks — в tasks.md изменения только текст


def render(title, header, stages, keep):
    L = ["# Tasks", "", header, ""]
    for num, name, rows in stages:
        rows = [r for r in rows if keep(r)]
        if not rows:
            continue
        L += [f"## {num}. {name}", ""]
        for tid, ttl, f, reqs, closed in rows:
            if closed:
                L.append(f"- [x] {tid} ~~{ttl}~~ — закрыта. Подробно: [docs/tasks/{f}](../../../docs/tasks/{f})")
                continue
            w = why(f)
            rq = ", ".join(reqs[:6]) + (" и др." if len(reqs) > 6 else "")
            L.append(f"- [ ] {tid} {ttl}" + (f": {w}" if w else "") + (f" Требования: {rq}." if rq else "")
                     + f" Подробно: [docs/tasks/{f}](../../../docs/tasks/{f})")
        L.append("")
    L += ["## Архивация", "", ARCHIVE_NOTE, ""]
    return "\n".join(L)


def main():
    st = roadmap()
    hdr = ("← [proposal](proposal.md) · [ROADMAP](../../../docs/ROADMAP.md) · [сводная таблица](../../../docs/TASKS.md)\n\n"
           "Задачи по этапам ROADMAP; файл собирается из ROADMAP (`html-view/tasksmd.py`). Подробности, INVEST, оценки и приёмка — в документе задачи. "
           "Задачи процесса ICPlan детализированы также в [icplan-agent-autopickup](../icplan-agent-autopickup/tasks.md).")
    (ROOT / "openspec/changes/define-agent-platform/tasks.md").write_text(render("", hdr, st, lambda r: True), encoding="utf-8", newline="\n")
    hdr2 = ("← [proposal](proposal.md) · [спека](specs/icplan-integration/spec.md) · [ROADMAP](../../../docs/ROADMAP.md)\n\n"
            "Задачи ROADMAP, закрывающие требования `R-ICP-*`; файл собирается из ROADMAP (`html-view/tasksmd.py`). "
            "Общий список — [define-agent-platform](../define-agent-platform/tasks.md).")
    (ROOT / "openspec/changes/add-icplan-integration/tasks.md").write_text(
        render("", hdr2, st, lambda r: any(x.startswith("R-ICP-") for x in r[3])), encoding="utf-8", newline="\n")


def check() -> list:
    """Сверка tasks.md с ROADMAP: каждая задача ROADMAP есть в define-agent-platform/tasks.md (О-39)."""
    ids = {r[0] for _, _, rows in roadmap() for r in rows}
    issues = []
    tm = ROOT / "openspec/changes/define-agent-platform/tasks.md"
    have = set(re.findall(r"^- \[[ x]\] (\d\.\d)", tm.read_text(encoding="utf-8"), re.M)) if tm.exists() else set()
    issues += [f"задача {i} из ROADMAP нет в define-agent-platform/tasks.md (python html-view/tasksmd.py)" for i in sorted(ids - have)]
    for ch in (ROOT / "openspec/changes").iterdir():
        if ch.is_dir() and ch.name != "archive" and not (ch / "tasks.md").exists():
            issues.append(f"у изменения {ch.name} нет tasks.md")
    return issues


if __name__ == "__main__":
    main()
    print("tasks.md собраны;", check() or "расхождений нет")
