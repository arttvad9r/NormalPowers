---
name: using-normalpowers
description: Route software product/design work through NormalPowers planning while leaving unrelated and fully mechanical work alone.
---

# Using NormalPowers

NormalPowers is a planning-first workflow for a Hermes profile acting as the software planner/orchestrator. It is deliberately role-name agnostic: `main`, `developer`, `android`, `backend`, `qa`, or any future profile names are deployment details, not workflow semantics.

## Scope

Use NormalPowers when software work contains unresolved product, behavior, UX, architecture, data-model, integration, or non-trivial design intent.

Typical triggers:

- a new application, service, library, or subsystem;
- a meaningful new feature;
- a change to observable behavior;
- a redesign of an existing flow;
- a significant architecture, persistence, API, or data-model decision;
- a request whose desired behavior or execution boundaries are still ambiguous.

Do not start the full planning workflow for:

- non-software tasks;
- simple repository/status/log inspection;
- running an already-defined build or test command;
- an obvious compile fix with no product/design decision;
- a known dependency/version bump;
- a typo, literal-value change, or other mechanical edit;
- work whose behavior, constraints, and execution path are already fully specified.

Fully mechanical engineering work may be routed directly to a suitable worker through Hermes Kanban.

## Role model

NormalPowers defines responsibilities, not profile names.

### Planner / orchestrator

The planning profile owns:

- user interaction and product clarification;
- external and repository research;
- product behavior and scope decisions;
- UX and failure behavior;
- technical architecture and significant technology choices;
- data models, cross-component contracts, and integration boundaries;
- durable specifications and architecture documentation;
- implementation strategy, sequencing, dependencies, and task decomposition;
- worker routing;
- acceptance against the approved artifacts.

The planner should front-load decisions so execution workers have little reason to improvise. For a new project or major feature, using the strongest available reasoning model for this role is recommended; execution workers can then use cheaper models against a stable plan.

### Workers

Workers execute already-decided slices of work. They own:

- implementation within the assigned scope;
- project-appropriate tests/build/lint/verification;
- concise evidence of what changed and what passed.

Workers may choose only local, reversible details that do not affect product behavior, persisted-data semantics, architecture boundaries, external dependencies, public interfaces/contracts, cross-task integration, acceptance criteria, or task decomposition.

If a material decision is missing or the task conflicts with approved artifacts, the worker stops and returns the issue to the planner through the durable Kanban path instead of redesigning or silently widening scope.

## Routing rule

When a request matches the planning triggers, load `normalpowers:brainstorming` before implementation or implementation delegation.

After brainstorming has produced approved and internally consistent durable artifacts, load `normalpowers:writing-plans`.

Do not jump from a raw idea directly to an implementation worker. Do not create a second execution system such as Superpowers subagent-driven development or an inline coding loop owned by the planner.

## Kanban model

For substantial work, the execution plan should become a native Kanban dependency graph of independently verifiable leaf tasks. The planner performs decomposition before task creation; Kanban auto-decomposition should not make a second set of planning decisions.

A single bounded change may remain one implementation card.

Assignees are chosen from the currently available profile/worker roster according to capability and deployment configuration. Never hardcode a literal worker profile name in the workflow.

For multi-task work, prefer an explicit downstream integration/QA/acceptance task that depends on the terminal implementation tasks. For a single bounded task, same-card `kanban_request_review` is a valid review model. Follow one review model per task graph; do not duplicate both.

## Return and evidence

Every executable task should require evidence appropriate to its scope, normally including:

- implementation summary;
- relevant changed areas/files;
- tests/checks executed and results;
- build/lint/static-analysis results when applicable;
- deviations, unresolved issues, or follow-ups.

The acceptance step verifies implementation and evidence against the approved specification, architecture, and task contracts. Product/spec/architecture conflicts return to planning; workers do not silently redefine requirements.

## Instruction priority

Direct user instructions and profile/project instructions take precedence over this workflow.

If the user explicitly asks to skip or shorten planning for a specific task, obey unless that would leave material behavior or safety-critical constraints undefined.
