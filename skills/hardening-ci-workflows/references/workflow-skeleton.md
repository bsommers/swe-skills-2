# Hardened workflow skeleton

```yaml
name: ci
on:
  pull_request:          # not pull_request_target
  push:
    branches: [main]
permissions:
  contents: read         # default for every job
concurrency:
  group: ci-${{ github.ref }}
  cancel-in-progress: true
jobs:
  test:
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]   # every shipped OS
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@<40-hex-sha> # v4.1.7
        with:
          persist-credentials: false
      - name: Run with untrusted input
        env:
          TITLE: ${{ github.event.pull_request.title }}   # data via env
        run: echo "title is $TITLE"                       # quoted, never ${{ }} here
      - name: Tests
        run: |
          echo "::group::test output"
          ./scripts/verify.sh || { tail -n 80 target/verify/fail.txt; exit 1; }
          echo "::endgroup::"
  release:
    needs: test
    permissions:
      contents: write    # only this job
```

## Dependency policy outline (cargo-deny style)

- advisories: deny known vulnerabilities; unmaintained flagged.
- licenses: allowlist generated from the actual tree; comment one reason per license.
- sources: unknown registry = deny, unknown git = deny.
- bans: wildcard version requirements = deny.

## Pin check

```bash
gh api repos/OWNER/REPO/commits/v1.2.3 -q .sha   # must equal the pinned SHA
```
Annotated tags: confirm the commit SHA, not the tag-object SHA.
