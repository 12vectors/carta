---
id: pattern-input-validation
title: Input Validation
type: pattern
category: security
maturity: stable
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

- Any system that accepts external input -- this applies universally to web applications, APIs, CLI tools, message consumers, and file upload handlers.
- At every trust boundary: between the client and server, between services, between your application and the database, and between your system and third-party integrations.
- When accepting structured data (JSON, XML, CSV) that will be parsed, stored, or forwarded -- schema validation prevents malformed data from propagating through the system.

There is no scenario in a web application where input validation is optional. The decision is not whether to validate, but where and how.

## When NOT to use

There is no case where input validation should be skipped entirely. However, the validation strategy differs by layer:

- **API boundary (syntactic validation):** Validate structure, types, required fields, string lengths, and allowed character sets. Reject requests that do not conform to the API schema. This is the first line of defence.
- **Business logic (semantic validation):** Validate domain rules -- e.g., an order quantity must be positive, an end date must be after a start date. This belongs in the domain layer, not at the HTTP handler.
- **Persistence layer:** Use parameterised queries and ORM constraints as a final safety net, not as the primary validation mechanism.

Do not conflate these layers. Putting all validation in one place leads to either an anaemic domain model or a bloated controller.

## Decision inputs

- **What is the input source?** Browser forms, API payloads, file uploads, message queues, and URL parameters each have different attack surfaces and require different validation approaches.
- **What character sets are legitimate?** Define allowlists rather than denylists. For example, a username field might permit `[a-zA-Z0-9_-]` with a length of 3-30 characters. Denylists are brittle and inevitably incomplete.
- **What is the maximum expected size?** Set explicit limits on string lengths, array sizes, file sizes, and nested object depth. Unbounded input is an invitation for denial-of-service.
- **Is the input used in a sensitive context?** Input that ends up in SQL queries, HTML output, shell commands, LDAP queries, or file paths requires context-specific encoding or escaping in addition to validation.

## Solution sketch

Implement validation as a layered defence:

**Layer 1 -- Schema validation at the API boundary.** Use a schema validator (JSON Schema, Zod, Joi, class-validator) to enforce structural rules before the request reaches application code:

```
// Example: Zod schema for a create-order request
const CreateOrderSchema = z.object({
  productId:  z.string().uuid(),
  quantity:   z.number().int().min(1).max(10000),
  notes:      z.string().max(500).optional(),
});
```

Reject invalid requests with a `422 Unprocessable Entity` and a structured error response listing all violations.

**Layer 2 -- Domain validation in business logic.** Validate business rules that depend on application state: Does the product exist? Is there sufficient inventory? Is the user authorised to place this order? These checks live in service or domain objects.

**Layer 3 -- Output encoding.** Even after validating input, apply context-appropriate encoding before rendering. Use parameterised queries for SQL, HTML-encode output for browser rendering, and percent-encode values inserted into URLs.

**Canonical form first.** Normalise input before validation -- for example, trim whitespace, normalise Unicode (NFC), and convert to lowercase where appropriate. Validating before canonicalisation can allow bypasses where visually similar but technically distinct characters pass the check.

## Trade-offs

| Gain | Cost |
|------|------|
| Prevents entire categories of injection attacks (SQLi, XSS, command injection, path traversal) | Validation logic must be maintained alongside schema changes -- a new field without validation is a regression |
| Catches malformed data early, producing clear error messages close to the source of the mistake | Complex validation rules (especially cross-field dependencies) add latency and code complexity |
| Makes the system more predictable -- downstream code can rely on invariants established at the boundary | Overly strict validation can create false rejections and poor user experience if not carefully calibrated |
| Reduces the attack surface for denial-of-service via oversized or deeply nested payloads | Validation at multiple layers risks duplication; requires discipline to keep each layer focused on its concern |

## Implementation checklist

- [ ] Define allowlist-based validation rules for every field at the API boundary using a schema validation library
- [ ] Set explicit maximum lengths for all string inputs and maximum sizes for arrays and file uploads
- [ ] Canonicalise input (trim, normalise Unicode, case-fold where appropriate) before applying validation rules
- [ ] Use parameterised queries or an ORM for all database interactions -- never concatenate input into query strings
- [ ] HTML-encode all user-supplied data before rendering in browser output
- [ ] Validate `Content-Type` headers and reject unexpected media types
- [ ] Log validation failures with enough context for investigation but without logging the raw malicious input in full
- [ ] Add automated tests that submit known-malicious payloads (SQL injection strings, XSS vectors, oversized inputs) and verify they are rejected

## See also

- [[pattern-rest-api]] -- input validation is a critical concern at every REST API boundary
