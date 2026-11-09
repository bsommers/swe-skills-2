# Contributing

Thanks for improving swe-skills. The full guidelines are in [docs/development.md](docs/development.md); agent-facing rules are in [AGENTS.md](AGENTS.md).

Quick version:

1. Branch from `main`; one logical change per PR.
2. Follow the skill authoring rules (`Use when` triggers-only description, body of about 500 words or fewer).
3. Run `python3 scripts/lint-skills.py --words` (must print OK) and `python3 -m unittest discover tests`.
4. Update docs, counts and `CHANGELOG.md` in the same change.
