"""Detroit 313 build-input audit. No third-party binaries are needed."""
from pathlib import Path
import argparse
import json
import zipfile

REQUIRED = (
    "build_detroit_studio_scene.py",
    "BUILD_DETROIT_WINDOWS.ps1",
    "preflight.py",
    "SPAWN_SURVEY_v24.json",
)

def audit(source):
    path = Path(source)
    if not path.is_file():
        return {"status": "missing", "message": "Upload an authorized source ZIP to begin scene generation"}
    with zipfile.ZipFile(path) as z:
        names = [n.replace("\\", "/") for n in z.namelist()]
        bad = [n for n in names if n.startswith("/") or ".." in Path(n).parts]
        if bad:
            raise ValueError("Unsafe ZIP path(s)")
        missing = [x for x in REQUIRED if not any(n.endswith("/" + x) or n == x for n in names)]
        return {"status": "ready" if not missing else "incomplete",
                "files": len(names), "missing": missing}

if __name__ == "__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--source", default="inputs/Detroit313_Source.zip")
    a=p.parse_args()
    result=audit(a.source)
    print(json.dumps(result, indent=2))
    if result["status"] == "incomplete":
        raise SystemExit(2)
