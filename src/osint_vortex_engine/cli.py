from __future__ import annotations

import argparse
import json
from pathlib import Path

from .extract import extract_from_snippets
from .graph import build_edges, entity_support


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="osint-vortex",
        description=(
            "Safe-by-default offline entity extraction + relationship graphing. "
            "No active scanning."
        ),
    )
    ap.add_argument("--input", type=str, required=True, help="Text file (one snippet per line)")
    ap.add_argument("--out", type=str, default="out.json", help="Output JSON path")
    args = ap.parse_args(argv)

    inp = Path(args.input)
    snippets = [line.strip() for line in inp.read_text(encoding="utf-8", errors="ignore").splitlines() if line.strip()]

    entities = extract_from_snippets(snippets)
    edges = build_edges(entities)
    support = entity_support(edges)

    report = {
        "snippets": len(snippets),
        "entities": sum(len(x) for x in entities),
        "unique_entities": len(support),
        "top_entities": sorted(support.items(), key=lambda kv: kv[1], reverse=True)[:25],
    }

    outp = Path(args.out)
    outp.write_text(json.dumps({"report": report}, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
