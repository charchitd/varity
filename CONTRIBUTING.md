# Contributing to Varity

## Getting Started

1. Fork the repository and clone your fork.
2. Create a virtual environment and install dev dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

## Branch Naming

| Type    | Pattern          | Example               |
|---------|------------------|-----------------------|
| Feature | `feat/xxx`       | `feat/gemini-provider` |
| Bug fix | `fix/xxx`        | `fix/vss-calculation`  |
| Docs    | `docs/xxx`       | `docs/algorithm`       |
| Chore   | `chore/xxx`      | `chore/update-deps`    |

## Commit Messages

Use [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add Gemini provider support
fix: correct VSS flip count for depth-0 claims
docs: clarify recursive verification algorithm
chore: bump httpx to 0.27
```

## Before Opening a PR

Run the full check suite — all three must pass:

```bash
python -m pytest tests/ -v        # tests
python -m ruff check varity/      # lint
python -m mypy varity/ --strict   # types
```

Fix any failures before submitting. PRs that break CI will not be merged.

## Code Style

- **Formatter/linter:** ruff (`line-length = 100`)
- **Types:** mypy strict — type hints required on all public functions
- **Docstrings:** Google style with one-line summary + Args/Returns/Raises
- **Async:** internal logic is async; public API uses `asyncio.run` sync wrappers
- **Prompts:** all prompt templates go in `varity/prompts.py` as `UPPER_SNAKE_CASE` constants

## Adding a Provider

Subclass `BaseLLMProvider` in `varity/providers/` and implement `complete()` and `complete_json()`. Use raw `httpx` — no SDK dependencies. Add unit tests using `MockProvider`.

## Security

Never log, print, or store API keys. Keys are passed per-call and must not appear in logs, errors, or test fixtures.
