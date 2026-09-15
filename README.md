# NormalPowers

NormalPowers is a planning-only workflow plugin for Hermes Agent, designed for a two-profile setup:

```text
User -> Main -> NormalPowers planning -> Hermes Kanban -> Developer -> evidence -> Main
```

It is inspired by the planning discipline of Superpowers, but intentionally removes Superpowers' execution layer. Main owns discovery, research, product decisions, specification, planning, delegation, and final acceptance. Developer owns implementation.

## What NormalPowers does

NormalPowers gives Main a durable software-planning workflow before implementation starts:

1. understand the user's intent;
2. inspect the existing repository when one exists;
3. research current platform/API/library facts when they matter;
4. clarify only the decisions that are genuinely unresolved;
5. compare reasonable approaches when there is a real design choice;
6. get explicit approval before implementation;
7. write concise durable product/spec/architecture artifacts;
8. create a practical implementation brief;
9. hand execution to Developer through Hermes Kanban;
10. verify returned evidence against the approved specification before accepting completion.

NormalPowers does **not** make Main a coding agent and does not use Superpowers subagent-driven execution.

## Install

Install it only into the Main Hermes profile:

```bash
HERMES_HOME=~/.hermes/profiles/main \
  hermes plugins install arttvad9r/NormalPowers --enable
```

Then start a **fresh Main session**. NormalPowers registers its routing rules as a cache-safe Hermes system-prompt section when a new session is created. Hermes freezes that section into the session prompt, so it survives context compression and process resume. Updating the plugin does not rewrite an already-existing session prompt; start a new session after updating NormalPowers.

Do not install NormalPowers into Developer for the initial setup. Developer should continue using its existing engineering, Android, Gradle, test, repository, and worktree tooling.

### Verify the install

```bash
HERMES_HOME=~/.hermes/profiles/main \
  hermes plugins doctor normalpowers --ci
```

You can also confirm that it is enabled with:

```bash
HERMES_HOME=~/.hermes/profiles/main \
  hermes plugins list
```

## Recommended Main role boundary

Keep SOUL/profile instructions short. A sufficient role statement is:

```text
Main is the user's primary software planning and coordination authority.
Main owns user interaction, discovery, research, product decisions,
specification, planning, delegation, and final acceptance.
Substantial implementation belongs to Developer and is delegated through Hermes Kanban.
```

The workflow details belong in this plugin, not in SOUL.md.

## Recommended Kanban configuration

```yaml
kanban:
  orchestrator_profile: main
  default_assignee: developer
  auto_decompose: false
```

NormalPowers already performs the meaningful decomposition before handoff. A second automatic Kanban decomposition pass would create competing planning decisions.

## Automatic behavior

Typical requests that should enter NormalPowers planning:

- "I want to build an Android app..."
- "Add this user-facing feature..."
- "Redesign this flow..."
- "Change this product behavior..."
- "We need to choose an architecture for..."

Typical requests that do not need the full planning workflow:

- run a build or test;
- fix an obvious compile failure;
- update a known dependency version;
- change a typo or literal value;
- inspect logs or repository state;
- perform other mechanical work where desired behavior is already fully determined.

Those can be delegated directly to Developer through Kanban.

## Project artifacts

NormalPowers deliberately does not create `docs/superpowers/...`.

Durable project truth is stored in conventional locations:

```text
project/
├── specs/
│   └── <feature-or-scope>.md
└── docs/
    ├── product.md
    ├── architecture.md
    └── decisions/
        └── <adr>.md
```

Rules:

- `specs/` describes intended observable behavior.
- `docs/product.md` holds long-lived product scope and principles for a new product.
- `docs/architecture.md` holds long-lived architecture, not implementation trivia.
- ADRs are created only for significant durable architectural decisions.
- implementation plans are operational and belong in the Kanban handoff by default, not in a permanent `docs/plans/` archive.

## Skills and routing

The plugin registers three Hermes skills:

- `normalpowers:using-normalpowers` — detailed routing and role-boundary reference;
- `normalpowers:brainstorming` — discovery, research, design, approval, and concise specification;
- `normalpowers:writing-plans` — implementation brief and Kanban handoff to Developer.

A compact always-on routing section tells Main when to load the two active workflow skills. It is deliberately much smaller than the full skill text and is stored in Hermes' cached system prompt so long-running Main sessions remain consistent across context compression.

Manual skill invocation should rarely be necessary. For debugging, the skills can be inspected with Hermes' native `skill_view("normalpowers:<skill>")` mechanism.

## Source-of-truth boundaries

```text
Desired product behavior -> specs/ and product docs
Architecture             -> docs/architecture.md and ADRs
Current implementation   -> code and tests
Execution state          -> Hermes Kanban
Long-term agent context  -> Mnemosyne
Reference knowledge      -> Wiki
```

Kanban, Wiki, and memory must not silently replace approved product requirements.

## Upstream

NormalPowers is derived from ideas and selected workflow structure in [obra/superpowers](https://github.com/obra/superpowers), initially based on Superpowers v6.3.0. It is not a drop-in distribution of Superpowers and intentionally changes its artifact model and execution handoff.

See `NOTICE.md` and `LICENSE` for attribution and licensing.
