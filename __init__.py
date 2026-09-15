import os
from pathlib import Path

ROUTING_SECTION_ID = "normalpowers.routing"
ROUTING_MAX_CHARS = 3000

ROUTING_SECTION = """NormalPowers is the planning-first software workflow for this profile when it is acting as the planner/orchestrator.

Use it for software requests with unresolved product, behavior, UX, architecture, data-model, integration, or non-trivial design intent: new products/subsystems, meaningful features, redesigns, and architectural changes.

Do not force the full workflow onto mechanical work whose desired behavior and constraints are already determined, such as running builds/tests, inspecting logs/status, fixing an obvious compile error, a known version bump, typo, or literal-value edit. Such work may go directly to a suitable worker through Hermes Kanban.

For planning work:
1. Load `normalpowers:brainstorming` before implementation or implementation delegation.
2. Treat a fresh product request as a clean scope. Memory, old sessions, Wiki, and unrelated repository history are research context, never product requirements unless the user explicitly asks to reuse them.
3. Clarify one material product decision at a time. Keep Confirmed, Proposed, and Out of Scope distinct; never promote an unrequested feature into the MVP.
4. Front-load decisions into planning. The planner researches and decides the technical architecture, data/contracts, implementation strategy, task boundaries, dependencies, and verification needed to keep worker discretion small. Escalate to the user only when a choice changes product intent, important trade-offs, risk, cost, privacy, or irreversible constraints.
5. Obtain user approval of product behavior and significant design/architecture before implementation.
6. Write concise durable truth under `specs/` and `docs/`, then run a cross-document consistency check.
7. Load `normalpowers:writing-plans` and materialize the execution plan as native Hermes Kanban work.
8. For substantial work, create multiple independently verifiable leaf tasks with explicit dependencies; do not send one giant project card and do not rely on Kanban auto-decomposition. A bounded task may remain one card.
9. Choose assignees from the currently available worker/profile roster by capability. Never assume literal profile names. Workers execute assigned scope; they do not redesign, re-scope, or re-decompose it. Material ambiguity returns to the planner.
10. Encode verification in the task graph. Prefer a pre-created downstream acceptance/QA task for multi-task projects; for a single bounded task, same-card `kanban_request_review` is acceptable. Do not combine both review models for the same work.

Role boundary: the planner owns research, product/design decisions, technical architecture, durable documentation, implementation planning, task decomposition, routing, and acceptance. Workers own implementation, required checks, and evidence within an already-decided scope.

Direct user instructions and profile/project instructions take precedence over these workflow rules."""


def _skills_dir() -> str:
    """Locate the NormalPowers skills tree next to the plugin."""
    skills_dir = os.path.realpath(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "skills")
    )
    routing_skill = os.path.join(skills_dir, "using-normalpowers", "SKILL.md")

    if os.path.isfile(routing_skill):
        return skills_dir

    raise RuntimeError(
        "normalpowers plugin: cannot find skills/using-normalpowers/SKILL.md. "
        "Reinstall the plugin from its repository."
    )


def register(ctx):
    skills_dir = _skills_dir()

    for name in sorted(os.listdir(skills_dir)):
        skill_md = os.path.join(skills_dir, name, "SKILL.md")
        if os.path.isfile(skill_md):
            ctx.register_skill(name, Path(skill_md))

    ctx.register_system_prompt_section(
        ROUTING_SECTION_ID,
        ROUTING_SECTION,
        position="after_memory",
        max_chars=ROUTING_MAX_CHARS,
    )
