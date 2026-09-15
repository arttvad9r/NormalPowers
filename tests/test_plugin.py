import importlib.util
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PLUGIN_PATH = REPO_ROOT / "__init__.py"


class FakeContext:
    def __init__(self):
        self.skills = {}
        self.system_prompt_sections = {}

    def register_skill(self, name, path):
        self.skills[name] = path

    def register_system_prompt_section(
        self, section_id, content, *, position="after_memory", max_chars=4000
    ):
        self.system_prompt_sections[section_id] = {
            "content": content,
            "position": position,
            "max_chars": max_chars,
        }


def load_plugin_module():
    spec = importlib.util.spec_from_file_location("normalpowers_plugin", PLUGIN_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class NormalPowersPluginTests(unittest.TestCase):
    def setUp(self):
        self.plugin = load_plugin_module()

    def test_registers_expected_skills(self):
        ctx = FakeContext()
        self.plugin.register(ctx)

        self.assertEqual(
            set(ctx.skills),
            {"brainstorming", "using-normalpowers", "writing-plans"},
        )

        for skill_path in ctx.skills.values():
            self.assertTrue(skill_path.is_file())
            self.assertEqual(skill_path.name, "SKILL.md")

    def test_registers_compression_safe_routing_section(self):
        ctx = FakeContext()
        self.plugin.register(ctx)

        self.assertEqual(set(ctx.system_prompt_sections), {"normalpowers.routing"})
        section = ctx.system_prompt_sections["normalpowers.routing"]

        self.assertEqual(section["position"], "after_memory")
        self.assertEqual(section["max_chars"], self.plugin.ROUTING_MAX_CHARS)
        self.assertLessEqual(len(section["content"]), section["max_chars"])
        self.assertIn("normalpowers:brainstorming", section["content"])
        self.assertIn("normalpowers:writing-plans", section["content"])
        self.assertIn("planner/orchestrator", section["content"])
        self.assertIn("Workers execute assigned scope", section["content"])
        self.assertIn("Never assume literal profile names", section["content"])
        self.assertIn("multiple independently verifiable leaf tasks", section["content"])
        self.assertIn("acceptance/QA task", section["content"])
        self.assertIn("clean scope", section["content"])
        self.assertIn("Confirmed, Proposed, and Out of Scope", section["content"])
        self.assertIn("plans/<feature>.md", section["content"])
        self.assertIn("Each card references the relevant plan section", section["content"])

    def test_routing_section_is_role_name_agnostic(self):
        content = self.plugin.ROUTING_SECTION

        self.assertNotIn("Developer", content)
        self.assertNotIn("Main", content)
        self.assertNotIn("`developer`", content)
        self.assertNotIn('reviewer="main"', content)

    def test_routing_section_does_not_force_planning_on_mechanical_work(self):
        content = self.plugin.ROUTING_SECTION

        self.assertIn("Do not force the full workflow onto mechanical work", content)
        self.assertIn("compile error", content)
        self.assertIn("version bump", content)

    def test_writing_plan_separates_execution_design_from_kanban_state(self):
        content = (REPO_ROOT / "skills" / "writing-plans" / "SKILL.md").read_text()

        self.assertIn("one living execution design", content)
        self.assertIn("plans/<feature>.md", content)
        self.assertIn("Kanban is execution state, not the sole plan artifact", content)
        self.assertIn("Execution design: `plans/<feature>.md#<specific-section>`", content)
        self.assertIn("Kanban mapping", content)

    def test_writing_plan_requires_decomposition_and_minimal_worker_discretion(self):
        content = (REPO_ROOT / "skills" / "writing-plans" / "SKILL.md").read_text()

        self.assertIn("one giant `Implement the whole project` card", content)
        self.assertIn("parents=[...]", content)
        self.assertIn("Workers execute assigned slices", content)
        self.assertIn("missing material decision", content)
        self.assertIn("downstream acceptance task", content)
        self.assertNotIn("assigned to the `developer` profile", content)

    def test_notice_is_role_agnostic_and_documents_plan_boundary(self):
        content = (REPO_ROOT / "NOTICE.md").read_text()

        self.assertNotIn("Hermes Main profile", content)
        self.assertNotIn("Developer profile", content)
        self.assertIn("planner/orchestrator and worker roles", content)
        self.assertIn("plans/<feature>.md", content)
        self.assertIn("rather than as the sole plan artifact", content)

    def test_routing_section_id_and_size_are_bounded(self):
        self.assertEqual(self.plugin.ROUTING_SECTION_ID, "normalpowers.routing")
        self.assertLessEqual(len(self.plugin.ROUTING_SECTION), 3000)


if __name__ == "__main__":
    unittest.main()
