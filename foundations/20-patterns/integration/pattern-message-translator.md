---
id: pattern-message-translator
title: Message Translator
type: pattern
category: integration
maturity: stable
pillars:
  - "[[pillar-operational-excellence]]"
tags: [pattern, stable, messaging, transformation, integration]
applies_to:
  - "[[context-web-application]]"
  - "[[context-event-driven-system]]"
prerequisites: []
related:
  - "[[pattern-anti-corruption-layer]]"
  - "[[pattern-content-based-router]]"
conflicts_with: []
contradicted_by: []
sources:
  - "EIP (Hohpe & Woolf, 2003) — https://www.enterpriseintegrationpatterns.com/patterns/messaging/MessageTranslator.html"
---

## When to use

- Producer and consumer use different message formats, schemas, or vocabularies.
- Integrating a legacy system whose shape you cannot change.
- Bridging protocols (XML ↔ JSON, Avro ↔ Protobuf) across a boundary.
- Normalising external-partner payloads into your canonical model.
- Enforcing a canonical event schema within a bounded context.

## When NOT to use

- Both sides already speak the same schema — translation adds no value.
- Transformation belongs inside the consumer as domain logic, not integration.
- Translation would hide a real modelling disagreement that should be resolved.
- Lossy translation risks losing fields critical to downstream consumers.

## Decision inputs

- Canonical vs point-to-point translation — one shared model or per-pair?
- Schema evolution policy on both sides — who breaks whom?
- Data loss tolerance — which fields can be dropped, defaulted, inferred?
- Translation engine — declarative mapping (JSLT, JOLT) vs code.
- Performance cost per message vs volume.
- Ownership: platform team or producing/consuming team?

## Solution sketch

A stateless stage between producer and consumer converts the message shape. The translator does not route, enrich from external sources, or make business decisions.

```
[Producer: schema A] -> [Translator] -> [Consumer: schema B]
```

- Prefer **declarative mappings** (JSLT, JOLT, XSLT, Avro converters) over hand-written code.
- Validate **both** the input and output against schemas — fail loud on drift.
- Version the mapping; keep old versions until all producers move.
- For cross-context integration, wrap the translator in an anti-corruption layer.
- Never bury translation inside a router — separate responsibilities.

## Trade-offs

| Gain | Cost |
|------|------|
| Decouples two systems with incompatible schemas | Extra hop and parse/serialise cost per message |
| Canonical model limits N×N mapping explosion | Canonical model can become a bottleneck and lowest-common-denominator |
| Localises schema evolution pain in one place | Silent field loss if mapping is not validated |
| Declarative mappings are easy to review and test | Complex business translations belong in code, not mapping DSL |

## Implementation checklist

- [ ] Choose declarative (JSLT, JOLT) over imperative where feasible.
- [ ] Validate input and output against schemas.
- [ ] Version mappings; keep old versions live during migrations.
- [ ] Test round-trip for every message type, including edge fields.
- [ ] Reject or DLQ on unmappable input — never silently drop fields.
- [ ] Emit metrics on translation failures and field-loss counts.
- [ ] Keep translator stateless for horizontal scaling.
- [ ] Document mapping ownership and schema change process.

## See also

- [[pattern-anti-corruption-layer]] — use a translator as the technical core of an ACL.
- [[pattern-content-based-router]] — often chained before/after a translator.
- [[pattern-publish-subscribe]] — translate once, fan out canonical events.
