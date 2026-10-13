"""Учёт расхода токенов по процессам методологии: журнал data/costs.yaml → сводка и docs/rules/token-costs.md.

Команды (через doctool):
    cost                                   сводка по процессам (последний замер на единицу против ожидания)
    cost add <процесс> <токены|-> <единиц> <единица> [--agents id,id] [--model M] [--min N] [--expect a-b] [--note ...]
                                           [--method путь#якорь] [--date ГГГГ-ММ-ДД]
                                           с --agents токены («-») и число вызовов берутся из журналов агентов (from-transcript)
    cost md                                сгенерировать docs/rules/token-costs.md (вызывается из build.py)
    cost from-transcript <agentId>…        фактический расход агента по журналу вызовов (сумма по message.id)
    cost agents [сессия]                   все агенты сессий: вызовы, сумма, итоговый контекст, описание
Токены: 409000, 409k или сумма 84.9k+68.6k; --expect: «2-4» (тыс.), «150k-250k», «2000-4000» (токены на единицу).
Статус ✅ — замер на единицу в [min/2, max*2] (допуск ±2×), иначе ⚠️. Методология: docs/rules/token-costs.md#measure.
"""
import re
import sys
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import yamldata as Y  # noqa: E402

ROOT = HERE.parent
FILE = Y.DATA / "costs.yaml"
PAGE = ROOT / "docs/rules/token-costs.md"
# человекочитаемые названия процессов (код процесса латиницей = якорь на странице)
TITLES = {
    "review-pack": "Проверка ролями (пакет review-pack)",
    "bulk-edit": "Партия правок компонента по замечаниям",
    "lint-conversion": "Перевод отказов в lint",
    "yaml-migration": "Перенос данных в YAML",
    "rules-transfer": "Перенос правил в методологию и «Справку»",
    "unit-read": "Чтение единицы для правки",
}


def load() -> list:
    if not FILE.exists():
        return []
    v, errs = Y.load_unit(FILE, "costs")
    if errs:
        raise SystemExit("data/costs.yaml: " + "; ".join(errs[:5]) + " (doctool yaml-check)")
    return v["costs"]


def per_unit(r) -> float:
    return r["tokens"] / r["units"]


def status(r) -> str:
    e = r.get("expected")
    if not e:
        return "—"
    pu = per_unit(r)
    return "✅" if e[0] / 2 <= pu <= e[1] * 2 else "⚠️ расхождение >2×"


def fmt_n(n) -> str:
    n = float(n)
    return f"{n:.0f}" if n < 1000 else f"{n / 1000:.1f}".replace(".", ",") + " тыс."


def fmt_exp(e) -> str:
    return f"{fmt_n(e[0])} – {fmt_n(e[1])}" if e else "—"


def by_process(rows) -> dict:
    out = {}
    for r in sorted(rows, key=lambda r: r["date"]):  # стабильно: внутри даты — порядок в файле
        out.setdefault(r["process"], []).append(r)
    return out


def parse_tokens(s: str) -> int:
    total = 0
    for part in s.replace(",", ".").split("+"):
        m = re.fullmatch(r"\s*([\d.]+)\s*(k|к|тыс)?\s*", part)
        if not m:
            raise SystemExit(f"токены «{s}»: нужно число, 409k или сумма 84.9k+68.6k")
        total += float(m.group(1)) * (1000 if m.group(2) else 1)
    return round(total)


def parse_expect(s: str) -> list:
    m = re.fullmatch(r"\s*([\d.]+)\s*(k|к)?\s*[-–]\s*([\d.]+)\s*(k|к)?\s*", s.replace(",", "."))
    if not m:
        raise SystemExit(f"--expect «{s}»: нужно a-b, например 2-4 (тыс.) или 150k-250k")
    lo, hi = float(m.group(1)), float(m.group(3))
    k = bool(m.group(2) or m.group(4)) or hi < 1000
    return [round(lo * (1000 if k else 1)), round(hi * (1000 if k else 1))]


def add(args) -> str:
    opts, pos, i = {}, [], 0
    while i < len(args):
        a = args[i]
        if a in ("--model", "--min", "--expect", "--note", "--method", "--date", "--agents"):
            j = i + 1
            while j < len(args) and not args[j].startswith("--"):
                j += 1
            opts[a[2:]] = " ".join(args[i + 1:j])
            i = j
        else:
            pos.append(a)
            i += 1
    if len(pos) < 4:
        raise SystemExit("cost add <процесс> <токены> <единиц> <единица> [--model M] [--min N] [--expect a-b] [--note …] [--method путь#якорь]")
    ids = [x for x in re.split(r"[,\s]+", opts.get("agents", "")) if x]
    us = [transcript_usage(agent_file(x)) for x in ids]
    tokens = sum(u["total"] for u in us) if ids else parse_tokens(pos[1])
    proc, units, unit = pos[0], int(pos[2]), " ".join(pos[3:])
    rows = load()
    prev = [r for r in rows if r["process"] == proc]
    method = opts.get("method") or (prev[-1]["methodology"] if prev else "")
    if not method:
        raise SystemExit(f"новый процесс {proc}: укажи --method путь#якорь (файл в docs/rules)")
    rec = {"date": opts.get("date", date.today().isoformat()), "process": proc, "methodology": method, "units": units, "unit": unit, "tokens": tokens}
    if "model" in opts:
        rec["model"] = opts["model"]
    if "min" in opts:
        rec["minutes"] = int(opts["min"])
    if "expect" in opts:
        rec["expected"] = parse_expect(opts["expect"])
    elif prev and prev[-1].get("expected"):
        rec["expected"] = prev[-1]["expected"]
    if ids:
        rec["agents"], rec["calls"], rec["context"] = ids, sum(u["calls"] for u in us), sum(u["last"] for u in us)
        rec.setdefault("model", us[0]["model"].removeprefix("claude-"))
    if "note" in opts:
        rec["note"] = opts["note"]
    Y.write_unit(FILE, "costs", {"costs": rows + [rec]})
    iss = Y.check(str(FILE))
    if iss:
        raise SystemExit("\n".join(iss))
    return f"{proc}: {fmt_n(tokens)} / {units} {unit} = {fmt_n(tokens / units)} на единицу — {status(rec)}"


def summary() -> str:
    L = ["| процесс | единица | ожидание на единицу | последний замер на единицу | статус | дата |", "|---|---|---|---|---|---|"]
    for p, rs in by_process(load()).items():
        r = rs[-1]
        L.append(f"| {p} | {r['unit']} | {fmt_exp(r.get('expected'))} | {fmt_n(per_unit(r))} | {status(r)} | {r['date']} |")
    return "\n".join(L)


def out_of_range() -> list:
    return [p for p, rs in by_process(load()).items() if status(rs[-1]).startswith("⚠️")]


def md() -> str:
    rows = load()
    procs = by_process(rows)
    L = ["# Расход токенов {#costs}", "",
         "← [Правила документации](README.md) · [методология подтверждений](approval-methodology.md) · [процесс изменения](change-process.md)", "",
         "Сколько токенов уходит на единицу работы по процессам методологии: ожидание, заявленное в методологии, против замера. "
         "Страница **генерируется** из `data/costs.yaml` (`python html-view/doctool.py cost md`, вызывается сборкой); править — журнал: "
         "`python html-view/doctool.py cost add …`, сводка — `doctool cost`.", "",
         "## Сводка", "",
         "| Процесс | Методология | Единица | Ожидание на единицу | Последний замер на единицу | Статус | Дата |", "|---|---|---|---|---|---|---|"]
    for p, rs in procs.items():
        r = rs[-1]
        m = r["methodology"]
        L.append(f"| [{TITLES.get(p, p)}](#{p}) | [{m}]({m}) | {r['unit']} | {fmt_exp(r.get('expected'))} | {fmt_n(per_unit(r))} | {status(r)} | {r['date']} |")
    L += ["", "## Как замерять {#measure}", "",
          "1. Расход агента — **сумма по всем вызовам модели** из журнала агента: input + запись кэша + чтение кэша + output по уникальным `message.id` "
          "(`python html-view/doctool.py cost from-transcript <agentId>`; в журнал — `cost add <процесс> - <единиц> <единица> --agents id,id`). "
          "`subagent_tokens` из отчёта о завершении — это **итоговый контекст** последнего вызова, а не расход: он занижает расход примерно в «число вызовов / 2» раз "
          "(хранится в поле `context` для сравнения). Делить на число единиц работы (пара документ × роль, документ, компонент, файл).",
          "2. Расход ≈ вызовы × средний контекст, поэтому главные рычаги — меньше вызовов (правки скриптом, потолок вызовов в брифе) и меньший контекст. "
          "Главный контекст оркестратора считается так же (`cost from-transcript <uuid сессии>`), отдельной строкой.",
          "3. Прерванные запуски в замер не входят; если расход известен только по завершённым частям, это отмечается в примечании.",
          "4. Допуск ±2×: замер на единицу в диапазоне от половины минимума до удвоенного максимума ожидания — ✅; иначе ⚠️ «расхождение >2×» — "
          "правят ожидание в методологии или процесс (что из этого — по причине расхождения).",
          "5. Цифры ожидания живут только в журнале: в методологиях — ссылка сюда, без повторения.", "",
          "## Замеры по процессам", ""]
    for p, rs in procs.items():
        r0 = rs[-1]
        L += [f"### {TITLES.get(p, p)} {{#{p}}}", "", f"Методология: [{r0['methodology']}]({r0['methodology']}).", "",
              "| Дата | Единиц | Единица | Токенов | На единицу | Вызовов | Итоговый контекст | Модель | Минут | Статус | Примечание |", "|---|---|---|---|---|---|---|---|---|---|---|"]
        for r in rs:
            ctx = fmt_n(r["context"]) if r.get("context") else "—"
            L.append(f"| {r['date']} | {r['units']} | {r['unit']} | {fmt_n(r['tokens'])} | {fmt_n(per_unit(r))} | {r.get('calls', '—')} | {ctx} | {r.get('model', '—')} | {r.get('minutes', '—')} | {status(r)} | {r.get('note', '')} |")
        L.append("")
    return "\n".join(L)


def write_md() -> bool:
    text = md()
    if PAGE.exists() and PAGE.read_text(encoding="utf-8") == text:
        return False
    PAGE.write_text(text, encoding="utf-8", newline="\n")
    return True


TRANSCRIPTS = Path.home() / ".claude/projects/d--"
USAGE_KEYS = ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens", "output_tokens")


def transcript_usage(path: Path) -> dict:
    """Сумма usage по уникальным message.id (одна запись на вызов модели; строки-блоки одного ответа дублируют usage)."""
    import json
    seen, tot, last, model = set(), dict.fromkeys(USAGE_KEYS, 0), 0, ""
    for line in path.read_text(encoding="utf-8").splitlines():
        try:
            m = json.loads(line).get("message") or {}
        except ValueError:
            continue
        u, mid = m.get("usage"), m.get("id")
        if not u or not mid or mid in seen:
            continue
        seen.add(mid)
        for k in USAGE_KEYS:
            tot[k] += u.get(k) or 0
        last = sum(u.get(k) or 0 for k in USAGE_KEYS)  # итоговый контекст ≈ subagent_tokens (старый замер)
        model = m.get("model", model)
    tot["calls"], tot["total"], tot["last"], tot["model"] = len(seen), sum(tot[k] for k in USAGE_KEYS), last, model
    return tot


def agent_files(session: str = "") -> list:
    return sorted(TRANSCRIPTS.glob(f"{session or '*'}/subagents/agent-*.jsonl"), key=lambda f: f.stat().st_mtime)


def agent_file(aid: str) -> Path:
    """Журнал агента по id или главной сессии по её uuid."""
    aid = aid.removeprefix("agent-")
    fs = list(TRANSCRIPTS.glob(f"*/subagents/agent-{aid}.jsonl")) or list(TRANSCRIPTS.glob(f"{aid}.jsonl"))
    if not fs:
        raise SystemExit(f"{aid}: журнал не найден ни в {TRANSCRIPTS}/*/subagents, ни как сессия")
    return fs[0]


def from_transcript(ids) -> str:
    L, grand = [], 0
    for aid in ids:
        t = transcript_usage(agent_file(aid))
        grand += t["total"]
        L.append(f"{aid}: {t['calls']} вызовов, всего {fmt_n(t['total'])} (чтение кэша {fmt_n(t['cache_read_input_tokens'])}, "
                 f"запись кэша {fmt_n(t['cache_creation_input_tokens'])}, вход {fmt_n(t['input_tokens'])}, выход {fmt_n(t['output_tokens'])}); "
                 f"итоговый контекст {fmt_n(t['last'])}; {t['model']}")
    if len(ids) > 1:
        L.append(f"итого: {grand} ({fmt_n(grand)}) — для cost add")
    return "\n".join(L)


def agents(session: str = "") -> str:
    import json
    L = ["| агент | описание | модель | вызовов | всего | итоговый контекст | дата |", "|---|---|---|---|---|---|---|"]
    for f in agent_files(session):
        meta = f.with_suffix(".meta.json")
        d = json.loads(meta.read_text(encoding="utf-8")).get("description", "") if meta.exists() else ""
        t = transcript_usage(f)
        from datetime import datetime
        L.append(f"| {f.stem.removeprefix('agent-')} | {d} | {t['model'].removeprefix('claude-')} | {t['calls']} | {fmt_n(t['total'])} | {fmt_n(t['last'])} | "
                 f"{datetime.fromtimestamp(f.stat().st_mtime):%m-%d %H:%M} |")
    return "\n".join(L)


def main(args) -> str:
    if not args:
        s = summary()
        bad = out_of_range()
        return s + ("\n\nвне ±2×: " + ", ".join(bad) if bad else "\n\nвсе замеры в пределах ±2×")
    if args[0] == "add":
        return add(args[1:])
    if args[0] == "md":
        return f"{PAGE.relative_to(ROOT).as_posix()}: " + ("обновлено" if write_md() else "без изменений")
    if args[0] == "from-transcript":
        return from_transcript(args[1:])
    if args[0] == "agents":
        return agents(args[1] if len(args) > 1 else "")
    raise SystemExit("cost [add …|md|from-transcript <agentId>…|agents [сессия]]")
