# Contributing

Thanks for improving swe-skills. The full guidelines are in [docs/development.md](docs/development.md); agent-facing rules are in [AGENTS.md](AGENTS.md).

Quick version:

1. Branch from `main`; one logical change per PR.
2. Follow the skill authoring rules (`Use when` triggers-only description, body of about 500 words or fewer).
3. Run `python3 scripts/lint-skills.py --words` (must print OK) and `python3 -m unittest discover tests`.
4. Update docs, counts and `CHANGELOG.md` in the same change.

CI (`.github/workflows/ci.yml`) runs the same lint and tests on every pull request; run them locally first so CI is a confirmation, not a debugger. Use the issue templates for bugs, skill feedback, and skill proposals. Report security problems privately (see [SECURITY.md](SECURITY.md)). Participation is covered by the [Code of Conduct](CODE_OF_CONDUCT.md).
