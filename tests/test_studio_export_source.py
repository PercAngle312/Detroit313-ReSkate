import ast, pathlib, unittest
class StudioExportSourceTests(unittest.TestCase):
    def test_python_syntax(self):
        ast.parse(pathlib.Path("scripts/export_studio_scene.py").read_text())
    def test_guards(self):
        s=pathlib.Path("scripts/export_studio_scene.py").read_text()
        for token in ['sk8.export_map','collision_mode="triangle_mesh"','collision_mode','map.json','Exactly one spawn','COMPLETED_NOT_COMPILED']:
            self.assertIn(token,s)
