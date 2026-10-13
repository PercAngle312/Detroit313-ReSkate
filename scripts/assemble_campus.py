"""Detroit313 Campus Martius Blender source build, using the supplied Studio exporter.

Blender usage:
  blender -b --factory-startup --python scripts/assemble_campus.py -- SOURCE_DIR STUDIO_ZIP OUTPUT.blend

Produces a .blend source scene, NOT a compiled ReSkate map.
"""
import json
import pathlib
import sys
import tempfile
import zipfile
import importlib.util
import bpy

def main():
    args = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    if len(args) != 3:
        raise SystemExit("Expected SOURCE_DIR STUDIO_ZIP OUTPUT.blend")
    root, studio, output = map(pathlib.Path, args)
    if not root.is_dir() or not studio.is_file():
        raise RuntimeError("Source directory and authorized Studio ZIP required")
    output = output.resolve()

    with tempfile.TemporaryDirectory() as temp:
        with zipfile.ZipFile(studio) as archive:
            # Install only the exporter module. Never execute ZIP contents as setup code.
            member = "Native/Blender/sk8_map_export.py"
            if member not in archive.namelist():
                raise RuntimeError("Studio ZIP missing " + member)
            addon_path = pathlib.Path(temp) / "sk8_map_export.py"
            addon_path.write_bytes(archive.read(member))
        spec = importlib.util.spec_from_file_location("sk8_map_export", addon_path)
        addon = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = addon
        spec.loader.exec_module(addon)
        addon.register()

        bpy.ops.object.select_all(action="SELECT")
        bpy.ops.object.delete(use_global=False)
        bpy.context.scene.unit_settings.system = "METRIC"
        bpy.context.scene.sk8_map.scale = 1.0
        bpy.context.scene.sk8_map.selected_only = False

        models = [
            ("Terrain", "CampusMartius_TerrainCollision_CANDIDATE.glb", "triangle_mesh"),
            ("Roads", "CampusMartius_Roads_VISUAL_ONLY.glb", "none"),
            ("Buildings", "CampusMartius_Buildings_VISUAL_ONLY.glb", "none"),
        ]
        folder = root / "exports" / "CAMPUS_COLLISION_CANDIDATE_v23"
        details = []
        for label, filename, mode in models:
            model = folder / filename
            if not model.is_file():
                raise FileNotFoundError(str(model))
            before = set(bpy.data.objects)
            bpy.ops.import_scene.gltf(filepath=str(model))
            imported = [obj for obj in bpy.data.objects if obj not in before and obj.type == "MESH"]
            if not imported:
                raise RuntimeError("No mesh objects imported from " + filename)
            for obj in imported:
                obj.name = label + "_" + obj.name
                obj.sk8_object.collision_mode = mode
                if mode != "none":
                    obj.sk8_object.collision_material = addon.DEFAULT_COLLISION_MATERIAL
                details.append({"name": obj.name, "faces": len(obj.data.polygons), "collision": mode})

        survey = json.loads((root / "SPAWN_SURVEY_v24.json").read_text(encoding="utf-8"))
        candidate = survey["candidates"][0]
        if candidate.get("status") != "SURVEY_CANDIDATE_ONLY":
            raise ValueError("Unexpected spawn survey schema")
        x, y, z = map(float, candidate["position_m"])
        spawn = bpy.data.objects.new("spawn", None)
        bpy.context.scene.collection.objects.link(spawn)
        spawn.location = (x, y, z + 1.25)

        output.parent.mkdir(parents=True, exist_ok=True)
        bpy.ops.wm.save_as_mainfile(filepath=str(output))
        (output.parent / "scene_audit.json").write_text(
            json.dumps({"studio_scene_scale": 1.0, "spawn": list(spawn.location),
                        "spawn_status": "UNTESTED", "meshes": details}, indent=2),
            encoding="utf-8")
        print("DETROIT313_SCENE_BUILT", output)

if __name__ == "__main__":
    main()
