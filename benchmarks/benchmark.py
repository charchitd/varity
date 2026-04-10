"""Varity benchmark runner.

Runs the shared dataset against a single provider and writes JSON results.

Usage:
    python benchmarks/benchmark.py --provider gemini --key AIzaSy... [--depth 1]
    python benchmarks/benchmark.py --provider anthropic --key sk-ant-...
    python benchmarks/benchmark.py --provider openai --key sk-...
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
import time


async def run_benchmark(
    provider_name: str,
    api_key: str,
    model: str | None,
    depth: int,
    output_path: str | None,
    delay: float = 0.0,
) -> None:
    import importlib.util, os
    from varity import Varity, VarityConfig
    from varity.providers import get_provider

    # Load dataset from the same directory as this script
    _ds_path = os.path.join(os.path.dirname(__file__), "dataset.py")
    _spec = importlib.util.spec_from_file_location("dataset", _ds_path)
    _mod = importlib.util.module_from_spec(_spec)  # type: ignore[arg-type]
    _spec.loader.exec_module(_mod)  # type: ignore[union-attr]
    BENCHMARK_CASES = _mod.BENCHMARK_CASES

    kwargs: dict[str, object] = {}
    if model:
        kwargs["model"] = model

    provider = get_provider(provider_name, api_key=api_key, **kwargs)
    config = VarityConfig(depth=depth, strategy="full")
    varity = Varity(provider=provider, config=config)

    results = []
    correct = 0
    total = len(BENCHMARK_CASES)
    total_latency_ms = 0
    total_tokens = 0

    tier_stats: dict[str, dict[str, int]] = {}

    print(f"\n{'='*72}")
    print(f"  Varity Benchmark  |  provider={provider_name}  depth={depth}")
    print(f"{'='*72}")

    try:
        for i, case in enumerate(BENCHMARK_CASES):
            if i > 0 and delay > 0:
                print(f"  ... waiting {delay:.0f}s before next case ...")
                await asyncio.sleep(delay)
            t0 = time.monotonic()
            try:
                result = await varity.acheck(case["response"])
                elapsed = int((time.monotonic() - t0) * 1000)
                actual_flagged = len(result.flagged_claims)
                expected = case["expected_flagged"]
                detection_ok = (
                    (expected == 0 and actual_flagged == 0)
                    or (expected > 0 and actual_flagged > 0)
                )
                if detection_ok:
                    correct += 1

                tier = case.get("tier", "UNKNOWN")
                if tier not in tier_stats:
                    tier_stats[tier] = {"correct": 0, "total": 0}
                tier_stats[tier]["total"] += 1
                if detection_ok:
                    tier_stats[tier]["correct"] += 1

                tok = result.token_usage.get("total_tokens", 0)
                total_latency_ms += elapsed
                total_tokens += tok

                status = "PASS" if detection_ok else "FAIL"
                label = "+" if detection_ok else "x"
                print(
                    f"  [{label}] [{case['id']}:{tier:<8}] {status}  "
                    f"conf={result.overall_confidence:.2f}  "
                    f"vss={result.vss_score:.2f}  "
                    f"flagged={actual_flagged}(exp={expected})  "
                    f"{elapsed}ms"
                )
                results.append({
                    "id": case["id"],
                    "tier": tier,
                    "status": status,
                    "overall_confidence": result.overall_confidence,
                    "vss_score": result.vss_score,
                    "flagged_count": actual_flagged,
                    "expected_flagged": expected,
                    "total_tokens": tok,
                    "duration_ms": elapsed,
                    "notes": case["notes"],
                })
            except Exception as exc:
                elapsed = int((time.monotonic() - t0) * 1000)
                print(f"  [!] [{case['id']}] ERROR  {exc}  {elapsed}ms")
                results.append({"id": case["id"], "status": "ERROR", "error": str(exc)})
    finally:
        await provider.close()

    # Summary
    accuracy = correct / total * 100
    avg_latency = total_latency_ms / total if total else 0
    avg_tokens = total_tokens / total if total else 0

    print(f"\n{'='*72}")
    print(f"  Overall detection accuracy : {accuracy:.1f}%  ({correct}/{total})")
    print(f"  Avg latency per check      : {avg_latency:.0f} ms")
    print(f"  Avg token usage (est.)     : {avg_tokens:.0f}")
    print()
    print("  Per-tier breakdown:")
    for tier, stats in sorted(tier_stats.items()):
        t_acc = stats["correct"] / stats["total"] * 100
        print(f"    {tier:<10}  {t_acc:.0f}%  ({stats['correct']}/{stats['total']})")
    print(f"{'='*72}\n")

    if output_path:
        summary = {
            "provider": provider_name,
            "model": model or "default",
            "depth": depth,
            "accuracy_pct": round(accuracy, 1),
            "avg_latency_ms": round(avg_latency),
            "avg_tokens": round(avg_tokens),
            "tier_accuracy": {
                t: {
                    "accuracy_pct": round(s["correct"] / s["total"] * 100, 1),
                    "correct": s["correct"],
                    "total": s["total"],
                }
                for t, s in tier_stats.items()
            },
            "cases": results,
        }
        with open(output_path, "w", encoding="utf-8") as fh:
            json.dump(summary, fh, indent=2)
        print(f"  Results saved → {output_path}\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Varity benchmark runner")
    parser.add_argument("--provider", default="gemini", help="Provider name (gemini/anthropic/openai)")
    parser.add_argument("--key", required=True, help="API key for the provider")
    parser.add_argument("--model", default=None, help="Override default model name")
    parser.add_argument("--depth", type=int, default=1, help="Verification depth (default: 1)")
    parser.add_argument("--output", default=None, help="Write results JSON to this path")
    parser.add_argument("--delay", type=float, default=5.0, help="Seconds to wait between cases (default: 5)")
    args = parser.parse_args()

    asyncio.run(
        run_benchmark(
            provider_name=args.provider,
            api_key=args.key,
            model=args.model,
            depth=args.depth,
            output_path=args.output,
            delay=args.delay,
        )
    )
    sys.exit(0)


if __name__ == "__main__":
    main()
