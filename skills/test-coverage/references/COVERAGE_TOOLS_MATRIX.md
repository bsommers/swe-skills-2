# Coverage Tooling Matrix

Detect the project's language(s) from its manifest files, then use the matching tool. Prefer a tool the project already has configured (check `package.json` scripts, `pyproject.toml`, `Makefile`, CI workflows) over introducing a new one.

| Language / Ecosystem | Detect via | Test Runner | Coverage Tool | Report Formats |
|---|---|---|---|---|
| **Bash / Shell** | `*.sh`, `bats` in `tests/` | bats-core | kcov (see `BASH_COVERAGE_NOTES.md` for real caveats) + `shell_function_reachability.sh` | kcov: `cobertura-xml`, HTML. Reachability: plain text. |
| **JavaScript/TypeScript (Node)** | `package.json` | jest / vitest / mocha | `vitest --coverage` (uses `c8`/`v8`), `jest --coverage` (istanbul), or standalone `nyc`/`c8` | lcov, HTML, text-summary, `coverage-final.json` |
| **Python** | `pyproject.toml`, `setup.py`, `requirements.txt` | pytest | `pytest-cov` (`pytest --cov=<pkg> --cov-report=html --cov-report=term-missing`) or `coverage.py` directly | HTML, XML (cobertura), terminal |
| **Go** | `go.mod` | `go test` | built-in: `go test -coverprofile=coverage.out ./...` | `go tool cover -html=coverage.out`, text via `-func` |
| **Rust** | `Cargo.toml` | `cargo test` | `cargo-tarpaulin` (Linux-friendly) or `cargo llvm-cov` (cross-platform, recommended) | lcov, HTML, `cobertura` |
| **Java / Kotlin** | `pom.xml`, `build.gradle` | JUnit | JaCoCo (`mvn jacoco:report` / Gradle `jacocoTestReport`) | HTML, XML, CSV |
| **Ruby** | `Gemfile` | RSpec / Minitest | SimpleCov | HTML, lcov |
| **C / C++** | `CMakeLists.txt`, `Makefile` | ctest / custom | `gcov` + `lcov`/`genhtml`, or `llvm-cov` | lcov HTML, text |
| **C# / .NET** | `*.csproj`, `*.sln` | `dotnet test` | `coverlet` (`dotnet test /p:CollectCoverage=true`) | cobertura, lcov, opencover |
| **PHP** | `composer.json` | PHPUnit | Xdebug or PCOV coverage driver, built into PHPUnit (`--coverage-html`) | HTML, clover XML, text |

## Multi-language repos

Run each ecosystem's tool independently and report them as separate sections — don't try to force a unified percentage across languages with fundamentally different semantics (e.g. a Bash script's "line" and a TypeScript branch aren't comparable units).

## Threshold guidance (starting points, not universal rules)

- New/actively-changing code: aim for the change's *diff* coverage (lines touched in the PR/commit) rather than a single repo-wide percentage — this is what actually prevents regressions.
- A repo-wide floor (e.g. "never drop below current baseline") is more sustainable than an arbitrary target percentage (e.g. "80%") picked without context — a 100%-covered getter/setter file is not more valuable than a 60%-covered file that tests every error path of the riskiest module.
- For CLI/infra tooling (like Bash projects), weight "is every external-tool-invoking function exercised via a mock at least once" above raw percentage — see the Shell Test-Quality Checklist in `SKILL.md`.
