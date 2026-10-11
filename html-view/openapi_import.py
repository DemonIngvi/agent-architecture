"""Снимок OpenAPI работающего ICPlan (форк) в icplan_openapi.json — источник структуры существующих API.

    python html-view/openapi_import.py [URL]   # по умолчанию http://localhost:3000/docs/json

Сохраняются только пути и схемы (запрос, параметры, ответ 2xx) с развёрнутыми $ref,
версия API и коммит форка. Сборка показывает структуру эндпоинтов «✅ есть» из этого снимка
и сверяет статус «✅ есть» в каталоге API с наличием пути (О-45).
"""
import json
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).parent
URL = "http://localhost:3000/docs/json"


def _deref(node, comps, depth=0):
    if depth > 12:
        return {"type": "object"}
    if isinstance(node, dict):
        if isinstance(node.get("$ref"), str):
            name = node["$ref"].split("/")[-1]
            return _deref(comps.get(name, {}), comps, depth + 1)
        return {k: _deref(v, comps, depth + 1) for k, v in node.items() if k not in ("examples", "example")}
    if isinstance(node, list):
        return [_deref(x, comps, depth + 1) for x in node]
    return node


def slim(doc: dict) -> dict:
    comps = doc.get("components", {}).get("schemas", {})
    out = {}
    for path, item in doc["paths"].items():
        for meth, op in item.items():
            if meth not in ("get", "post", "put", "patch", "delete"):
                continue
            body = op.get("requestBody", {}).get("content", {})
            req = next((v.get("schema") for k, v in body.items() if "json" in k), None) or \
                next((v.get("schema") for v in body.values()), None)
            resp = None
            code = None
            for c, r in sorted(op.get("responses", {}).items()):
                if str(c).startswith("2"):
                    code = c
                    cont = r.get("content", {}) if isinstance(r, dict) else {}
                    resp = next((v.get("schema") for k, v in cont.items() if "json" in k), None)
                    break
            out[f"{meth.upper()} {path}"] = {
                "summary": op.get("summary", ""),
                "params": [{"name": p.get("name"), "in": p.get("in"), "required": p.get("required", False),
                            "type": p.get("schema", {}).get("type", "")} for p in op.get("parameters", [])],
                "request": _deref(req, comps) if req else None,
                "status": code,
                "response": _deref(resp, comps) if resp else None,
            }
    return out


def main():
    url = sys.argv[1] if len(sys.argv) > 1 else URL
    doc = json.load(urllib.request.urlopen(url, timeout=30))
    data = {"version": doc.get("info", {}).get("version"), "source": url, "operations": slim(doc)}
    (HERE / "icplan_openapi.json").write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"операций {len(data['operations'])}, версия {data['version']}")


if __name__ == "__main__":
    main()
