---
name: using-normalpowers
description: Session routing for Hermes Main. Applies NormalPowers to software product/design work while leaving unrelated and mechanical tasks alone.
---

# Using NormalPowers

NormalPowers is a planning workflow for the Main Hermes profile. It is not a general-purpose behavior layer and must not hijack unrelated work.

## Scope

Use NormalPowers when Main is handling software work that contains product, behavior, UX, architecture, or non-trivial design intent.

Typical triggers:

- a new application, service, library, or subsystem;
- a new user-facing feature;
- a change to observable behavior;
- a redesign of an existing flow;
- a meaningful architecture or data-model decision;
- a request whose desired product behavior is still ambiguous.

Do not start the full planning workflow for:

- non-software tasks;
- simple repository/status/log inspection;
- running an already-defined build or test command;
- an obvious compile fix with no product decision;
- a known dependency/version bump;
- a typo, literal-value change, or other mechanical edit;
- work whose desired behavior and implementation constraints are already fully specified.

Mechanical engineering work may be sent directly to Developer through Hermes Kanban.

## Role Boundary

Main owns:

- user interaction;
- discovery and research;
- product decisions;
- concise specifications;
- architecture decisions when required;
- implementation planning at the workstream level;
- Kanban delegation;
- final acceptance against the approved specification.

Developer owns substantial implementation.

Main must not replace Developer by writing substantial project code, performing the implementation plan itself, or spawning an alternative coding workflow when the normal durable path is available.

The default durable path is:

```text
User -> Main -> NormalPowers planning -> Kanban -> Developer -> evidence -> Main
```

## Routing Rule

When a software request matches the planning triggers above, load `normalpowers:brainstorming` before taking implementation action.

After brainstorming has produced an approved durable specification, load `normalpowers:writing-plans`.

Do not jump directly from an unresolved idea to Kanban implementation.

Do not create a second execution system. In particular, NormalPowers never transitions to Superpowers subagent-driven development, inline execution, or a Main-owned coding loop.

## Return Path

When Developer returns completion evidence through Kanban, Main checks it against the approved specification and relevant architecture constraints before accepting the work as complete.

Evidence should cover at least:

- what was implemented;
- relevant changed areas/files;
- tests and their results;
- lint/build/verification results where applicable;
- any deviation, unresolved issue, or follow-up.

If evidence shows a product/specification/architecture conflict, Main resolves the decision before further implementation. Developer must not silently redefine the requirement.

## Instruction Priority

Direct user instructions and profile/project instructions take precedence over this workflow.

If the user explicitly asks to skip or shorten planning for a specific task, obey that request unless doing so would make the task materially unsafe or impossible to understand.
