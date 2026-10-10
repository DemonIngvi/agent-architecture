"""SVG-диаграммы для сайта: процессы в нотации BPMN и граф связности документов."""
import html

LANE_H, COL_W, LABEL_W = 92, 128, 118


def _wrap(s: str, n: int = 16) -> list:
    words, lines, cur = s.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > n and cur:
            lines.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    return lines + ([cur] if cur else [])


def bpmn_svg(proc: dict, artifacts: dict = None) -> str:
    artifacts = artifacts or {}
    lanes, steps = proc["lanes"], proc["steps"]
    col = {s[0]: i for i, s in enumerate(steps)}
    pos = {s[0]: (LABEL_W + col[s[0]] * COL_W + COL_W / 2, s[1] * LANE_H + LANE_H / 2) for s in steps}
    W, H = LABEL_W + len(steps) * COL_W + 10, len(lanes) * LANE_H + 30
    out = [f'<svg class="bpmn" viewBox="0 0 {W} {H}" width="100%" xmlns="http://www.w3.org/2000/svg">',
           '<defs><marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
           '<path d="M0,0 L10,5 L0,10 z" class="b-arrow"/></marker></defs>']
    for i, ln in enumerate(lanes):
        y = i * LANE_H
        out.append(f'<rect x="0" y="{y}" width="{W}" height="{LANE_H}" class="b-lane{i % 2}"/>')
        out.append(f'<rect x="0" y="{y}" width="{LABEL_W - 8}" height="{LANE_H}" class="b-lanehead"/>')
        for k, line in enumerate(_wrap(ln, 14)):
            out.append(f'<text x="{(LABEL_W - 8) / 2}" y="{y + LANE_H / 2 - 6 + k * 13}" class="b-lanetext">{html.escape(line)}</text>')
    half = {"task": 52, "gateway": 20, "start": 15, "end": 15, "error": 15}
    for sid, lane, typ, label, nxt in steps:
        x1, y1 = pos[sid]
        for tgt, lab in nxt:
            x2, y2 = pos[tgt]
            ttyp = next(s[2] for s in steps if s[0] == tgt)
            if col[tgt] > col[sid]:
                sx, ex = x1 + half[typ], x2 - half[ttyp]
                d = f"M{sx},{y1} C{sx + 35},{y1} {ex - 35},{y2} {ex},{y2}"
                lx, ly = (sx + ex) / 2, (y1 + y2) / 2 - 5
            else:
                base = len(lanes) * LANE_H + 18
                d = f"M{x1},{y1 + 20} C{x1},{base} {x2},{base} {x2},{y2 + 20}"
                lx, ly = (x1 + x2) / 2, base - 4
            out.append(f'<path d="{d}" class="b-flow" marker-end="url(#ar)"/>')
            if lab:
                out.append(f'<text x="{lx}" y="{ly}" class="b-flowtext">{html.escape(lab)}</text>')
    for sid, lane, typ, label, nxt in steps:
        x, y = pos[sid]
        lines = _wrap(label)
        if typ == "task":
            out.append(f'<rect x="{x - 52}" y="{y - 24}" width="104" height="48" rx="9" class="b-task"/>')
            ty = y - (len(lines) - 1) * 6.5 + 4
        elif typ == "gateway":
            out.append(f'<path d="M{x},{y - 20} L{x + 20},{y} L{x},{y + 20} L{x - 20},{y} z" class="b-gw"/>'
                       f'<text x="{x}" y="{y + 5}" class="b-gwx">×</text>')
            ty = y - 26 - (len(lines) - 1) * 13
        else:
            cls = {"start": "b-start", "end": "b-end", "error": "b-error"}[typ]
            out.append(f'<circle cx="{x}" cy="{y}" r="15" class="{cls}"/>')
            if typ == "error":
                out.append(f'<text x="{x}" y="{y + 5}" class="b-gwx">⚡</text>')
            ty = y + 30
        for k, line in enumerate(lines):
            out.append(f'<text x="{x}" y="{ty + k * 13}" class="b-text">{html.escape(line)}</text>')
        arts = artifacts.get(sid, [])
        if arts:
            ay = (y + 36) if typ == "task" else (ty + len(lines) * 13 + 2)
            label = "📄 " + ", ".join(arts)
            out.append(f'<text x="{x}" y="{ay}" class="b-art">{html.escape(label if len(label) < 34 else label[:32] + "…")}<title>{html.escape(", ".join(arts))}</title></text>')
    out.append("</svg>")
    legend = ('<div class="b-legend"><span><i class="lg lg-start"></i>начало</span><span><i class="lg lg-task"></i>задача</span>'
              '<span><i class="lg lg-gw"></i>развилка</span><span><i class="lg lg-end"></i>конец</span><span><i class="lg lg-err"></i>ошибка</span></div>')
    return '<div class="bpmn-wrap">' + "".join(out) + legend + "</div>"


def graph_svg(layers: list, edges: list) -> str:
    """layers: [(подпись слоя, [узлы])]; edges: [(от, к, подпись)]."""
    NW, NH, GX, GY = 150, 38, 60, 18
    pos = {}
    maxn = max(len(n) for _, n in layers)
    H = maxn * (NH + GY) + 40
    W = len(layers) * (NW + GX)
    out = [f'<svg class="dgraph" viewBox="0 0 {W} {H}" width="100%" xmlns="http://www.w3.org/2000/svg">',
           '<defs><marker id="ga" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L10,5 L0,10 z" class="b-arrow"/></marker></defs>']
    for li, (lab, nodes) in enumerate(layers):
        x = li * (NW + GX) + 10
        out.append(f'<text x="{x + NW / 2}" y="16" class="g-layer">{html.escape(lab)}</text>')
        off = (maxn - len(nodes)) * (NH + GY) / 2
        for ni, n in enumerate(nodes):
            y = 30 + off + ni * (NH + GY)
            pos[n] = (x, y)
    for a, b, lab in edges:
        (xa, ya), (xb, yb) = pos[a], pos[b]
        if xb > xa:
            sx, sy, ex, ey = xa + NW, ya + NH / 2, xb, yb + NH / 2
            d = f"M{sx},{sy} C{sx + 30},{sy} {ex - 30},{ey} {ex},{ey}"
        else:
            sx, sy, ex, ey = xa + NW / 2, ya + NH, xb + NW / 2, yb + NH
            d = f"M{sx},{sy} C{sx},{sy + 40} {ex},{ey + 40} {ex},{ey}"
        out.append(f'<path d="{d}" class="g-edge" marker-end="url(#ga)"><title>{html.escape(a + " → " + b + (": " + lab if lab else ""))}</title></path>')
    for n, (x, y) in pos.items():
        out.append(f'<rect x="{x}" y="{y}" width="{NW}" height="{NH}" rx="8" class="g-node"/>')
        for k, line in enumerate(_wrap(n, 20)):
            out.append(f'<text x="{x + NW / 2}" y="{y + 16 + k * 12}" class="b-text">{html.escape(line)}</text>')
    out.append("</svg>")
    return '<div class="bpmn-wrap">' + "".join(out) + "</div>"
