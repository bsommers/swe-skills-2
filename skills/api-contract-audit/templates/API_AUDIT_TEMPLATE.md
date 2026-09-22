# API Contract & Schema Drift Audit Report

> **Project Name:** `[Project Name]`  
> **Date:** `[YYYY-MM-DD]`  
> **Audited Contracts:** `[e.g., docs/openapi.yaml, src/schema.graphql, src/dto/*]`  
> **Total Endpoints / Operations:** `[XX]`  
> **Contract Conformance Grade:** `[A / B / C / D / F]` (Score: `[XX]/100`)

---

## 1. Executive Summary
*Brief overview of the API architecture, contract coverage, and whether specification drift is present.*

---

## 2. 🚨 Breaking Changes & Contract Regressions
*Changes that will cause existing API consumers (mobile apps, web frontends, third parties) to fail.*

### Issue 1: [Issue Title]
- **Operation / Route:** `[METHOD /path/to/endpoint]`
- **Contract Spec:** `[docs/openapi.yaml#L123]`
- **Implementation Code:** `[src/controllers/user.ts#L45]`
- **Drift Description:** *[e.g., Renamed property 'user_id' -> 'id', or changed return type from array to paginated object]*
- **Remediation:**
```json
// ❌ Current Spec Expectation:
{ "user_id": "123" }

// ⚠️ Breaking Backend Payload:
{ "id": "123" }

// ✅ Recommended Non-Breaking Transformation:
{ "id": "123", "user_id": "123" }
```

---

## 3. ⚠️ Schema Drift & Undocumented Fields
*Fields or parameters supported in code but missing from official specifications, or vice-versa.*

| Endpoint | Parameter / Field | Drift Direction | Risk / Impact | Action Required |
| :--- | :--- | :---: | :--- | :--- |
| `POST /api/v1/auth/login` | `rememberMe` | In Code Only | Low | Add field to OpenAPI request body |
| `GET /api/v1/orders` | `trackingNumber` | In Spec Only | Medium | Implement field or remove from spec |

---

## 4. ⚡ Nullability & Type Inconsistencies
*Differences between schema type constraints (`required`, `nullable`, `enum`) and runtime database/application constraints.*

- [ ] **[Model/Route]**: `[Field]` - *[e.g. Marked required in schema, but can return null in DB]*

---

## 5. 🛡️ Security, Auth & Status Code Alignment
- **Auth Guard Audit:** *[Do all protected endpoints document security schemes (Bearer, Cookie, APIKey)?]*
- **Error Status Codes:** *[Are 400/401/403/404/422 responses formally modeled?]*
- **Sensitive Data Exposure:** *[Are internal DB columns (passwords, salts, tenant IDs) shielded from responses?]*
