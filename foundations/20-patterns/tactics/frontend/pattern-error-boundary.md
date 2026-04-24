---
id: pattern-error-boundary
title: Error Boundary
type: pattern
category: frontend
maturity: stable
pillars:
  - "[[pillar-reliability]]"
tags: [pattern, stable, frontend, react, fault-tolerance]
applies_to:
  - "[[context-web-application]]"
prerequisites: []
related:
  - "[[pattern-component-composition]]"
  - "[[pattern-circuit-breaker]]"
conflicts_with: []
contradicted_by: []
sources:
  - "React — Component (componentDidCatch, getDerivedStateFromError): https://react.dev/reference/react/Component"
---

## When to use

- Protecting a sub-tree where a render-time exception would crash the whole app.
- Third-party widgets or content whose failure shouldn't take the surrounding UI down.
- Routes or feature modules where you want per-feature fallbacks rather than one global crash screen.
- As a last-resort safety net — not a substitute for handling expected errors close to the source.

## When NOT to use

- Event handlers, async callbacks, server functions — boundaries only catch *render* errors.
- Blanket wrapping the app root alone — you lose per-feature isolation.
- Expected validation errors — handle those in component state, not a boundary.
- Pre-hooks class avoidance — boundaries still require class components (or a library) in React as of 2026.

## Decision inputs

- Granularity — per-route, per-feature, or per-widget boundary?
- Fallback content — graceful placeholder, retry affordance, or error report?
- Logging — does the boundary report the error to an observability sink?
- Reset strategy — does a route change or key change reset the boundary?

## Solution sketch

```jsx
class ErrorBoundary extends React.Component {
  state = { error: null }
  static getDerivedStateFromError(error) { return { error } }
  componentDidCatch(error, info) { logToSink(error, info) }
  render() { return this.state.error ? <Fallback/> : this.props.children }
}
```

Wrap feature sub-trees, not the whole app. Inside suspenseful routes pair with `<Suspense>`. Libraries like `react-error-boundary` give a hooks-friendly API.

## Trade-offs

| Gain | Cost |
|------|------|
| A single component's crash doesn't kill the app | Only catches render-time errors; async/event-handler bugs still escape |
| Each feature can fail independently with its own fallback | More boundaries = more fallback UI to design and maintain |
| Hook for structured error reporting | Suppressed errors can hide real bugs if logging is absent |

## Implementation checklist

- [ ] Wrap each top-level route in its own boundary; per-widget boundaries for risky trees.
- [ ] Report every caught error to your observability sink, including component stack.
- [ ] Fallback UI must provide a recovery action or at least communicate the failure.
- [ ] Reset boundary state on route change or on an explicit user action.
- [ ] Handle async errors at their source — boundaries won't save you there.
- [ ] Write tests that force a child to throw and assert the fallback renders.

## See also

- [[pattern-component-composition]] — boundaries are composable wrappers.
- [[pattern-circuit-breaker]] — the backend analogue for failing fast on a downstream.
