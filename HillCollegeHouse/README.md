# Hill College House

`NA_HillCollegeHouse_10x6` - Cities: Skylines II asset (1 unit = 1 m, pivot at bottom centre of lot, FBX Forward -Z / Up Y).

| | |
|---|---|
| Lot | 10x6 |
| Model bounds (incl. lot surface) | 80.0 x 48.0 x 24.25 m |
| Real reference | OSM rel 5235124 78.9x45.7 m; Saarinen 1960 |
| LOD0 tris (Base / Win / Gls) | 36146 / 540 / 0 |
| LOD1 tris (Base / Win / Gls) | 23018 / 540 / 0 |
| LOD2 tris | 72 |

Textures (`textures/`, 4096 px LOD0/LOD1 shared, 1024 px LOD2): `_BaseColor`, `_Normal` (OpenGL), `_MaskMap` (R metallic, G coat=0, B=0, A gloss), `_ControlMask`, `_Emissive`.
`settings.json` maps LOD1 textures to the shared LOD0 set (`sharedAssets`). Win sub-mesh uses the 5x5 window UV grid.

LOD verification: side-by-side LOD0/LOD1/LOD2 renders in `renders/lod_compare_*.png`; mesh checks (no flipped closed shells, no bad winding, no loose vertices, no floating parts in Base meshes) in table below.

| mesh | tris | boundary edges | non-manifold edges | zero-area faces | bad winding | flipped shells | floating parts |
|---|---|---|---|---|---|---|---|
| NA_HillCollegeHouse_10x6_Base | 36146 | 0 | 574 | 0 | 0 | 0 | 0 |
| NA_HillCollegeHouse_10x6_Win | 540 | 1080 | 0 | 0 | 0 | 0 | 270 |
| NA_HillCollegeHouse_10x6_LOD1_Base | 23018 | 0 | 574 | 0 | 0 | 0 | 0 |
| NA_HillCollegeHouse_10x6_LOD1_Win | 540 | 1080 | 0 | 0 | 0 | 0 | 270 |
| NA_HillCollegeHouse_10x6_LOD2_Base | 72 | 0 | 0 | 0 | 0 | 0 | 0 |

(Boundary / non-manifold edges come from intentionally open trim pieces and touching/overlapping detail blocks; Win/Gls panes are single-sided planes that sit on the Base mesh, so they count as 'floating' inside their own sub-mesh.)

See `SOURCES.txt` / `ATTRIBUTION.txt` for dimensions sources and credits.

![front](renders/render_01_front34.png)
