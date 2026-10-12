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
CLASSES = [
    "  classDef done fill:#e8f5e9,stroke:#2e7d32,color:#1b5e20",
    "  classDef part fill:#fff8e1,stroke:#f9a825,color:#5d4037",
    "  classDef todo fill:#f5f5f5,stroke:#9e9e9e,color:#424242",
    "  classDef ext fill:#fff3e0,stroke:#ef6c00,color:#e65100,stroke-dasharray:4 3",
    "  classDef user fill:#e3f2fd,stroke:#1565c0,color:#0d47a1",
    "  classDef store fill:#ede7f6,stroke:#5e35b1,color:#311b92",
    "  classDef back fill:#fafafa,stroke:#bdbdbd,color:#9e9e9e,stroke-dasharray:2 2",
    "  classDef zone fill:#fafafa,stroke:#9fa8da,color:#1a237e",
]


def _q(s):
    return s.replace('"', "'")


def mermaid_c3(rows):
    """C3 — устройство компонента (FORMAT.md): зона — подграф; ряд блоков — один уровень (невидимые связи ~~~);
    подпись потока — одна стрелка между рядами."""
    n = [0]
    out = []

    def node(b):
        n[0] += 1
        i = f"b{n[0]}"
        title = b["title"] + (f" [{b['g']}]" if b["g"] else "") + (" (бэклог)" if b["kind"] == "back" else "")
        lab = f"<b>{_q(title)}</b>" + (f"<br/><small>{_q(b['desc'])}</small>" if b["desc"] else "")
        shape = {"store": ('[("', '")]'), "user": ('(["', '"])')}.get(b["kind"], ('["', '"]'))
        cls = b["kind"] if b["kind"] in ("ext", "user", "store", "back") else (b["st"] or "todo")
        return i, f"{i}{shape[0]}{lab}{shape[1]}:::{cls}"

    def walk(rs, ind):
        """→ (узлы первого ряда, узлы последнего ряда)."""
        first, prev, label = None, None, ""
        for r in rs:
            if isinstance(r, str):
                label = r.strip(" ↓↑")
                continue
            if isinstance(r, dict):
                n[0] += 1
                out.append(f'{ind}subgraph z{n[0]}["{_q(r["zone"])}' + (f' [{r["g"]}]' if r.get("g") else "") + '"]')
                zid = f"z{n[0]}"
                top, bottom = walk(r["rows"], ind + "  ")
                out.append(f"{ind}end")
                out.append(f"{ind}class {zid} zone")
            else:
                ids = []
                for blk in r:
                    i, line = node(blk)
                    out.append(ind + line)
                    ids.append(i)
                top = bottom = ids
            if prev and top:
                out.append(f'{ind}{prev[0]} -->|"{_q(label)}"| {top[0]}' if label else f"{ind}{prev[0]} --> {top[0]}")
                out.extend(f"{ind}{prev[0]} ~~~ {x}" for x in top[1:])  # тот же уровень для всего ряда
            first = first or top
            prev, label = bottom, ""
        return first or [], prev or []

    walk(rows, "  ")
    return ["```mermaid", "flowchart TB", *CLASSES, *out, "```"]


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
         "Схема C3 по [FORMAT.md](../../../../../FORMAT.md). Цвет: зелёный — есть, жёлтый — частично, серый — не начато; оранжевый пунктир — соседний компонент.", "",
         "## Схема", ""] + mermaid_c3(rows) + ["",
         "## Блоки", "", "| Блок | Задача | Статус |", "|---|---|---|"]
    seen = set()
    for b in blocks_of(rows):
        if b["kind"] in ("ext", "user") or b["title"] in seen:
            continue
        seen.add(b["title"])
        st = "бэклог" if b["kind"] == "back" else ST.get(b["st"], "—")
        L.append(f"| {b['title']} | {b['desc'] or '—'} | {st} |")
    L += ["", "## Настройка", "", "Параметры модуля — [interfaces.md](interfaces.md) (раздел «Параметры модуля»); на сайте — вкладка «Deploy» компонента, раздел «Конфигурация»."]
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
