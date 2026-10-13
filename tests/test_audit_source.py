import tempfile
import unittest
import zipfile
from pathlib import Path
from scripts.audit_source import audit, REQUIRED

class TestInputAudit(unittest.TestCase):
    def test_absent_input_is_reported(self):
        self.assertEqual(audit("does-not-exist.zip")["status"], "missing")

    def test_required_inputs_pass(self):
        with tempfile.TemporaryDirectory() as root:
            p=Path(root)/"good.zip"
            with zipfile.ZipFile(p, "w") as z:
                for required in REQUIRED:
                    z.writestr("Detroit313/" + required, "data")
            self.assertEqual(audit(p)["status"], "ready")

    def test_incomplete_input_reported(self):
        with tempfile.TemporaryDirectory() as root:
            p=Path(root)/"bad.zip"
            with zipfile.ZipFile(p, "w") as z:
                z.writestr("Detroit313/README.md", "data")
            self.assertEqual(audit(p)["status"], "incomplete")

    def test_zip_traversal_rejected(self):
        with tempfile.TemporaryDirectory() as root:
            p=Path(root)/"unsafe.zip"
            with zipfile.ZipFile(p, "w") as z:
                z.writestr("../escape.txt", "data")
            with self.assertRaises(ValueError):
                audit(p)

if __name__ == "__main__":
    unittest.main()
