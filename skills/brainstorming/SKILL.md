---
name: brainstorming
description: Use before non-trivial software product/design work. Turns a raw idea into approved, concise durable specs without starting implementation.
---

# Brainstorming

Turn a raw software idea into an approved design and durable specification before implementation begins.

## Hard Gate

Do not write substantial project code, scaffold the application, or delegate implementation to Developer until the intended behavior/design has been presented and approved by the user.

Planning artifacts are allowed before implementation. For a brand-new project, Main may create the project directory/repository after approval solely to store planning documents; do not scaffold product code at that stage.

## First: classify the request

Choose the lightest path that preserves correctness.

### 1. Spike

Use for feasibility/research questions where the output is knowledge, not production code.

Flow:

```text
frame the question -> get approval for the probe -> investigate -> report recommendation
```

Do not create durable product specs unless the user turns the finding into an implementation request.

### 2. Bounded change

Use when an existing system already contains the flow being changed and the requested behavior is narrow.

Examples: a small user-visible behavior change, a focused interaction change, a contained feature extension.

Flow:

```text
inspect context -> clarify only what matters -> present short design -> user approves -> write concise spec if observable behavior changes -> writing-plans
```

Purely mechanical work with no product/design decision should not have entered this skill; route it directly to Developer through Kanban.

### 3. Architectural / new project

Use for new products, new subsystems, broad features, new data models, or changes that affect long-lived interfaces/architecture.

Flow:

```text
understand intent -> research -> clarify -> compare approaches -> present design -> user approves -> write durable docs/spec -> writing-plans
```

When uncertain between bounded and architectural, choose architectural.

## Understand before proposing

For an existing repository:

- inspect relevant code, tests, documentation, and current conventions;
- follow established architecture unless there is a concrete reason not to;
- identify constraints that are already encoded in the repository;
- avoid unrelated cleanup or redesign.

For a new project:

- do not require a pre-existing repository to begin brainstorming;
- understand the product before choosing libraries or architecture;
- keep the initial scope deliberately small.

## Memory hygiene

Treat a fresh project or fresh brainstorming request as a clean product context by default.

Long-term memory, prior sessions, Wiki notes, and remembered project details are background context, not product requirements.

Rules:

- Do not silently reuse requirements, scope, architecture, feature choices, defaults, or product decisions from a previous project/session.
- Do not present remembered project details as if the user stated them in the current brainstorming session.
- Only carry prior project decisions forward when the user explicitly indicates they are continuing the same project, references the prior work, or explicitly confirms the remembered details.
- Stable user preferences may inform presentation or recommendations, but must not become product requirements unless they are relevant and confirmed.
- If remembered context appears relevant but project identity is uncertain, ask whether this is the same project before using it.
- For a clearly new project, ignore project-specific remembered details and derive the specification from the current conversation and repository only.

During brainstorming, keep three conceptual buckets separate:

```text
CONFIRMED    = explicitly stated or approved in the current project context
PROPOSED     = agent suggestions that still require approval
OUT OF SCOPE = not required for the current MVP unless the user asks for it
```

Never promote `PROPOSED` or remembered content into `CONFIRMED` without explicit approval.

## Research when facts matter

Use external research when a decision depends on current or uncertain facts such as:

- platform APIs and version support;
- library maturity or current recommendations;
- security/privacy constraints;
- protocol or service capabilities;
- ecosystem/tooling compatibility.

Research should answer a decision, not become an open-ended report. Prefer existing/native/platform-supported solutions over custom machinery when they satisfy the requirement.

## Clarification discipline

Ask questions only for decisions that materially affect the result.

- Ask one question at a time.
- Prefer concrete alternatives when possible.
- Focus on purpose, success criteria, constraints, non-goals, UX behavior, data ownership, and failure behavior.
- Do not ask the user to decide routine implementation details that Developer can safely choose later.
- Do not silently invent product requirements to fill gaps.
- Do not introduce unrequested features into the MVP merely because they are common or useful.
- When a conservative narrow default fully preserves the user's stated intent, prefer that default over opening an unnecessary product decision.
- Clearly label optional ideas as proposals rather than requirements.

If the request contains several independent products/subsystems, decompose the scope before refining details and start with the first independently useful slice.

## Explore approaches

When there is a meaningful design choice, present 2-3 viable approaches with trade-offs and a recommendation.

Do not manufacture fake alternatives for obvious decisions.

Apply YAGNI aggressively. The recommended design should be the smallest design that fully satisfies the approved behavior and constraints.

## Present the design

Scale the design to the task. Cover only the dimensions that materially matter:

- product behavior and key user flows;
- UX/state transitions;
- components and responsibilities;
- data ownership and persistence;
- external integrations;
- error/failure behavior;
- testing/verification strategy;
- compatibility or migration concerns.

For a bounded change, this may be a few paragraphs.

For architectural work, present the design in sections and allow the user to correct assumptions before finalizing it.

Do not move to implementation until the user explicitly approves the design.

## Durable artifacts

NormalPowers does not create `docs/superpowers/...`.

### New project

After the design is approved, create or update as needed:

```text
docs/product.md
docs/architecture.md
specs/initial-scope.md
```

`docs/product.md` should contain durable product truth only:

- purpose;
- target user/use case;
- primary workflows;
- scope and explicit non-goals;
- important product principles/constraints.

`docs/architecture.md` should contain durable architecture only:

- major components and boundaries;
- data flow and ownership;
- persistence and external interfaces;
- key technologies where they are architectural constraints;
- important testing/deployment constraints.

Do not turn either file into a chronological design diary.

### Existing product / feature

For a meaningful observable behavior change, create or update:

```text
specs/<feature-or-change>.md
```

Update `docs/product.md` only when long-lived product scope/principles change.

Update `docs/architecture.md` only when long-lived architecture changes.

Create an ADR in `docs/decisions/` only for a significant durable architectural decision whose rationale will matter later. Do not create ADRs for routine implementation choices.

## Specification format

A feature/scope spec should be concise and normative. Use this shape when applicable:

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

- Exact constraints that implementation must preserve.

## Out of Scope

- Explicitly excluded behavior when ambiguity is likely.
```

Rules:

- describe what the system must do, not the exact code Developer should write;
- every important requirement should be testable or observable;
- use concrete scenarios for edge cases and state transitions;
- avoid implementation details unless they are part of the required contract;
- avoid speculative future requirements;
- do not add sections that carry no useful information.

## Self-review before handoff

Before moving on, check the written artifacts for:

1. missing or contradictory requirements;
2. vague words that permit materially different implementations;
3. hidden scope expansion;
4. architecture choices unsupported by the approved design;
5. requirements that cannot be verified;
6. implementation detail accidentally presented as product truth;
7. remembered or proposed requirements that were never confirmed in the current project context.

Fix issues directly.

If writing the document introduces a new substantive decision that the user did not approve, present that decision and get approval before continuing.

## Transition

Once the durable specification is approved and internally consistent, load `normalpowers:writing-plans`.

Do not invoke an implementation skill and do not implement the plan in Main.
