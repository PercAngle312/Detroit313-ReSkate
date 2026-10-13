import ast
import pathlib
import unittest
class TestBlenderSource(unittest.TestCase):
    def test_scene_script_is_valid_python(self):
        path=pathlib.Path("scripts/assemble_campus.py")
        ast.parse(path.read_text())
    def test_spawn_and_collision_contract_are_present(self):
        content=pathlib.Path("scripts/assemble_campus.py").read_text()
        for expected in ('"spawn"','"triangle_mesh"','"none"','scale=1.0','save_as_mainfile'):
            self.assertIn(expected,content)
