import os
import re
from pathlib import Path

BOOTSTRAP_MARKER = "normalpowers:using-normalpowers bootstrap for hermes"


def _skills_dir() -> str:
    """Locate the NormalPowers skills tree next to the plugin."""
    skills_dir = os.path.realpath(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "skills")
    )
    bootstrap_skill = os.path.join(skills_dir, "using-normalpowers", "SKILL.md")

    if os.path.isfile(bootstrap_skill):
        return skills_dir

    raise RuntimeError(
        "normalpowers plugin: cannot find skills/using-normalpowers/SKILL.md. "
        "Reinstall the plugin from its repository."
    )


def _strip_frontmatter(content: str) -> str:
    match = re.match(r"^---\n[\s\S]*?\n---\n([\s\S]*)$", content)
    return (match.group(1) if match else content).strip()


def _build_bootstrap(skills_dir: str) -> str:
    bootstrap_path = os.path.join(skills_dir, "using-normalpowers", "SKILL.md")
    with open(bootstrap_path, encoding="utf-8") as file:
        body = _strip_frontmatter(file.read())

    return (
        "<NORMALPOWERS>\n"
        f"{BOOTSTRAP_MARKER}\n\n"
        "NormalPowers is installed for this Hermes session.\n\n"
        "The using-normalpowers skill is included below and is already loaded. "
        "Follow it now; do not reload using-normalpowers.\n\n"
        f"{body}\n\n"
        "## Loading NormalPowers skills on Hermes\n\n"
        "NormalPowers skills use Hermes' native skill loader. Load them with:\n"
        '- `skill_view("normalpowers:brainstorming")`\n'
        '- `skill_view("normalpowers:writing-plans")`\n\n'
        f"Skills directory: `{skills_dir}`\n\n"
        "Direct user instructions and profile/project instructions take precedence "
        "over this workflow.\n"
        "</NORMALPOWERS>"
    )


def register(ctx):
    skills_dir = _skills_dir()
    bootstrap = _build_bootstrap(skills_dir)

    for name in sorted(os.listdir(skills_dir)):
        skill_md = os.path.join(skills_dir, name, "SKILL.md")
        if os.path.isfile(skill_md):
            ctx.register_skill(name, Path(skill_md))

    def pre_llm_call(
        session_id=None,
        user_message=None,
        conversation_history=None,
        is_first_turn=None,
        model=None,
        platform=None,
        **kwargs,
    ):
        if is_first_turn:
            return {"context": bootstrap}
        return None

    ctx.register_hook("pre_llm_call", pre_llm_call)
