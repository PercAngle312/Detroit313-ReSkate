"""Inspect a Detroit source ZIP and emit a SHA-256 inventory without unpacking it."""
import argparse, hashlib, json, zipfile
from pathlib import Path, PurePosixPath

REQUIRED = [
    "build_detroit_studio_scene.py",
    "BUILD_DETROIT_WINDOWS.ps1",
    "preflight.py",
    "SPAWN_SURVEY_v24.json",
    "exports/CAMPUS_COLLISION_CANDIDATE_v23/CampusMartius_TerrainCollision_CANDIDATE.glb",
    "exports/CAMPUS_COLLISION_CANDIDATE_v23/CampusMartius_Roads_VISUAL_ONLY.glb",
    "exports/CAMPUS_COLLISION_CANDIDATE_v23/CampusMartius_Buildings_VISUAL_ONLY.glb",
]

def inventory(archive):
    with zipfile.ZipFile(archive) as z:
        names = {}
        for info in z.infolist():
            name = info.filename.replace("\\", "/")
            if name.startswith("/") or ".." in PurePosixPath(name).parts:
                raise ValueError("Unsafe archive member: " + info.filename)
            if info.is_dir():
                continue
            for required in REQUIRED:
                if name == required or name.endswith("/" + required):
                    if required in names:
                        raise ValueError("Duplicate source: " + required)
                    names[required] = info
        missing = sorted(set(REQUIRED) - set(names))
        entries = []
        for required, info in sorted(names.items()):
            data = z.read(info)
            entries.append({"file": required, "bytes": len(data),
                            "sha256": hashlib.sha256(data).hexdigest()})
        return {"valid": not missing, "missing": missing, "assets": entries}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("archive", type=Path)
    args = parser.parse_args()
    result = inventory(args.archive)
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["valid"] else 2)
