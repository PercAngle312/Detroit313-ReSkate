"""Validate the real Detroit v3.2 source bundle without unpacking untrusted paths."""
from pathlib import Path
import argparse, json, zipfile
REQUIRED = {
"build_detroit_studio_scene.py",
"BUILD_DETROIT_WINDOWS.ps1",
"preflight.py",
"SPAWN_SURVEY_v24.json",
"exports/CAMPUS_COLLISION_CANDIDATE_v23/CampusMartius_TerrainCollision_CANDIDATE.glb",
"exports/CAMPUS_COLLISION_CANDIDATE_v23/CampusMartius_Roads_VISUAL_ONLY.glb",
"exports/CAMPUS_COLLISION_CANDIDATE_v23/CampusMartius_Buildings_VISUAL_ONLY.glb",
}
def scan(path):
    with zipfile.ZipFile(path) as z:
        bad=[i.filename for i in z.infolist() if i.filename.startswith(('/', '\\')) or '..' in Path(i.filename.replace('\\','/')).parts]
        if bad: raise ValueError("Unsafe ZIP members: "+repr(bad[:3]))
        names={n.split('/',1)[1] if '/' in n else n for n in z.namelist()}
        missing=sorted(REQUIRED-names)
        return {"status":"complete" if not missing else "missing_files","missing":missing,
                "files":len(z.namelist()),"size_bytes":Path(path).stat().st_size}
if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("zip",type=Path)
    a=p.parse_args()
    result=scan(a.zip)
    print(json.dumps(result,indent=2))
    raise SystemExit(0 if result["status"]=="complete" else 2)
