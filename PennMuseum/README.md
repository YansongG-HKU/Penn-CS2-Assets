# Penn Museum

`NA_PennMuseum_21x15` - Cities: Skylines II asset (1 unit = 1 m, pivot at bottom centre of lot, FBX Forward -Z / Up Y).

| | |
|---|---|
| Lot | 21x15 |
| Model bounds (incl. lot surface) | 168.0 x 120.0 x 31.05 m |
| Real reference | OSM rel 5231601 164.9x114.0 m |
| LOD0 tris (Base / Win / Gls) | 5384 / 176 / 0 |
| LOD1 tris (Base / Win / Gls) | 4352 / 176 / 0 |
| LOD2 tris | 232 |

Textures (`textures/`, 4096 px LOD0/LOD1 shared, 1024 px LOD2): `_BaseColor`, `_Normal` (OpenGL), `_MaskMap` (R metallic, G coat=0, B=0, A gloss), `_ControlMask`, `_Emissive`.
`settings.json` maps LOD1 textures to the shared LOD0 set (`sharedAssets`). Win sub-mesh uses the 5x5 window UV grid.

LOD verification: side-by-side LOD0/LOD1/LOD2 renders in `renders/lod_compare_*.png`; mesh checks (no flipped closed shells, no bad winding, no loose vertices, no floating parts in Base meshes) in table below.

| mesh | tris | boundary edges | non-manifold edges | zero-area faces | bad winding | flipped shells | floating parts |
|---|---|---|---|---|---|---|---|
| NA_PennMuseum_21x15_Base | 5384 | 0 | 492 | 0 | 0 | 0 | 0 |
| NA_PennMuseum_21x15_Win | 176 | 240 | 0 | 0 | 0 | 0 | 32 |
| NA_PennMuseum_21x15_LOD1_Base | 4352 | 0 | 492 | 0 | 0 | 0 | 0 |
| NA_PennMuseum_21x15_LOD1_Win | 176 | 240 | 0 | 0 | 0 | 0 | 32 |
| NA_PennMuseum_21x15_LOD2_Base | 232 | 0 | 0 | 0 | 0 | 0 | 0 |

(Boundary / non-manifold edges come from intentionally open trim pieces and touching/overlapping detail blocks; Win/Gls panes are single-sided planes that sit on the Base mesh, so they count as 'floating' inside their own sub-mesh.)

See `SOURCES.txt` / `ATTRIBUTION.txt` for dimensions sources and credits.

![front](renders/render_01_front34.png)
