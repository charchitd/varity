"""Varity benchmark results analyzer.

Reads one or more provider JSON result files and prints a clean
multi-provider comparison table suitable for copy-pasting into
a README, research paper, or social media post.

Usage:
    python benchmarks/analyze.py benchmarks/results_gemini.json
    python benchmarks/analyze.py benchmarks/results_*.json
    python benchmarks/analyze.py results_gemini.json results_anthropic.json results_openai.json
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


TIER_ORDER = ["EASY", "MEDIUM", "HARD", "CLEAN_S", "CLEAN_L"]


def load(path: str) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def col(s: str, width: int) -> str:
    """Left-justified column of fixed width."""
    return s[:width].ljust(width)


def render_table(results: list[dict]) -> None:
    if not results:
        print("No results to display.")
        return

    providers = [r["provider"] for r in results]

    print("\n" + "=" * 72)
    print("  VARITY BENCHMARK RESULTS")
    print("=" * 72)

    # --- Main summary table ---
    header = ["Metric"] + providers
    rows = [
        ["Detection Accuracy"] + [f"{r['accuracy_pct']}%" for r in results],
        ["Avg Latency (ms)"]   + [str(r.get("avg_latency_ms", "—")) for r in results],
        ["Avg Token Usage"]    + [str(r.get("avg_tokens", "—")) for r in results],
        ["Depth"]              + [str(r.get("depth", "—")) for r in results],
        ["Model"]              + [str(r.get("model", "default")) for r in results],
    ]

    col_w = max(20, *(len(p) + 4 for p in providers))
    label_w = 22

    print()
    print("  " + col("Metric", label_w) + "  " + "  ".join(col(p, col_w) for p in providers))
    print("  " + "-" * label_w + "  " + "  ".join("-" * col_w for _ in providers))
    for row in rows:
        label = row[0]
        vals  = row[1:]
        print("  " + col(label, label_w) + "  " + "  ".join(col(v, col_w) for v in vals))

    # --- Per-tier breakdown ---
    print()
    print("  Per-tier Accuracy:")
    print("  " + col("Tier", 12) + "  " + "  ".join(col(p, col_w) for p in providers))
    print("  " + "-" * 12 + "  " + "  ".join("-" * col_w for _ in providers))

    all_tiers: list[str] = []
    for r in results:
        all_tiers.extend(r.get("tier_accuracy", {}).keys())
    tiers = sorted(set(all_tiers), key=lambda t: TIER_ORDER.index(t) if t in TIER_ORDER else 99)

    for tier in tiers:
        vals = []
        for r in results:
            ta = r.get("tier_accuracy", {}).get(tier)
            if ta:
                vals.append(f"{ta['accuracy_pct']}%  ({ta['correct']}/{ta['total']})")
            else:
                vals.append("—")
        print("  " + col(tier, 12) + "  " + "  ".join(col(v, col_w) for v in vals))

    # --- Markdown export ---
    print()
    print("=" * 72)
    print("  Markdown Table (copy-paste ready):")
    print("=" * 72)
    print()

    md_cols = ["Metric"] + providers
    md_rows = [
        ["**Detection Accuracy**"] + [f"**{r['accuracy_pct']}%**" for r in results],
        ["Avg Latency"] + [f"{r.get('avg_latency_ms', '—')} ms" for r in results],
        ["Avg Token Usage"] + [str(r.get("avg_tokens", "—")) for r in results],
        ["Depth"] + [str(r.get("depth", "—")) for r in results],
        ["Model"] + [str(r.get("model", "default")) for r in results],
    ]
    for tier in tiers:
        row = [f"Tier: {tier}"]
        for r in results:
            ta = r.get("tier_accuracy", {}).get(tier)
            row.append(f"{ta['accuracy_pct']}%" if ta else "—")
        md_rows.append(row)

    def md_row(cells: list[str]) -> str:
        return "| " + " | ".join(cells) + " |"

    print(md_row(md_cols))
    print("|" + "|".join(["---"] * len(md_cols)) + "|")
    for row in md_rows:
        print(md_row(row))
    print()


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python benchmarks/analyze.py results_*.json")
        sys.exit(1)

    paths = sys.argv[1:]
    results = []
    for p in paths:
        try:
            results.append(load(p))
            print(f"  Loaded: {p}")
        except Exception as exc:
            print(f"  ✗ Failed to load {p}: {exc}", file=sys.stderr)

    render_table(results)


if __name__ == "__main__":
    main()
