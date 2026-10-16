# Franklin Field

`NA_FranklinField_28x19` - Cities: Skylines II asset (1 unit = 1 m, pivot at bottom centre of lot, FBX Forward -Z / Up Y).

| | |
|---|---|
| Lot | 28x19 |
| Model bounds (incl. lot surface) | 224.0 x 152.0 x 24.05 m |
| Real reference | OSM way 665447049 219.7x149.9 m; exterior shell |
| LOD0 tris (Base / Win / Gls) | 16120 / 506 / 0 |
| LOD1 tris (Base / Win / Gls) | 10600 / 506 / 0 |
| LOD2 tris | 96 |

Textures (`textures/`, 4096 px LOD0/LOD1 shared, 1024 px LOD2): `_BaseColor`, `_Normal` (OpenGL), `_MaskMap` (R metallic, G coat=0, B=0, A gloss), `_ControlMask`, `_Emissive`.
`settings.json` maps LOD1 textures to the shared LOD0 set (`sharedAssets`). Win sub-mesh uses the 5x5 window UV grid.

LOD verification: side-by-side LOD0/LOD1/LOD2 renders in `renders/lod_compare_*.png`; mesh checks (no flipped closed shells, no bad winding, no loose vertices, no floating parts in Base meshes) in table below.

| mesh | tris | boundary edges | non-manifold edges | zero-area faces | bad winding | flipped shells | floating parts |
|---|---|---|---|---|---|---|---|
| NA_FranklinField_28x19_Base | 16120 | 0 | 1380 | 0 | 0 | 0 | 0 |
| NA_FranklinField_28x19_Win | 506 | 690 | 0 | 0 | 0 | 0 | 92 |
| NA_FranklinField_28x19_LOD1_Base | 10600 | 0 | 1380 | 0 | 0 | 0 | 0 |
| NA_FranklinField_28x19_LOD1_Win | 506 | 690 | 0 | 0 | 0 | 0 | 92 |
| NA_FranklinField_28x19_LOD2_Base | 96 | 0 | 0 | 0 | 0 | 0 | 0 |

(Boundary / non-manifold edges come from intentionally open trim pieces and touching/overlapping detail blocks; Win/Gls panes are single-sided planes that sit on the Base mesh, so they count as 'floating' inside their own sub-mesh.)

See `SOURCES.txt` / `ATTRIBUTION.txt` for dimensions sources and credits.

![front](renders/render_01_front34.png)
