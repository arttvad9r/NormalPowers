---
name: writing-plans
description: Use after approved, internally consistent specs/architecture to create an explicit execution plan and materialize it as a Hermes Kanban dependency graph for workers.
---

# Writing Plans

Turn approved product and architecture artifacts into an execution plan whose worker tasks require minimal independent design decisions.

The execution plan is operational state. By default, materialize it in Hermes Kanban rather than maintaining a permanent chronological `docs/plans/` archive.

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

## Build the execution plan

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

Reference durable artifacts by path rather than copying them wholesale.

## Materialize the Kanban graph

Use native Hermes Kanban as the execution plan.

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

## Review and acceptance topology

Choose one native Kanban review model for the work graph.

### Multi-task project: downstream acceptance task (default)

For substantial work, pre-create an integration/QA/acceptance task whose `parents` are the terminal implementation tasks. Assign it to the planning/orchestration profile or to an explicitly configured reviewer/QA profile.

Implementation workers then finish their leaf cards with `kanban_complete` plus structured evidence. The downstream acceptance task becomes ready only when its parents are done, and verifies the assembled result against the approved specs, architecture, and project-level acceptance criteria.

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
- unresolved deviations are surfaced rather than silently accepted.

If acceptance finds a defect or contract violation, create or return concrete rework through Kanban. If it reveals a missing product/architecture decision, return to planning before further implementation.

## Stop after delegation

Once the graph has been created successfully:

- do not implement it in the planning profile;
- do not spawn an alternative coding/subagent execution system;
- let workers execute the planned cards and report evidence through Kanban;
- resume planning only for blocked material decisions, changed requirements, or final acceptance.
