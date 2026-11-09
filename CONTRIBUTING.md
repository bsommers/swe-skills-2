# Contributing

Thanks for improving swe-skills. The full guidelines are in [docs/development.md](docs/development.md); agent-facing rules are in [AGENTS.md](AGENTS.md).

Quick version:

1. Branch from `main`; one logical change per PR.
2. Follow the skill authoring rules (`Use when` triggers-only description, body of about 500 words or fewer).
3. Run `scripts/verify.sh` (lint, tests, installer dry run); it must end with `verify: all checks passed`.
4. Update docs, counts and `CHANGELOG.md` in the same change.

Run `scripts/verify.sh` before pushing. It is local CI: the same checks `.github/workflows/ci.yml` runs on pull requests, which is only the final confirmation gate. Use the issue templates for bugs, skill feedback, and skill proposals. Report security problems privately (see [SECURITY.md](SECURITY.md)). Participation is covered by the [Code of Conduct](CODE_OF_CONDUCT.md).
