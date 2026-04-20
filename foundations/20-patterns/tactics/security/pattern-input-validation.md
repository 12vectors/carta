---
id: pattern-input-validation
title: Input Validation
type: pattern
category: security
maturity: stable
pillars:
  - "[[pillar-security]]"
  - "[[pillar-reliability]]"
tags: [pattern, stable, security, validation, injection-prevention]
applies_to:
  - "[[context-web-application]]"
prerequisites: []
related: []
conflicts_with: []
contradicted_by: []
sources:
  - "OWASP Input Validation Cheat Sheet -- https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html"
  - "Secure by Design (Johnsson et al., 2019) ch. 5"
---

## When to use

- Any system accepting external input: web apps, APIs, CLIs, message consumers, file uploads.
- At every trust boundary (client/server, service/service, app/database, system/third-party).
- On all structured data (JSON, XML, CSV) before parse/store/forward.

Input validation is never optional in a web application. The only question is where and how.

## When NOT to use

Never skip entirely. Differentiate by layer instead:

- Syntactic validation at the API boundary (shape, type, length, charset).
- Semantic validation in the domain layer (business rules).
- Parameterised queries / ORM constraints as a persistence safety net.

Collapsing layers leads to anaemic domains or bloated controllers.

## Decision inputs

- Input source (form, API, upload, queue, URL param) — each has a different attack surface.
- Allowlist patterns per field (denylists are brittle).
- Maximum size/depth limits — unbounded input is a DoS invitation.
- Downstream sink (SQL, HTML, shell, LDAP, filesystem) — determines required encoding.

## Solution sketch

Three layers:

1. **API boundary** — schema validator (JSON Schema, Zod, Joi, class-validator); reject with `422` and structured errors.
2. **Domain** — state-dependent rules (ownership, inventory, transitions).
3. **Output** — context-appropriate encoding (parameterised SQL, HTML-escape, URL-encode).

Canonicalise first (trim, Unicode NFC, case-fold) *before* validation to close Unicode-bypass holes. See OWASP source for the complete rule set.

## Trade-offs

| Gain | Cost |
|------|------|
| Blocks entire injection classes (SQLi, XSS, command, path traversal) | Validation must co-evolve with schema — new field without rules is a regression |
| Clear errors close to the source of the bug | Cross-field rules add latency and code |
| Predictable invariants downstream | Over-strict rules cause false rejections and UX friction |
| Reduces DoS surface from oversized payloads | Multi-layer validation risks duplication; requires discipline |

## Implementation checklist

- [ ] Allowlist-based schema validation on every boundary field.
- [ ] Explicit maximum lengths on strings, arrays, and file uploads.
- [ ] Canonicalise (trim, NFC, case-fold) before applying rules.
- [ ] Parameterised queries or ORM for all DB access — never string concat.
- [ ] HTML-encode all user data before browser rendering.
- [ ] Validate `Content-Type` and reject unexpected media types.
- [ ] Log validation failures without echoing raw malicious input.
- [ ] Automated tests with known-malicious payloads (SQLi, XSS, oversize).

## See also

- [[pattern-rest-api]] — input validation is the first concern at every REST boundary.
