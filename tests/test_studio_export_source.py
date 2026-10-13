import ast
import pathlib
import unittest

SCRIPT = pathlib.Path("scripts/export_studio_scene.py")

class StudioExportSourceTests(unittest.TestCase):
    def test_python_syntax(self):
        ast.parse(SCRIPT.read_text())

    def test_real_studio_export_contract(self):
        source = SCRIPT.read_text()
        for token in (
            "sk8.export_map",
            'collision_mode="triangle_mesh"',
            '"map.json"',
            "Exactly one spawn",
            "COMPLETED_NOT_COMPILED",
            'doc.get("format") != 1',
            'doc.get("units") != "meters"',
            'joinpath("meshes")',
        ):
            self.assertIn(token, source)

    def test_no_false_compilation_claim(self):
        source = SCRIPT.read_text()
        self.assertIn("NOT a compiled/playable map", source)
