"""Extract only vetted Detroit authoring inputs, never execute code from the ZIP."""
import argparse, pathlib, zipfile
from scripts.inventory_detroit_assets import inventory, REQUIRED

def extract(archive, target):
    archive=pathlib.Path(archive); target=pathlib.Path(target)
    checked=inventory(archive)
    if not checked["valid"]:
        raise ValueError("Missing assets: "+", ".join(checked["missing"]))
    target.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(archive) as z:
        for name in REQUIRED:
            matches=[entry for entry in z.namelist() if entry==name or entry.endswith("/"+name)]
            if len(matches)!=1:
                raise ValueError("Missing or duplicate member: "+name)
            file=target / name
            file.parent.mkdir(parents=True,exist_ok=True)
            file.write_bytes(z.read(matches[0]))
    print("EXTRACTED",len(REQUIRED),"source files to",target)

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("archive")
    ap.add_argument("output")
    a=ap.parse_args()
    extract(a.archive,a.output)
