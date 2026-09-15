# Attribution

NormalPowers is an independent Hermes planning plugin inspired by and partially derived from the workflow concepts of [Superpowers](https://github.com/obra/superpowers) by Jesse Vincent.

Initial reference version: Superpowers v6.3.0 (released 2026-08-12).

NormalPowers intentionally changes the upstream workflow in several ways:

- planning-only scope for the Hermes Main profile;
- no subagent-driven or inline execution layer;
- execution handoff through Hermes Kanban to a separate Developer profile;
- concise durable specs under `specs/`;
- durable product/architecture docs under `docs/`;
- implementation plans treated as operational Kanban state by default;
- selective software-only bootstrap instead of a universal skill-first policy.

Superpowers is distributed under the MIT License. The original copyright notice is preserved in `LICENSE`.
