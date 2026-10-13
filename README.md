# Detroit 313 — ReSkate (1:1)

Real-scale Downtown Detroit map project. Start with Campus Martius, eventually expand to all Detroit. Lite edition comes later.

## Current status

- Source assets exist in the separately archived **Detroit313 Texture Lab Safety Gate v3.2** project.
- Scene generation and ReSkate Studio compilation have **not** yet been executed successfully.
- The Studio compiler is third-party and **must not be committed to this public repository** unless redistribution is authorized.
- An installed Skate game may be required by `reskate_cli compile-map`. No game binaries/assets are included here.

## Cloud build roadmap

The Actions workflow runs on Windows and checks the environment. A scene build requires a separately supplied authorized Detroit source bundle and Studio ZIP; merely running this workflow does not create a playable mod.

Do not upload private tokens, proprietary game files, or the ReSkate Studio archive to public repo history or public Actions artifacts. **Public workflows and their logs are visible.**

## Source provenance

- Building footprints and street centerlines: Detroit/SEMCOG GIS source data (licenses and current accuracy need review before public redistribution).
- Terrain: USGS 3DEP raster, initial 280 × 280 m tile.
- Building heights and road widths are partly provisional.

First playtest goals: compile-map succeeds, map registers with ReSkate, spawn works, terrain collision works. No playtest claimed yet.
