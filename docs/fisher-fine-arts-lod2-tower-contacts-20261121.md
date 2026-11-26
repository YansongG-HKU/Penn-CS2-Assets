# Fisher Fine Arts LOD2 tower contact patch

2026-11-21. Offline staged native FBX patch to the canonical 8x6 LOD2. Rebuilt only the two nested cap contacts at model z=6.5 and 17.5 m, restoring the exposed top ring (~19.27 m²) and underside (~111.98 m²). Cancelled 119 opposed triangle pairs across these planes. Remaining scan has 49 opposed and 15 same-orientation pairs (base/side blocks), not covered here. This scan is not a general self-intersection or geometry survey.

- FBX SHA-256: source b79831fff39e9db0354dd6d7bd6e2a79a5394b0361556ce8072349712c9b1523; candidate 079e2239ebec87beebd9d9f922d64a3a0c0f13bfa2f65ee13e68127eafad551a. 184 vertices and all 104 unaffected original polygons/corner UV/normals unchanged. 336 -> 344 triangles; 516 paired consistently wound triangle edges across six indexed closed components, not one merged physical shell. All ten existing textures byte-identical. Keep canonical intact.
- Reimport-tested exact extracted ZIP in Blender 4.3.2; 123,201 exterior rays, 26,934 hits, max first-hit shift 0.0333 mm. 5,450 close exposed and 1,250 internal rays additionally checked. No LOD0/1 or gameplay/editor acceptance or publishing.
- Archive: Penn-Fisher-远景塔身两处接缝修补-未游戏验收.zip (19,507,398 bytes), SHA-256 691db007f095920e6c9b103ec63acd84a178a93cf9be2bdefc3c9584bb81945d. Documentation only, not a canonical binary/LFS update.
