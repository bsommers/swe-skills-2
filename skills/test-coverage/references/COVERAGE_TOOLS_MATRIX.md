# Coverage Tooling Matrix

Detect the project's language(s) from its manifest files, then use the matching tool. Prefer a tool the project already has configured (check `package.json` scripts, `pyproject.toml`, `Makefile`, CI workflows) over introducing a new one.

| Language / Ecosystem | Detect via | Test Runner | Coverage Tool | OS Support (Windows / macOS / Linux) | Report Formats |
|---|---|---|---|---|---|
| **Bash / Shell** | `*.sh`, `bats` in `tests/` | bats-core | `kcov` (Linux/macOS; see `BASH_COVERAGE_NOTES.md`) + `shell_function_reachability.sh` | `shell_function_reachability.sh`: **Windows** (Git Bash/MSYS2/WSL), **macOS** (Bash 3.2+), **Linux**. `kcov`: macOS & Linux. | kcov: `cobertura-xml`, HTML. Reachability: plain text. |
| **JavaScript/TypeScript (Node)** | `package.json` | jest / vitest / mocha | `vitest --coverage` (`c8`/`v8`), `jest --coverage` (istanbul), or `c8` | **Windows, macOS, Linux** (native) | lcov, HTML, text-summary, `coverage-final.json` |
| **Python** | `pyproject.toml`, `setup.py`, `requirements.txt` | pytest | `pytest-cov` (`pytest --cov=<pkg> --cov-report=html --cov-report=term-missing`) or `coverage.py` | **Windows, macOS, Linux** (native) | HTML, XML (cobertura), terminal |
| **Go** | `go.mod` | `go test` | built-in: `go test -coverprofile=coverage.out ./...` | **Windows, macOS, Linux** (native) | `go tool cover -html=coverage.out`, text via `-func` |
| **Rust** | `Cargo.toml` | `cargo test` | `cargo llvm-cov` (recommended cross-platform) or `cargo-tarpaulin` (Linux-only) | `cargo llvm-cov`: **Windows (MSVC/GNU), macOS, Linux** | lcov, HTML, `cobertura` |
| **Java / Kotlin** | `pom.xml`, `build.gradle` | JUnit | JaCoCo (`mvn jacoco:report` / Gradle `jacocoTestReport`) | **Windows, macOS, Linux** (native) | HTML, XML, CSV |
| **Ruby** | `Gemfile` | RSpec / Minitest | SimpleCov | **Windows, macOS, Linux** (native) | HTML, lcov |
| **C / C++** | `CMakeLists.txt`, `Makefile` | ctest / custom | `llvm-cov` (`clang` / `clang-cl`) or `gcov` + `lcov` | `llvm-cov`: **Windows, macOS, Linux** | lcov HTML, text |
| **C# / .NET** | `*.csproj`, `*.sln` | `dotnet test` | `coverlet` (`dotnet test /p:CollectCoverage=true`) | **Windows, macOS, Linux** (native) | cobertura, lcov, opencover |
| **PHP** | `composer.json` | PHPUnit | Xdebug or PCOV coverage driver (`--coverage-html`) | **Windows, macOS, Linux** (native) | HTML, clover XML, text |

## Tri-OS Coverage & Driver Seam Auditing (Windows, macOS, Linux)

- **Audit OS-gated branches:** Inspect `#[cfg(windows)]`, `#[cfg(target_os = "macos")]`, `#[cfg(target_os = "linux")]`, `sys.platform`, and `process.platform` modules (`designing-plugin-contracts`). Single-OS coverage runs silently report 0% on other OS drivers unless:
  1. OS driver logic is unit-tested on every host via injected syscall/transport seams (`designing-testable-seams`), and
  2. CI runs native test + coverage jobs across `windows-latest`, `macos-latest`, and `ubuntu-latest` and merges or gates each OS report.

## Multi-language repos

Run each ecosystem's tool independently and report them as separate sections — don't try to force a unified percentage across languages with fundamentally different semantics (e.g. a Bash script's "line" and a TypeScript branch aren't comparable units).

## Threshold guidance (starting points, not universal rules)

- New/actively-changing code: aim for the change's *diff* coverage (lines touched in the PR/commit) rather than a single repo-wide percentage — this is what actually prevents regressions.
- A repo-wide floor (e.g. "never drop below current baseline") is more sustainable than an arbitrary target percentage (e.g. "80%") picked without context — a 100%-covered getter/setter file is not more valuable than a 60%-covered file that tests every error path of the riskiest module.
- For CLI/infra tooling (like Bash projects), weight "is every external-tool-invoking function exercised via a mock at least once" above raw percentage — see the Shell Test-Quality Checklist in `SKILL.md`.
