---
name: writing-plans
description: Use after approved, internally consistent specs/architecture to write a living execution design and materialize it as a Hermes Kanban dependency graph for workers.
---

# Writing Plans

Turn approved product and architecture artifacts into an execution design whose worker tasks require minimal independent design decisions.

The plan and Kanban have different jobs:

- `plans/<feature>.md` is the single living execution design for the active project/feature;
- Hermes Kanban is the execution graph/state: assignees, dependencies, progress, blockers, review handoffs, and evidence.

Do not make Kanban cards the only place where project-wide sequencing, shared interfaces, invariants, or decomposition rationale exist.

## Preconditions

Before execution planning:

- intended product behavior is approved;
- durable specs exist for observable behavior changes;
- significant architecture/technology decisions are recorded;
- persistent-data semantics and cross-component contracts needed for implementation are decided;
- unresolved material product or architecture choices have been closed;
- the artifacts pass the NormalPowers consistency audit.

If not, return to `normalpowers:brainstorming`.

## Planner / worker boundary

The planner decides and records:

- implementation strategy and order;
- task boundaries and dependencies;
- which worker capability each task needs;
- significant technologies and architectural patterns;
- shared data structures/contracts and integration points;
- migration/compatibility rules;
- acceptance criteria and required verification;
- where integration, QA, or final acceptance occurs.

Workers execute assigned slices. A worker may choose only local, reversible details that do not change approved behavior, persisted-data semantics, architecture boundaries, external dependencies, public/cross-task contracts, acceptance criteria, or task decomposition.

If implementation exposes a missing material decision, the worker must stop/block and return it to the planner. "Figure it out" is not an acceptable hidden requirement for a worker task.

The plan should be detailed enough that a cheaper worker model can execute its slice without reconstructing the project's architecture or reasoning.

## Write the living execution design

Create or update one non-chronological plan at:

```text
plans/<feature>.md
```

For a greenfield project, use a stable scope name such as `plans/initial-implementation.md`. For a substantial later feature, use a descriptive feature name. Do not create a dated plan archive by default.

The plan is version-controlled while the work is active, but it is not normative product truth. Product behavior remains in `specs/` / product docs; architecture remains in architecture docs / ADRs.

The execution design should contain the project-wide information that would otherwise be fragmented across cards:

```markdown
# <Feature / project> execution design

## Objective
What the implementation must deliver and which approved specs define success.

## Source of truth
- product/spec paths
- architecture/ADR paths

## Implementation strategy
High-level technical approach and why this ordering/decomposition was chosen.

## Shared contracts and invariants
Cross-task data models, APIs, interfaces, persistence rules, compatibility rules, state-flow rules, or other invariants every affected worker must preserve.

## Workstreams and ordering
### W1 — <name>
- outcome
- dependencies
- important implementation constraints
- verification

### W2 — <name>
...

## Dependency graph
Human-readable overview of which workstreams can run in parallel and which must wait.

## Integration strategy
How independently implemented slices come together and where shared-contract compatibility is checked.

## Acceptance strategy
Project-level checks that must pass after all implementation slices complete.

## Kanban mapping
Map each workstream/plan section to its executable Kanban task title/ID once created.
```

Keep rationale where it helps future workers understand boundaries or ordering. Do not turn the plan into line-by-line coding instructions.

If planning changes materially during execution, update this file first (and durable specs/architecture when those truths changed), then reconcile affected Kanban cards/dependencies. The plan should describe the current execution design, not preserve obsolete branches of thought.

After acceptance, retain, archive, move, or delete the plan according to project policy. It may remain useful project context, but it never overrides current specs, architecture, code, or tests.

## Build the execution graph

Inspect the repository enough to understand the current implementation and identify an efficient dependency graph.

For a substantial new project or broad feature, decompose into a small set of independently executable, independently verifiable tasks. Typical scale is roughly 4-10 leaf tasks, but use the structure the work actually requires.

A good task is:

- large enough to produce a coherent outcome;
- small enough that one worker does not need to re-plan the project internally;
- explicit about why it exists and how it fits the whole;
- explicit about dependencies and shared contracts;
- independently testable or verifiable;
- narrow enough to avoid unrelated redesign.

Avoid both extremes:

- one giant `Implement the whole project` card;
- file/function-level micromanagement such as one card per entity, method, or UI component.

A bounded change that is already coherent and independently verifiable may remain one card.

## Task card contract

Each executable Kanban card should contain enough context to execute without inventing missing project decisions:

```markdown
# <Task title>

## Goal
Concrete outcome this task must produce.

## Why
How this task contributes to the approved product/architecture and what downstream work depends on it.

## Source of truth
- Spec: `specs/...`
- Product: `docs/product.md` when relevant
- Architecture/ADR: `docs/architecture.md`, `docs/decisions/...`
- Execution design: `plans/<feature>.md#<specific-section>`

## Dependencies / inputs
- prerequisite task IDs or existing components;
- exact contracts/interfaces/data assumptions this task consumes.

## Scope
- implementation outcomes included in this card;
- explicit exclusions when scope could be confused with adjacent work.

## Decided technical constraints
- selected technologies/patterns relevant to this task;
- data structures, interfaces, invariants, or integration contracts it must preserve;
- migration/compatibility constraints.

## Acceptance criteria
Observable conditions that make the task complete.

## Verification
Tests/build/lint/manual checks required for this slice.

## Evidence
Return through Kanban:
- implementation summary;
- relevant changed files/areas;
- verification commands/checks and results;
- deviations, blockers, or follow-ups.

## Decision boundary
Do not redesign, re-scope, change shared contracts, add significant dependencies, or weaken requirements. If a material missing decision is discovered, block/escalate it to the planner.
```

Reference durable artifacts and the exact relevant plan section by path rather than copying them wholesale.

## Materialize the Kanban graph

Use native Hermes Kanban to materialize the already-written execution design. Kanban is execution state, not the sole plan artifact.

### Assignee routing

`kanban_create` requires an explicit assignee. Select the best-fit worker/profile from the currently available Hermes roster and its capability descriptions or from deployment-specific routing instructions.

Never assume a literal profile name such as `developer`. If no suitable assignee can be resolved from the current environment, report/block the handoff instead of inventing one.

### Dependencies

Create tasks in a dependency-aware order. Use `parents=[...]` on `kanban_create` (or `kanban_link` when linking after creation) so downstream work remains `todo` until prerequisites complete.

Examples:

```text
foundation ─┬─> data/persistence ─┬─> feature flows ─┐
            └─> app shell/UI ─────┘                 ├─> integration/acceptance
                                                    └─> final verification
```

Parallelize only when tasks do not depend on undecided shared contracts or overlapping edits that make parallel work unsafe.

Do not ask Kanban triage/auto-decomposition to decompose the plan again. The planner already owns decomposition.

Use a shared tenant/project namespace when the deployment benefits from isolating several simultaneous projects.

After task creation, update the plan's `Kanban mapping` with returned task IDs so the overview and executable graph stay traceable without duplicating task state into the plan.

## Review and acceptance topology

Choose one native Kanban review model for the work graph.

### Multi-task project: downstream acceptance task (default)

For substantial work, pre-create an integration/QA/acceptance task whose `parents` are the terminal implementation tasks. Assign it to the planning/orchestration profile or to an explicitly configured reviewer/QA profile.

Implementation workers then finish their leaf cards with `kanban_complete` plus structured evidence. The downstream acceptance task becomes ready only when its parents are done, and verifies the assembled result against the approved specs, architecture, execution design, and project-level acceptance criteria.

This is normally preferable to sending every leaf card back through an expensive planning model.

### Single bounded task: same-card review

For a single implementation card, `kanban_request_review(summary=..., metadata=..., reviewer=...)` may hand the task to the planner or configured reviewer before final completion.

Do not also create a downstream review child for the same task. Hermes supports both review models, but combining them duplicates or strands review work.

## Final project acceptance task

For a new project or broad feature, the final acceptance/QA card should verify at minimum:

- all relevant scenarios and requirements from durable specs;
- integration between completed slices;
- required build/test/lint/static-analysis checks;
- migration/persistence behavior where applicable;
- no unapproved scope expansion or architecture drift;
- execution matches the current plan's shared contracts and integration strategy;
- unresolved deviations are surfaced rather than silently accepted.

If acceptance finds a defect or contract violation, create or return concrete rework through Kanban. If it reveals a missing product/architecture decision, return to planning before further implementation.

## Stop after delegation

Once the plan and graph have been created successfully:

- do not implement them in the planning profile;
- do not spawn an alternative coding/subagent execution system;
- let workers execute the planned cards and report evidence through Kanban;
- resume planning only for blocked material decisions, changed requirements, plan reconciliation, or final acceptance.
