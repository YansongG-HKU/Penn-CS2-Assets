# Quad Memorial Tower — LOD2 annex roof lighting, offline

3×3, same QuadMemorialTowerTrial import unit. Source ZIP SHA-256 `d8c436b8622f763102dacc75ea53144b5e9f862a64bf7ad5e50a1894cc48fe3b` (prior ridge weld and open arch). New ZIP SHA-256 `7d7a4522245a552230a052678821fbe217b61d4481a8d0535d1fb07d161146b2`, 8,256,242 bytes, all ZIP member checksums verified.

Only the LOD2 FBX changes to `d87e9ab8c291df5d0f7ea321cba14a7e7bccbc77986b2f95eaf7dcb330a24cbe`; fifteen other runtime files byte-identical. No geometry, polygon indices, ridge, opening, UVs, maps, smoothing flags, or material nodes changed. Corrected normals and tangents/binormals for four triangles on the visibly glossy planar roof. Old normal error was 69.45–73.20°; all twelve new corners align to <0.1° in Blender readback. The four immediate underside triangles share a normal fan and respond locally during Blender import; outside those eight faces the other 464 face corners are unchanged to 1e-6. No dome faceting introduced.

Matched three Workbench views show roof highlight removed; three unlit RGB and three Emissive map passes are pixel-identical. Former weld and portal ray evidence is labeled as historical geometry check. This does not certify rendered in-game sampling, pedestrian paths, collisions, night, adjacency or save/reopen. No Editor, .pmod or release.
