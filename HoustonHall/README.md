# Houston Hall

`NA_HoustonHall_11x5` - Cities: Skylines II asset (1 unit = 1 m, pivot at bottom centre of lot, FBX Forward -Z / Up Y).

| | |
|---|---|
| Lot | 11x5 |
| Model bounds (incl. lot surface) | 88.0 x 40.0 x 21.55 m |
| Real reference | OSM way 51469194 84.0x37.3 m; 4 floors; 1894-96 |
| LOD0 tris (Base / Win / Gls) | 13788 / 204 / 0 |
| LOD1 tris (Base / Win / Gls) | 9168 / 204 / 0 |
| LOD2 tris | 60 |

Textures (`textures/`, 4096 px LOD0/LOD1 shared, 1024 px LOD2): `_BaseColor`, `_Normal` (OpenGL), `_MaskMap` (R metallic, G coat=0, B=0, A gloss), `_ControlMask`, `_Emissive`.
`settings.json` maps LOD1 textures to the shared LOD0 set (`sharedAssets`). Win sub-mesh uses the 5x5 window UV grid.

LOD verification: side-by-side LOD0/LOD1/LOD2 renders in `renders/lod_compare_*.png`; mesh checks (no flipped closed shells, no bad winding, no loose vertices, no floating parts in Base meshes) in table below.

| mesh | tris | boundary edges | non-manifold edges | zero-area faces | bad winding | flipped shells | floating parts |
|---|---|---|---|---|---|---|---|
| NA_HoustonHall_11x5_Base | 13788 | 0 | 209 | 0 | 0 | 0 | 0 |
| NA_HoustonHall_11x5_Win | 204 | 408 | 0 | 0 | 0 | 0 | 102 |
| NA_HoustonHall_11x5_LOD1_Base | 9168 | 0 | 209 | 0 | 0 | 0 | 0 |
| NA_HoustonHall_11x5_LOD1_Win | 204 | 408 | 0 | 0 | 0 | 0 | 102 |
| NA_HoustonHall_11x5_LOD2_Base | 60 | 0 | 0 | 0 | 0 | 0 | 0 |

(Boundary / non-manifold edges come from intentionally open trim pieces and touching/overlapping detail blocks; Win/Gls panes are single-sided planes that sit on the Base mesh, so they count as 'floating' inside their own sub-mesh.)

See `SOURCES.txt` / `ATTRIBUTION.txt` for dimensions sources and credits.

![front](renders/render_01_front34.png)
