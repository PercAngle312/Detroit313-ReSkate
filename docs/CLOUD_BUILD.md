# Detroit 313 cloud-build inputs

This public repository does **not** contain the original ReSkate Studio executable, game installation or 3D Detroit source bundle.

## Source bundle
Place the authorized `Detroit313_Source.zip` locally in `inputs/`. The archive must include the scene generator, spawn survey and the three terrain/road/building meshes. Use `python scripts/inventory_detroit_assets.py inputs/Detroit313_Source.zip` to inspect it.

## Scene build (Windows)
`powershell -ExecutionPolicy Bypass -File scripts/build_scene_windows.ps1 -SourceZip inputs/Detroit313_Source.zip -StudioZip "C:\path\ReSkate Studio.zip" -BlenderExe "C:\Program Files\Blender Foundation\Blender 4.5\blender.exe"`

Add `-Compile -GamePath "C:\path\Skate"` only if you have the authorized game installation and compiler permitted for your environment.

**Do not** check in ReSkate Studio, proprietary assets, private binaries or their extracted copies. Public Actions logs and artifacts may be accessible to anyone. The build may require further exporter compatibility work.
