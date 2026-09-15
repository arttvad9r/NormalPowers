---
name: writing-plans
description: Use after an approved spec to create a concise implementation brief and hand work to Developer through Hermes Kanban.
---

# Writing Plans

Create an implementation brief that is detailed enough for Developer to execute confidently, but not so detailed that Main pre-implements the task on paper.

The plan is operational state. By default it belongs in the Kanban handoff, not in a permanent `docs/plans/` archive.

## Preconditions

Before planning implementation:

- the intended product behavior must already be approved;
- the durable specification must exist when the task changes observable behavior;
- relevant architecture constraints must be known;
- unresolved product decisions must be returned to the user/Main planning loop, not guessed here.

If those conditions are not true, return to `normalpowers:brainstorming`.

## Main / Developer boundary

Main decides and records:

- what outcome must be produced;
- which approved spec(s) and architecture constraints govern the work;
- meaningful workstreams and dependencies;
- how the result will be verified;
- what evidence Developer must return.

Developer decides routine, reversible implementation details.

Do not prescribe exact code, line numbers, private function names, or step-by-step edits unless an exact implementation detail is itself an approved constraint.

## Build the implementation brief

Inspect the repository enough to identify the major workstreams and existing conventions. Do not duplicate the repository exploration Developer will need during execution.

Use this shape:

```markdown
# <Task> — Implementation Brief

## Goal

One concise statement of the implementation outcome.

## Source of truth

- Spec: `specs/...`
- Product: `docs/product.md` (when relevant)
- Architecture: `docs/architecture.md` / ADRs (when relevant)

## Workstreams

### 1. <Area>

Outcome to implement.

Verification:
- test/check that proves this workstream is correct.

### 2. <Area>

Outcome to implement.

Verification:
- test/check that proves this workstream is correct.

## Constraints

- approved constraints copied or referenced from the spec/architecture;
- no unrelated redesign or refactoring;
- preserve compatibility requirements.

## Decision boundary

Developer may choose local reversible implementation details consistent with the approved artifacts.

Developer must stop/block and return the decision to Main if implementation requires:
- changing approved product behavior;
- expanding or narrowing scope;
- changing an architectural boundary;
- adding a significant new external dependency;
- changing a public API/schema/protocol contract;
- a destructive or irreversible migration;
- ignoring or weakening an approved requirement.

## Final verification

Run the project-appropriate test/lint/build checks and verify every relevant scenario from the approved spec.

## Completion evidence

Return through Kanban:
- implementation summary;
- changed areas/files;
- tests executed and results;
- lint/build/verification results;
- deviations, unresolved issues, or follow-ups.
```

## Plan quality

A good plan describes outcomes and verification, not keystrokes.

Prefer:

```text
Add persistence support for removing the latest intake.
Verification: deletion and total-recalculation tests.
```

Avoid:

```text
Open FooRepository.kt, add method X at line 84, create MutableStateFlow Y...
```

Developer is an engineering profile, not a blind script runner.

Keep the number of workstreams small. Split only when the pieces are independently meaningful, have different verification, or have a real dependency boundary.

## Kanban handoff

After the brief is ready, create a Hermes Kanban task assigned to the `developer` profile using the native Kanban tooling (normally `kanban_create`).

The card should include:

- repository/path;
- task goal;
- source-of-truth spec path(s);
- architecture/ADR references when relevant;
- the concise implementation brief;
- constraints and decision boundary;
- required completion evidence.

Do not paste the full contents of durable specs into the card. Reference them by path so there is one source of truth.

Do not ask Kanban to auto-decompose an already planned task. NormalPowers assumes meaningful decomposition was performed here.

If the native Kanban tool is unavailable, report the handoff problem instead of implementing the task in Main.

## Stop after delegation

Once the Kanban task has been created successfully:

- do not implement it in Main;
- do not spawn coding subagents as an alternative execution path;
- do not create Superpowers execution sessions;
- wait for the normal durable Developer -> Kanban evidence -> Main return path.

When evidence returns, Main verifies it against the approved spec and architecture constraints before accepting completion.
