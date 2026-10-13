"""Generate an inspectable Detroit .blend from public geometry; no Studio addon required.
Blender: blender -b --factory-startup --python scripts/build_public_blend.py -- SOURCE_DIR OUTPUT.blend
This is NOT a ReSkate-compatible export or compiled mod.
"""
import bpy, json, pathlib, sys
args=sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else []
if len(args)!=2: raise SystemExit("Expected SOURCE_DIR OUTPUT.blend")
root,output=map(pathlib.Path,args)
out=output.resolve()
mesh_dir=root/"exports"/"CAMPUS_COLLISION_CANDIDATE_v23"
assets=[
 ("Terrain","CampusMartius_TerrainCollision_CANDIDATE.glb"),
 ("Roads","CampusMartius_Roads_VISUAL_ONLY.glb"),
 ("Buildings","CampusMartius_Buildings_VISUAL_ONLY.glb"),
]
bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)
bpy.context.scene.unit_settings.system="METRIC"
counts={}
for label,filename in assets:
    path=mesh_dir/filename
    if not path.is_file(): raise FileNotFoundError(str(path))
    before=set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=str(path))
    imported=[x for x in bpy.data.objects if x not in before and x.type=="MESH"]
    if not imported: raise RuntimeError("No meshes loaded for "+label)
    for obj in imported: obj.name="D313_"+label+"_"+obj.name
    counts[label]={"meshes":len(imported),"triangles":sum(sum(max(0,len(p.vertices)-2) for p in o.data.polygons) for o in imported)}
survey=json.loads((root/"SPAWN_SURVEY_v24.json").read_text(encoding="utf-8"))
candidate=survey["candidates"][0]
xyz=candidate["position_m"]
if len(xyz)!=3 or candidate.get("status")!="SURVEY_CANDIDATE_ONLY": raise ValueError("Unexpected spawn survey")
spawn=bpy.data.objects.new("spawn",None)
bpy.context.scene.collection.objects.link(spawn)
spawn.location=tuple(float(v) for v in xyz)
spawn["d313_status"]="SURVEY_CANDIDATE_ONLY"
out.parent.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=str(out))
audit={"type":"BLENDER_SOURCE_SCENE_NOT_RESKATE_EXPORT","blender_version":bpy.app.version_string,"meshes":counts,"spawn_candidate_m":xyz,"studio_export":"NOT_PERFORMED"}
(out.parent/"source_scene_audit.json").write_text(json.dumps(audit,indent=2),encoding="utf-8")
print("DETROIT_SOURCE_SCENE_PASS",json.dumps(audit))
