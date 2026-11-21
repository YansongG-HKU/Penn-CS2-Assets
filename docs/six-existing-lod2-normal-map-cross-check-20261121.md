# Six existing Penn LOD2 variants: normal-map cross-check

Re-read exact old/candidate files, no editing. For n-gons, build a transient tangent probe from Blender's exact evaluated triangles, preserving imported UVs and corner normals, then recompute Blender tangent and sign. Use the same original 1,024 px normal map per pair (SHA-256 fixture checked), sample bilinearly as Non-Color with consistent OpenGL tangent convention. Checks do not prove game importer/camera/filter/lighting equivalence. Original game project and canonical asset files untouched.

Seven staged comparisons across six buildings drew 261,121 exterior rays with 45,526 matched hits. Maximum first-hit shift 0.0552 mm; all hit masks agreed. 63,849 additional local matched samples, no tangent handedness flips. Local peak of reconstructed texture-space-to-world direction difference:

- Irvine Auditorium, original→tower crown: exactly zero on 9,335 sampled exterior hits. Crown→all four contacts (cumulative): local max 0.148°, worst contact P95 0.000385°.
- Fisher Fine Arts two tower contacts: local max 0.405°, worst P95 0.001334°. Penn Museum eave: max 0.321°, worst P95 0.001173°.
- Annenberg eave max 0.000865°, Wistar platform max 0.001521°, Franklin Field previous shoulder→final shell max 0.001478°, on matched contact samples.

All six exact variants remain offline candidates; no adoption in canonical sources. Scope limited to representative visible surfaces and contact neighborhoods, not all remaining geometric intersections, PBR, pivot/collision, LOD transitions or Editor acceptance. Evidence-only ZIP SHA-256 `fb325715f4c120573f4387fcbd3a7b324df67c7fba094d3608169303a53ac6bf` (11,913 bytes). Per-stage original and output hashes, map hashes, outside and local metric distributions are in results.json, scope/pins in checks.json.
