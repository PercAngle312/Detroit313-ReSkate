# Upload the Detroit 313 authoring source from a phone

Upload only `Detroit313_Source.zip` (the ~245 KB project source ZIP) to the public repository at `inputs/Detroit313_Source.zip`. Do not upload the ReSkate Studio ZIP, EA Skate game binaries, accounts, or tokens.

GitHub mobile: open `inputs/` on the repository website (switch to desktop site if GitHub hides Add file), choose **Add file → Upload files**, choose the source ZIP, and commit to `main`.

The `Detroit 313 Source Bundle CI` workflow will validate the archive and create a manifest artifact. The bundle contains the Campus Martius terrain, roads, buildings, Blender scene script, and spawn survey.

This ZIP is an **authoring input**, not a playable mod. Scene generation still needs Blender and a legal local copy of the Studio exporter. The public Actions runner must not receive the third-party Studio ZIP via source checkout unless its terms authorize disclosure.

Prior uploaded bundles may contain upstream geographic datasets; verify source-data licenses before uploading any expanded GIS data.
