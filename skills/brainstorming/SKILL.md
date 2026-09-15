---
name: brainstorming
description: Use before non-trivial software product/design work. Turns a raw idea into approved product, architecture, and concise durable specs before execution planning.
---

# Brainstorming

Turn a raw software idea into an approved design and sufficiently decided architecture before implementation begins.

## Hard gate

Do not write substantial project code, scaffold the product, or delegate implementation until the intended behavior and significant design/architecture have been presented and approved by the user.

Planning artifacts are allowed before implementation. For a brand-new project, the planner may create the project directory/repository after approval solely to store planning documents; do not scaffold product code at that stage.

## First: classify the request

Choose the lightest path that preserves correctness.

### 1. Spike

Use for feasibility/research questions where the output is knowledge rather than production implementation.

```text
frame the question -> investigate -> report recommendation
```

Do not create durable product specs unless the user turns the finding into an implementation request.

### 2. Bounded change

Use when an existing system already contains the flow being changed and the requested behavior is narrow.

```text
inspect context -> clarify material ambiguity -> decide design -> user approval -> concise spec/architecture update if needed -> writing-plans
```

Purely mechanical work with no product/design decision should not have entered this skill.

### 3. Architectural / new project

Use for new products, new subsystems, broad features, new persistent data models, or changes that affect long-lived interfaces/architecture.

```text
understand intent -> research -> clarify product choices -> decide architecture -> present design -> user approval -> durable artifacts -> writing-plans
```

When uncertain between bounded and architectural, choose architectural.

## Scope discipline

Maintain three explicit buckets throughout planning:

- **Confirmed** — behavior, constraints, and goals stated or approved by the user in the current planning conversation. A previous-session item enters this bucket only after the user explicitly asks to reuse it or re-confirms it.
- **Proposed** — an optional product idea or alternative awaiting user approval. It is not a requirement.
- **Out of Scope** — behavior not required for the current scope. Unrequested adjacent features belong here by default.

Never promote an unrequested feature into the MVP. Do not turn common adjacent ideas such as export, sync, recurring operations, themes, analytics, or advanced filters into requirements merely because similar products often contain them.

Prefer the narrowest product that fully satisfies Confirmed behavior.

## Session and memory boundary

Treat a new raw product request as a clean product scope unless the user explicitly says to continue, reuse, or modify a named earlier design/specification.

- Memory, prior sessions, Wiki notes, and unrelated repository history may inform research, but they are never Confirmed requirements by themselves.
- Do not say or imply that saved context has supplied current requirements.
- Do not copy old answers into the current MVP.
- If prior material seems relevant but reuse was not requested, ignore it for scope.
- When reuse is explicitly requested, summarize candidate prior decisions as Proposed and re-confirm the material ones before treating them as current truth.

## Understand before deciding

For an existing repository:

- inspect relevant code, tests, docs, build files, and current conventions;
- preserve established architecture when it remains suitable;
- identify existing contracts and migration constraints;
- avoid unrelated cleanup or redesign.

For a new project:

- do not require a pre-existing repository to begin planning;
- understand the product before choosing the stack;
- keep scope deliberately small;
- deliberately choose enough of the technical foundation that workers do not need to invent it later.

## Research before technical decisions

Research current external facts whenever they materially affect the design, including:

- platform APIs and version support;
- current official architecture guidance;
- library/tool maturity and compatibility;
- security/privacy constraints;
- persistence or protocol choices;
- ecosystem/tooling limitations.

Research should answer concrete decisions. Prefer native, official, mature solutions over custom machinery when they satisfy the requirement.

## Planner decision authority

The planner is expected to make high-quality technical decisions, not defer them wholesale to execution workers.

For significant work, decide and document as applicable:

- target platform/runtime and supported versions;
- major technologies/libraries where the choice affects the architecture;
- module/component boundaries and responsibilities;
- data ownership, persistent model, and important invariants;
- public/internal cross-component interfaces and contracts;
- error/failure and migration behavior;
- integration strategy and ordering constraints;
- testing/verification strategy;
- constraints that downstream workers must preserve.

Do not ask the user to choose routine technical details merely to avoid responsibility. Escalate a technical choice to the user when it materially changes product behavior, UX, cost, privacy, irreversible constraints, maintenance burden, or an explicit user preference.

Concrete architectural choices are appropriate in `docs/architecture.md` when the planner has researched and intentionally selected them. Do not over-specify private code structure, line-level edits, or details that have no cross-task consequence.

## Clarification discipline

Ask only for decisions that materially affect product behavior, data ownership/semantics, meaningful UX, important trade-offs, or acceptance criteria.

- Ask one material product decision at a time.
- Prefer concrete alternatives when useful.
- State current Confirmed scope and conservative defaults before asking the next question.
- Do not ask about unrequested adjacent features; keep them Out of Scope unless their absence blocks Confirmed behavior.
- Do not ask the user to decide routine engineering implementation details that the planner can resolve through research.
- Do not use remembered prior-session requirements to answer a current clarification question.

## Explore real alternatives

When there is a meaningful product or architectural choice, compare 2-3 viable approaches with trade-offs and make a recommendation.

Do not manufacture fake alternatives for obvious decisions. Apply YAGNI aggressively.

## Present the design for approval

Before implementation, present a concise design that lets the user verify intent without drowning them in engineering trivia.

Include as applicable:

- Confirmed product scope and explicit non-goals;
- key user flows and failure behavior;
- significant architecture and technology decisions;
- data ownership/persistence semantics;
- meaningful integrations/contracts;
- important trade-offs or constraints;
- verification strategy.

Product suggestions still awaiting approval remain Proposed and must not be smuggled into the design.

Do not move to execution planning until the user explicitly approves the product/design direction.

## Durable artifacts

NormalPowers does not create `docs/superpowers/...`.

### New project

After approval, create or update as needed:

```text
docs/product.md
docs/architecture.md
specs/initial-scope.md
```

`docs/product.md` contains durable product truth:

- purpose and target user/use case;
- primary workflows;
- approved scope;
- explicit non-goals;
- important product principles and behavioral rules.

`docs/architecture.md` contains durable technical truth needed to constrain execution:

- selected platform/stack and significant technologies;
- major components/modules and responsibilities;
- data model, ownership, persistence, and important invariants;
- cross-component/external interfaces;
- migration/compatibility constraints;
- testing/deployment constraints that shape implementation;
- rationale for significant choices when it prevents later re-litigation.

Use ADRs under `docs/decisions/` only for significant durable decisions whose alternatives/rationale will matter later.

### Existing product / feature

For meaningful observable behavior changes, create or update:

```text
specs/<feature-or-change>.md
```

Update product/architecture docs only when their long-lived truth actually changes.

## Specification format

Use concise normative specs. A useful default shape is:

```markdown
# <Feature or Scope>

## Goal

Why this exists and what outcome it must produce.

## Requirements

### <Requirement name>

Observable, testable behavior.

## Scenarios

### <Scenario name>

Given ...
When ...
Then ...

## Constraints

- Exact constraints implementation must preserve.

## Out of Scope

- Explicitly excluded behavior when ambiguity is likely.
```

Rules:

- describe what the system must do, not private code mechanics;
- every important requirement should be observable or verifiable;
- make edge cases and state transitions concrete where ambiguity matters;
- include implementation constraints only when they are part of the approved contract or architecture;
- avoid speculative future requirements;
- omit sections that carry no useful information.

## Decision and consistency audit

Before execution planning, explicitly audit the artifacts:

1. Every material product behavior is Confirmed or clearly Out of Scope.
2. Every significant technical choice needed by workers is decided or intentionally delegated as a harmless local detail.
3. No important cross-task interface, persistent-data rule, migration rule, or dependency boundary is left for a worker to invent.
4. Product, spec, and architecture documents do not contradict each other.
5. No Proposed or remembered requirement was silently promoted to approved truth.
6. Acceptance-relevant requirements are testable/verifiable.
7. Concrete technology choices are supported by research or existing project constraints.

If a new product decision appears while writing the docs, return it to the user. If a new technical decision appears, research and resolve it here unless it crosses the user-escalation boundary above.

## Transition

Once the approved durable artifacts are internally consistent and material design decisions are closed, load `normalpowers:writing-plans`.

Do not implement the project in the planning profile.
