---
id: pattern-rest-api
title: "REST API (Org: OpenAPI-first with FastAPI)"
type: pattern
category: communication
maturity: stable
tags: [pattern, stable, api, http, rest, openapi, fastapi]
applies_to:
  - "[[context-web-application]]"
prerequisites: []
related:
  - "[[standard-api-versioning]]"
conflicts_with: []
contradicted_by: []
sources:
  - "RESTful Web APIs (Richardson & Amundsen, 2013)"
  - "https://martinfowler.com/articles/richardsonMaturityModel.html"
  - "https://fastapi.tiangolo.com/"
  - "https://swagger.io/specification/"
---

## When to use

- Building APIs consumed by external or third-party clients where a widely understood contract matters.
- Multi-client systems (web, mobile, CLI) that benefit from a uniform interface and content negotiation.
- Defining boundaries between microservices where independent deployability and technology heterogeneity are goals.
- Exposing public-facing services where discoverability, self-documentation, and HTTP caching provide significant value.

## When NOT to use

- Real-time bidirectional communication (prefer WebSockets or Server-Sent Events).
- Internal high-throughput, low-latency service-to-service calls where binary protocols like gRPC reduce serialisation overhead and provide strict schema enforcement via Protobuf.
- Simple CRUD operations with no external consumers and no foreseeable need for a public contract -- a direct database integration or internal RPC may be simpler.
- Scenarios requiring complex, multi-entity mutations in a single interaction -- consider GraphQL or a dedicated command endpoint instead of forcing multiple round trips.

## Org guidance

- **All new APIs MUST define an OpenAPI 3.1 spec before writing implementation code.** This is spec-first, not code-first. The spec is the source of truth; implementation conforms to it.
- **FastAPI is the default framework for Python services.** See [[adr-0001-fastapi-as-default.org]] for rationale. Exceptions require an ADR explaining why FastAPI is inappropriate for the specific use case.
- **Auto-generated OpenAPI docs must be exposed at `/docs` (Swagger UI) and `/redoc`.** These endpoints must be available in all non-production environments. Production exposure is optional but recommended for internal APIs.
- **All request/response models must use Pydantic v2.** Do not use plain dictionaries or dataclasses for API boundaries. Pydantic models provide runtime validation, serialisation, and automatic schema generation that stays in sync with the OpenAPI spec.
- **API versioning follows [[standard-api-versioning]].** All endpoints must be served under a versioned path prefix (e.g. `/v1/`).

## Decision inputs

- **Who are the API consumers?** External developers need stable contracts, versioning, and thorough documentation. Internal teams may tolerate tighter coupling.
- **What are the latency requirements?** REST's text-based serialisation (JSON) and HTTP/1.1 overhead add measurable latency compared to binary protocols. Measure whether this matters for your P99.
- **Do you need hypermedia controls?** Richardson Maturity Level 3 (HATEOAS) adds discoverability but increases payload size and client complexity. Most teams operate effectively at Level 2 (HTTP verbs + resources).
- **What caching behaviour is expected?** REST over HTTP gives you ETags, Cache-Control, and conditional requests essentially for free. If your read-to-write ratio is high, this is a significant advantage.

## Solution sketch

The org workflow for building a new REST API is:

1. **Write the OpenAPI 3.1 spec.** Define paths, request bodies, response schemas, and error shapes in a YAML or JSON file. Review the spec in a pull request before any implementation begins.
2. **Generate Pydantic v2 models from the spec.** Use `datamodel-code-generator` or write them by hand, ensuring the models match the spec exactly. These models are the contract between the API layer and business logic.
3. **Implement FastAPI endpoints.** Each endpoint receives and returns Pydantic models. FastAPI auto-generates OpenAPI docs from these models, which must match the original spec.
4. **Validate against the spec in CI.** Run `openapi-diff` or equivalent tooling in the CI pipeline to ensure the generated OpenAPI output from FastAPI matches the source-of-truth spec. Drift fails the build.

```python
# Example: a minimal FastAPI endpoint following org conventions
from fastapi import FastAPI, status
from pydantic import BaseModel

app = FastAPI(title="Payments API", version="1.0.0")

class PaymentRequest(BaseModel):
    amount_cents: int
    currency: str
    idempotency_key: str

class PaymentResponse(BaseModel):
    payment_id: str
    status: str

@app.post(
    "/v1/payments",
    response_model=PaymentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_payment(request: PaymentRequest) -> PaymentResponse:
    ...
```

## Trade-offs

| Gain | Cost |
|------|------|
| Spec-first development catches contract mismatches before implementation begins | Writing and maintaining a separate OpenAPI spec adds upfront effort per endpoint |
| FastAPI standardisation reduces framework-choice debates and enables shared tooling | Teams with deep Flask or Django experience face a learning curve for async patterns |
| Pydantic v2 provides runtime validation and automatic schema generation | Strict model enforcement can slow down rapid prototyping if models must be defined first |
| Auto-generated docs at `/docs` and `/redoc` keep documentation in sync with code | Developers must still verify that generated docs match the source-of-truth spec |

## Implementation checklist

- [ ] Write an OpenAPI 3.1 spec and get it reviewed before writing any endpoint code
- [ ] Define all request and response models as Pydantic v2 `BaseModel` subclasses
- [ ] Implement endpoints in FastAPI, returning Pydantic models
- [ ] Verify `/docs` (Swagger UI) and `/redoc` endpoints are accessible
- [ ] Add a CI step that compares the FastAPI-generated OpenAPI schema against the source-of-truth spec
- [ ] Apply URL-path versioning per [[standard-api-versioning]]
- [ ] Use standard HTTP status codes and a consistent error response structure
- [ ] Add pagination to all list endpoints
- [ ] Implement rate limiting and return `429 Too Many Requests` with `Retry-After` header
- [ ] Enable CORS with an explicit allowlist if the API is consumed from browser clients

## See also

- [[adr-0001-fastapi-as-default.org]] -- decision record for choosing FastAPI
- [[standard-api-versioning]] -- org standard for URL-path versioning
- [[pattern-input-validation]] -- validate all input at the API boundary before it reaches business logic
