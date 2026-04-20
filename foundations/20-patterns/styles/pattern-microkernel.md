---
id: pattern-microkernel
title: Microkernel (Plugin)
type: pattern
category: style
maturity: stable
pillars:
  - "[[pillar-operational-excellence]]"
tags: [pattern, stable, style, plugin, extensibility]
applies_to:
  - "[[context-web-application]]"
prerequisites: []
related:
  - "[[pattern-layered-architecture]]"
  - "[[pattern-hexagonal-architecture]]"
conflicts_with: []
contradicted_by: []
sources:
  - "Software Architecture Patterns (Richards, 2015) ch. 3"
  - "https://www.oreilly.com/library/view/software-architecture-patterns/9781491971437/"
---

## When to use

- Products extended by third parties or customer-specific variants (IDEs, browsers, CMSs).
- Rule/workflow engines where domain logic changes faster than the core.
- Applications where features must be enabled, disabled, or versioned per tenant.
- Systems where core and extensions have different release cadences.

## When NOT to use

- Small applications with no plausible extension points.
- Hot-path features — plugin dispatch adds indirection and registry lookup cost.
- Systems where plugins need deep, unconstrained access to internal state.
- Domains with a single, stable feature set — layered is simpler.

## Decision inputs

- Plugin contract stability — changes break every extension.
- Trust level of plugin authors (first-party vs third-party sandboxing needs).
- Discovery mechanism (static registry, manifest scan, remote registry).
- Isolation boundary — in-process class, separate process, container.
- Versioning and compatibility policy between core and plugins.

## Solution sketch

A minimal **core system** provides essential shared services and a plugin API. **Plug-in modules** deliver feature-specific logic and are loaded by the core. Core knows nothing about specific plugins — only the contract. Plugins may know the core but not each other.

```
        [ plugin A ]   [ plugin B ]   [ plugin C ]
             \             |             /
              \            |            /
               [---  core system  ---]
                (registry + plugin API)
```

Contracts are usually interfaces plus a manifest. See Richards ch. 3 (linked) for registry, contract, and isolation guidance.

## Trade-offs

| Gain | Cost |
|------|------|
| Features ship independently of core releases | Plugin contract becomes a frozen interface — hard to evolve |
| Per-tenant or per-customer customisation | Registry, discovery, lifecycle, and versioning to maintain |
| Clear extension surface for third parties | Cross-plugin features awkward or impossible |
| Core stays small and stable | Debugging spans core + unknown plugin set |

## Implementation checklist

- [ ] Define the plugin contract (interfaces, lifecycle, extension points).
- [ ] Choose a discovery mechanism (manifest, registry, DI).
- [ ] Decide isolation level (in-process, subprocess, sandbox).
- [ ] Version the contract; document compatibility policy.
- [ ] Provide plugin-author documentation and a reference plugin.
- [ ] Log plugin load/unload and failures with plugin identity.
- [ ] Test core with zero plugins and with failing plugins.

## See also

- [[pattern-layered-architecture]] — alternative for non-extensible applications.
- [[pattern-hexagonal-architecture]] — related idea: isolate core from external variability.
- [[pattern-sidecar]] — out-of-process extension shape for richer isolation.
