## What and why

<!-- One logical change. Link issues with "Closes #N". -->

## Checklist

- [ ] `python3 scripts/lint-skills.py --words` prints `OK`
- [ ] `python3 -m unittest discover tests` passes
- [ ] New or renamed skill: listed in `using-swe-skills`, the README table, `docs/EVIDENCE.md`, and `docs/TESTING.md`
- [ ] Changed skill behavior: `docs/TESTING.md` scenario updated
- [ ] Manifest versions still match (lint checks this)
- [ ] Docs, counts, and `CHANGELOG.md` updated in this PR
- [ ] No absolute machine paths, private project names, or secrets
