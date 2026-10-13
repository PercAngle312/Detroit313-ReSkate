"""Apply the installed ReSkate Studio Blender addon to an existing Detroit source scene.

Run inside Blender with an authorized Studio addon installed:
 blender -b Detroit313_CampusMartius_SOURCE.blend --python scripts/export_studio_scene.py -- OUTPUT_DIR

This exports a Studio map.json handshake and GLBs, not a compiled/playable map.
"""
import bpy, json, pathlib, sys
args=sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else []
if len(args)!=1: raise SystemExit("Usage: OUTPUT_DIR")
destination=pathlib.Path(args[0]).resolve()
destination.mkdir(parents=True,exist_ok=True)

try:
    import sk8_map_export as addon
except ImportError as exc:
    raise RuntimeError("Install authorized ReSkate Studio Blender add-on first; do not commit its binary distribution") from exc
if not hasattr(bpy.context.scene, "sk8_map"):
    addon.register()
if not hasattr(bpy.context.scene, "sk8_map"):
    raise RuntimeError("Studio addon failed to register its scene properties")

scene=bpy.context.scene
scene.sk8_map.scale=1.0
scene.sk8_map.selected_only=False
scene.sk8_map.folder=str(destination)
meshes=[ob for ob in scene.objects if ob.type=="MESH"]
spawn=[ob for ob in scene.objects if ob.type=="EMPTY" and ob.name.casefold()=="spawn"]
if len(spawn)!=1: raise RuntimeError("Exactly one spawn Empty required")
names={"Terrain":[],"Roads":[],"Buildings":[]}
for obj in meshes:
    category=next((k for k in names if obj.name.startswith("D313_"+k+"_")),None)
    if category is None: raise RuntimeError("Unrecognized Detroit mesh: "+obj.name)
    names[category].append(obj)
    obj.sk8_object.collision_mode="triangle_mesh" if category=="Terrain" else "none"
    if category=="Terrain": obj.sk8_object.collision_material=addon.DEFAULT_COLLISION_MATERIAL
for kind,items in names.items():
    if not items: raise RuntimeError("Missing scene category: "+kind)
result=bpy.ops.sk8.export_map()
if "FINISHED" not in result: raise RuntimeError("Studio export operator returned "+str(result))
manifest=destination/"map.json"
if not manifest.is_file(): raise RuntimeError("Studio failed to write map.json")
doc=json.loads(manifest.read_text(encoding="utf-8"))
if doc.get("format") != 1 or doc.get("units") != "meters":
    raise RuntimeError("Studio map.json has unexpected format or units")
if not doc.get("objects"): raise RuntimeError("Export produced no objects")
exported_names = [obj.get("name", "") for obj in doc["objects"]]
if not any("Terrain" in name for name in exported_names):
    raise RuntimeError("Studio export lost the terrain mesh")
if not manifest.parent.joinpath("meshes").is_dir():
    raise RuntimeError("Studio export missing meshes directory")
(destination/"detroit_studio_audit.json").write_text(json.dumps({
    "studio_export":"COMPLETED_NOT_COMPILED",
    "objects":{k:len(v) for k,v in names.items()},
    "spawn":[float(v) for v in spawn[0].location],
    "map_json_bytes":manifest.stat().st_size
},indent=2),encoding="utf-8")
print("DETROIT313_STUDIO_EXPORT_PASS",manifest)
