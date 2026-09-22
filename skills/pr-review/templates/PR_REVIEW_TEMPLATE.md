# Pull Request Review: [PR Title / Branch Name]

> **PR Number / Branch:** `#[PR_NUMBER] / [BRANCH_NAME]`  
> **Author:** `@[AUTHOR]`  
> **Reviewer:** `[AGENT_OR_MODEL_NAME]`  
> **Date:** `[YYYY-MM-DD]`  
> **Verdict:** `[APPROVE | REQUEST_CHANGES | COMMENT]`  
> **Risk Score:** `[Low | Medium | High | Critical]`

---

## 1. Executive Summary
*Provide a concise 2-3 sentence overview of what this pull request changes, the architectural impact, and overall quality.*

---

## 2. 🚨 Blocking Findings (Must Fix Before Merge)
*Issues that introduce logic bugs, security vulnerabilities, breaking contract changes, or data corruption risks.*

### Finding 1: [Issue Title]
- **File & Location:** [`path/to/file.ext#L10-L25`](file:///absolute/path/or/relative/path)
- **Category:** `[Correctness | Security | Breaking Change | Architecture | Concurrency]`
- **Impact & Risk:** *[Explanation of why this cannot be merged as-is]*
- **Recommended Remediation:**
```typescript
// ❌ Current Code in PR:
...

// ✅ Recommended Solution:
...
```

---

## 3. 💡 Suggestions & Polish (Non-Blocking)
*Maintainability, performance opportunities, naming, or minor simplification.*

- [ ] **[Suggestion 1]**: [`path/to/file.ext#L50`](file:///path) - *[Details]*
- [ ] **[Suggestion 2]**: [`path/to/file.ext#L85`](file:///path) - *[Details]*

---

## 4. 🧪 Test Coverage & Verification Assessment
- **Existing Test Status:** `[All Passing | Failing | No Tests Added]`
- **Coverage Gap Analysis:** *[Did the PR introduce new branches or logic paths without test coverage?]*
- **Recommended Test Cases to Add:**
  1. `[Test Case 1 Description - e.g. Handle null token payload]`
  2. `[Test Case 2 Description - e.g. Timeout retry behavior]`

---

## 5. 🛡️ Security & Contract Stability Audit
- **Breaking API Changes:** `[None | Deprecations | Breaking Change Detected]`
- **Input Validation & Sanitization:** `[Verified | Needs Work]`
- **Data Integrity & Migrations:** `[Safe | Risk of Lock or Downtime]`
