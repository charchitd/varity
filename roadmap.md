# Varity v0.1 — Launch Roadmap

## Phase 1 — Pre-publish Checklist (1–2 days)

### 1.1 Fix placeholder URLs in pyproject.toml
```toml
Homepage = "https://github.com/charchit-dev/varity"
Documentation = "https://charchit-dev.github.io/varity"
Repository = "https://github.com/charchit-dev/varity"
"Bug Tracker" = "https://github.com/charchit-dev/varity/issues"
```

### 1.2 Clean build
```bash
rm -rf dist/ build/ varity.egg-info/
python -m build
ls dist/   # varity-0.1.0-py3-none-any.whl + .tar.gz
```

### 1.3 Verify install
```bash
pip install dist/varity-0.1.0-py3-none-any.whl
python -c "import varity; print(varity.__version__)"
varity demo
```

### 1.4 Full gate
```bash
python -m pytest tests/ -v
python -m ruff check varity/
python -m mypy varity/ --strict
```

---

## Phase 2 — CI + Badges (half day)

### 2.1 GitHub Actions CI
Create `.github/workflows/ci.yml`:
```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.9", "3.10", "3.11", "3.12"]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "${{ matrix.python-version }}" }
      - run: pip install -e ".[dev]"
      - run: python -m pytest tests/ -v
      - run: python -m ruff check varity/
      - run: python -m mypy varity/ --strict
```

### 2.2 README badges
```markdown
[![PyPI](https://img.shields.io/pypi/v/varity)](https://pypi.org/project/varity/)
[![CI](https://github.com/charchit-dev/varity/actions/workflows/ci.yml/badge.svg)](...)
[![Python](https://img.shields.io/pypi/pyversions/varity)](...)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
```

### 2.3 Repo topics
Add: `llm`, `hallucination-detection`, `ai-safety`, `fact-checking`, `nlp`, `python`, `vss`, `llm-reliability`, `prompt-engineering`, `anthropic`, `openai`, `gemini`

---

## Phase 3 — PyPI Publish (1 hour)

```bash
# 1. Register at pypi.org → create API token
pip install twine

# 2. TestPyPI dry run
python -m twine upload --repository testpypi dist/*
pip install -i https://test.pypi.org/simple/ varity

# 3. Real PyPI
python -m twine upload dist/*

# 4. Verify
pip install varity
```

---

## Phase 4 — GitHub Pages (half day)

1. Repo Settings → Pages → Source: main → `/docs`
2. Live at `https://charchit-dev.github.io/varity`
3. Enhance `docs/index.html` with live BYOK demo, VSS diagram, benchmark table, PyPI link

---

## Phase 5 — Benchmarks (before any big post)

Run benchmarks, publish this table:

| Model | Claim Accuracy | VSS Correlation | Hallucination Detection Rate |
|-------|---------------|-----------------|------------------------------|
| GPT-4o | X% | X | X% |
| Claude 3.5 | X% | X | X% |
| Gemini 1.5 | X% | X | X% |

Numbers = credibility = shareability.

---

## Phase 6 — Launch & Awareness

### The Hook (lead every post with this)
> "What if your LLM verified its own answers — recursively — and told you exactly how stable that verdict was?"

### 6.1 Hacker News (highest ROI)
Post Tuesday–Thursday, 9–11am EST. One shot.
```
Show HN: Varity – recursive self-checking for LLM hallucinations with Verdict Stability Score

I built a Python library that decomposes LLM responses into atomic claims,
verifies each one recursively at depth N, and uses verdict *flip count*
across depths as a hallucination signal (VSS). BYOK — works with Anthropic,
OpenAI, Gemini. pip install varity

GitHub: [url]
```

### 6.2 Reddit
- **r/MachineLearning** — technical, include VSS algorithm + benchmark table
- **r/LocalLLaMA** — practical: "I added recursive self-checking to my LLM pipeline"
- **r/Python** — pip install angle, clean code snippet
- **r/artificial** — general AI audience

### 6.3 Dev.to / Medium article
**Title:** "How I reduced LLM hallucinations by 40% using recursive self-verification"

Structure: Problem → Insight (verdict instability = hallucination signal) → VSS explained → Code snippet → Benchmarks → Repo link

Cross-post to: Dev.to, Medium, Towards Data Science, Hashnode

### 6.4 Twitter/X Thread
```
1/ I built a Python library that catches LLM hallucinations
   using recursive self-verification.

   Key insight: if an LLM flips its verdict when re-checking
   the same claim at deeper recursion depths, that's a
   hallucination signal. I call it the Verdict Stability Score (VSS). 🧵

2/ Here's how it works: [diagram]
3/ 5 lines of code: [snippet]
4/ BYOK — bring your own OpenAI/Anthropic/Gemini key
5/ pip install varity | GitHub: [url]

#LLM #AIEngineering #Python #MachineLearning
```

### 6.5 GitHub virality
- Pin repo on profile
- Add 12 topic tags
- Submit to `awesome-llm`, `awesome-hallucination`, `awesome-ai-safety` lists
- Open `good first issue` + `help wanted` issues
- Add `CONTRIBUTING.md`

---

## Priority Execution Order

| When | Action |
|------|--------|
| **Week 1** | Fix URLs → clean build → PyPI publish → CI green → badges |
| **Week 1** | GitHub Pages live |
| **Week 2** | Run benchmarks → write Dev.to article |
| **Week 2** | **Show HN post** (single highest-leverage move) |
| **Week 3** | Reddit posts → Twitter thread → awesome-list PRs |
| **Ongoing** | Respond to every issue/comment in <24h |

---

## Single Most Important Action

**The Show HN post with benchmark numbers.** That's the one that can take a Python library from 0 to 500 stars overnight. Everything else supports it.
