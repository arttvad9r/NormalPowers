# NormalPowers

NormalPowers is a planning-first workflow plugin for Hermes Agent. It separates **high-quality software planning** from **lower-cost execution** without hardcoding profile names.

```text
User
  -> planner/orchestrator (NormalPowers)
  -> approved product + architecture + specs
  -> living execution design in plans/<feature>.md
  -> Kanban dependency graph
  -> worker(s)
  -> integration / acceptance
```

The profile currently called `main`, `developer`, `android`, `backend`, `qa`, or anything else is just deployment configuration. NormalPowers reasons in roles: **planner** and **workers**.

It is inspired by the planning discipline of [Superpowers](https://github.com/obra/superpowers), but intentionally replaces Superpowers' execution layer with native Hermes Kanban.

## Core idea

Front-load important decisions into the planner, then make worker execution as mechanical as practical.

The planner owns:

- discovery and research;
- product/UX decisions;
- technical architecture and significant technology choices;
- durable product/spec/architecture artifacts;
- shared data/contracts and integration boundaries;
- the living execution design;
- implementation strategy and task decomposition;
- Kanban routing and dependencies;
- project-level acceptance.

Workers own:

- implementation of already-decided slices;
- required tests/build/lint/verification;
- structured evidence.

Workers do **not** own product design, architecture redesign, scope expansion, cross-task contract changes, or hidden re-decomposition of a giant project request.

## Recommended model split

For a brand-new project or major architectural change, run the planning profile on the strongest reasoning model you are willing to spend on. That is where ambiguity, research, architecture, data semantics, sequencing, decomposition, and acceptance criteria are resolved.

Once the plan is stable, execution cards can be assigned to cheaper worker models because each card should already explain **what**, **why**, **constraints/contracts**, **dependencies**, and **how completion is verified**.

NormalPowers does not hardcode model names or prices; this is a deployment recommendation.

## What the workflow does

For non-trivial software work NormalPowers:

1. understands the user's intent;
2. treats fresh product requests as clean scope rather than importing old memory as requirements;
3. researches current platform/library/tooling facts when they affect decisions;
4. clarifies one material product decision at a time;
5. separates Confirmed, Proposed, and Out-of-Scope behavior;
6. makes significant technical architecture decisions in the planning stage;
7. gets user approval for the product/design direction;
8. writes concise durable product/spec/architecture artifacts;
9. audits those artifacts for missing decisions and contradictions;
10. writes or updates one living execution design under `plans/<feature>.md`;
11. turns that design into an explicit dependency graph of executable work;
12. materializes that graph as native Hermes Kanban tasks;
13. routes each task to a suitable worker profile by capability rather than by a hardcoded name;
14. finishes through a native Kanban review/acceptance topology.

NormalPowers does not make the planner a coding agent and does not use Superpowers subagent-driven execution.

## Install

Install NormalPowers into whichever Hermes profile acts as the planner/orchestrator:

```bash
HERMES_HOME=~/.hermes/profiles/<planner-profile> \
  hermes plugins install arttvad9r/NormalPowers --enable
```

For a production setup, prefer pinning a reviewed full commit SHA:

```bash
HERMES_HOME=~/.hermes/profiles/<planner-profile> \
  hermes plugins install arttvad9r/NormalPowers \
  --ref <reviewed-40-character-commit-sha> --enable
```

Then restart the affected Hermes gateway/profile as appropriate and start a **fresh planner session**. NormalPowers registers a cache-safe Hermes system-prompt section; existing session prompts are not rewritten by a plugin update.

Do not install NormalPowers into execution-only workers unless you intentionally want those profiles to act as planners too. Worker constraints are carried in project artifacts, the execution design, and Kanban cards.

### Verify

```bash
HERMES_HOME=~/.hermes/profiles/<planner-profile> \
  hermes plugins doctor normalpowers --ci
```

```bash
HERMES_HOME=~/.hermes/profiles/<planner-profile> \
  hermes plugins list
```

## Kanban configuration

NormalPowers assumes planning/decomposition happens **before** work reaches workers. Keep Kanban auto-decomposition disabled:

```yaml
kanban:
  auto_decompose: false
```

Profile names, orchestrator profile, and default worker routing belong to Hermes deployment configuration, not to this plugin.

`kanban_create` itself requires an explicit assignee. During planning, NormalPowers selects a suitable profile from the currently available Hermes roster/capability descriptions or from explicit deployment instructions. It never assumes a profile literally named `developer`.

## Execution design vs Kanban

NormalPowers deliberately separates the unified plan from execution state.

### `plans/<feature>.md`

This is the **single living execution design** for an active project or substantial feature. It is non-chronological: update the same file when the implementation strategy changes instead of creating a dated archive by default.

It should preserve the project-wide context that would be awkward or fragmented across Kanban cards:

- objective and source-of-truth references;
- implementation strategy and ordering rationale;
- workstreams;
- shared interfaces/contracts;
- cross-task invariants;
- dependency graph;
- integration strategy;
- acceptance strategy;
- mapping from plan sections to Kanban task IDs.

For a greenfield project, a stable name such as `plans/initial-implementation.md` is appropriate. For a later broad feature, use a descriptive feature name.

The plan is version-controlled while work is active, but it is **not** product truth. If it conflicts with specs or architecture, the durable product/architecture artifacts win and the plan must be reconciled.

After acceptance, the project may keep, archive, move, or delete the plan according to its own policy. It can remain useful context without becoming a permanent chronological plan log.

### Hermes Kanban

Kanban stores execution state:

- concrete leaf tasks;
- explicit dependencies;
- assignees;
- ready/running/blocked/review/done state;
- handoffs;
- review/acceptance routing;
- structured evidence.

Each worker card references the exact relevant section of `plans/<feature>.md` plus the durable spec/product/architecture files. Kanban should not be the only location where shared design rationale or cross-task contracts exist.

## What Kanban should look like

A substantial project should not arrive at a worker as one card saying `Implement the whole project`.

Instead the planner first defines the workstreams in the execution design and then creates a dependency graph of coherent, independently verifiable slices, for example:

```text
Foundation
   ├──> Persistence / data contracts ──┐
   └──> App shell / navigation ────────┤
                                       ├──> Core feature flows
                                       │        ├──> Budgets
                                       │        └──> History / editing
                                       └───────────────┬──────────────
                                                       v
                                             Integration / acceptance
```

Each worker card contains:

- **Goal** — the concrete outcome;
- **Why** — why this slice exists and what depends on it;
- **Source of truth** — relevant spec/product/architecture paths and an exact execution-plan section;
- **Dependencies / inputs** — prerequisite task IDs and shared contracts;
- **Scope** — included outcomes and explicit exclusions;
- **Decided technical constraints** — technologies, interfaces, invariants, persistence/migration rules;
- **Acceptance criteria**;
- **Verification**;
- **Evidence** expected on completion;
- **Decision boundary** telling the worker what must be escalated instead of improvised.

Task granularity is intentionally between two bad extremes: neither one giant project card nor one card per file/function.

## Review topology

Hermes supports two useful native models. NormalPowers chooses one per graph.

### Multi-task project — downstream acceptance task

Default for a new project or broad feature:

```text
implementation task A --\
implementation task B ----> integration / QA / acceptance
implementation task C --/
```

Workers complete leaf cards with structured evidence. The final acceptance card depends on all terminal implementation tasks and is assigned to the planner/orchestrator or an explicitly configured reviewer/QA profile.

This avoids paying the strongest planning model to review every trivial leaf task while still giving the final assembled result an explicit gate.

### Single bounded task — same-card review

For one coherent change, the worker may use `kanban_request_review(..., reviewer=<resolved reviewer profile>)`, after which the planner/reviewer accepts or requests concrete changes.

Do not combine same-card review with a pre-created downstream review child for the same task.

## Worker decision policy

Worker discretion should be small, not zero.

Workers may decide local reversible mechanics such as private names, tiny refactors, and equivalent implementation details that do not affect shared contracts.

Workers must escalate instead of deciding when the change would affect:

- approved product behavior or scope;
- persistent-data semantics or migrations;
- architecture/component boundaries;
- significant external dependencies;
- public or cross-task APIs/contracts;
- integration ordering/dependencies;
- acceptance criteria;
- the planned task decomposition.

A missing material decision is a planning defect, not an invitation for a cheaper worker to invent the project.

## Brainstorming scope discipline

NormalPowers keeps three explicit buckets:

- **Confirmed** — user-requested or explicitly approved product requirements;
- **Proposed** — optional product suggestions awaiting approval;
- **Out of Scope** — behavior not required now.

Only Confirmed behavior becomes product scope. For a fresh request, old memory/session/Wiki material cannot silently become Confirmed requirements.

Technical decisions are different: once product intent is clear, the planner is expected to research and choose an appropriate architecture rather than asking the user to choose every library or pushing those choices to workers.

## Project artifacts

NormalPowers deliberately does not create `docs/superpowers/...`.

Project information is separated by purpose:

```text
project/
├── specs/
│   └── <feature-or-scope>.md
├── docs/
│   ├── product.md
│   ├── architecture.md
│   └── decisions/
│       └── <adr>.md
└── plans/
    └── <feature>.md
```

- `specs/` — intended observable behavior and acceptance-relevant constraints;
- `docs/product.md` — long-lived product purpose/scope/principles;
- `docs/architecture.md` — selected stack, component boundaries, data/contracts, persistence/integration/migration/testing constraints that workers must follow;
- `docs/decisions/` — only significant durable decisions whose rationale matters later;
- `plans/<feature>.md` — current implementation strategy, workstreams, ordering, shared invariants, integration and acceptance design;
- code/tests — actual implementation state;
- Hermes Kanban — execution state, dependencies, worker handoffs, blockers, review, and evidence.

NormalPowers does **not** keep a dated chronological plan archive by default. A plan file is a living execution design for the current scope.

## Skills

The plugin registers three Hermes skills:

- `normalpowers:using-normalpowers` — routing and role model;
- `normalpowers:brainstorming` — research, product/design decisions, architecture, approval, durable artifacts;
- `normalpowers:writing-plans` — living execution design, decomposition, Kanban graph, routing, and acceptance topology.

A compact always-on system-prompt section tells the planner when to load the active skills. It is stored in Hermes' cached system prompt so the routing survives context compression.

## Source-of-truth boundaries

```text
Product behavior           -> specs/ + product docs
Technical architecture     -> docs/architecture.md + ADRs
Execution design           -> plans/<feature>.md
Actual implementation      -> code + tests
Execution state/evidence   -> Hermes Kanban graph
Long-term personal context -> memory
Reference knowledge        -> Wiki / research sources
```

Memory, Wiki, plan text, Kanban prose, or worker improvisation must not silently replace approved product/architecture truth.

## Upstream

NormalPowers is derived from ideas and selected workflow structure in [obra/superpowers](https://github.com/obra/superpowers), initially based on Superpowers v6.3.0. It is not a drop-in distribution of Superpowers and intentionally changes its artifact model and execution handoff.

See `NOTICE.md` and `LICENSE` for attribution and licensing.
