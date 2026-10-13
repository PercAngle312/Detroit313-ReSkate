import bpy
import json
from pathlib import Path
bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)
bpy.ops.mesh.primitive_cube_add(size=2)
obj=bpy.context.object
obj.name="Detroit313_BlenderSmoke"
bpy.context.scene.unit_settings.system="METRIC"
assert obj.name=="Detroit313_BlenderSmoke"
result={"blender_version":bpy.app.version_string,"object":obj.name,"metric_units":bpy.context.scene.unit_settings.system}
out=Path(__file__).resolve().parent.parent/"build_output"
out.mkdir(parents=True, exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=str(out/"Detroit313_BlenderSmoke.blend"))
(out/"blender_smoke.json").write_text(json.dumps(result,indent=2))
print("DETROIT313_BLENDER_SMOKE_PASS",result)
