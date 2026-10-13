import ast
import pathlib
import unittest

class TestBlenderSource(unittest.TestCase):
    def test_scene_script_is_valid_python(self):
        ast.parse(pathlib.Path("scripts/assemble_campus.py").read_text())

    def test_studio_contract_and_survey(self):
        code = pathlib.Path("scripts/assemble_campus.py").read_text()
        for token in ('"spawn"', '"triangle_mesh"', '"none"', 'sk8_map.scale = 1.0',
                      'save_as_mainfile', 'survey["candidates"][0]', 'position_m'):
            self.assertIn(token, code)
