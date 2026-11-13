from __future__ import annotations
import json
from pathlib import Path

def rows(path):
    if not Path(path).is_file():
        return []
    return [json.loads(l) for l in Path(path).read_text().splitlines() if l.strip()]

def run_verify(args) -> int:
    out=Path(args.out)
    exp=json.loads(Path(args.expect).read_text())
    items={r["sku"]: r for r in rows(out/"items.jsonl")}
    errors=[]
    exp_items={r["sku"]: r for r in exp["items"]}
    if set(items)!=set(exp_items):
        errors.append(f"sku extra={sorted(set(items)-set(exp_items))} missing={sorted(set(exp_items)-set(items))}")
    for sku,e in exp_items.items():
        g=items.get(sku)
        if not g:
            continue
        for k in ("title","price"):
            if g.get(k)!=e.get(k):
                errors.append(f"{sku} {k} {g.get(k)!r} != {e.get(k)!r}")
    report={}
    rp=out/"report.json"
    if rp.is_file():
        report=json.loads(rp.read_text())
    if report.get("template_broken") is not False and exp.get("template_broken") is False:
        errors.append(f"template_broken {report.get('template_broken')!r}")
    if errors:
        print("verify failed:")
        for e in errors:
            print(" -", e)
        return 1
    print("verify ok")
    return 0
