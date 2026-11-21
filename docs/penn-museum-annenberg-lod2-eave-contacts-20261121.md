# Penn Museum and Annenberg Center LOD2 eave-underside patches

2026-11-21, exact offline comparison. Removed opposing internal contact caps at Penn Museum z=18.5 m and Annenberg Center z=28 m, preserving exposed eave rings of 603.77 and 24.32 model m². Coplanar pair counts were 126→77 and 39→32 respectively; remaining base and wing conflicts are outside this fix. No general intersecting-volume review. Patched meshes retain five connected indexed closed components each; the full building has not been fused.

- Candidate SHA-256: Penn Museum 0a310f571d89e031739613f1415ec9b0d02513d290d0c507d3da5d08a6bd4404; Annenberg a9d0db64c2a27c7ab2b1f32728379f31b1eca57905cee004ed17b11b94beac32. Original positions, unrelated 74 / 38 polygons and their per-corner UV/normals unchanged. Nonmesh FBX sections exact by parse, material links retained; textures not repackaged or rendered.
- Exact ZIP fresh Blender 4.3.2 reimport: 246,402 exterior probes, 134,081 hits, max first-hit shift 0.0333 mm, max UV delta 1.65e-7; 5,889 ring probes and 1,250 internal probes. No game import or validation of near and middle LODs. Keep canonical assets and LFS unchanged.
- Archive `Penn-Museum-Annenberg-远景修补-未游戏验收.zip`, 248,910 bytes, SHA-256 aeb1124a5b7e1be3fad6297b1dcb21a29b2c8f4319ec08baf0a8586feaf1e95a.
