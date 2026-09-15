# Attribution

NormalPowers is an independent Hermes planning plugin inspired by and partially derived from the workflow concepts of [Superpowers](https://github.com/obra/superpowers) by Jesse Vincent.

Initial reference version: Superpowers v6.3.0 (released 2026-08-12).

NormalPowers intentionally changes the upstream workflow in several ways:

- planner/orchestrator and worker roles are capability-based rather than tied to literal Hermes profile names;
- no subagent-driven or inline execution layer;
- execution handoff through native Hermes Kanban to one or more configured worker profiles;
- concise durable specs under `specs/`;
- durable product/architecture docs under `docs/`;
- a non-chronological living execution design under `plans/<feature>.md`;
- Kanban used for execution state, dependencies, handoffs, blockers, review, and evidence rather than as the sole plan artifact;
- selective software-only bootstrap instead of a universal skill-first policy.

Superpowers is distributed under the MIT License. The original copyright notice is preserved in `LICENSE`.
