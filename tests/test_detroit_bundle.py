import unittest, zipfile, tempfile
from pathlib import Path
from scripts.audit_detroit_bundle import scan, REQUIRED
class TestDetroitBundle(unittest.TestCase):
    def test_complete(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'ok.zip'
            with zipfile.ZipFile(p,'w') as z:
                for n in REQUIRED: z.writestr('Detroit313/'+n,'demo')
            self.assertEqual(scan(p)['status'],'complete')
    def test_missing(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'missing.zip'
            with zipfile.ZipFile(p,'w') as z: z.writestr('Detroit313/README.md','demo')
            self.assertEqual(scan(p)['status'],'missing_files')
    def test_traversal(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'evil.zip'
            with zipfile.ZipFile(p,'w') as z: z.writestr('../bad','demo')
            with self.assertRaises(ValueError): scan(p)
