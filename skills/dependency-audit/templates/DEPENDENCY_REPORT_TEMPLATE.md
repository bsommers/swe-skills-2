# Dependency Security & Supply Chain Audit Report

> **Project Name:** `[Project Name]`  
> **Date:** `[YYYY-MM-DD]`  
> **Ecosystem(s):** `[Node.js / Python / Rust / Go / Java]`  
> **Package Manifests Audited:** `[package.json, pyproject.toml, Cargo.toml]`  
> **Total Direct Dependencies:** `[XX]`  
> **Total Transitive Dependencies:** `[XX]`  
> **Overall Security Health:** `[A (Clean) | B (Low) | C (Medium) | D (High) | F (Critical CVEs)]`

---

## 1. Executive Summary
*Provide a concise summary of the overall dependency hygiene, CVE exposure, and upgrade priorities.*

---

## 2. 🚨 Known Vulnerabilities (CVE Matrix)

| Package | Installed | Patched In | Severity / CVSS | CVE Identifier | Vulnerability Summary |
| :--- | :---: | :---: | :---: | :--- | :--- |
| `[pkg-name]` | `[1.0.0]` | `[1.0.2]` | **HIGH (7.5)** | `CVE-202X-XXXX` | *[e.g., ReDoS, SQL Injection]* |

### Vulnerability Remediation Details
- **Issue: `[Package Name]`**
  - **Dependency Path:** `[direct-dep] -> [sub-dep] -> [vulnerable-pkg]`
  - **Recommended Action:** `[e.g. npm update <pkg-name> or bump direct dependency]`
  - **Remediation Command:**
```bash
npm install [package]@[fixed-version]
```

---

## 3. 📦 Outdated & Lagging Dependencies

| Dependency | Installed Version | Latest Version | Lag Type | Risk Assessment | Action |
| :--- | :---: | :---: | :---: | :--- | :--- |
| `[package]` | `1.2.0` | `2.0.0` | Major | Breaking API changes possible | Test in branch |
| `[package]` | `3.1.0` | `3.1.4` | Patch | Safe bug fix | Bump immediately |

---

## 4. 📜 License & Compliance Audit
- **Permissive Licenses (MIT / Apache / BSD):** `[XX] packages`
- **Weak Copyleft (MPL / LGPL):** `[XX] packages`
- **High-Risk / Non-Permissive (GPL / AGPL):** `[None | List packages]`

---

## 5. 🛠️ Actionable Upgrade Roadmap
- [ ] **Step 1 (Immediate):** Patch all Critical and High CVEs.
- [ ] **Step 2:** Apply safe patch and minor updates.
- [ ] **Step 3:** Plan major version migrations with dedicated characterization tests.
