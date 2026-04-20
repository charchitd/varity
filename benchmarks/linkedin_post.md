# Introducing Varity v0.1: A Novel Metric for LLM Hallucination Detection

I'm excited to share **Varity v0.1** — a Python library introducing a fundamentally different approach to detecting LLM hallucinations.

## The Problem
LLMs generate plausible but factually incorrect statements with absolute confidence. Traditional single-pass fact-checking suffers from **confirmation bias**: asking one LLM "Is this true?" often results in it ratifying another model's hallucination.

## The Novel Metric: Verdict Stability Score (VSS)
Varity introduces **VSS** — a mathematical metric measuring hallucination through *verdict instability* across recursive verification depths.

**Core thesis**: Hallucinatory claims exist sparsely in an LLM's latent space. Under iterative adversarial questioning (Depth-N), these claims contradict themselves — flipping between VERIFIED, CONTRADICTED, and UNCERTAIN. True facts remain stable regardless of questioning intensity.

VSS algorithmically tracks these "flips." Low VSS = mathematical instability = hallucination.

## Addressing the Research Gap
Recent work (SelfCheckGPT - Manakul et al., 2023; Chain-of-Verification - Dhuliawala et al., 2023) showed LLMs possess latent self-critique capabilities. However, prior approaches relied on single-pass heuristics rather than algorithmic scoring.

Varity operationalizes this through:
1. **Atomic Claim Decomposition**: Breaking responses into typed nodes to prevent "poisoned claims" hiding behind surrounding truths
2. **Depth-N Recursive Interrogation**: Forcing iterative verification across isolated chambers
3. **Dual-Signal Flagging**: Combining Bayesian confidence with VSS to catch "confidently wrong" hallucinations

## Changing Development Paradigms
Varity shifts from external RAG verification (which goes stale) to **internal recursive self-checking** using the LLM's parametric knowledge as oracle.

Architecture: Zero vendor SDKs (raw httpx), BYOK (keys never logged), provider agnostic (Anthropic/OpenAI/Gemini), async-first with graceful degradation.

## Benchmark Performance (v0.1.11)
15 hand-labeled cases (obvious errors → subtle misconceptions):
- **100% detection accuracy** (gpt-4o-mini, depth=1)
- **100% VSS scores** on verified facts
- **0% false positives** on clean statements

## Commercial Applications
Deterministic verification enables:
- Zero-Hallucination Legal/Medical Writers (VSS > 0.70 filter)
- Academic Fact-Checking Automation (browser extensions)
- Enterprise Middleware (API proxy)

**Try it**: `pip install varity`  
**Demo**: https://charchitd.github.io/Varity-v0.1/  
**Whitepaper**: docs/CONCEPTS.md

Part of ongoing research at Aston University on GenAI reliability. Research community feedback deeply appreciated.

#MachineLearning #LLMs #AI #Hallucination #NLP #Research #GenAI #FactChecking
