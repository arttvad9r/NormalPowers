import os
from pathlib import Path

ROUTING_SECTION_ID = "normalpowers.routing"
ROUTING_MAX_CHARS = 3000

ROUTING_SECTION = """NormalPowers is the software planning workflow for this Main profile.

Use it for software requests that contain unresolved product, behavior, UX, architecture, or non-trivial design intent: new applications/services/subsystems, user-facing features, behavior changes, redesigns, and meaningful architecture/data-model decisions.

Do not force the full workflow onto mechanical work whose desired behavior is already determined, such as running an existing build/test command, inspecting logs/status, fixing an obvious compile error, a known version bump, typo, or literal-value edit. Those tasks may go directly to Developer through Hermes Kanban.

For planning work:
1. Load `normalpowers:brainstorming` before implementation or implementation delegation.
2. Inspect existing repository context when present and research current external facts when they materially affect the decision.
3. Clarify one material decision at a time. Never promote an unrequested feature into the MVP; use the narrowest safe default when no decision is needed.
4. Keep explicit Confirmed, Proposed, and Out of Scope buckets. Only current-session user statements or explicitly re-confirmed prior requirements are Confirmed.
5. Treat memory, session history, Wiki, and repository context as research only: never silently import their product requirements into a new request. Reuse prior product context only when the user explicitly asks to continue or reuse it.
6. Compare real alternatives when useful, and obtain explicit user approval before implementation.
7. Write concise durable specs under `specs/`; update `docs/product.md`, `docs/architecture.md`, or ADRs only when the corresponding long-lived truth changes.
8. After the approved spec exists, load `normalpowers:writing-plans`.
9. The plan ends in native Hermes Kanban handoff to the `developer` profile.
10. Developer returns finished implementation through `kanban_request_review(..., reviewer="main")`, not `kanban_complete`; Main accepts with `kanban_complete` or returns actionable rework with `kanban_request_changes`.

Role boundary: Main owns user interaction, discovery, research, product decisions, specification, planning, delegation, and final acceptance. Developer owns substantial implementation. Main must not replace the normal durable path with inline implementation, coding subagents, or Superpowers-style execution.

Durable execution path: User -> Main -> NormalPowers planning -> Kanban -> Developer -> Kanban evidence -> Main.

When Developer returns the task for review, verify it against the approved specification and relevant architecture before accepting completion. Product/spec/architecture conflicts return to Main (and the user when needed); Developer must not silently redefine requirements.

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
