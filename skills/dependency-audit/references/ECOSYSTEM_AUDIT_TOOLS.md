# Ecosystem Dependency Audit Tools & CLI Reference

A quick-reference guide for running dependency scanners across language ecosystems.

---

## 1. Node.js / TypeScript Ecosystem
- `npm audit`: Scans `package-lock.json` against GitHub Advisory Database.
- `npm audit fix`: Automatically updates compatible semver patches for vulnerable dependencies.
- `npm outdated`: Lists outdated dependencies with current, wanted, and latest versions.
- `pnpm audit`: Built-in scanner for pnpm workspaces.
- `yarn audit`: Yarn dependency auditor.

## 2. Python Ecosystem
- `pip-audit`: Audits Python environments against the Python Packaging Advisory Database and OSV.
  ```bash
  pip-audit -r requirements.txt
  ```
- `safety check`: Scans installed dependencies against the Safety DB.
- `pip list --outdated`: Shows packages that have newer releases on PyPI.

## 3. Rust Ecosystem
- `cargo audit`: Audits `Cargo.lock` against the RustSec Advisory Database.
  ```bash
  cargo install cargo-audit
  cargo audit
  ```
- `cargo outdated`: Checks for newer versions of crates.

## 4. Go Ecosystem
- `govulncheck`: Official Go vulnerability scanner analyzing call graphs to detect if vulnerable code is actually executed.
  ```bash
  go install golang.org/x/vuln/cmd/govulncheck@latest
  govulncheck ./...
  ```

## 5. Multi-Language Universal Scanners
- **OSV-Scanner** (`osv-scanner`): Google's open source vulnerability scanner supporting lockfiles from 14+ package managers.
  ```bash
  osv-scanner -r .
  ```
- **Trivy** (`trivy`): Comprehensive vulnerability scanner for repositories, container images, and filesystems.
  ```bash
  trivy fs .
  ```
