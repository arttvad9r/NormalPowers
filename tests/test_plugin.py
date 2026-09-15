import importlib.util
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PLUGIN_PATH = REPO_ROOT / "__init__.py"


class FakeContext:
    def __init__(self):
        self.skills = {}
        self.hooks = {}

    def register_skill(self, name, path):
        self.skills[name] = path

    def register_hook(self, name, callback):
        self.hooks[name] = callback


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

    def test_registers_pre_llm_call_hook(self):
        ctx = FakeContext()
        self.plugin.register(ctx)

        self.assertIn("pre_llm_call", ctx.hooks)

    def test_bootstrap_is_injected_only_on_first_turn(self):
        ctx = FakeContext()
        self.plugin.register(ctx)
        hook = ctx.hooks["pre_llm_call"]

        first_turn = hook(is_first_turn=True)
        later_turn = hook(is_first_turn=False)

        self.assertIsInstance(first_turn, dict)
        self.assertIn("context", first_turn)
        self.assertIn(self.plugin.BOOTSTRAP_MARKER, first_turn["context"])
        self.assertIn("normalpowers:brainstorming", first_turn["context"])
        self.assertIn("normalpowers:writing-plans", first_turn["context"])
        self.assertIsNone(later_turn)

    def test_bootstrap_frontmatter_is_not_injected(self):
        skills_dir = self.plugin._skills_dir()
        bootstrap = self.plugin._build_bootstrap(skills_dir)

        self.assertNotIn("name: using-normalpowers", bootstrap)
        self.assertIn("# Using NormalPowers", bootstrap)


if __name__ == "__main__":
    unittest.main()
