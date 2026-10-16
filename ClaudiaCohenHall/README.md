# Claudia Cohen Hall

`NA_ClaudiaCohenHall_7x5` - Cities: Skylines II asset (1 unit = 1 m, pivot at bottom centre of lot, FBX Forward -Z / Up Y).

| | |
|---|---|
| Lot | 7x5 |
| Model bounds (incl. lot surface) | 56.0 x 40.0 x 23.05 m |
| Real reference | OSM way 51367397 49.5x34.7 m; ex-Logan Hall |
| LOD0 tris (Base / Win / Gls) | 14522 / 216 / 0 |
| LOD1 tris (Base / Win / Gls) | 9266 / 216 / 0 |
| LOD2 tris | 36 |

Textures (`textures/`, 4096 px LOD0/LOD1 shared, 1024 px LOD2): `_BaseColor`, `_Normal` (OpenGL), `_MaskMap` (R metallic, G coat=0, B=0, A gloss), `_ControlMask`, `_Emissive`.
`settings.json` maps LOD1 textures to the shared LOD0 set (`sharedAssets`). Win sub-mesh uses the 5x5 window UV grid.

LOD verification: side-by-side LOD0/LOD1/LOD2 renders in `renders/lod_compare_*.png`; mesh checks (no flipped closed shells, no bad winding, no loose vertices, no floating parts in Base meshes) in table below.

| mesh | tris | boundary edges | non-manifold edges | zero-area faces | bad winding | flipped shells | floating parts |
|---|---|---|---|---|---|---|---|
| NA_ClaudiaCohenHall_7x5_Base | 14522 | 0 | 224 | 0 | 0 | 0 | 0 |
| NA_ClaudiaCohenHall_7x5_Win | 216 | 432 | 0 | 0 | 0 | 0 | 108 |
| NA_ClaudiaCohenHall_7x5_LOD1_Base | 9266 | 0 | 224 | 0 | 0 | 0 | 0 |
| NA_ClaudiaCohenHall_7x5_LOD1_Win | 216 | 432 | 0 | 0 | 0 | 0 | 108 |
| NA_ClaudiaCohenHall_7x5_LOD2_Base | 36 | 0 | 0 | 0 | 0 | 0 | 0 |

(Boundary / non-manifold edges come from intentionally open trim pieces and touching/overlapping detail blocks; Win/Gls panes are single-sided planes that sit on the Base mesh, so they count as 'floating' inside their own sub-mesh.)

See `SOURCES.txt` / `ATTRIBUTION.txt` for dimensions sources and credits.

![front](renders/render_01_front34.png)
