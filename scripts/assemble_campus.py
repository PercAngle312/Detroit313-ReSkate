"""Blender background entry: blender -b --python scripts/assemble_campus.py -- source_dir studio.zip output.blend"""
import sys, pathlib, zipfile, tempfile, importlib.util, json
import bpy

argv=sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else []
if len(argv)!=3: raise SystemExit("Usage: source_dir studio.zip output.blend")
root,studio,dest=map(pathlib.Path,argv)
if not root.is_dir() or not studio.is_file(): raise RuntimeError("Missing source folder or authorized Studio ZIP")
with tempfile.TemporaryDirectory() as tmp:
    with zipfile.ZipFile(studio) as z:
        member="Native/Blender/sk8_map_export.py"
        if member not in z.namelist(): raise RuntimeError("Studio add-on missing")
        z.extract(member,tmp)
    spec=importlib.util.spec_from_file_location("sk8_map_export",str(pathlib.Path(tmp)/member))
    addon=importlib.util.module_from_spec(spec)
    sys.modules[spec.name]=addon
    spec.loader.exec_module(addon)
    addon.register()
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    bpy.context.scene.unit_settings.system="METRIC"
    bpy.context.scene.sk8_map.scale=1.0
    bpy.context.scene.sk8_map.selected_only=False
    meshes=[
        ("Terrain","exports/CAMPUS_COLLISION_CANDIDATE_v23/CampusMartius_TerrainCollision_CANDIDATE.glb","triangle_mesh"),
        ("Roads","exports/CAMPUS_COLLISION_CANDIDATE_v23/CampusMartius_Roads_VISUAL_ONLY.glb","none"),
        ("Buildings","exports/CAMPUS_COLLISION_CANDIDATE_v23/CampusMartius_Buildings_VISUAL_ONLY.glb","none"),
    ]
    report=[]
    for label,rel,mode in meshes:
        path=root/rel
        if not path.is_file(): raise RuntimeError("Missing model "+str(path))
        before=set(bpy.data.objects)
        bpy.ops.import_scene.gltf(filepath=str(path))
        imported=[o for o in (set(bpy.data.objects)-before) if o.type=="MESH"]
        if not imported: raise RuntimeError("No mesh imported from "+rel)
        for ob in imported:
            ob.name=label+"_"+ob.name
            ob.sk8_object.collision_mode=mode
            ob.sk8_object.collision_material=addon.DEFAULT_COLLISION_MATERIAL
            report.append({"object":ob.name,"polygons":len(ob.data.polygons),"collision":mode})
    survey=json.loads((root/"SPAWN_SURVEY_v24.json").read_text())
    x,y,z=survey["candidates"][0]["position_m"]
    spawn=bpy.data.objects.new("spawn",None)
    bpy.context.scene.collection.objects.link(spawn)
    spawn.location=(float(x),float(y),float(z)+1.25)
    dest.parent.mkdir(parents=True,exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(dest))
    (dest.parent/"scene_audit.json").write_text(json.dumps({"scale":1.0,"spawn":list(spawn.location),"mesh_objects":report},indent=2))
    print("DETROIT313_SCENE_BUILT",dest)
