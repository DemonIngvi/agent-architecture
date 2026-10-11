"""Схемы architecture.md спек define-agent-platform из components.py и R&D (правило: docs/rules/change-process.md). Запуск: python html-view/archgen.py"""
import sys, re, os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from components import BLOCKS, BY_SLUG, B, Z  # noqa
from rationale import RATIONALE, REFS  # noqa

ROOT = str(Path(__file__).resolve().parent.parent).replace("\\", "/") + "/"
CAP = {"agent-runner": "agent-runner", "agent-sandbox": "sandbox", "agent-harness": "harness", "agent-memory": "memory",
       "tool-integration": "mcp-tools", "guardrails": "guardrails", "llm-gateway": "llm-gateway", "observability": "observability",
       "control-plane": "platform-module", "agent-registry": "icplan"}
REGISTRY = [
    [B("Control Plane UI", "настройка агентов", "ext", to="icplan"), B("Platform module", "наши настройки", "ext", to="platform-module")],
    "↓ сохранение",
    Z("Registry (БД ICPlan)", [
        [B("Агенты", "", "core", "done"), B("Тулы и навыки", "", "core", "done"), B("MCP-серверы", "", "core", "done")],
        [B("Ключи провайдеров", "→ LiteLLM", "core", "part"), B("Версии агента", "", "core", "todo"), B("Экспорт / импорт YAML", "", "core", "todo")],
    ]),
    "↓ определение агента",
    [B("Agent Runner", "", "ext", to="agent-runner"), B("Harness", "", "ext", to="harness")],
]
MARK = {"done": "✓", "part": "~", "todo": "·", "": ""}
W = 76


def box_row(blocks, width):
    n = len(blocks)
    base = (width - 2 * (n - 1)) // n
    rest = width - 2 * (n - 1) - base * n
    top, mid, bot = [], [], []
    for k, b in enumerate(blocks):
        bw = base + (rest if k == n - 1 else 0)
        mark = MARK.get(b["st"], "")
        title = (("↗ " if b["kind"] == "ext" else "") + b["title"] + (f" [{b['g']}]" if b["g"] else "") + (f" {mark}" if mark else ""))
        if b["kind"] == "back":
            title += " (бэклог)"
        title = title[: bw - 4]
        top.append("┌" + "─" * (bw - 2) + "┐")
        mid.append("│ " + title.ljust(bw - 4) + " │")
        bot.append("└" + "─" * (bw - 2) + "┘")
    return ["  ".join(top), "  ".join(mid), "  ".join(bot)]


def render(rows, width=W, indent=""):
    out = []
    for r in rows:
        if isinstance(r, str):
            out.append(indent + r.center(width).rstrip())
        elif isinstance(r, dict):
            title = f" {r['zone']}" + (f" [{r['g']}]" if r.get("g") else "") + " "
            out.append(indent + "┌─" + title + "─" * (width - 3 - len(title)) + "┐")
            for line in render(r["rows"], width - 4, ""):
                out.append(indent + "│ " + line.ljust(width - 4) + " │")
            out.append(indent + "└" + "─" * (width - 2) + "┘")
        else:
            out += [indent + l for l in box_row(r, width)]
    return out


def blocks_of(rows):
    for r in rows:
        if isinstance(r, dict):
            yield from blocks_of(r["rows"])
        elif isinstance(r, list):
            yield from r


def rnd_minus(slug):
    for _, p in REFS.get(slug, []):
        if p.startswith("docs/rnd/"):
            t = open(ROOT + p, encoding="utf-8").read()
            if "**Риски и пересмотр**" in t:  # R&D v3.1: карточка рисков
                seg = t.split("**Риски и пересмотр**", 1)[1].split("</div>", 1)[0]
                return [l[2:].strip() for l in seg.splitlines() if l.startswith("- ")], p
            if "**Минусы и риски**" in t:
                seg = t.split("**Минусы и риски**", 1)[1].split("## ", 1)[0]
                return [l[2:].strip() for l in seg.splitlines() if l.startswith("- ")], p
    return [], None


ST = {"done": "✅ есть", "part": "⚠️ частично", "todo": "⬜ не начато", "": "—"}
for cap, slug in CAP.items():
    rows = REGISTRY if cap == "agent-registry" else BLOCKS[slug]
    name = "Registry (ICPlan)" if cap == "agent-registry" else BY_SLUG[slug][1]
    L = [f"# {cap} — схема", "", "← [spec.md](spec.md)", "",
         "Схема в формате [FORMAT.md](../../../../../FORMAT.md). Легенда: ✓ есть · ~ частично · · не начато · ↗ соседний компонент.", "",
         "## Схема", "", "```"] + render(rows) + ["```", "",
         "## Блоки", "", "| Блок | Задача | Статус |", "|---|---|---|"]
    seen = set()
    for b in blocks_of(rows):
        if b["kind"] in ("ext", "user") or b["title"] in seen:
            continue
        seen.add(b["title"])
        st = "бэклог" if b["kind"] == "back" else ST.get(b["st"], "—")
        L.append(f"| {b['title']} | {b['desc'] or '—'} | {st} |")
    cfg = RATIONALE.get(slug, {}).get("config", [])
    if cfg:
        L += ["", "## Расширения и настройка", "", "```"]
        L += [f"{n:<34} → {e}" for n, _, e, _, _ in cfg[:8]]
        L += ["```"]
    minus, p = rnd_minus(slug)
    plus = RATIONALE.get(slug, {}).get("gain", [])
    if plus or minus:
        L += ["", "## Плюсы / минусы", "", "| ➕ | ➖ |", "|---|---|"]
        for i in range(max(len(plus), len(minus))):
            a = plus[i] if i < len(plus) else ""
            b = minus[i] if i < len(minus) else ""
            L.append(f"| {a} | {b.replace('**', '')} |")
        if p:
            L += ["", f"Обоснование: [R&D](../../../../../{p})."]
    out = (os.environ["OUTDIR"] + f"/{cap}.md") if os.environ.get("OUTDIR") else ROOT + f"openspec/changes/define-agent-platform/specs/{cap}/architecture.md"
    open(out, "w", encoding="utf-8", newline=chr(10)).write("\n".join(L) + "\n")
    print(cap, len(L))
